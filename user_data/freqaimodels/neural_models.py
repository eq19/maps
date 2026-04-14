"""
Neural Network Models for FreqAI (FINAL STABLE VERSION)
=====================================================

Key Features:
- Noise-resistant (clip + Huber loss)
- Proper sequence handling
- Transformer with positional encoding
- Confidence-based do_predict filter
- Stable fallback model
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from typing import Dict, Any
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


# =========================================================
# POSITIONAL ENCODING (FOR TRANSFORMER)
# =========================================================
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


# =========================================================
# PYTORCH MODELS
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
# LSTM REGRESSOR (MAIN MODEL)
# =========================================================
class PyTorchLSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.sequence_length = 20
        self.scaler = StandardScaler()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def _create_sequences(self, X, y=None):
        Xs, ys = [], []
        for i in range(len(X) - self.sequence_length):
            Xs.append(X[i:i+self.sequence_length])
            if y is not None:
                ys.append(y[i+self.sequence_length])
        return np.array(Xs), np.array(ys)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]

        # 🔥 handle spikes
        X = np.clip(X, -10, 10)

        X = self.scaler.fit_transform(X)
        X_seq, y_seq = self._create_sequences(X, y)

        if len(X_seq) == 0:
            raise ValueError("Not enough data for LSTM")

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

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

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

        if len(preds) < len(unfiltered_df):
            preds = np.concatenate([
                np.full(len(unfiltered_df) - len(preds), preds[0]),
                preds
            ])

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        # 🔥 confidence filter
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

    def _create_sequences(self, X, y=None):
        Xs, ys = [], []
        for i in range(len(X) - self.sequence_length):
            Xs.append(X[i:i+self.sequence_length])
            if y is not None:
                ys.append(y[i+self.sequence_length])
        return np.array(Xs), np.array(ys)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]

        X = np.clip(X, -10, 10)
        X = self.scaler.fit_transform(X)

        X_seq, y_seq = self._create_sequences(X, y)

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

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

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

        if len(preds) < len(unfiltered_df):
            preds = np.concatenate([
                np.full(len(unfiltered_df) - len(preds), preds[0]),
                preds
            ])

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        volatility = np.std(preds) + 1e-8
        do_predict = (np.abs(preds) > 0.1 * volatility).astype(int)

        return pred_df, do_predict


# =========================================================
# SAFE FALLBACK MODEL
# =========================================================
class LSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=6,
            min_samples_leaf=5,
            random_state=42
        )

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = np.array(data_dictionary["train_labels"]).ravel()

        self.model.fit(X, y)
        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        preds = self.model.predict(features.values)

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        do_predict = np.ones(len(preds), dtype=np.int_)

        return pred_df, do_predict
