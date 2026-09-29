from typing import Any, Dict
import torch
import torch.nn as nn
from freqtrade.freqai.base_models.BasePyTorchRegressor import BasePyTorchRegressor
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.torch.PyTorchDataConvertor import (
    DefaultPyTorchDataConvertor,
    PyTorchDataConvertor,
)
from freqtrade.freqai.torch.PyTorchModelTrainer import PyTorchModelTrainer


class LSTMRegressor(nn.Module):
    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int,
        output_size: int = 1,
        dropout_rate: float = 0.25,
    ):
        super(LSTMRegressor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # Define the LSTM layer
        self.lstm = nn.LSTM(
            input_size,
            hidden_size,
            num_layers,
            batch_first=True,
            dropout=dropout_rate if num_layers > 1 else 0.0,
        )

        # Define the fully connected output layer
        self.fc = nn.Linear(hidden_size, output_size)

        # Initialize LSTM weights using Xavier/Glorot initialization
        for name, param in self.lstm.named_parameters():
            if 'weight_ih' in name or 'weight_hh' in name:  # Weights of LSTM
                nn.init.xavier_uniform_(param.data)
            elif 'bias' in name:  # Biases of LSTM
                nn.init.zeros_(param.data)

        # Initialize fully connected layer weights using Xavier/Glorot initialization
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Add a dimension if input is 2D
        if x.dim() == 2:
            x = x.unsqueeze(1)

        # Initialize hidden and cell states
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)

        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))

        # Pass through the fully connected layer
        out = self.fc(out[:, -1, :])

        # If output_size is 1, remove the last dimension
        if out.size(-1) == 1:
            out = out.squeeze(-1)

        return out


class ZHU_LSTMTradeRegressor(BasePyTorchRegressor):
    @property
    def data_convertor(self) -> PyTorchDataConvertor:
        return DefaultPyTorchDataConvertor(
            target_tensor_type=torch.float, squeeze_target_tensor=True
        )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        config = self.freqai_info.get("model_training_parameters", {})

        self.model_kwargs: Dict[str, Any] = config.get("model_kwargs", {})
        self.hidden_size = self.model_kwargs.get("hidden_size", 768)
        self.num_layers = self.model_kwargs.get("num_layers", 4)
        self.dropout_rate = self.model_kwargs.get("dropout_rate", 0.2)
        self.learning_rate: float = self.model_kwargs.get("learning_rate", 0.001)

        self.trainer_kwargs: Dict[str, Any] = config.get("trainer_kwargs", {})

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        n_features = data_dictionary["train_features"].shape[-1]

        model = LSTMRegressor(
            input_size=n_features,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            dropout_rate=self.dropout_rate
        )
        model.to(self.device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=self.learning_rate)
        criterion = torch.nn.MSELoss()
        trainer = self.get_init_model(dk.pair)
        if trainer is None:
            trainer = PyTorchModelTrainer(
                model=model,
                optimizer=optimizer,
                criterion=criterion,
                model_meta_data={},
                device=self.device,
                data_convertor=self.data_convertor,
                tb_logger=self.tb_logger,
                **self.trainer_kwargs,
            )
        trainer.fit(data_dictionary, self.splits)
        return trainer
