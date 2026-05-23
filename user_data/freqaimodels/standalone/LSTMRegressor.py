import torch
import torch.nn as nn
import torch.optim as optim


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

