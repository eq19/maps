"""
Neural Network Models for FreqAI
================================

This module contains neural network models optimized for trading:
- PyTorch LSTM: Long Short-Term Memory networks
- PyTorch Transformer: Attention-based models
- LSTM Regressor: Traditional LSTM implementation

These models are particularly good for:
- Time series prediction
- Sequence modeling
- Complex pattern recognition
- GPU acceleration (MPS support)
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from typing import Dict, Any, Optional, Tuple, List
from sklearn.preprocessing import StandardScaler
import warnings

# FreqAI imports
try:
    from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
except ImportError:
    # Fallback for when FreqAI is not available
    FreqaiDataKitchen = type('FreqaiDataKitchen', (), {})

# Use FreqAI base model
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

logger = logging.getLogger(__name__)


class PyTorchLSTMRegressor(BaseFreqAIModel):
    """
    PyTorch LSTM Regressor for FreqAI
    
    LSTM (Long Short-Term Memory) networks are excellent for time series
    prediction and can capture complex temporal patterns in financial data.
    
    Advantages:
    - Excellent for time series data
    - Can handle long sequences
    - GPU acceleration support
    - Memory efficient
    """
    
    model_type = "neural_network"
    default_parameters = {
        "hidden_dim": 128,
        "num_layers": 2,
        "dropout": 0.2,
        "learning_rate": 0.001,
        "batch_size": 64,
        "epochs": 100,
        "sequence_length": 20,
        "device": "auto"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize parameters from kwargs or defaults
        self.parameters = kwargs.copy()
        for key, value in self.default_parameters.items():
            if key not in self.parameters:
                self.parameters[key] = value
        
        self.scaler = StandardScaler()
        self.sequence_length = self.parameters.get("sequence_length", 20)
        # Force MPS device (Apple Silicon). No CUDA, no auto.
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            print("MPS device used")
        else:
            self.device = torch.device("cpu")
            print("CPU device used as fallback")
    
    def _create_sequences(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        sequences = []
        targets = []
        
        for i in range(len(X) - self.sequence_length):
            seq = X[i:(i + self.sequence_length)]
            target = y[i + self.sequence_length] if y is not None else 0
            sequences.append(seq)
            targets.append(target)
        
        return np.array(sequences), np.array(targets)
    
    def _prepare_data_for_prediction(self, X: np.ndarray) -> np.ndarray:
        """Prepare data for prediction, handling different input sizes"""
        if len(X) < self.sequence_length:
            # Pad with zeros if not enough data
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])
        
        # Create sequences - ensure we have at least one sequence
        sequences = []
        max_start = max(0, len(X) - self.sequence_length)
        for i in range(max_start + 1):
            seq = X[i:(i + self.sequence_length)]
            sequences.append(seq)
        # If no sequences created, create one with padding
        if not sequences:
            padding = np.zeros((self.sequence_length, X.shape[1]))
            sequences = [padding]
        return np.array(sequences)
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'PyTorchLSTMRegressor':
        """Train the PyTorch LSTM model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Create sequences
        X_seq, y_seq = self._create_sequences(X_scaled, y)
        
        # Convert to PyTorch tensors
        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)
        
        # Create data loader
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(
            dataset, 
            batch_size=self.parameters.get("batch_size", 64),
            shuffle=True
        )
        
        # Initialize model
        input_dim = X.shape[1]
        self.model = LSTMModel(
            input_dim=input_dim,
            hidden_dim=self.parameters.get("hidden_dim", 128),
            num_layers=self.parameters.get("num_layers", 2),
            dropout=self.parameters.get("dropout", 0.2)
        ).to(self.device)
        
        # Setup training
        criterion = nn.MSELoss()
        optimizer = optim.Adam(
            self.model.parameters(), 
            lr=self.parameters.get("learning_rate", 0.001)
        )
        
        # Training loop
        self.model.train()
        for epoch in range(self.parameters.get("epochs", 100)):
            total_loss = 0
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs.squeeze(), batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}, Loss: {total_loss/len(dataloader):.6f}")
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"PyTorch LSTM model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        # Prepare sequences for prediction
        X_seq = self._prepare_data_for_prediction(X_scaled)
        
        # Convert to tensor
        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        
        # Make predictions
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(X_tensor).cpu().numpy()
        
        # Ensure predictions are 1D first
        predictions = predictions.squeeze()
        if predictions.ndim > 1:
            predictions = predictions.flatten()
        
        # Handle the case where we have fewer predictions than input samples
        # This happens because sequences reduce the number of predictions
        if len(predictions) < len(X):
            # Pad with the last prediction or zeros
            padding = np.full(len(X) - len(predictions), predictions[-1] if len(predictions) > 0 else 0.0)
            predictions = np.concatenate([predictions, padding])
        
        # Final check to ensure 1D output
        if predictions.ndim > 1:
            predictions = predictions.flatten()
        
        return predictions
    
    def train(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """Train the model - required by FreqAI"""
        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]
        return self._fit_model(X, y, **kwargs)
    
    def predict(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> np.ndarray:
        """Predict - required by FreqAI"""
        X = data_dictionary["predict_features"]
        return self._predict_model(X)
    
    def _fit_model(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'PyTorchLSTMRegressor':
        """Internal fit method to avoid recursion"""
        return self.fit(X, y, **kwargs)
    
    def _predict_model(self, X: np.ndarray) -> np.ndarray:
        """Internal predict method to avoid recursion"""
        return super().predict(X)


class EnhancedPyTorchTransformerRegressor(BaseFreqAIModel):
    """
    PyTorch Transformer Regressor for FreqAI
    
    Transformer models use attention mechanisms and are excellent for
    capturing complex patterns in sequential data.
    
    Advantages:
    - Attention mechanism for complex patterns
    - Parallel processing capability
    - Excellent for long sequences
    - State-of-the-art performance
    """
    
    model_type = "neural_network"
    default_parameters = {
        "hidden_dim": 128,
        "num_heads": 8,
        "num_layers": 4,
        "dropout": 0.1,
        "learning_rate": 0.0001,
        "batch_size": 32,
        "epochs": 100,
        "sequence_length": 50,
        "device": "auto"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize parameters from kwargs or defaults
        self.parameters = kwargs.copy()
        for key, value in self.default_parameters.items():
            if key not in self.parameters:
                self.parameters[key] = value
        
        self.scaler = StandardScaler()
        self.sequence_length = self.parameters.get("sequence_length", 50)
        # Force MPS device (Apple Silicon). No CUDA, no auto.
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
    
    def _create_sequences(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for Transformer training"""
        sequences = []
        targets = []
        
        for i in range(len(X) - self.sequence_length):
            seq = X[i:(i + self.sequence_length)]
            target = y[i + self.sequence_length] if y is not None else 0
            sequences.append(seq)
            targets.append(target)
        
        return np.array(sequences), np.array(targets)
    
    def _prepare_data_for_prediction(self, X: np.ndarray) -> np.ndarray:
        """Prepare data for prediction, handling different input sizes"""
        if len(X) < self.sequence_length:
            # Pad with zeros if not enough data
            padding = np.zeros((self.sequence_length - len(X), X.shape[1]))
            X = np.vstack([padding, X])
        
        # Create sequences - ensure we have at least one sequence
        sequences = []
        max_start = max(0, len(X) - self.sequence_length)
        for i in range(max_start + 1):
            seq = X[i:(i + self.sequence_length)]
            sequences.append(seq)
        # If no sequences created, create one with padding
        if not sequences:
            padding = np.zeros((self.sequence_length, X.shape[1]))
            sequences = [padding]
        return np.array(sequences)
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'PyTorchTransformerRegressor':
        """Train the PyTorch Transformer model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Create sequences
        X_seq, y_seq = self._create_sequences(X_scaled, y)
        
        # Convert to PyTorch tensors
        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        y_tensor = torch.FloatTensor(y_seq).to(self.device)
        
        # Create data loader
        dataset = TensorDataset(X_tensor, y_tensor)
        dataloader = DataLoader(
            dataset, 
            batch_size=self.parameters.get("batch_size", 32),
            shuffle=True
        )
        
        # Initialize model
        input_dim = X.shape[1]
        self.model = TransformerModel(
            input_dim=input_dim,
            hidden_dim=self.parameters.get("hidden_dim", 128),
            num_heads=self.parameters.get("num_heads", 8),
            num_layers=self.parameters.get("num_layers", 4),
            dropout=self.parameters.get("dropout", 0.1)
        ).to(self.device)
        
        # Setup training
        criterion = nn.MSELoss()
        optimizer = optim.Adam(
            self.model.parameters(), 
            lr=self.parameters.get("learning_rate", 0.0001)
        )
        
        # Training loop
        self.model.train()
        for epoch in range(self.parameters.get("epochs", 100)):
            total_loss = 0
            for batch_X, batch_y in dataloader:
                optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = criterion(outputs.squeeze(), batch_y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch}, Loss: {total_loss/len(dataloader):.6f}")
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"PyTorch Transformer model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        # Prepare sequences for prediction
        X_seq = self._prepare_data_for_prediction(X_scaled)
        
        # Convert to tensor
        X_tensor = torch.FloatTensor(X_seq).to(self.device)
        
        # Make predictions
        self.model.eval()
        with torch.no_grad():
            predictions = self.model(X_tensor).cpu().numpy()
        
        # Ensure predictions are 1D first
        predictions = predictions.squeeze()
        if predictions.ndim > 1:
            predictions = predictions.flatten()
        
        # Handle the case where we have fewer predictions than input samples
        # This happens because sequences reduce the number of predictions
        if len(predictions) < len(X):
            # Pad with the last prediction or zeros
            padding = np.full(len(X) - len(predictions), predictions[-1] if len(predictions) > 0 else 0.0)
            predictions = np.concatenate([predictions, padding])
        
        # Final check to ensure 1D output
        if predictions.ndim > 1:
            predictions = predictions.flatten()
        
        return predictions


class LSTMRegressor(BaseFreqAIModel):
    """
    Traditional LSTM Regressor for FreqAI
    
    A simpler LSTM implementation that can be used as an alternative
    to the PyTorch version.
    """
    
    model_type = "neural_network"
    default_parameters = {
        "units": 50,
        "dropout": 0.2,
        "recurrent_dropout": 0.2,
        "epochs": 100,
        "batch_size": 32,
        "validation_split": 0.2
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize parameters from kwargs or defaults
        self.parameters = kwargs.copy()
        for key, value in self.default_parameters.items():
            if key not in self.parameters:
                self.parameters[key] = value
        
        try:
            import tensorflow as tf
            from tensorflow import keras
            self.tf = tf
            self.keras = keras
            
            # Check for MPS/GPU availability
            self.device = 'cpu'
            if tf.config.list_physical_devices('GPU'):
                self.device = 'gpu'
                logger.info("GPU detected for TensorFlow")
            elif hasattr(tf.config, 'list_physical_devices') and tf.config.list_physical_devices('GPU'):
                self.device = 'gpu'
                logger.info("GPU detected for TensorFlow")
            else:
                logger.info("Using CPU for TensorFlow")
                
        except ImportError:
            raise ImportError("TensorFlow is required for LSTMRegressor. Install with: pip install tensorflow")
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'LSTMRegressor':
        """Train the LSTM model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Add feature scaling for better performance
        from sklearn.preprocessing import StandardScaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Reshape for LSTM (samples, timesteps, features)
        X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
        
        # Build improved model
        self.model = self.keras.Sequential([
            self.keras.layers.Input(shape=(X_reshaped.shape[1], X_reshaped.shape[2])),
            self.keras.layers.LSTM(
                units=self.parameters.get("units", 64),
                dropout=self.parameters.get("dropout", 0.2),
                recurrent_dropout=self.parameters.get("recurrent_dropout", 0.2),
                return_sequences=True
            ),
            self.keras.layers.LSTM(
                units=self.parameters.get("units", 32),
                dropout=self.parameters.get("dropout", 0.2),
                recurrent_dropout=self.parameters.get("recurrent_dropout", 0.2),
                return_sequences=False
            ),
            self.keras.layers.Dropout(0.3),
            self.keras.layers.Dense(16, activation='relu'),
            self.keras.layers.Dense(1)
        ])
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        
        # Train model
        self.model.fit(
            X_reshaped, y,
            epochs=self.parameters.get("epochs", 100),
            batch_size=self.parameters.get("batch_size", 32),
            validation_split=self.parameters.get("validation_split", 0.2),
            verbose=0
        )
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"LSTM model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        X_reshaped = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))
        
        return self.model.predict(X_reshaped).flatten()


# PyTorch Model Definitions

class LSTMModel(nn.Module):
    """LSTM model for PyTorch"""
    
    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int, dropout: float = 0.2):
        super(LSTMModel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_dim, 
            hidden_dim, 
            num_layers, 
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, 1)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        # Take the last output
        last_output = lstm_out[:, -1, :]
        out = self.dropout(last_output)
        out = self.fc(out)
        return out


class TransformerModel(nn.Module):
    """Transformer model for PyTorch"""
    
    def __init__(self, input_dim: int, hidden_dim: int, num_heads: int, num_layers: int, dropout: float = 0.1):
        super(TransformerModel, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        # Input projection
        self.input_projection = nn.Linear(input_dim, hidden_dim)
        
        # Positional encoding
        self.pos_encoding = nn.Parameter(torch.randn(1000, hidden_dim))
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=hidden_dim,
            nhead=num_heads,
            dim_feedforward=hidden_dim * 4,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output layers
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim, 1)
    
    def forward(self, x):
        # Project input to hidden dimension
        x = self.input_projection(x)
        
        # Add positional encoding
        seq_len = x.size(1)
        pos_enc = self.pos_encoding[:seq_len, :].unsqueeze(0)
        x = x + pos_enc
        
        # Apply transformer
        x = self.transformer(x)
        
        # Take mean of sequence
        x = x.mean(dim=1)
        
        # Output layer
        x = self.dropout(x)
        x = self.fc(x)
        return x


class NeuralModelUtils:
    """Utility class for neural network models"""
    
    @staticmethod
    def get_optimal_hyperparameters(model_type: str, data_size: int, sequence_length: int = 20) -> Dict[str, Any]:
        """Get optimal hyperparameters based on data size"""
        if model_type == "lstm":
            if data_size < 1000:
                return {"hidden_dim": 64, "num_layers": 1, "dropout": 0.1, "epochs": 50}
            elif data_size < 10000:
                return {"hidden_dim": 128, "num_layers": 2, "dropout": 0.2, "epochs": 100}
            else:
                return {"hidden_dim": 256, "num_layers": 3, "dropout": 0.3, "epochs": 150}
        
        elif model_type == "transformer":
            if data_size < 1000:
                return {"hidden_dim": 64, "num_heads": 4, "num_layers": 2, "dropout": 0.1, "epochs": 50}
            elif data_size < 10000:
                return {"hidden_dim": 128, "num_heads": 8, "num_layers": 4, "dropout": 0.1, "epochs": 100}
            else:
                return {"hidden_dim": 256, "num_heads": 16, "num_layers": 6, "dropout": 0.1, "epochs": 150}
        
        return {}
    
    @staticmethod
    def create_attention_weights(model, X: np.ndarray) -> np.ndarray:
        """Create attention weights for interpretability"""
        if hasattr(model, 'transformer'):
            # For transformer models
            with torch.no_grad():
                X_tensor = torch.FloatTensor(X).to(model.device)
                attention_weights = model.transformer.get_attention_weights(X_tensor)
                return attention_weights.cpu().numpy()
        else:
            logger.warning("Attention weights not available for this model type")
            return np.array([])
    
    @staticmethod
    def analyze_model_complexity(model) -> Dict[str, Any]:
        """Analyze model complexity"""
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        return {
            "total_parameters": total_params,
            "trainable_parameters": trainable_params,
            "model_size_mb": total_params * 4 / (1024 * 1024)  # Assuming float32
        } 