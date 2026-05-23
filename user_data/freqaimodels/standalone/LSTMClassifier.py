from pandas import DataFrame
import torch
import torch.nn as nn
import torch.optim as optim


class LSTMClassifier(nn.Module):
    def __init__(self, input_size,
                 hidden_size, num_layers,
                 num_classes, dropout_rate=0.25):

        super(LSTMClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True,
                            dropout=dropout_rate if num_layers > 1 else 0.0)
        self.fc = nn.Linear(hidden_size, num_classes)

        # Initialize LSTM weights using Xavier/Glorot initialization
        for name, param in self.lstm.named_parameters():
            if 'weight_ih' in name or 'weight_hh' in name:  # Weights of LSTM
                nn.init.xavier_uniform_(param.data)
            elif 'bias' in name:  # Biases of LSTM
                nn.init.zeros_(param.data)

        # Initialize fully connected layer weights using Xavier/Glorot initialization
        nn.init.xavier_uniform_(self.fc.weight)
        nn.init.zeros_(self.fc.bias)

    def forward(self, x):
        if x.dim() == 2:
            x = x.unsqueeze(1)

        h0 = torch.zeros(self.num_layers, x.size(
            0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(
            0), self.hidden_size).to(x.device)

        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out
