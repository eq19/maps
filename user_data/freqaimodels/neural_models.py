"""
Neural Network Models for FreqAI (FIXED VERSION)
===============================================

FreqAI compatible:
- Uses data_dictionary + dk
- Outputs (&-s_predict, do_predict)
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim

from typing import Dict, Any
from sklearn.preprocessing import StandardScaler

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


# =========================================================
# PYTORCH LSTM MODEL
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

        X = self.scaler.fit_transform(X)
        X_seq, y_seq = self._create_sequences(X, y)

        if len(X_seq) == 0:
            raise ValueError("Not enough data for LSTM sequence")

        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)

        self.model = LSTMModel(input_dim=X.shape[1]).to(self.device)

        optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        loss_fn = nn.MSELoss()

        self.model.train()
        for _ in range(10):
            optimizer.zero_grad()
            output = self.model(X_tensor).squeeze()
            loss = loss_fn(output, y_tensor)
            loss.backward()
            optimizer.step()

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = self.scaler.transform(features.values)

        if len(X) < self.sequence_length:
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])

        sequences = []
        for i in range(len(X) - self.sequence_length + 1):
            sequences.append(X[i:i+self.sequence_length])

        X_tensor = torch.FloatTensor(np.array(sequences)).to(self.device)

        self.model.eval()
        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy().flatten()

        # pad to match dataframe length
        if len(preds) < len(unfiltered_df):
            preds = np.concatenate([
                np.full(len(unfiltered_df) - len(preds), preds[0]),
                preds
            ])

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        do_predict = np.ones(len(preds), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# TRANSFORMER MODEL
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

        X = self.scaler.fit_transform(X)
        X_seq, y_seq = self._create_sequences(X, y)

        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)

        self.model = TransformerModel(input_dim=X.shape[1]).to(self.device)

        optimizer = optim.Adam(self.model.parameters(), lr=0.0005)
        loss_fn = nn.MSELoss()

        self.model.train()
        for _ in range(10):
            optimizer.zero_grad()
            output = self.model(X_tensor).squeeze()
            loss = loss_fn(output, y_tensor)
            loss.backward()
            optimizer.step()

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = self.scaler.transform(features.values)

        if len(X) < self.sequence_length:
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])

        sequences = []
        for i in range(len(X) - self.sequence_length + 1):
            sequences.append(X[i:i+self.sequence_length])

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

        do_predict = np.ones(len(preds), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# SIMPLE LSTM (SAFE FALLBACK)
# =========================================================
class LSTMRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from sklearn.ensemble import RandomForestRegressor
        self.model = RandomForestRegressor(n_estimators=100)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]
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


# =========================================================
# PYTORCH MODELS
# =========================================================
class LSTMModel(nn.Module):

    def __init__(self, input_dim):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, 64, batch_first=True)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])


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
        return self.fc(x.mean(dim=1))
