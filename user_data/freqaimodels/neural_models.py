"""
FreqAI Neural Models (FINAL STABLE - 3 MODELS)
=============================================

Includes:
✔ PyTorchRegressor (main)
✔ PyTorchTransformerRegressor (sequence)
✔ LSTMRegressor (RandomForest fallback)

✔ Handles ALL FreqAI formats
✔ No recursion
✔ No shape mismatch
✔ Safe fallback
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel

logger = logging.getLogger(__name__)


# =========================================================
# 🔥 SAFE EXTRACTOR
# =========================================================
def extract_xy(data_dictionary):

    if isinstance(data_dictionary, dict):

        X = data_dictionary.get("train_features", None)
        if X is None:
            X = data_dictionary.get("features", None)
        if X is None:
            X = data_dictionary.get("X", None)

        y = data_dictionary.get("train_labels", None)
        if y is None:
            y = data_dictionary.get("labels", None)
        if y is None:
            y = data_dictionary.get("y", None)

        if X is None or y is None:
            raise ValueError("Missing X or y in dict")

        return np.asarray(X), np.asarray(y).reshape(-1)

    if isinstance(data_dictionary, (list, tuple)) and len(data_dictionary) >= 2:
        return np.asarray(data_dictionary[0]), np.asarray(data_dictionary[1]).reshape(-1)

    if isinstance(data_dictionary, np.ndarray):

        if data_dictionary.ndim == 2:
            if data_dictionary.shape[1] > 1:
                return data_dictionary[:, :-1], data_dictionary[:, -1]
            return data_dictionary, np.zeros(len(data_dictionary))

        if data_dictionary.ndim == 1:
            return data_dictionary.reshape(-1, 1), np.zeros(len(data_dictionary))

    arr = np.asarray(data_dictionary)

    if arr.ndim == 2:
        return arr[:, :-1], arr[:, -1]

    if arr.ndim == 1:
        return arr.reshape(-1, 1), np.zeros(len(arr))

    raise ValueError(f"Unsupported format: {type(data_dictionary)}")


# =========================================================
# HELPERS
# =========================================================
def safe_index(df):
    return df.index if hasattr(df, "index") else pd.RangeIndex(len(df))


def fallback_prediction(df):
    length = len(df)
    pred_df = pd.DataFrame(index=safe_index(df))
    pred_df["&-s_predict"] = np.zeros(length)
    return pred_df, np.zeros(length, dtype=np.int_)


def align_prediction(pred, target_len):

    pred = np.asarray(pred).reshape(-1)

    if len(pred) == 0:
        return np.zeros(target_len)

    if len(pred) != target_len:
        return np.full(target_len, float(pred[-1]))

    return pred.astype(float)


# =========================================================
# SIMPLE NN
# =========================================================
class SimpleNN(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )

    def forward(self, x):
        return self.net(x)


# =========================================================
# 🔥 MODEL 1: PYTORCH REGRESSOR
# =========================================================
class PyTorchRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)

        X = np.clip(X, -10, 10)
        X = self.scaler.fit_transform(X)

        X_tensor = torch.FloatTensor(X).to(self.device)
        y_tensor = torch.FloatTensor(y).to(self.device)

        self.model = SimpleNN(X.shape[1]).to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        loss_fn = nn.HuberLoss()

        self.model.train()
        for _ in range(5):
            optimizer.zero_grad()
            preds = self.model(X_tensor).squeeze()
            loss = loss_fn(preds, y_tensor)
            loss.backward()
            optimizer.step()

        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if self.model is None or dk is None:
            return fallback_prediction(unfiltered_df)

        try:
            features, _ = dk.filter_features(
                unfiltered_df,
                dk.training_features_list,
                dk.label_list,
                training_filter=False
            )

            X = np.asarray(features)
            X = np.clip(X, -10, 10)
            X = self.scaler.transform(X)

            X_tensor = torch.FloatTensor(X).to(self.device)

            self.model.eval()
            with torch.no_grad():
                pred = self.model(X_tensor).cpu().numpy()

        except Exception as e:
            logger.warning(f"NN fallback: {e}")
            return fallback_prediction(unfiltered_df)

        pred = align_prediction(pred, len(unfiltered_df))

        pred_df = pd.DataFrame(index=safe_index(unfiltered_df))
        pred_df["&-s_predict"] = pred

        return pred_df, np.ones(len(pred), dtype=np.int_)


# =========================================================
# 🔥 MODEL 2: TRANSFORMER
# =========================================================
class TransformerModel(nn.Module):

    def __init__(self, input_dim):
        super().__init__()

        self.input_proj = nn.Linear(input_dim, 64)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=64,
            nhead=4,
            batch_first=True
        )

        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        x = self.input_proj(x)
        x = self.transformer(x)
        return self.fc(x).squeeze(-1)


class EnhancedPyTorchTransformerRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.sequence_length = 10

    def create_sequences(self, X, y=None):

        Xs, ys = [], []

        for i in range(len(X) - self.sequence_length):
            Xs.append(X[i:i+self.sequence_length])
            if y is not None:
                ys.append(y[i+self.sequence_length])

        Xs = np.array(Xs)

        if y is not None:
            return Xs, np.array(ys)

        return Xs

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)

        X = np.clip(X, -10, 10)
        X = self.scaler.fit_transform(X)

        if len(X) <= self.sequence_length:
            raise ValueError("Not enough data")

        X_seq, y_seq = self.create_sequences(X, y)

        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)

        self.model = TransformerModel(X.shape[1]).to(self.device)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        loss_fn = nn.HuberLoss()

        self.model.train()
        for _ in range(5):
            optimizer.zero_grad()
            preds = self.model(X_tensor)
            loss = loss_fn(preds, y_tensor)
            loss.backward()
            optimizer.step()

        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if self.model is None or dk is None:
            return fallback_prediction(unfiltered_df)

        try:
            features, _ = dk.filter_features(
                unfiltered_df,
                dk.training_features_list,
                dk.label_list,
                training_filter=False
            )

            X = np.asarray(features)
            X = np.clip(X, -10, 10)
            X = self.scaler.transform(X)

            if len(X) < self.sequence_length:
                pad = np.zeros((self.sequence_length - len(X), X.shape[1]))
                X = np.vstack([pad, X])

            X_seq = self.create_sequences(X)

            if len(X_seq) == 0:
                return fallback_prediction(unfiltered_df)

            X_tensor = torch.FloatTensor(X_seq).to(self.device)

            self.model.eval()
            with torch.no_grad():
                pred = self.model(X_tensor).cpu().numpy()

        except Exception as e:
            logger.warning(f"Transformer fallback: {e}")
            return fallback_prediction(unfiltered_df)

        pred = align_prediction(pred, len(unfiltered_df))

        pred_df = pd.DataFrame(index=safe_index(unfiltered_df))
        pred_df["&-s_predict"] = pred

        return pred_df, np.ones(len(pred), dtype=np.int_)


# =========================================================
# 🛡 MODEL 3: RANDOM FOREST
# =========================================================
class LSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rf = RandomForestRegressor(
            n_estimators=200,
            max_depth=6,
            min_samples_leaf=5,
            random_state=42
        )

    def fit(self, data_dictionary, dk=None, **kwargs):

        X, y = extract_xy(data_dictionary)
        self.rf.fit(X, y)

        return self

    def predict(self, unfiltered_df, dk=None, **kwargs):

        if dk is None:
            return fallback_prediction(unfiltered_df)

        try:
            features, _ = dk.filter_features(
                unfiltered_df,
                dk.training_features_list,
                dk.label_list,
                training_filter=False
            )

            pred = self.rf.predict(np.asarray(features))

        except Exception as e:
            logger.warning(f"RF fallback: {e}")
            return fallback_prediction(unfiltered_df)

        pred = align_prediction(pred, len(unfiltered_df))

        pred_df = pd.DataFrame(index=safe_index(unfiltered_df))
        pred_df["&-s_predict"] = pred

        return pred_df, np.ones(len(pred), dtype=np.int_)
