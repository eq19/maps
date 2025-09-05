"""
Enhanced LSTM Model V2 - Production-Ready Version
Based on Netanelshoshan's FreqAI-LSTM with comprehensive improvements
Features all requested enhancements for institutional-grade trading
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
import shap

try:
    from .base import BaseFreqAIModel
except ImportError:
    try:
        from base import BaseFreqAIModel
    except ImportError:
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

class TemporalAttention(nn.Module):
    """Temporal Attention Layer to learn which time steps matter most"""
    
    def __init__(self, hidden_dim: int, num_heads: int = 8):
        super(TemporalAttention, self).__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=num_heads,
            batch_first=True
        )
        self.layer_norm = nn.LayerNorm(hidden_dim)
        
    def forward(self, x):
        # Self-attention
        attn_output, attn_weights = self.attention(x, x, x)
        # Residual connection + layer norm
        return self.layer_norm(x + attn_output), attn_weights

class NetanelEnhancedLSTMModelV2(nn.Module):
    """
    Enhanced LSTM Model V2 with comprehensive improvements:
    - Temporal Attention Layer
    - Mixed Precision Support
    - Uncertainty Estimation
    - Advanced Architecture
    """
    
    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 128,
        num_lstm_layers: int = 3,
        dropout_percent: float = 0.4,
        window_size: int = 5,
        output_dim: int = 1,
        use_attention: bool = True,
        attention_heads: int = 8,
        uncertainty_estimation: bool = True
    ):
        super(NetanelEnhancedLSTMModelV2, self).__init__()
        
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_lstm_layers = num_lstm_layers
        self.dropout_percent = dropout_percent
        self.window_size = window_size
        self.output_dim = output_dim
        self.use_attention = use_attention
        self.uncertainty_estimation = uncertainty_estimation
        
        # LSTM layers with batch normalization and dropout
        self.lstm_layers = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        
        for i in range(num_lstm_layers):
            input_size = input_dim if i == 0 else hidden_dim
            lstm = nn.LSTM(
                input_size=input_size,
                hidden_size=hidden_dim,
                batch_first=True,
                dropout=dropout_percent if i < num_lstm_layers - 1 else 0
            )
            self.lstm_layers.append(lstm)
            self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
            self.dropouts.append(nn.Dropout(dropout_percent))
        
        # Temporal Attention Layer
        if use_attention:
            self.attention = TemporalAttention(hidden_dim, attention_heads)
        
        # Fully connected layers for mean prediction
        self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu = nn.ReLU()
        self.alpha_dropout = nn.AlphaDropout(dropout_percent)
        self.fc_mean = nn.Linear(hidden_dim // 2, output_dim)
        
        # Uncertainty estimation layers
        if uncertainty_estimation:
            self.fc_log_var = nn.Linear(hidden_dim // 2, output_dim)
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize model weights using best practices"""
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
        x = self.relu(x)
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
    """Trading-specific metrics calculator"""
    
    @staticmethod
    def calculate_hit_rate(y_true, y_pred, threshold=0.0):
        """Calculate directional accuracy (hit rate)"""
        y_true_direction = np.sign(y_true - threshold)
        y_pred_direction = np.sign(y_pred - threshold)
        return np.mean(y_true_direction == y_pred_direction)
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.0):
        """Calculate Sharpe ratio"""
        excess_returns = returns - risk_free_rate
        if np.std(excess_returns) == 0:
            return 0.0
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)  # Annualized
    
    @staticmethod
    def calculate_max_drawdown(cumulative_returns):
        """Calculate maximum drawdown"""
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - peak) / peak
        return np.min(drawdown)
    
    @staticmethod
    def calculate_profit_factor(returns):
        """Calculate profit factor (gross profit / gross loss)"""
        gains = returns[returns > 0].sum()
        losses = abs(returns[returns < 0].sum())
        return gains / losses if losses != 0 else np.inf

class EnsembleModel:
    """Ensemble wrapper for multiple models"""
    
    def __init__(self, n_models=5, **model_kwargs):
        self.n_models = n_models
        self.models = []
        self.model_kwargs = model_kwargs
        self.is_trained = False
    
    def fit(self, X, y, **kwargs):
        """Train ensemble of models with different random seeds"""
        self.models = []
        
        for i in range(self.n_models):
            # Set different random seed for each model
            torch.manual_seed(42 + i)
            np.random.seed(42 + i)
            
            from copy import deepcopy
            model_kwargs = deepcopy(self.model_kwargs)
            model = NetanelEnhancedLSTMRegressorV2(**model_kwargs)
            model.fit(X, y, **kwargs)
            self.models.append(model)
        
        self.is_trained = True
        return self
    
    def predict(self, X, return_uncertainty=False):
        """Predict using ensemble averaging"""
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before prediction")
        
        predictions = []
        uncertainties = []
        
        for model in self.models:
            pred = model.predict(X, return_uncertainty=True)
            if isinstance(pred, dict):
                predictions.append(pred['mean'])
                if 'std' in pred:
                    uncertainties.append(pred['std'])
            else:
                predictions.append(pred)
        
        # Ensemble averaging
        ensemble_pred = np.mean(predictions, axis=0)
        
        if return_uncertainty:
            # Ensemble uncertainty (epistemic + aleatoric)
            pred_std = np.std(predictions, axis=0)  # Epistemic uncertainty
            if uncertainties:
                aleatoric_std = np.mean(uncertainties, axis=0)  # Average aleatoric uncertainty
                total_std = np.sqrt(pred_std**2 + aleatoric_std**2)
            else:
                total_std = pred_std
            
            return {'mean': ensemble_pred, 'std': total_std}
        
        return ensemble_pred

class NetanelEnhancedLSTMRegressorV2(BaseFreqAIModel):
    """
    Production-Ready Enhanced LSTM Regressor V2
    
    New Features:
    - Model Persistence (save/load)
    - Loss Plotting with Training Curves  
    - Batch-wise Evaluation Metrics (R², MAE, RMSE)
    - Ensemble Support
    - Mixed Precision Training
    - Prediction Confidence/Uncertainty
    - Temporal Attention Layer
    - Trading-Specific Metrics
    - SHAP Explainability
    - Hyperparameter Tuning Ready
    """
    
    model_type = "neural_enhanced_v2"
    default_parameters = {
        "hidden_dim": 128,
        "num_lstm_layers": 3,
        "dropout_percent": 0.4,
        "window_size": 5,
        "learning_rate": 3e-3,
        "batch_size": 32,
        "epochs": 100,
        "early_stopping_patience": 10,
        "validation_split": 0.2,
        "sequence_length": 10,
        "use_attention": True,
        "attention_heads": 8,
        "uncertainty_estimation": True,
        "mixed_precision": True,
        "ensemble_size": 1,
        "plot_training": True,
        "calculate_shap": False
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Enhanced parameters
        self.hidden_dim = kwargs.get('hidden_dim', 128)
        self.num_lstm_layers = kwargs.get('num_lstm_layers', 3)
        self.dropout_percent = kwargs.get('dropout_percent', 0.4)
        self.window_size = kwargs.get('window_size', 5)
        self.learning_rate = kwargs.get('learning_rate', 3e-3)
        self.batch_size = kwargs.get('batch_size', 32)
        self.epochs = kwargs.get('epochs', 100)
        self.early_stopping_patience = kwargs.get('early_stopping_patience', 10)
        self.validation_split = kwargs.get('validation_split', 0.2)
        self.sequence_length = kwargs.get('sequence_length', 10)
        
        # V2 Features
        self.use_attention = kwargs.get('use_attention', True)
        self.attention_heads = kwargs.get('attention_heads', 8)
        self.uncertainty_estimation = kwargs.get('uncertainty_estimation', True)
        self.mixed_precision = kwargs.get('mixed_precision', True)
        self.ensemble_size = kwargs.get('ensemble_size', 1)
        self.plot_training = kwargs.get('plot_training', True)
        self.calculate_shap = kwargs.get('calculate_shap', False)
        
        # Device selection with enhanced logic
        if torch.backends.mps.is_available() and kwargs.get('use_mps', True):
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
        self.ensemble = None
        self.scaler = StandardScaler()
        self.optimizer = None
        self.criterion = nn.MSELoss()
        self.scaler_grad = None
        
        # Training tracking
        self.training_history = []
        self.best_model_state = None
        self.feature_names = None
        self.explainer = None
        
        # Create model directory
        self.model_dir = Path("saved_models")
        self.model_dir.mkdir(exist_ok=True)
    
    def save_model(self, filepath: Optional[str] = None):
        """Save complete model state including weights, scaler, and metadata"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.model_dir / f"netanel_enhanced_v2_{timestamp}.pt"
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
                'window_size': self.window_size,
                'use_attention': self.use_attention,
                'attention_heads': self.attention_heads,
                'uncertainty_estimation': self.uncertainty_estimation
            },
            'scaler': self.scaler,
            'training_history': self.training_history,
            'feature_names': self.feature_names,
            'parameters': {
                'learning_rate': self.learning_rate,
                'batch_size': self.batch_size,
                'sequence_length': self.sequence_length
            },
            'device': str(self.device),
            'timestamp': datetime.now().isoformat()
        }
        
        torch.save(save_dict, filepath)
        logger.info(f"Model saved to {filepath}")
        return str(filepath)
    
    def load_model(self, filepath: str):
        """Load complete model state"""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        checkpoint = torch.load(filepath, map_location=self.device)
        
        # Recreate model with saved configuration
        config = checkpoint['model_config']
        self.model = NetanelEnhancedLSTMModelV2(**config).to(self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Restore other components
        self.scaler = checkpoint['scaler']
        self.training_history = checkpoint.get('training_history', [])
        self.feature_names = checkpoint.get('feature_names')
        
        # Update parameters
        params = checkpoint.get('parameters', {})
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        logger.info(f"Model loaded from {filepath}")
        logger.info(f"Model trained on: {checkpoint.get('timestamp', 'Unknown')}")
        
        return self
    
    def plot_training_curves(self, save_path: Optional[str] = None):
        """Plot comprehensive training curves"""
        if not self.training_history:
            logger.warning("No training history available for plotting")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Training Progress - Netanel Enhanced LSTM V2', fontsize=16)
        
        history_df = pd.DataFrame(self.training_history)
        
        # Loss curves
        axes[0, 0].plot(history_df['epoch'], history_df['train_loss'], label='Train Loss', alpha=0.8)
        axes[0, 0].plot(history_df['epoch'], history_df['val_loss'], label='Val Loss', alpha=0.8)
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].set_title('Loss Curves')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # R² scores
        if 'train_r2' in history_df.columns:
            axes[0, 1].plot(history_df['epoch'], history_df['train_r2'], label='Train R²', alpha=0.8)
            axes[0, 1].plot(history_df['epoch'], history_df['val_r2'], label='Val R²', alpha=0.8)
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('R² Score')
            axes[0, 1].set_title('R² Score Progress')
            axes[0, 1].legend()
            axes[0, 1].grid(True, alpha=0.3)
        
        # MAE
        if 'train_mae' in history_df.columns:
            axes[1, 0].plot(history_df['epoch'], history_df['train_mae'], label='Train MAE', alpha=0.8)
            axes[1, 0].plot(history_df['epoch'], history_df['val_mae'], label='Val MAE', alpha=0.8)
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('MAE')
            axes[1, 0].set_title('Mean Absolute Error')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Learning Rate
        if 'learning_rate' in history_df.columns:
            axes[1, 1].plot(history_df['epoch'], history_df['learning_rate'], alpha=0.8, color='red')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_title('Learning Rate Schedule')
            axes[1, 1].set_yscale('log')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Training curves saved to {save_path}")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.model_dir / f"training_curves_{timestamp}.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        return str(save_path)
    
    def calculate_batch_metrics(self, y_true, y_pred):
        """Calculate comprehensive batch metrics"""
        metrics = {}
        
        # Basic regression metrics
        metrics['mse'] = mean_squared_error(y_true, y_pred)
        metrics['rmse'] = np.sqrt(metrics['mse'])
        metrics['mae'] = mean_absolute_error(y_true, y_pred)
        metrics['r2'] = r2_score(y_true, y_pred)
        
        # Trading-specific metrics
        metrics['hit_rate'] = TradingMetrics.calculate_hit_rate(y_true, y_pred)
        
        if len(y_pred) > 1:
            returns = np.diff(y_pred)
            if len(returns) > 0 and np.std(returns) > 0:
                metrics['sharpe_ratio'] = TradingMetrics.calculate_sharpe_ratio(returns)
                cumulative_returns = np.cumsum(returns)
                metrics['max_drawdown'] = TradingMetrics.calculate_max_drawdown(cumulative_returns)
                metrics['profit_factor'] = TradingMetrics.calculate_profit_factor(returns)
        
        return metrics
    
    def _create_sequences(self, data, target, sequence_length):
        """Create sequences for LSTM training"""
        sequences = []
        targets = []
        
        for i in range(len(data) - sequence_length):
            seq = data[i:i + sequence_length]
            tar = target[i + sequence_length]
            sequences.append(seq)
            targets.append(tar)
        
        return np.array(sequences), np.array(targets)
    
    def _calculate_dynamic_weights(self, dataframe):
        """Enhanced dynamic weights calculation"""
        base_weights = {
            'ma': 0.15, 'macd': 0.15, 'roc': 0.10, 'rsi': 0.15,
            'bb_width': 0.10, 'cci': 0.10, 'momentum': 0.10,
            'stoch': 0.08, 'atr': 0.07
        }
        
        # Market regime adaptations
        if 'close' in dataframe.columns and 'ma' in dataframe.columns:
            trend_strength = abs(dataframe['ma'] - dataframe['close']).rolling(window=14).mean()
            trend_std = trend_strength.rolling(window=14).std()
            strong_trend_threshold = trend_strength.rolling(window=14).mean() + 1.5 * trend_std
            
            is_strong_trend = trend_strength > strong_trend_threshold
            momentum_multiplier = np.where(is_strong_trend, 1.5, 1.0)
            base_weights['momentum'] *= momentum_multiplier.iloc[-1] if len(momentum_multiplier) > 0 else 1.0
        
        return base_weights
    
    def _calculate_market_regime_filter(self, dataframe):
        """Market regime filter calculation"""
        regime_filter = np.zeros(len(dataframe))
        
        if all(col in dataframe.columns for col in ['close', 'bb_upperband', 'bb_lowerband', 'bb_middleband']):
            upper_condition = (dataframe['close'] > dataframe['bb_middleband']) & (dataframe['close'] > dataframe['bb_upperband'])
            lower_condition = (dataframe['close'] < dataframe['bb_middleband']) & (dataframe['close'] < dataframe['bb_lowerband'])
            
            regime_filter[upper_condition] = 1
            regime_filter[lower_condition] = -1
        
        return regime_filter
    
    def _calculate_volatility_adjustment(self, dataframe):
        """Volatility adjustment calculation"""
        volatility_adj = np.ones(len(dataframe))
        
        if all(col in dataframe.columns for col in ['bb_upperband', 'bb_lowerband', 'bb_middleband']):
            bb_width = (dataframe['bb_upperband'] - dataframe['bb_lowerband']) / dataframe['bb_middleband']
            volatility_adj = 1 / (bb_width + 1e-8)
        
        return volatility_adj
    
    def _calculate_target_score(self, dataframe):
        """Enhanced target score calculation"""
        weights = self._calculate_dynamic_weights(dataframe)
        regime_filter = self._calculate_market_regime_filter(dataframe)
        volatility_adj = self._calculate_volatility_adjustment(dataframe)
        
        aggregate_score = np.zeros(len(dataframe))
        
        for indicator, weight in weights.items():
            if f'normalized_{indicator}' in dataframe.columns:
                aggregate_score += weight * dataframe[f'normalized_{indicator}'].fillna(0)
        
        target_score = aggregate_score * regime_filter * volatility_adj
        return target_score
    
    def fit(self, X, y, **kwargs):
        """Enhanced training with all V2 features"""
        try:
            logger.info("Starting NetanelEnhancedLSTMRegressorV2 training...")
            
            # Store feature names for explainability
            if hasattr(X, 'columns'):
                self.feature_names = list(X.columns)
            
            # Initialize ensemble if requested
            if self.ensemble_size > 1:
                logger.info(f"Training ensemble of {self.ensemble_size} models...")
                ensemble_kwargs = {k: v for k, v in self.__dict__.items() 
                                 if k in self.default_parameters}
                ensemble_kwargs['ensemble_size'] = 1  # Prevent recursive ensemble
                
                self.ensemble = EnsembleModel(self.ensemble_size, **ensemble_kwargs)
                self.ensemble.fit(X, y, **kwargs)
                return self
            
            # Prepare data
            X_scaled = self.scaler.fit_transform(X)
            X_seq, y_seq = self._create_sequences(X_scaled, y, self.sequence_length)
            
            # Validation split
            val_size = int(len(X_seq) * self.validation_split)
            X_train, X_val = X_seq[:-val_size], X_seq[-val_size:]
            y_train, y_val = y_seq[:-val_size], y_seq[-val_size:]
            
            # Convert to tensors
            X_train = torch.FloatTensor(X_train).to(self.device)
            y_train = torch.FloatTensor(y_train).to(self.device)
            X_val = torch.FloatTensor(X_val).to(self.device)
            y_val = torch.FloatTensor(y_val).to(self.device)
            
            # Initialize model
            input_dim = X_train.shape[-1]
            self.model = NetanelEnhancedLSTMModelV2(
                input_dim=input_dim,
                hidden_dim=self.hidden_dim,
                num_lstm_layers=self.num_lstm_layers,
                dropout_percent=self.dropout_percent,
                window_size=self.window_size,
                use_attention=self.use_attention,
                attention_heads=self.attention_heads,
                uncertainty_estimation=self.uncertainty_estimation
            ).to(self.device)
            
            # Optimizer
            self.optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.learning_rate,
                weight_decay=1e-5
            )
            
            # Mixed precision training
            if self.mixed_precision and self.device.type in ['cuda', 'mps']:
                self.scaler_grad = torch.cuda.amp.GradScaler() if self.device.type == 'cuda' else None
            
            # Learning rate scheduler
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                self.optimizer, mode='min', factor=0.5, patience=5
            )
            
            # Training loop
            best_val_loss = float('inf')
            patience_counter = 0
            
            for epoch in range(self.epochs):
                # Training phase
                self.model.train()
                train_loss = 0
                train_preds, train_targets = [], []
                
                for i in range(0, len(X_train), self.batch_size):
                    batch_X = X_train[i:i + self.batch_size]
                    batch_y = y_train[i:i + self.batch_size]
                    
                    self.optimizer.zero_grad()
                    
                    # Mixed precision forward pass
                    if self.mixed_precision and self.scaler_grad:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(batch_X)
                            if isinstance(outputs, dict):
                                predictions = outputs['mean']
                                if self.uncertainty_estimation and 'log_var' in outputs:
                                    # Negative log-likelihood loss for uncertainty
                                    loss = 0.5 * (torch.exp(-outputs['log_var']) * (predictions.squeeze() - batch_y)**2 + outputs['log_var']).mean()
                                else:
                                    loss = self.criterion(predictions.squeeze(), batch_y)
                            else:
                                predictions = outputs
                                loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        self.scaler_grad.scale(loss).backward()
                        self.scaler_grad.unscale_(self.optimizer)
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                        self.scaler_grad.step(self.optimizer)
                        self.scaler_grad.update()
                    else:
                        outputs = self.model(batch_X)
                        if isinstance(outputs, dict):
                            predictions = outputs['mean']
                            if self.uncertainty_estimation and 'log_var' in outputs:
                                loss = 0.5 * (torch.exp(-outputs['log_var']) * (predictions.squeeze() - batch_y)**2 + outputs['log_var']).mean()
                            else:
                                loss = self.criterion(predictions.squeeze(), batch_y)
                        else:
                            predictions = outputs
                            loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        loss.backward()
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                        self.optimizer.step()
                    
                    train_loss += loss.item()
                    train_preds.extend(predictions.squeeze().detach().cpu().numpy())
                    train_targets.extend(batch_y.detach().cpu().numpy())
                
                # Validation phase
                self.model.eval()
                val_preds, val_targets = [], []
                val_loss = 0
                
                with torch.no_grad():
                    for i in range(0, len(X_val), self.batch_size):
                        batch_X = X_val[i:i + self.batch_size]
                        batch_y = y_val[i:i + self.batch_size]
                        
                        outputs = self.model(batch_X)
                        if isinstance(outputs, dict):
                            predictions = outputs['mean']
                            if self.uncertainty_estimation and 'log_var' in outputs:
                                loss = 0.5 * (torch.exp(-outputs['log_var']) * (predictions.squeeze() - batch_y)**2 + outputs['log_var']).mean()
                            else:
                                loss = self.criterion(predictions.squeeze(), batch_y)
                        else:
                            predictions = outputs
                            loss = self.criterion(predictions.squeeze(), batch_y)
                        
                        val_loss += loss.item()
                        val_preds.extend(predictions.squeeze().cpu().numpy())
                        val_targets.extend(batch_y.cpu().numpy())
                
                val_loss /= len(X_val)
                train_loss /= len(X_train)
                
                # Calculate comprehensive metrics
                train_metrics = self.calculate_batch_metrics(train_targets, train_preds)
                val_metrics = self.calculate_batch_metrics(val_targets, val_preds)
                
                # Learning rate scheduling
                scheduler.step(val_loss)
                
                # Early stopping
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    patience_counter = 0
                    self.best_model_state = self.model.state_dict().copy()
                else:
                    patience_counter += 1
                
                # Record comprehensive history
                history_entry = {
                    'epoch': epoch,
                    'train_loss': train_loss,
                    'val_loss': val_loss,
                    'train_r2': train_metrics.get('r2', 0),
                    'val_r2': val_metrics.get('r2', 0),
                    'train_mae': train_metrics.get('mae', 0),
                    'val_mae': val_metrics.get('mae', 0),
                    'train_rmse': train_metrics.get('rmse', 0),
                    'val_rmse': val_metrics.get('rmse', 0),
                    'train_hit_rate': train_metrics.get('hit_rate', 0),
                    'val_hit_rate': val_metrics.get('hit_rate', 0),
                    'learning_rate': self.optimizer.param_groups[0]['lr']
                }
                
                # Add trading metrics if available
                for metric in ['sharpe_ratio', 'max_drawdown', 'profit_factor']:
                    if metric in train_metrics:
                        history_entry[f'train_{metric}'] = train_metrics[metric]
                    if metric in val_metrics:
                        history_entry[f'val_{metric}'] = val_metrics[metric]
                
                self.training_history.append(history_entry)
                
                # Logging
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Train Loss = {train_loss:.6f}, Val Loss = {val_loss:.6f}, "
                              f"Train R² = {train_metrics.get('r2', 0):.4f}, Val R² = {val_metrics.get('r2', 0):.4f}, "
                              f"Val Hit Rate = {val_metrics.get('hit_rate', 0):.4f}")
                
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Load best model state
            if hasattr(self, 'best_model_state'):
                self.model.load_state_dict(self.best_model_state)
            
            # Final evaluation
            self.model.eval()
            with torch.no_grad():
                train_outputs = self.model(X_train)
                val_outputs = self.model(X_val)
                
                if isinstance(train_outputs, dict):
                    train_pred = train_outputs['mean'].cpu().numpy()
                    val_pred = val_outputs['mean'].cpu().numpy()
                else:
                    train_pred = train_outputs.cpu().numpy()
                    val_pred = val_outputs.cpu().numpy()
                
                final_train_metrics = self.calculate_batch_metrics(y_train.cpu().numpy(), train_pred)
                final_val_metrics = self.calculate_batch_metrics(y_val.cpu().numpy(), val_pred)
                
                logger.info(f"Training completed - Train R²: {final_train_metrics.get('r2', 0):.4f}, "
                          f"Val R²: {final_val_metrics.get('r2', 0):.4f}, "
                          f"Val Hit Rate: {final_val_metrics.get('hit_rate', 0):.4f}")
            
            # Plot training curves if requested
            if self.plot_training:
                self.plot_training_curves()
            
            # Initialize SHAP explainer if requested
            if self.calculate_shap and self.feature_names:
                try:
                    # Create a wrapper for SHAP
                    def model_predict(X):
                        X_scaled = self.scaler.transform(X)
                        return self.predict(X_scaled)
                    
                    # Use a sample of training data for SHAP
                    sample_size = min(100, len(X))
                    sample_X = X.iloc[:sample_size] if hasattr(X, 'iloc') else X[:sample_size]
                    self.explainer = shap.Explainer(model_predict, sample_X)
                    logger.info("SHAP explainer initialized")
                except Exception as e:
                    logger.warning(f"Could not initialize SHAP explainer: {e}")
            
            return self
            
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise
    
    def predict(self, X, return_uncertainty=False):
        """Enhanced prediction with uncertainty estimation"""
        try:
            # Use ensemble if available
            if self.ensemble and self.ensemble.is_trained:
                return self.ensemble.predict(X, return_uncertainty=return_uncertainty)
            
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            X_scaled = self.scaler.transform(X)
            predictions = []
            uncertainties = []
            
            for i in range(len(X_scaled)):
                start_idx = max(0, i + 1 - self.sequence_length)
                end_idx = i + 1
                
                sequence_data = X_scaled[start_idx:end_idx]
                
                if len(sequence_data) < self.sequence_length:
                    padding_needed = self.sequence_length - len(sequence_data)
                    padding = np.zeros((padding_needed, X_scaled.shape[1]))
                    sequence_data = np.vstack([padding, sequence_data])
                
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    
                    if isinstance(outputs, dict):
                        pred = outputs['mean'].cpu().numpy().flatten()[0]
                        predictions.append(pred)
                        
                        if return_uncertainty and 'std' in outputs:
                            uncertainty = outputs['std'].cpu().numpy().flatten()[0]
                            uncertainties.append(uncertainty)
                    else:
                        pred = outputs.cpu().numpy().flatten()[0]
                        predictions.append(pred)
            
            predictions = np.array(predictions)
            
            if return_uncertainty and uncertainties:
                return {'mean': predictions, 'std': np.array(uncertainties)}
            elif return_uncertainty:
                # Estimate uncertainty using dropout inference
                return self._monte_carlo_dropout_prediction(X)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            return np.zeros(len(X))
    
    def _monte_carlo_dropout_prediction(self, X, n_samples=50):
        """Monte Carlo dropout for uncertainty estimation"""
        if self.model is None:
            return {'mean': np.zeros(len(X)), 'std': np.zeros(len(X))}
        
        self.model.train()  # Enable dropout
        predictions = []
        
        for _ in range(n_samples):
            pred = self.predict_single_pass(X)
            predictions.append(pred)
        
        predictions = np.array(predictions)
        mean_pred = np.mean(predictions, axis=0)
        std_pred = np.std(predictions, axis=0)
        
        return {'mean': mean_pred, 'std': std_pred}
    
    def predict_single_pass(self, X):
        """Single forward pass prediction (helper for MC dropout)"""
        X_scaled = self.scaler.transform(X)
        predictions = []
        
        for i in range(len(X_scaled)):
            start_idx = max(0, i + 1 - self.sequence_length)
            end_idx = i + 1
            
            sequence_data = X_scaled[start_idx:end_idx]
            
            if len(sequence_data) < self.sequence_length:
                padding_needed = self.sequence_length - len(sequence_data)
                padding = np.zeros((padding_needed, X_scaled.shape[1]))
                sequence_data = np.vstack([padding, sequence_data])
            
            X_seq = sequence_data.reshape(1, self.sequence_length, -1)
            X_tensor = torch.FloatTensor(X_seq).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(X_tensor)
                
                if isinstance(outputs, dict):
                    pred = outputs['mean'].cpu().numpy().flatten()[0]
                else:
                    pred = outputs.cpu().numpy().flatten()[0]
                
                predictions.append(pred)
        
        return np.array(predictions)
    
    def get_feature_importance(self, X_sample=None, n_samples=100):
        """Get feature importance using SHAP"""
        if not self.explainer:
            logger.warning("SHAP explainer not initialized. Set calculate_shap=True during training.")
            return None
        
        try:
            if X_sample is None:
                if hasattr(self, 'X_train_sample'):
                    X_sample = self.X_train_sample
                else:
                    logger.warning("No sample data available for SHAP analysis")
                    return None
            
            # Calculate SHAP values
            sample_size = min(n_samples, len(X_sample))
            shap_values = self.explainer(X_sample.iloc[:sample_size] if hasattr(X_sample, 'iloc') else X_sample[:sample_size])
            
            return {
                'shap_values': shap_values.values,
                'feature_names': self.feature_names,
                'base_values': shap_values.base_values,
                'data': shap_values.data
            }
        except Exception as e:
            logger.error(f"Error calculating SHAP values: {e}")
            return None
    
    def plot_feature_importance(self, X_sample=None, save_path=None):
        """Plot feature importance using SHAP"""
        importance_data = self.get_feature_importance(X_sample)
        
        if importance_data is None:
            return None
        
        try:
            import shap
            
            # Create SHAP plots
            fig, axes = plt.subplots(1, 2, figsize=(20, 8))
            
            # Summary plot
            plt.sca(axes[0])
            shap.summary_plot(importance_data['shap_values'], 
                            features=importance_data['data'],
                            feature_names=importance_data['feature_names'],
                            show=False)
            axes[0].set_title('Feature Importance - SHAP Summary')
            
            # Bar plot
            plt.sca(axes[1])
            shap.summary_plot(importance_data['shap_values'],
                            features=importance_data['data'], 
                            feature_names=importance_data['feature_names'],
                            plot_type="bar", show=False)
            axes[1].set_title('Feature Importance - SHAP Bar Plot')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Feature importance plot saved to {save_path}")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = self.model_dir / f"feature_importance_{timestamp}.png"
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
            plt.show()
            return str(save_path)
            
        except Exception as e:
            logger.error(f"Error plotting feature importance: {e}")
            return None
    
    def get_model_info(self):
        """Get comprehensive model information"""
        info = {
            "model_name": "NetanelEnhancedLSTMRegressorV2",
            "model_type": self.model_type,
            "version": "2.0",
            "parameters": {
                "hidden_dim": self.hidden_dim,
                "num_lstm_layers": self.num_lstm_layers,
                "dropout_percent": self.dropout_percent,
                "window_size": self.window_size,
                "sequence_length": self.sequence_length,
                "learning_rate": self.learning_rate,
                "batch_size": self.batch_size,
                "epochs": self.epochs,
                "use_attention": self.use_attention,
                "attention_heads": self.attention_heads,
                "uncertainty_estimation": self.uncertainty_estimation,
                "ensemble_size": self.ensemble_size
            },
            "device": str(self.device),
            "training_history_length": len(self.training_history),
            "features_v2": [
                "Model Persistence (save/load)",
                "Loss Plotting with Training Curves",
                "Batch-wise Evaluation Metrics (R², MAE, RMSE)",
                "Ensemble Support",
                "Mixed Precision Training",
                "Prediction Confidence/Uncertainty",
                "Temporal Attention Layer",
                "Trading-Specific Metrics (Hit Rate, Sharpe, Drawdown)",
                "SHAP Explainability",
                "Monte Carlo Dropout Uncertainty",
                "Enhanced Market Regime Filters",
                "Advanced Architecture with Batch Normalization"
            ],
            "trading_metrics": [
                "Hit Rate (Directional Accuracy)",
                "Sharpe Ratio",
                "Maximum Drawdown", 
                "Profit Factor"
            ],
            "recommended_use": "Production-grade crypto trading with institutional requirements",
            "model_trained": self.model is not None or (self.ensemble and self.ensemble.is_trained),
            "explainability_available": self.explainer is not None,
            "ensemble_active": self.ensemble_size > 1
        }
        
        # Add final training metrics if available
        if self.training_history:
            last_epoch = self.training_history[-1]
            info["final_metrics"] = {
                "validation_r2": last_epoch.get('val_r2', 0),
                "validation_hit_rate": last_epoch.get('val_hit_rate', 0),
                "validation_loss": last_epoch.get('val_loss', 0),
                "final_learning_rate": last_epoch.get('learning_rate', 0)
            }
        
        return info

# Utility functions for hyperparameter tuning
def suggest_hyperparameters_optuna(trial):
    """Suggest hyperparameters for Optuna optimization"""
    return {
        'hidden_dim': trial.suggest_categorical('hidden_dim', [64, 128, 256, 512]),
        'num_lstm_layers': trial.suggest_int('num_lstm_layers', 2, 5),
        'dropout_percent': trial.suggest_float('dropout_percent', 0.1, 0.7),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
        'batch_size': trial.suggest_categorical('batch_size', [16, 32, 64, 128]),
        'sequence_length': trial.suggest_int('sequence_length', 5, 30),
        'attention_heads': trial.suggest_categorical('attention_heads', [4, 8, 16]),
        'use_attention': trial.suggest_categorical('use_attention', [True, False])
    }

def create_ensemble_model(n_models=5, **kwargs):
    """Factory function to create ensemble model"""
    return NetanelEnhancedLSTMRegressorV2(ensemble_size=n_models, **kwargs)

# Export main classes
__all__ = [
    'NetanelEnhancedLSTMRegressorV2',
    'NetanelEnhancedLSTMModelV2', 
    'EnsembleModel',
    'TradingMetrics',
    'TemporalAttention',
    'suggest_hyperparameters_optuna',
    'create_ensemble_model'
]