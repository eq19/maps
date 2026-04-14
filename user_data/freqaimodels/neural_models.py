"""
Neural Network Models for FreqAI (ULTIMATE STABLE VERSION)
=========================================================

This version fixes:
- All FreqAI input inconsistencies
- Sequence length mismatch
- Prediction length mismatch (CRITICAL)
- Data format variability
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel

logger = logging.getLogger(__name__)


# =========================================================
# SAFE UTILITIES
# =========================================================

def extract_xy(data_dictionary):
    """
    Fully tolerant extractor for ANY FreqAI structure
    """

    # dict case
    if isinstance(data_dictionary, dict):

        X = None
        y = None

        for key in ["train_features", "features", "X"]:
            if key in data_dictionary:
                X = data_dictionary[key]
                break

        for key in ["train_labels", "labels", "y"]:
            if key in data_dictionary:
                y = data_dictionary[key]
                break

        if X is None or y is None:
            raise ValueError("Missing X or y in dict")

        if hasattr(X, "values"):
            X = X.values
        if hasattr(y, "values"):
            y = y.values

        return X, np.array(y).ravel()

    # tuple/list case
    if isinstance(data_dictionary, (list, tuple)):

        arrays = [x for x in data_dictionary if hasattr(x, "__len__")]

        if len(arrays) >= 2:
            X = arrays[0]
            y = arrays[1]
            return X, np.array(y).ravel()

    raise ValueError(f"Unsupported data format: {type(data_dictionary)}")


def safe_index(df):
    if hasattr(df, "index"):
        return df.index
    return pd.RangeIndex(len(df))


def fallback_prediction(df):
    length = len(df)
    index = safe_index(df)

    preds = np.zeros(length)

    pred_df = pd.DataFrame(index=index)
    pred_df["&-s_predict"] = preds

    do_predict = np.zeros(length, dtype=np.int_)
    return pred_df, do_predict


def align_predictions(preds, target_len):
    preds = np.array(preds).flatten()

    if len(preds) == 0:
        return np.zeros(target_len)

    if len(preds) < target_len:
        return np.pad(preds, (target_len - len(preds), 0), mode='edge')

    if len(preds) > target_len:
        return preds[-target_len:]

    return preds


# =========================================================
# MODELS
# =========================================================

class LSTMModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, 64, batch_first=True)
        self.dropout = nn.Dropout(0.2)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.dropout(out[:, -1, :])
        return self.fc(out)


class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=500):
        super().__init__()

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model)
        )

        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)

        self.pe = pe.unsqueeze(0)

    def forward(self, x):
        return x + self.pe[:, :x.size(1)].to(x.device)


class TransformerModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()

        self.input_proj = nn.Linear(input_dim, 64)
        self.pos_encoding = PositionalEncoding(64)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=64,
            nhead=4,
            dropout=0.2,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        x = self.input_proj(x)
        x = self.pos_encoding(x)
        x = self.transformer(x)
        return self.fc(x.mean(dim=1))


# =========================================================
# LSTM REGRESSOR
# =========================================================

class PyTorchLSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sequence_length = 20
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def _create_sequences(self, X, y=None):
        Xs, ys = [], []
        for i in range(len(X) - self.sequence_length):
            Xs.append(X[i:i+self.sequence_length])
            if y is not None:
                ys.append(y[i+self.sequence_length])
        return np.array(Xs), np.array(ys)

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)

        X = np.clip(X, -10, 10)
        X = self.scaler.fit_transform(X)

        X_seq, y_seq = self._create_sequences(X, y)

        if len(X_seq) == 0:
            raise ValueError("Not enough data")

        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)

        self.model = LSTMModel(input_dim=X.shape[1]).to(self.device)

        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        loss_fn = nn.HuberLoss()

        self.model.train()
        for _ in range(15):
            optimizer.zero_grad()

            output = self.model(X_tensor).squeeze()
            loss = loss_fn(output, y_tensor)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            optimizer.step()

        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if self.model is None or dk is None:
            return fallback_prediction(unfiltered_df)

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = np.clip(features.values, -10, 10)
        X = self.scaler.transform(X)

        if len(X) < self.sequence_length:
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])

        sequences = [
            X[i:i+self.sequence_length]
            for i in range(len(X) - self.sequence_length + 1)
        ]

        X_tensor = torch.FloatTensor(np.array(sequences)).to(self.device)

        self.model.eval()
        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy().flatten()

        preds = align_predictions(preds, len(unfiltered_df))

        index = safe_index(unfiltered_df)

        pred_df = pd.DataFrame(index=index)
        pred_df["&-s_predict"] = preds

        volatility = np.std(preds) + 1e-8
        do_predict = (np.abs(preds) > 0.1 * volatility).astype(int)

        return pred_df, do_predict


# =========================================================
# TRANSFORMER REGRESSOR
# =========================================================

class PyTorchTransformerRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sequence_length = 30
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def _create_sequences(self, X, y=None):
        Xs, ys = [], []
        for i in range(len(X) - self.sequence_length):
            Xs.append(X[i:i+self.sequence_length])
            if y is not None:
                ys.append(y[i+self.sequence_length])
        return np.array(Xs), np.array(ys)

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)

        X = np.clip(X, -10, 10)
        X = self.scaler.fit_transform(X)

        X_seq, y_seq = self._create_sequences(X, y)

        if len(X_seq) == 0:
            raise ValueError("Not enough data")

        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)

        self.model = TransformerModel(input_dim=X.shape[1]).to(self.device)

        optimizer = optim.Adam(self.model.parameters(), lr=0.0005)
        loss_fn = nn.HuberLoss()

        self.model.train()
        for _ in range(15):
            optimizer.zero_grad()

            output = self.model(X_tensor).squeeze()
            loss = loss_fn(output, y_tensor)

            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            optimizer.step()

        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if self.model is None or dk is None:
            return fallback_prediction(unfiltered_df)

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = np.clip(features.values, -10, 10)
        X = self.scaler.transform(X)

        if len(X) < self.sequence_length:
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])

        sequences = [
            X[i:i+self.sequence_length]
            for i in range(len(X) - self.sequence_length + 1)
        ]

        X_tensor = torch.FloatTensor(np.array(sequences)).to(self.device)

        self.model.eval()
        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy().flatten()

        preds = align_predictions(preds, len(unfiltered_df))

        index = safe_index(unfiltered_df)

        pred_df = pd.DataFrame(index=index)
        pred_df["&-s_predict"] = preds

        volatility = np.std(preds) + 1e-8
        do_predict = (np.abs(preds) > 0.1 * volatility).astype(int)

        return pred_df, do_predict


# =========================================================
# FALLBACK MODEL
# =========================================================

class LSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)

        if self.model is None:
            self.model = RandomForestRegressor(
                n_estimators=200,
                max_depth=6,
                min_samples_leaf=5,
                random_state=42
            )

        self.model.fit(X, y)
        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if self.model is None or dk is None:
            return fallback_prediction(unfiltered_df)

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        preds = self.model.predict(features.values)
        preds = align_predictions(preds, len(unfiltered_df))

        index = safe_index(unfiltered_df)

        pred_df = pd.DataFrame(index=index)
        pred_df["&-s_predict"] = preds

        do_predict = np.ones(len(preds), dtype=np.int_)
        return pred_df, do_predict
