"""
Neural Network Trinary Classifiers based on nateemma's strategies
Includes LSTM, Transformer, and ensemble classifiers for crypto trading
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from typing import Dict, Any, Optional, List, Tuple
import warnings

try:
    from .base import BaseFreqAIModel
except ImportError:
    # Fallback for direct execution
    try:
        from base import BaseFreqAIModel
    except ImportError:
        # Final fallback - create minimal base class
        class BaseFreqAIModel:
            def __init__(self, **kwargs):
                self.parameters = kwargs
                self.is_trained = False
                
            def fit(self, X, y, **kwargs):
                raise NotImplementedError
                
            def predict(self, X):
                raise NotImplementedError
                
            def get_model_info(self):
                return {"model_name": "BaseFreqAIModel"}

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')


class NNTCLSTMModel(nn.Module):
    """
    Neural Network Trinary Classifier using LSTM
    Based on nateemma's NNTC architecture
    """
    
    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2, dropout: float = 0.3):
        super(NNTCLSTMModel, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        
        self.batch_norm = nn.BatchNorm1d(hidden_dim * 2)  # *2 for bidirectional
        self.dropout = nn.Dropout(dropout)
        self.fc1 = nn.Linear(hidden_dim * 2, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, 3)  # 3 classes: sell, hold, buy
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        
        # Take the last output
        last_output = lstm_out[:, -1, :]
        
        # Batch normalization
        normalized = self.batch_norm(last_output)
        
        # Fully connected layers
        x = self.dropout(normalized)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        
        return self.softmax(x)


class NNTCTransformerModel(nn.Module):
    """
    Neural Network Trinary Classifier using Transformer
    """
    
    def __init__(self, input_dim: int, d_model: int = 64, nhead: int = 8, num_layers: int = 2, dropout: float = 0.3):
        super(NNTCTransformerModel, self).__init__()
        
        self.d_model = d_model
        self.input_projection = nn.Linear(input_dim, d_model)
        
        # Positional encoding
        self.pos_encoding = nn.Parameter(torch.randn(100, d_model))
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model // 2, 3),
            nn.Softmax(dim=1)
        )
    
    def forward(self, x):
        seq_len = x.size(1)
        
        # Project input to d_model dimension
        x = self.input_projection(x)
        
        # Add positional encoding
        x = x + self.pos_encoding[:seq_len, :].unsqueeze(0)
        
        # Transformer encoding
        x = self.transformer(x)
        
        # Global average pooling
        x = x.mean(dim=1)
        
        # Classification
        return self.classifier(x)


class NateemmaNeuralClassifier(BaseFreqAIModel):
    """
    Neural Network Trinary Classifier based on nateemma's proven strategies
    Features:
    - PCA dimensionality reduction
    - Multiple neural architectures (LSTM, Transformer, Ensemble)
    - Trinary classification (sell, hold, buy)
    - Crypto-optimized indicators
    """
    
    model_type = "neural_classifier"
    default_parameters = {
        "architecture": "lstm",  # lstm, transformer, ensemble
        "hidden_dim": 64,
        "num_layers": 2,
        "dropout": 0.3,
        "sequence_length": 10,
        "pca_components": 10,
        "use_pca": True,
        "learning_rate": 1e-3,
        "batch_size": 32,
        "epochs": 100,
        "early_stopping_patience": 15,
        "validation_split": 0.2,
        "class_weights": [1.0, 1.0, 1.0],  # sell, hold, buy
        "confidence_threshold": 0.6
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Model parameters
        self.architecture = kwargs.get('architecture', 'lstm')
        self.hidden_dim = kwargs.get('hidden_dim', 64)
        self.num_layers = kwargs.get('num_layers', 2)
        self.dropout = kwargs.get('dropout', 0.3)
        self.sequence_length = kwargs.get('sequence_length', 10)
        self.pca_components = kwargs.get('pca_components', 10)
        self.use_pca = kwargs.get('use_pca', True)
        self.learning_rate = kwargs.get('learning_rate', 1e-3)
        self.batch_size = kwargs.get('batch_size', 32)
        self.epochs = kwargs.get('epochs', 100)
        self.early_stopping_patience = kwargs.get('early_stopping_patience', 15)
        self.validation_split = kwargs.get('validation_split', 0.2)
        self.class_weights = torch.FloatTensor(kwargs.get('class_weights', [1.0, 1.0, 1.0]))
        self.confidence_threshold = kwargs.get('confidence_threshold', 0.6)
        
        # Device selection
        if torch.backends.mps.is_available():
            self.device = torch.device('mps')
            logger.info("Using MPS (Apple Silicon) acceleration")
        elif torch.cuda.is_available():
            self.device = torch.device('cuda')
            logger.info("Using CUDA acceleration")
        else:
            self.device = torch.device('cpu')
            logger.info("Using CPU")
        
        self.class_weights = self.class_weights.to(self.device)
        
        # Components
        self.model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.pca_components) if self.use_pca else None
        self.training_history = []
        
        # Class mapping
        self.class_names = ['sell', 'hold', 'buy']
        self.class_mapping = {0: 'sell', 1: 'hold', 2: 'buy'}
    
    def _create_sequences(self, data: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for neural network training"""
        sequences = []
        targets = []
        
        for i in range(len(data) - self.sequence_length + 1):
            seq = data[i:i + self.sequence_length]
            target = labels[i + self.sequence_length - 1]  # Use the last label in sequence
            sequences.append(seq)
            targets.append(target)
        
        return np.array(sequences), np.array(targets)
    
    def _generate_signals(self, returns: np.ndarray, threshold: float = 0.01) -> np.ndarray:
        """
        Generate trading signals based on forward returns
        0: sell, 1: hold, 2: buy
        """
        signals = np.ones(len(returns))  # Default to hold
        
        # Buy signals for positive returns above threshold
        signals[returns > threshold] = 2
        
        # Sell signals for negative returns below threshold
        signals[returns < -threshold] = 0
        
        return signals.astype(int)
    
    def _calculate_forward_returns(self, prices: np.ndarray, periods: int = 5) -> np.ndarray:
        """Calculate forward returns for signal generation"""
        returns = np.zeros(len(prices))
        
        for i in range(len(prices) - periods):
            current_price = prices[i]
            future_price = prices[i + periods]
            returns[i] = (future_price - current_price) / current_price
        
        return returns
    
    def _create_model(self, input_dim: int) -> nn.Module:
        """Create neural network model based on architecture"""
        if self.architecture == 'lstm':
            return NNTCLSTMModel(
                input_dim=input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.num_layers,
                dropout=self.dropout
            )
        elif self.architecture == 'transformer':
            return NNTCTransformerModel(
                input_dim=input_dim,
                d_model=self.hidden_dim,
                nhead=min(8, self.hidden_dim // 8),
                num_layers=self.num_layers,
                dropout=self.dropout
            )
        elif self.architecture == 'ensemble':
            # Create ensemble of LSTM and Transformer
            lstm_model = NNTCLSTMModel(input_dim, self.hidden_dim, self.num_layers, self.dropout)
            transformer_model = NNTCTransformerModel(input_dim, self.hidden_dim, min(8, self.hidden_dim // 8), self.num_layers, self.dropout)
            
            class EnsembleModel(nn.Module):
                def __init__(self, lstm, transformer):
                    super().__init__()
                    self.lstm = lstm
                    self.transformer = transformer
                    self.combiner = nn.Linear(6, 3)  # 3 outputs from each model
                    self.softmax = nn.Softmax(dim=1)
                
                def forward(self, x):
                    lstm_out = self.lstm(x)
                    transformer_out = self.transformer(x)
                    combined = torch.cat([lstm_out, transformer_out], dim=1)
                    return self.softmax(self.combiner(combined))
            
            return EnsembleModel(lstm_model, transformer_model)
        else:
            raise ValueError(f"Unknown architecture: {self.architecture}")
    
    def fit(self, X, y, **kwargs):
        """
        Train the neural classifier
        """
        try:
            logger.info(f"Starting NateemmaNeuralClassifier training with {self.architecture} architecture...")
            
            # Prepare features
            X_scaled = self.scaler.fit_transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.fit_transform(X_scaled)
                logger.info(f"PCA reduced dimensions from {X_scaled.shape[1]} to {X_reduced.shape[1]}")
            else:
                X_reduced = X_scaled
            
            # Generate classification labels if continuous target is provided
            if len(np.unique(y)) > 3:
                # Assume y is price data, calculate forward returns and generate signals
                forward_returns = self._calculate_forward_returns(y)
                y_class = self._generate_signals(forward_returns)
                logger.info("Generated classification signals from continuous target")
            else:
                # Assume y is already classification labels
                y_class = y.astype(int)
            
            # Create sequences
            X_seq, y_seq = self._create_sequences(X_reduced, y_class)
            
            # Split validation data
            val_size = int(len(X_seq) * self.validation_split)
            X_train, X_val = X_seq[:-val_size], X_seq[-val_size:]
            y_train, y_val = y_seq[:-val_size], y_seq[-val_size:]
            
            # Convert to tensors
            X_train = torch.FloatTensor(X_train).to(self.device)
            y_train = torch.LongTensor(y_train).to(self.device)
            X_val = torch.FloatTensor(X_val).to(self.device)
            y_val = torch.LongTensor(y_val).to(self.device)
            
            # Create model
            input_dim = X_train.shape[-1]
            self.model = self._create_model(input_dim).to(self.device)
            
            # Optimizer and loss function
            optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.learning_rate,
                weight_decay=1e-5
            )
            
            criterion = nn.CrossEntropyLoss(weight=self.class_weights)
            
            # Learning rate scheduler
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, mode='min', factor=0.5, patience=5
            )
            
            # Training loop
            best_val_acc = 0.0
            patience_counter = 0
            
            for epoch in range(self.epochs):
                # Training phase
                self.model.train()
                train_loss = 0
                train_correct = 0
                train_total = 0
                
                for i in range(0, len(X_train), self.batch_size):
                    batch_X = X_train[i:i + self.batch_size]
                    batch_y = y_train[i:i + self.batch_size]
                    
                    optimizer.zero_grad()
                    outputs = self.model(batch_X)
                    loss = criterion(outputs, batch_y)
                    loss.backward()
                    
                    # Gradient clipping
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                    
                    optimizer.step()
                    
                    train_loss += loss.item()
                    _, predicted = torch.max(outputs.data, 1)
                    train_total += batch_y.size(0)
                    train_correct += (predicted == batch_y).sum().item()
                
                # Validation phase
                self.model.eval()
                val_loss = 0
                val_correct = 0
                val_total = 0
                
                with torch.no_grad():
                    for i in range(0, len(X_val), self.batch_size):
                        batch_X = X_val[i:i + self.batch_size]
                        batch_y = y_val[i:i + self.batch_size]
                        
                        outputs = self.model(batch_X)
                        loss = criterion(outputs, batch_y)
                        
                        val_loss += loss.item()
                        _, predicted = torch.max(outputs.data, 1)
                        val_total += batch_y.size(0)
                        val_correct += (predicted == batch_y).sum().item()
                
                # Calculate accuracies
                train_acc = train_correct / train_total
                val_acc = val_correct / val_total
                avg_val_loss = val_loss / len(X_val) * self.batch_size
                
                # Learning rate scheduling
                scheduler.step(avg_val_loss)
                
                # Early stopping based on validation accuracy
                if val_acc > best_val_acc:
                    best_val_acc = val_acc
                    patience_counter = 0
                    # Save best model state
                    self.best_model_state = self.model.state_dict().copy()
                else:
                    patience_counter += 1
                
                # Log progress
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Train Acc = {train_acc:.4f}, Val Acc = {val_acc:.4f}")
                
                # Record training history
                self.training_history.append({
                    'epoch': epoch,
                    'train_loss': train_loss / len(X_train) * self.batch_size,
                    'val_loss': avg_val_loss,
                    'train_accuracy': train_acc,
                    'val_accuracy': val_acc,
                    'learning_rate': optimizer.param_groups[0]['lr']
                })
                
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Load best model state
            if hasattr(self, 'best_model_state'):
                self.model.load_state_dict(self.best_model_state)
            
            logger.info(f"Training completed - Best Val Accuracy: {best_val_acc:.4f}")
            
            return self
            
        except Exception as e:
            logger.error(f"Error during NateemmaNeuralClassifier training: {str(e)}")
            raise
    
    def predict(self, X):
        """
        Make predictions using the trained classifier
        Returns numerical predictions (0=sell, 1=hold, 2=buy) for compatibility
        """
        try:
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            # Prepare features
            X_scaled = self.scaler.transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.transform(X_scaled)
            else:
                X_reduced = X_scaled
            
            # For prediction, we need to create predictions for each sample
            predictions = []
            
            for i in range(len(X_reduced)):
                # Get sequence ending at current point
                start_idx = max(0, i + 1 - self.sequence_length)
                end_idx = i + 1
                
                sequence_data = X_reduced[start_idx:end_idx]
                
                # Pad if necessary
                if len(sequence_data) < self.sequence_length:
                    padding_needed = self.sequence_length - len(sequence_data)
                    padding = np.zeros((padding_needed, X_reduced.shape[1]))
                    sequence_data = np.vstack([padding, sequence_data])
                
                # Reshape for model input (1, seq_len, features)
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                
                # Convert to tensor
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                # Make prediction
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    probabilities = outputs.cpu().numpy()[0]
                    predicted_class = np.argmax(probabilities)
                    confidence = np.max(probabilities)
                
                # Apply confidence threshold
                if confidence < self.confidence_threshold:
                    predicted_class = 1  # Default to hold if low confidence
                
                predictions.append(predicted_class)
            
            return np.array(predictions)
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return np.ones(len(X))  # Default to hold class
    
    def predict_proba(self, X):
        """Return prediction probabilities for all classes"""
        try:
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            # Prepare features
            X_scaled = self.scaler.transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.transform(X_scaled)
            else:
                X_reduced = X_scaled
            
            # For prediction, we need to create predictions for each sample
            all_probabilities = []
            
            for i in range(len(X_reduced)):
                # Get sequence ending at current point
                start_idx = max(0, i + 1 - self.sequence_length)
                end_idx = i + 1
                
                sequence_data = X_reduced[start_idx:end_idx]
                
                # Pad if necessary
                if len(sequence_data) < self.sequence_length:
                    padding_needed = self.sequence_length - len(sequence_data)
                    padding = np.zeros((padding_needed, X_reduced.shape[1]))
                    sequence_data = np.vstack([padding, sequence_data])
                
                # Reshape for model input (1, seq_len, features)
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                
                # Convert to tensor
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                # Make prediction
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    probabilities = outputs.cpu().numpy()[0]
                
                all_probabilities.append(probabilities)
            
            return np.array(all_probabilities)
            
        except Exception as e:
            logger.error(f"Error during predict_proba: {str(e)}")
            # Return default probabilities (uniform distribution)
            return np.full((len(X), 3), 1/3)
    
    def get_model_info(self):
        """Get detailed model information"""
        return {
            "model_name": "NateemmaNeuralClassifier",
            "model_type": self.model_type,
            "architecture": self.architecture,
            "parameters": {
                "hidden_dim": self.hidden_dim,
                "num_layers": self.num_layers,
                "dropout": self.dropout,
                "sequence_length": self.sequence_length,
                "pca_components": self.pca_components if self.use_pca else None,
                "learning_rate": self.learning_rate,
                "batch_size": self.batch_size,
                "epochs": self.epochs,
                "confidence_threshold": self.confidence_threshold
            },
            "device": str(self.device),
            "training_history_length": len(self.training_history),
            "classes": self.class_names,
            "features": [
                "Trinary classification (sell/hold/buy)",
                "PCA dimensionality reduction",
                "Multiple architectures (LSTM/Transformer/Ensemble)",
                "Confidence-based predictions",
                "Early stopping and learning rate scheduling",
                "Class-weighted loss function",
                "Gradient clipping"
            ],
            "recommended_use": "Signal generation for crypto trading strategies"
        }