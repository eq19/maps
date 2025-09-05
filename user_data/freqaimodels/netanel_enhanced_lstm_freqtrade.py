"""
FreqTrade-Optimized Netanel Enhanced LSTM V2 with Hyperopt Support
Production-ready LSTM regressor specifically designed for FreqTrade integration
with comprehensive hyperparameter optimization support
"""

import logging
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, Optional, List, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd
import os
from pathlib import Path
import pickle
import json
from datetime import datetime

# FreqTrade imports
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class TemporalAttention(nn.Module):
    """Temporal Attention Layer optimized for financial time series"""
    
    def __init__(self, hidden_dim: int, num_heads: int = 8):
        super(TemporalAttention, self).__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=num_heads,
            batch_first=True,
            dropout=0.1
        )
        self.layer_norm = nn.LayerNorm(hidden_dim)
        
    def forward(self, x):
        attn_output, attn_weights = self.attention(x, x, x)
        return self.layer_norm(x + attn_output), attn_weights

class NetanelEnhancedLSTMModel(nn.Module):
    """
    FreqTrade-optimized Enhanced LSTM Model with Hyperopt Support
    
    Features:
    - Temporal Attention Layer
    - Mixed Precision Support
    - Uncertainty Estimation
    - FreqTrade-specific optimizations
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 128,
        num_lstm_layers: int = 3,
        dropout_percent: float = 0.4,
        sequence_length: int = 10,
        output_dim: int = 1,
        use_attention: bool = True,
        attention_heads: int = 8,
        uncertainty_estimation: bool = True,
        activation: str = 'relu'
    ):
        super(NetanelEnhancedLSTMModel, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_lstm_layers = num_lstm_layers
        self.dropout_percent = dropout_percent
        self.sequence_length = sequence_length
        self.output_dim = output_dim
        self.use_attention = use_attention
        self.uncertainty_estimation = uncertainty_estimation
        
        # LSTM layers with enhanced architecture
        self.lstm_layers = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        
        for i in range(num_lstm_layers):
            input_size = input_dim if i == 0 else hidden_dim
            lstm = nn.LSTM(
                input_size=input_size,
                hidden_size=hidden_dim,
                batch_first=True,
                dropout=dropout_percent if i < num_lstm_layers - 1 else 0,
                bidirectional=False  # Simplified for FreqTrade
            )
            self.lstm_layers.append(lstm)
            self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
            self.dropouts.append(nn.Dropout(dropout_percent))
        
        # Temporal Attention Layer
        if use_attention:
            self.attention = TemporalAttention(hidden_dim, attention_heads)
        
        # Activation function selection
        if activation == 'relu':
            self.activation = nn.ReLU()
        elif activation == 'gelu':
            self.activation = nn.GELU()
        elif activation == 'swish':
            self.activation = nn.SiLU()
        else:
            self.activation = nn.ReLU()
        
        # Enhanced fully connected layers
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.alpha_dropout = nn.AlphaDropout(dropout_percent)
        
        # Main prediction head
        self.fc_mean = nn.Linear(hidden_dim // 2, output_dim)
        
        # Uncertainty estimation head
        if uncertainty_estimation:
            self.fc_log_var = nn.Linear(hidden_dim // 2, output_dim)
        
        # Initialize weights with Xavier/He initialization
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights using best practices for LSTM"""
        for name, param in self.named_parameters():
            if 'weight_ih' in name:
                nn.init.xavier_uniform_(param.data)
            elif 'weight_hh' in name:
                nn.init.orthogonal_(param.data)
            elif 'bias' in name:
                param.data.fill_(0)
            elif 'fc' in name and 'weight' in name:
                nn.init.kaiming_normal_(param.data)
    
    def forward(self, x, return_attention_weights=False):
        batch_size, seq_len, _ = x.shape
        attention_weights = None
        
        # Pass through LSTM layers
        for i, (lstm, batch_norm, dropout) in enumerate(zip(self.lstm_layers, self.batch_norms, self.dropouts)):
            lstm_out, _ = lstm(x)
            
            # Apply batch normalization
            lstm_out_reshaped = lstm_out.contiguous().view(-1, self.hidden_dim)
            lstm_out_normalized = batch_norm(lstm_out_reshaped)
            lstm_out = lstm_out_normalized.view(batch_size, seq_len, self.hidden_dim)
            
            x = dropout(lstm_out)
        
        # Apply temporal attention if enabled
        if self.use_attention:
            x, attention_weights = self.attention(x)
        
        # Take the last time step
        x = x[:, -1, :]
        
        # Fully connected layers
        x = self.fc1(x)
        x = self.activation(x)
        x = self.alpha_dropout(x)
        
        # Mean prediction
        mean = self.fc_mean(x)
        
        outputs = {'mean': mean}
        
        # Uncertainty estimation
        if self.uncertainty_estimation:
            log_var = self.fc_log_var(x)
            outputs['log_var'] = log_var
            outputs['std'] = torch.exp(0.5 * log_var)
        
        if return_attention_weights and attention_weights is not None:
            outputs['attention_weights'] = attention_weights
        
        return outputs

class TradingMetrics:
    """FreqTrade-specific trading metrics calculator"""
    
    @staticmethod
    def calculate_directional_accuracy(y_true, y_pred, threshold=0.0):
        """Calculate directional accuracy for trading signals"""
        y_true_direction = np.sign(y_true - threshold)
        y_pred_direction = np.sign(y_pred - threshold)
        return np.mean(y_true_direction == y_pred_direction)
    
    @staticmethod
    def calculate_freqtrade_metrics(y_true, y_pred):
        """Calculate metrics specifically relevant to FreqTrade"""
        metrics = {}
        
        # Basic regression metrics
        metrics['mse'] = mean_squared_error(y_true, y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['r2'] = r2_score(y_true, y_pred)
        
        # Trading-specific metrics
        metrics['directional_accuracy'] = TradingMetrics.calculate_directional_accuracy(y_true, y_pred)
        
        # Price movement prediction accuracy
        if len(y_pred) > 1:
            pred_changes = np.diff(y_pred)
            true_changes = np.diff(y_true)
            if len(pred_changes) > 0:
                change_correlation = np.corrcoef(pred_changes, true_changes)[0, 1]
                metrics['change_correlation'] = change_correlation if not np.isnan(change_correlation) else 0
        
        return metrics

class NetanelEnhancedLSTMFreqTrade(BaseRegressionModel):
    """
    FreqTrade-Optimized Enhanced LSTM Regressor with Hyperopt Support
    
    This model is specifically designed for FreqTrade integration with:
    - Full hyperopt parameter support
    - FreqTrade-specific optimizations
    - Production-ready features
    - Model persistence
    - Trading-specific metrics
    """
    
    def __init__(self, dk: FreqaiDataKitchen, **kwargs):
        super().__init__(dk, **kwargs)
        
        # FreqTrade model parameters with hyperopt support
        self.freqai_info = dk.freqai_info
        model_params = self.freqai_info.get("model_training_parameters", {})
        
        # Core LSTM parameters (hyperopt-enabled)
        self.hidden_dim = model_params.get('hidden_dim', 128)
        self.num_lstm_layers = model_params.get('num_lstm_layers', 3)
        self.dropout_percent = model_params.get('dropout_percent', 0.4)
        self.sequence_length = model_params.get('sequence_length', 10)
        self.learning_rate = model_params.get('learning_rate', 3e-3)
        self.batch_size = model_params.get('batch_size', 32)
        self.epochs = model_params.get('epochs', 100)
        
        # Enhanced features (hyperopt-enabled)
        self.use_attention = model_params.get('use_attention', True)
        self.attention_heads = model_params.get('attention_heads', 8)
        self.uncertainty_estimation = model_params.get('uncertainty_estimation', True)
        self.mixed_precision = model_params.get('mixed_precision', True)
        self.activation = model_params.get('activation', 'relu')
        
        # Training parameters (hyperopt-enabled)
        self.early_stopping_patience = model_params.get('early_stopping_patience', 15)
        self.validation_split = model_params.get('validation_split', 0.2)
        self.weight_decay = model_params.get('weight_decay', 1e-5)
        self.gradient_clip_norm = model_params.get('gradient_clip_norm', 1.0)
        
        # Optimizer parameters (hyperopt-enabled)
        self.optimizer_type = model_params.get('optimizer_type', 'adamw')
        self.scheduler_type = model_params.get('scheduler_type', 'plateau')
        self.scheduler_patience = model_params.get('scheduler_patience', 5)
        self.scheduler_factor = model_params.get('scheduler_factor', 0.5)
        
        # Device selection with FreqTrade compatibility
        if torch.backends.mps.is_available() and model_params.get('use_mps', True):
            self.device = torch.device('mps')
            logger.info("Using MPS (Apple Silicon) acceleration")
        elif torch.cuda.is_available():
            self.device = torch.device('cuda')
            logger.info("Using CUDA acceleration")
        else:
            self.device = torch.device('cpu')
            logger.info("Using CPU")
        
        # Model components
        self.model = None
        self.scaler = StandardScaler()
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.scaler_grad = None
        
        # Training tracking
        self.training_history = []
        self.best_model_state = None
        
        # FreqTrade-specific attributes
        self.CONV_WIDTH = model_params.get('conv_width', 1)  # For FreqTrade compatibility
        
        # Create model directory
        self.model_dir = Path("user_data/models/netanel_lstm")
        self.model_dir.mkdir(parents=True, exist_ok=True)
    
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen) -> Any:
        """
        FreqTrade-compatible training method with comprehensive features
        """
        try:
            logger.info("Starting NetanelEnhancedLSTMFreqTrade training...")
            
            # Extract data from FreqTrade data dictionary
            X_train = data_dictionary["train_features"].values
            y_train = data_dictionary["train_labels"].values.ravel()
            
            # Validation data if available
            if "test_features" in data_dictionary:
                X_val = data_dictionary["test_features"].values
                y_val = data_dictionary["test_labels"].values.ravel()
            else:
                # Split validation from training data
                val_size = int(len(X_train) * self.validation_split)
                X_val = X_train[-val_size:]
                y_val = y_train[-val_size:]
                X_train = X_train[:-val_size]
                y_train = y_train[:-val_size]
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_val_scaled = self.scaler.transform(X_val)
            
            # Create sequences for LSTM
            X_train_seq, y_train_seq = self._create_sequences(X_train_scaled, y_train)
            X_val_seq, y_val_seq = self._create_sequences(X_val_scaled, y_val)
            
            # Convert to tensors
            X_train_tensor = torch.FloatTensor(X_train_seq).to(self.device)
            y_train_tensor = torch.FloatTensor(y_train_seq).to(self.device)
            X_val_tensor = torch.FloatTensor(X_val_seq).to(self.device)
            y_val_tensor = torch.FloatTensor(y_val_seq).to(self.device)
            
            # Initialize model
            input_dim = X_train_tensor.shape[-1]
            self.model = NetanelEnhancedLSTMModel(
                input_dim=input_dim,
                hidden_dim=self.hidden_dim,
                num_lstm_layers=self.num_lstm_layers,
                dropout_percent=self.dropout_percent,
                sequence_length=self.sequence_length,
                use_attention=self.use_attention,
                attention_heads=self.attention_heads,
                uncertainty_estimation=self.uncertainty_estimation,
                activation=self.activation
            ).to(self.device)
            
            # Optimizer selection (hyperopt-enabled)
            if self.optimizer_type == 'adamw':
                self.optimizer = torch.optim.AdamW(
                    self.model.parameters(),
                    lr=self.learning_rate,
                    weight_decay=self.weight_decay
                )
            elif self.optimizer_type == 'adam':
                self.optimizer = torch.optim.Adam(
                    self.model.parameters(),
                    lr=self.learning_rate,
                    weight_decay=self.weight_decay
                )
            elif self.optimizer_type == 'sgd':
                self.optimizer = torch.optim.SGD(
                    self.model.parameters(),
                    lr=self.learning_rate,
                    momentum=0.9,
                    weight_decay=self.weight_decay
                )
            
            # Mixed precision training
            if self.mixed_precision and self.device.type in ['cuda']:
                self.scaler_grad = torch.cuda.amp.GradScaler()
            
            # Learning rate scheduler (hyperopt-enabled)
            if self.scheduler_type == 'plateau':
                scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                    self.optimizer, 
                    mode='min', 
                    factor=self.scheduler_factor, 
                    patience=self.scheduler_patience
                )
            elif self.scheduler_type == 'cosine':
                scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                    self.optimizer, T_max=self.epochs
                )
            elif self.scheduler_type == 'exponential':
                scheduler = torch.optim.lr_scheduler.ExponentialLR(
                    self.optimizer, gamma=0.95
                )
            else:
                scheduler = None
            
            # Training loop
            best_val_loss = float('inf')
            patience_counter = 0
            
            for epoch in range(self.epochs):
                # Training phase
                self.model.train()
                train_loss = 0
                train_preds = []
                train_targets = []
                
                for i in range(0, len(X_train_tensor), self.batch_size):
                    batch_X = X_train_tensor[i:i + self.batch_size]
                    batch_y = y_train_tensor[i:i + self.batch_size]
                    
                    self.optimizer.zero_grad()
                    
                    # Mixed precision forward pass
                    if self.mixed_precision and self.scaler_grad:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(batch_X)
                            predictions = outputs['mean'] if isinstance(outputs, dict) else outputs
                            
                            if isinstance(outputs, dict) and 'log_var' in outputs:
                                # Uncertainty-aware loss
                                precision = torch.exp(-outputs['log_var'])
                                loss = torch.mean(precision * (predictions.squeeze() - batch_y)**2 + outputs['log_var'])
                            else:
                                loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        self.scaler_grad.scale(loss).backward()
                        self.scaler_grad.unscale_(self.optimizer)
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=self.gradient_clip_norm)
                        self.scaler_grad.step(self.optimizer)
                        self.scaler_grad.update()
                    else:
                        outputs = self.model(batch_X)
                        predictions = outputs['mean'] if isinstance(outputs, dict) else outputs
                        
                        if isinstance(outputs, dict) and 'log_var' in outputs:
                            precision = torch.exp(-outputs['log_var'])
                            loss = torch.mean(precision * (predictions.squeeze() - batch_y)**2 + outputs['log_var'])
                        else:
                            loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        loss.backward()
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=self.gradient_clip_norm)
                        self.optimizer.step()
                    
                    train_loss += loss.item()
                    train_preds.extend(predictions.squeeze().detach().cpu().numpy())
                    train_targets.extend(batch_y.detach().cpu().numpy())
                
                # Validation phase
                self.model.eval()
                val_loss = 0
                val_preds = []
                val_targets = []
                
                with torch.no_grad():
                    for i in range(0, len(X_val_tensor), self.batch_size):
                        batch_X = X_val_tensor[i:i + self.batch_size]
                        batch_y = y_val_tensor[i:i + self.batch_size]
                        
                        outputs = self.model(batch_X)
                        predictions = outputs['mean'] if isinstance(outputs, dict) else outputs
                        
                        if isinstance(outputs, dict) and 'log_var' in outputs:
                            precision = torch.exp(-outputs['log_var'])
                            loss = torch.mean(precision * (predictions.squeeze() - batch_y)**2 + outputs['log_var'])
                        else:
                            loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        val_loss += loss.item()
                        val_preds.extend(predictions.squeeze().cpu().numpy())
                        val_targets.extend(batch_y.cpu().numpy())
                
                # Calculate metrics
                train_loss /= len(X_train_tensor)
                val_loss /= len(X_val_tensor)
                
                train_metrics = TradingMetrics.calculate_freqtrade_metrics(
                    np.array(train_targets), np.array(train_preds)
                )
                val_metrics = TradingMetrics.calculate_freqtrade_metrics(
                    np.array(val_targets), np.array(val_preds)
                )
                
                # Learning rate scheduling
                if scheduler:
                    if self.scheduler_type == 'plateau':
                        scheduler.step(val_loss)
                    else:
                        scheduler.step()
                
                # Early stopping
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                    self.best_model_state = self.model.state_dict().copy()
                else:
                    patience_counter += 1
                
                # Record training history
                history_entry = {
                    'epoch': epoch,
                    'train_loss': train_loss,
                    'val_loss': val_loss,
                    'train_r2': train_metrics.get('r2', 0),
                    'val_r2': val_metrics.get('r2', 0),
                    'train_directional_accuracy': train_metrics.get('directional_accuracy', 0),
                    'val_directional_accuracy': val_metrics.get('directional_accuracy', 0),
                    'learning_rate': self.optimizer.param_groups[0]['lr']
                }
                self.training_history.append(history_entry)
                
                # Logging for FreqTrade
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Train Loss = {train_loss:.6f}, Val Loss = {val_loss:.6f}, "
                              f"Val R² = {val_metrics.get('r2', 0):.4f}, "
                              f"Val Dir. Acc = {val_metrics.get('directional_accuracy', 0):.4f}")
                
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Load best model state
            if hasattr(self, 'best_model_state'):
                self.model.load_state_dict(self.best_model_state)
            
            # Final evaluation
            self.model.eval()
            with torch.no_grad():
                train_outputs = self.model(X_train_tensor)
                val_outputs = self.model(X_val_tensor)
                
                train_pred = train_outputs['mean'].cpu().numpy() if isinstance(train_outputs, dict) else train_outputs.cpu().numpy()
                val_pred = val_outputs['mean'].cpu().numpy() if isinstance(val_outputs, dict) else val_outputs.cpu().numpy()
                
                final_train_metrics = TradingMetrics.calculate_freqtrade_metrics(y_train_seq, train_pred.ravel())
                final_val_metrics = TradingMetrics.calculate_freqtrade_metrics(y_val_seq, val_pred.ravel())
                
                logger.info(f"Training completed - Train R²: {final_train_metrics.get('r2', 0):.4f}, "
                          f"Val R²: {final_val_metrics.get('r2', 0):.4f}, "
                          f"Val Dir. Acc: {final_val_metrics.get('directional_accuracy', 0):.4f}")
            
            # Save model for FreqTrade
            self.save_model()
            
            return self
            
        except Exception as e:
            logger.error(f"Error during NetanelEnhancedLSTMFreqTrade training: {str(e)}")
            raise
    
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        FreqTrade-compatible prediction method
        """
        try:
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            # Extract features for prediction
            X = unfiltered_df[dk.training_features_list].values
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make predictions
            predictions = []
            uncertainties = []
            
            for i in range(len(X_scaled)):
                # Get sequence ending at current point
                start_idx = max(0, i + 1 - self.sequence_length)
                end_idx = i + 1
                
                sequence_data = X_scaled[start_idx:end_idx]
                
                # Pad if necessary
                if len(sequence_data) < self.sequence_length:
                    padding_needed = self.sequence_length - len(sequence_data)
                    padding = np.zeros((padding_needed, X_scaled.shape[1]))
                    sequence_data = np.vstack([padding, sequence_data])
                
                # Reshape for model input
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                # Make prediction
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    
                    if isinstance(outputs, dict):
                        pred = outputs['mean'].cpu().numpy().flatten()[0]
                        predictions.append(pred)
                        
                        if 'std' in outputs:
                            uncertainty = outputs['std'].cpu().numpy().flatten()[0]
                            uncertainties.append(uncertainty)
                        else:
                            uncertainties.append(0.0)
                    else:
                        pred = outputs.cpu().numpy().flatten()[0]
                        predictions.append(pred)
                        uncertainties.append(0.0)
            
            # Create prediction DataFrame for FreqTrade
            predictions_df = pd.DataFrame(predictions, columns=[f"&-{dk.label_list[0]}"])
            predictions_df.index = unfiltered_df.index
            
            # Create do_predict DataFrame (FreqTrade requirement)
            do_predict = pd.DataFrame(np.ones(len(predictions)), columns=["do_predict"])
            do_predict.index = unfiltered_df.index
            
            return predictions_df, do_predict
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            # Return zeros for safety
            predictions_df = pd.DataFrame(np.zeros(len(unfiltered_df)), columns=[f"&-{dk.label_list[0]}"])
            predictions_df.index = unfiltered_df.index
            do_predict = pd.DataFrame(np.ones(len(unfiltered_df)), columns=["do_predict"])
            do_predict.index = unfiltered_df.index
            return predictions_df, do_predict
    
    def _create_sequences(self, data: np.ndarray, target: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for LSTM training"""
        sequences = []
        targets = []
        
        for i in range(len(data) - self.sequence_length):
            seq = data[i:i + self.sequence_length]
            tar = target[i + self.sequence_length]
            sequences.append(seq)
            targets.append(tar)
        
        return np.array(sequences), np.array(targets)
    
    def save_model(self, filepath: Optional[str] = None):
        """Save model for FreqTrade persistence"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.model_dir / f"netanel_freqtrade_{timestamp}.pt"
        else:
            filepath = Path(filepath)
        
        if self.model is None:
            raise ValueError("No trained model to save")
        
        save_dict = {
            'model_state_dict': self.model.state_dict(),
            'model_config': {
                'input_dim': self.model.input_dim,
                'hidden_dim': self.hidden_dim,
                'num_lstm_layers': self.num_lstm_layers,
                'dropout_percent': self.dropout_percent,
                'sequence_length': self.sequence_length,
                'use_attention': self.use_attention,
                'attention_heads': self.attention_heads,
                'uncertainty_estimation': self.uncertainty_estimation,
                'activation': self.activation
            },
            'scaler': self.scaler,
            'training_history': self.training_history,
            'hyperopt_parameters': {
                'hidden_dim': self.hidden_dim,
                'num_lstm_layers': self.num_lstm_layers,
                'dropout_percent': self.dropout_percent,
                'learning_rate': self.learning_rate,
                'batch_size': self.batch_size,
                'use_attention': self.use_attention,
                'attention_heads': self.attention_heads,
                'optimizer_type': self.optimizer_type,
                'scheduler_type': self.scheduler_type,
                'activation': self.activation
            },
            'device': str(self.device),
            'timestamp': datetime.now().isoformat()
        }
        
        torch.save(save_dict, filepath)
        logger.info(f"FreqTrade model saved to {filepath}")
        return str(filepath)
    
    def load_model(self, filepath: str):
        """Load model for FreqTrade"""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        checkpoint = torch.load(filepath, map_location=self.device)
        
        # Recreate model with saved configuration
        config = checkpoint['model_config']
        self.model = NetanelEnhancedLSTMModel(**config).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Restore other components
        self.scaler = checkpoint['scaler']
        self.training_history = checkpoint.get('training_history', [])
        
        logger.info(f"FreqTrade model loaded from {filepath}")
        return self

    @staticmethod
    def get_hyperopt_parameters():
        """
        Return hyperopt parameter space for FreqTrade optimization
        
        This method defines the search space for hyperparameter optimization
        specifically designed for FreqTrade's hyperopt functionality.
        """
        from freqtrade.optimize.space import Categorical, Integer, Real
        
        return [
            # Core LSTM architecture parameters
            Integer('hidden_dim', 64, 512, default=128),
            Integer('num_lstm_layers', 1, 5, default=3),
            Real('dropout_percent', 0.1, 0.7, default=0.4),
            Integer('sequence_length', 5, 30, default=10),
            
            # Learning parameters
            Real('learning_rate', 1e-5, 1e-2, default=3e-3),
            Integer('batch_size', 16, 128, default=32),
            Integer('epochs', 50, 300, default=100),
            
            # Enhanced features
            Categorical('use_attention', [True, False], default=True),
            Integer('attention_heads', 4, 16, default=8),
            Categorical('uncertainty_estimation', [True, False], default=True),
            Categorical('activation', ['relu', 'gelu', 'swish'], default='relu'),
            
            # Optimization parameters
            Categorical('optimizer_type', ['adamw', 'adam', 'sgd'], default='adamw'),
            Categorical('scheduler_type', ['plateau', 'cosine', 'exponential'], default='plateau'),
            Real('weight_decay', 1e-6, 1e-3, default=1e-5),
            Integer('early_stopping_patience', 5, 25, default=15),
            
            # Scheduler parameters
            Integer('scheduler_patience', 3, 10, default=5),
            Real('scheduler_factor', 0.1, 0.8, default=0.5),
            Real('gradient_clip_norm', 0.5, 2.0, default=1.0),
        ]
    
    def get_model_info(self):
        """Get model information for FreqTrade"""
        return {
            "model_name": "NetanelEnhancedLSTMFreqTrade",
            "model_type": "neural_enhanced_freqtrade",
            "version": "2.0",
            "freqtrade_compatible": True,
            "hyperopt_enabled": True,
            "parameters": {
                "hidden_dim": self.hidden_dim,
                "num_lstm_layers": self.num_lstm_layers,
                "dropout_percent": self.dropout_percent,
                "sequence_length": self.sequence_length,
                "learning_rate": self.learning_rate,
                "use_attention": self.use_attention,
                "uncertainty_estimation": self.uncertainty_estimation
            },
            "device": str(self.device),
            "training_history_length": len(self.training_history),
            "features": [
                "FreqTrade Integration",
                "Hyperopt Parameter Support",
                "Temporal Attention Layer",
                "Uncertainty Estimation",
                "Mixed Precision Training", 
                "Advanced Optimizers & Schedulers",
                "Trading-Specific Metrics",
                "Model Persistence",
                "Early Stopping",
                "Gradient Clipping"
            ],
            "hyperopt_parameters": self.get_hyperopt_parameters(),
            "recommended_use": "Production FreqTrade crypto price prediction with hyperopt optimization"
        }