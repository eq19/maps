import logging
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
from typing import Optional

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel

logger = logging.getLogger(__name__)
BaseFreqAIModel = BaseRegressionModel


# =========================
# LSTM MODEL
# =========================
class FreqAILSTMModel(nn.Module):
    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dim: int = 128,
        num_lstm_layers: int = 2,
        dropout_percent: float = 0.2,
    ):
        super().__init__()

        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers=num_lstm_layers,
            batch_first=True,
            dropout=dropout_percent if num_lstm_layers > 1 else 0,
        )

        self.fc1 = nn.Linear(hidden_dim, 36)
        self.dropout = nn.Dropout(dropout_percent)
        self.fc2 = nn.Linear(36, output_dim)

        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(1)  # (batch, seq=1, features)

        out, _ = self.lstm(x)

        # take last timestep
        out = out[:, -1, :]

        out = self.relu(self.fc1(out))
        out = self.dropout(out)
        out = self.fc2(out)

        return out


# =========================
# REGRESSOR
# =========================
class FreqAILSTMRegressor(BaseFreqAIModel):

    model_type = "neural_network"

    default_parameters = {
        "hidden_dim": 128,
        "num_lstm_layers": 2,
        "dropout_percent": 0.2,
        "learning_rate": 0.001,
        "epochs": 50,
        "batch_size": 64,
        "device": "auto",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scaler = StandardScaler()
        self.model: Optional[nn.Module] = None
        self.is_trained = False

        self.device = self._get_device()
        logger.info(f"Using device: {self.device}")

    def _get_device(self):
        device_param = self.parameters.get("device", "auto")

        if device_param == "cpu":
            return torch.device("cpu")

        if device_param == "cuda" and torch.cuda.is_available():
            return torch.device("cuda")

        if device_param == "mps" and torch.backends.mps.is_available():
            return torch.device("mps")

        # AUTO
        if torch.cuda.is_available():
            return torch.device("cuda")
        if torch.backends.mps.is_available():
            return torch.device("mps")

        return torch.device("cpu")

    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs):
        self.validate_data(X, y)

        X = self.preprocess_features(X)
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
            output_dim=1,
            hidden_dim=self.parameters["hidden_dim"],
            num_lstm_layers=self.parameters["num_lstm_layers"],
            dropout_percent=self.parameters["dropout_percent"],
        ).to(self.device)

        optimizer = torch.optim.Adam(
            self.model.parameters(),
            lr=self.parameters["learning_rate"],
        )

        criterion = nn.MSELoss()

        epochs = self.parameters["epochs"]

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

        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")

        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)

        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).to(self.device)

        self.model.eval()

        with torch.no_grad():
            preds = self.model(X_tensor).cpu().numpy()

        return preds.squeeze()
