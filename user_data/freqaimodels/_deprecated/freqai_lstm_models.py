"""
FreqAI LSTM Model - FULLY FIXED (FreqAI Native)
"""

import logging
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel

logger = logging.getLogger(__name__)


# =====================================
# LSTM MODEL
# =====================================
class FreqAILSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=2, dropout=0.2):
        super().__init__()

        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
        )

        self.fc1 = nn.Linear(hidden_dim, 32)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)

        out, _ = self.lstm(x)
        out = out[:, -1, :]

        out = self.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)

        return out


# =====================================
# REGRESSOR
# =====================================
class FreqAILSTMRegressor(BaseRegressionModel):

    model_type = "neural_network"

    default_parameters = {
        "hidden_dim": 128,
        "num_layers": 2,
        "dropout": 0.2,
        "learning_rate": 0.001,
        "epochs": 50,
        "batch_size": 64,
        "device": "auto",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scaler = StandardScaler()
        self.model = None
        self.device = None

    # ---------------------------------
    # DEVICE
    # ---------------------------------
    def _get_device(self):
        params = getattr(self, "parameters", {}) or {}
        device_param = params.get("device", "auto")

        if device_param == "cpu":
            return torch.device("cpu")

        if device_param == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")

        if device_param == "mps" and torch.backends.mps.is_available():
            return torch.device("mps")

        if torch.cuda.is_available():
            return torch.device("cuda")

        return torch.device("cpu")

    # ---------------------------------
    # FIT (FreqAI style)
    # ---------------------------------
    def fit(self, dataframe, dk):

        self.device = self._get_device()
        logger.info(f"Using device: {self.device}")

        # Extract features + labels from DataKitchen
        X = dk.data["train_features"].values
        y = dk.data["train_labels"].values

        # Scale
        X_scaled = self.scaler.fit_transform(X)

        X_tensor = torch.tensor(X_scaled, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)

        dataset = torch.utils.data.TensorDataset(X_tensor, y_tensor)

        loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=self.parameters.get("batch_size", 64),
            shuffle=True,
        )

        self.model = FreqAILSTMModel(
            input_dim=X.shape[1],
            hidden_dim=self.parameters.get("hidden_dim", 128),
            num_layers=self.parameters.get("num_layers", 2),
            dropout=self.parameters.get("dropout", 0.2),
        ).to(self.device)

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=self.parameters.get("learning_rate", 0.001),
        )

        criterion = nn.MSELoss()
        epochs = self.parameters.get("epochs", 50)

        self.model.train()

        for epoch in range(epochs):
            total_loss = 0

            for xb, yb in loader:
                xb = xb.to(self.device)
                yb = yb.to(self.device)

                optimizer.zero_grad()

                preds = self.model(xb).squeeze()
                loss = criterion(preds, yb)

                loss.backward()
                optimizer.step()

                total_loss += loss.item()

            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch} | Loss: {total_loss:.6f}")

        return self

    # ---------------------------------
    # PREDICT (FreqAI style)
    # ---------------------------------
    def predict(self, dataframe, dk):

        X = dk.data["prediction_features"].values
        X_scaled = self.scaler.transform(X)

        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)

        self.model.eval()

        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy()

        return preds.squeeze()
