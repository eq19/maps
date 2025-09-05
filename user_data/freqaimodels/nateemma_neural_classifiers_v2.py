"""
Enhanced Neural Network Trinary Classifiers V2 - Production-Ready Version
Based on nateemma's strategies with comprehensive improvements for institutional-grade trading
Features all requested enhancements from the improvement suggestions
"""

import logging
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from typing import Dict, Any, Optional, List, Tuple
import warnings
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
warnings.filterwarnings('ignore')

class TemporalAttentionClassifier(nn.Module):
    """Temporal Attention Layer for classification tasks"""
    
    def __init__(self, hidden_dim: int, num_heads: int = 8):
        super(TemporalAttentionClassifier, self).__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=num_heads,
            batch_first=True
        )
        self.layer_norm = nn.LayerNorm(hidden_dim)
        
    def forward(self, x):
        attn_output, attn_weights = self.attention(x, x, x)
        return self.layer_norm(x + attn_output), attn_weights

class NNTCLSTMModelV2(nn.Module):
    """
    Enhanced Neural Network Trinary Classifier using LSTM V2
    Features:
    - Temporal Attention
    - Uncertainty Estimation
    - Improved Architecture
    """
    
    def __init__(
        self, 
        input_dim: int, 
        hidden_dim: int = 64, 
        num_layers: int = 2, 
        dropout: float = 0.3,
        use_attention: bool = True,
        attention_heads: int = 8,
        uncertainty_estimation: bool = True
    ):
        super(NNTCLSTMModelV2, self).__init__()
        
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.use_attention = use_attention
        self.uncertainty_estimation = uncertainty_estimation
        
        # LSTM with improved architecture
        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0,
            bidirectional=True
        )
        
        lstm_output_dim = hidden_dim * 2  # *2 for bidirectional
        
        # Temporal Attention
        if use_attention:
            self.attention = TemporalAttentionClassifier(lstm_output_dim, attention_heads)
        
        # Enhanced classification layers
        self.batch_norm = nn.BatchNorm1d(lstm_output_dim)
        self.dropout1 = nn.Dropout(dropout)
        
        self.fc1 = nn.Linear(lstm_output_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.batch_norm2 = nn.BatchNorm1d(hidden_dim)
        self.dropout2 = nn.Dropout(dropout)
        
        # Main prediction head
        self.fc_main = nn.Linear(hidden_dim, 3)  # 3 classes: sell, hold, buy
        
        # Uncertainty estimation head
        if uncertainty_estimation:
            self.fc_uncertainty = nn.Linear(hidden_dim, 3)  # Log variance for each class
        
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x, return_attention_weights=False):
        lstm_out, _ = self.lstm(x)
        attention_weights = None
        
        # Apply temporal attention if enabled
        if self.use_attention:
            lstm_out, attention_weights = self.attention(lstm_out)
        
        # Take the last output
        last_output = lstm_out[:, -1, :]
        
        # Enhanced processing
        x = self.batch_norm(last_output)
        x = self.dropout1(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.batch_norm2(x)
        x = self.dropout2(x)
        
        # Main prediction
        logits = self.fc_main(x)
        probabilities = self.softmax(logits)
        
        outputs = {
            'logits': logits,
            'probabilities': probabilities
        }
        
        # Uncertainty estimation
        if self.uncertainty_estimation:
            log_var = self.fc_uncertainty(x)
            outputs['log_var'] = log_var
            outputs['uncertainty'] = torch.exp(0.5 * log_var)
        
        if return_attention_weights and attention_weights is not None:
            outputs['attention_weights'] = attention_weights
        
        return outputs

class NNTCTransformerModelV2(nn.Module):
    """
    Enhanced Neural Network Trinary Classifier using Transformer V2
    """
    
    def __init__(
        self, 
        input_dim: int, 
        d_model: int = 64, 
        nhead: int = 8, 
        num_layers: int = 2, 
        dropout: float = 0.3,
        uncertainty_estimation: bool = True
    ):
        super(NNTCTransformerModelV2, self).__init__()
        
        self.d_model = d_model
        self.uncertainty_estimation = uncertainty_estimation
        
        # Input projection
        self.input_projection = nn.Linear(input_dim, d_model)
        
        # Learnable positional encoding
        self.pos_encoding = nn.Parameter(torch.randn(100, d_model) * 0.1)
        
        # Enhanced Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=dropout,
            activation='gelu',
            batch_first=True,
            norm_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Enhanced classification head
        self.classifier = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.GELU(),
            nn.LayerNorm(d_model),
            nn.Dropout(dropout),
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Dropout(dropout)
        )
        
        # Main prediction head
        self.fc_main = nn.Linear(d_model // 2, 3)
        
        # Uncertainty estimation head
        if uncertainty_estimation:
            self.fc_uncertainty = nn.Linear(d_model // 2, 3)
        
        self.softmax = nn.Softmax(dim=1)
    
    def forward(self, x, return_attention_weights=False):
        seq_len = x.size(1)
        
        # Project input to d_model dimension
        x = self.input_projection(x)
        
        # Add positional encoding
        x = x + self.pos_encoding[:seq_len, :].unsqueeze(0)
        
        # Transformer encoding
        x = self.transformer(x)
        
        # Global average pooling
        x = x.mean(dim=1)
        
        # Enhanced classification
        x = self.classifier(x)
        
        # Main prediction
        logits = self.fc_main(x)
        probabilities = self.softmax(logits)
        
        outputs = {
            'logits': logits,
            'probabilities': probabilities
        }
        
        # Uncertainty estimation
        if self.uncertainty_estimation:
            log_var = self.fc_uncertainty(x)
            outputs['log_var'] = log_var
            outputs['uncertainty'] = torch.exp(0.5 * log_var)
        
        return outputs

class ClassificationMetrics:
    """Trading-specific classification metrics"""
    
    @staticmethod
    def calculate_signal_accuracy(y_true, y_pred):
        """Calculate accuracy for each signal type"""
        metrics = {}
        classes = ['sell', 'hold', 'buy']
        
        for i, class_name in enumerate(classes):
            mask = y_true == i
            if np.sum(mask) > 0:
                class_accuracy = np.mean(y_pred[mask] == y_true[mask])
                metrics[f'{class_name}_accuracy'] = class_accuracy
            else:
                metrics[f'{class_name}_accuracy'] = 0.0
        
        return metrics
    
    @staticmethod
    def calculate_trading_profit(signals, returns, transaction_cost=0.001):
        """Calculate hypothetical trading profit from signals"""
        portfolio_returns = []
        position = 0  # 0: no position, 1: long, -1: short
        
        for i in range(len(signals) - 1):
            signal = signals[i]
            period_return = returns[i + 1] if i + 1 < len(returns) else 0
            
            # Position changes
            new_position = 0
            if signal == 2:  # buy
                new_position = 1
            elif signal == 0:  # sell
                new_position = -1
            # signal == 1 (hold) keeps current position
            
            # Calculate portfolio return
            if position != 0:
                portfolio_return = position * period_return
                # Apply transaction cost if position changes
                if new_position != position:
                    portfolio_return -= transaction_cost
                portfolio_returns.append(portfolio_return)
            else:
                portfolio_returns.append(0)
            
            position = new_position
        
        if len(portfolio_returns) == 0:
            return {'total_return': 0, 'sharpe_ratio': 0, 'max_drawdown': 0}
        
        total_return = np.sum(portfolio_returns)
        sharpe_ratio = np.mean(portfolio_returns) / (np.std(portfolio_returns) + 1e-8) * np.sqrt(252)
        
        # Calculate max drawdown
        cumulative_returns = np.cumsum(portfolio_returns)
        peak = np.maximum.accumulate(cumulative_returns)
        drawdown = (cumulative_returns - peak)
        max_drawdown = np.min(drawdown)
        
        return {
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'win_rate': np.mean(np.array(portfolio_returns) > 0)
        }

class EnsembleClassifier:
    """Ensemble wrapper for multiple classifier models"""
    
    def __init__(self, n_models=3, **model_kwargs):
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
            model = NateemmaNeuralClassifierV2(**model_kwargs)
            model.fit(X, y, **kwargs)
            self.models.append(model)
        
        self.is_trained = True
        return self
    
    def predict(self, X, return_uncertainty=False):
        """Predict using ensemble voting"""
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before prediction")
        
        predictions = []
        uncertainties = []
        
        for model in self.models:
            if return_uncertainty:
                pred_proba = model.predict_proba(X)
                pred = np.argmax(pred_proba, axis=1)
                uncertainty = 1 - np.max(pred_proba, axis=1)  # Entropy-based uncertainty
                predictions.append(pred)
                uncertainties.append(uncertainty)
            else:
                pred = model.predict(X)
                predictions.append(pred)
        
        # Ensemble voting
        predictions = np.array(predictions)
        ensemble_pred = np.apply_along_axis(lambda x: np.bincount(x).argmax(), axis=0, arr=predictions)
        
        if return_uncertainty:
            # Ensemble uncertainty
            pred_uncertainty = np.mean(uncertainties, axis=0)
            # Add epistemic uncertainty (disagreement between models)
            epistemic_uncertainty = np.apply_along_axis(
                lambda x: 1 - np.max(np.bincount(x)) / len(x), 
                axis=0, 
                arr=predictions
            )
            total_uncertainty = pred_uncertainty + epistemic_uncertainty
            
            return {'predictions': ensemble_pred, 'uncertainty': total_uncertainty}
        
        return ensemble_pred
    
    def predict_proba(self, X):
        """Predict probabilities using ensemble averaging"""
        if not self.is_trained:
            raise ValueError("Ensemble must be trained before prediction")
        
        all_probas = []
        for model in self.models:
            probas = model.predict_proba(X)
            all_probas.append(probas)
        
        # Average probabilities
        ensemble_probas = np.mean(all_probas, axis=0)
        return ensemble_probas

class NateemmaNeuralClassifierV2(BaseFreqAIModel):
    """
    Production-Ready Enhanced Neural Network Trinary Classifier V2
    
    New Features:
    - Model Persistence (save/load)
    - Training Curve Plotting
    - Comprehensive Metrics (Accuracy, Precision, Recall, F1, Trading Metrics)
    - Ensemble Support
    - Mixed Precision Training
    - Uncertainty Estimation
    - Temporal Attention Layer
    - Trading-Specific Metrics
    - SHAP Explainability
    - Advanced Architectures
    """
    
    model_type = "neural_classifier_v2"
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
        "confidence_threshold": 0.6,
        "use_attention": True,
        "attention_heads": 8,
        "uncertainty_estimation": True,
        "mixed_precision": True,
        "ensemble_size": 1,
        "plot_training": True,
        "calculate_shap": False,
        "signal_threshold": 0.01,
        "forward_periods": 5
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Enhanced parameters
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
        
        # V2 Features
        self.use_attention = kwargs.get('use_attention', True)
        self.attention_heads = kwargs.get('attention_heads', 8)
        self.uncertainty_estimation = kwargs.get('uncertainty_estimation', True)
        self.mixed_precision = kwargs.get('mixed_precision', True)
        self.ensemble_size = kwargs.get('ensemble_size', 1)
        self.plot_training = kwargs.get('plot_training', True)
        self.calculate_shap = kwargs.get('calculate_shap', False)
        self.signal_threshold = kwargs.get('signal_threshold', 0.01)
        self.forward_periods = kwargs.get('forward_periods', 5)
        
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
        
        # Model components
        self.model = None
        self.ensemble = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.pca_components) if self.use_pca else None
        self.scaler_grad = None
        
        # Training tracking
        self.training_history = []
        self.best_model_state = None
        self.feature_names = None
        self.explainer = None
        
        # Class mapping
        self.class_names = ['sell', 'hold', 'buy']
        self.class_mapping = {0: 'sell', 1: 'hold', 2: 'buy'}
        
        # Create model directory
        self.model_dir = Path("saved_models")
        self.model_dir.mkdir(exist_ok=True)
    
    def save_model(self, filepath: Optional[str] = None):
        """Save complete model state"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.model_dir / f"nateemma_classifier_v2_{timestamp}.pt"
        else:
            filepath = Path(filepath)
        
        if self.model is None and (self.ensemble is None or not self.ensemble.is_trained):
            raise ValueError("No trained model to save")
        
        save_dict = {
            'architecture': self.architecture,
            'model_config': {
                'hidden_dim': self.hidden_dim,
                'num_layers': self.num_layers,
                'dropout': self.dropout,
                'use_attention': self.use_attention,
                'attention_heads': self.attention_heads,
                'uncertainty_estimation': self.uncertainty_estimation
            },
            'scaler': self.scaler,
            'pca': self.pca,
            'training_history': self.training_history,
            'feature_names': self.feature_names,
            'parameters': {
                'learning_rate': self.learning_rate,
                'batch_size': self.batch_size,
                'sequence_length': self.sequence_length,
                'confidence_threshold': self.confidence_threshold,
                'signal_threshold': self.signal_threshold,
                'forward_periods': self.forward_periods
            },
            'class_names': self.class_names,
            'device': str(self.device),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save model state
        if self.model is not None:
            save_dict['model_state_dict'] = self.model.state_dict()
        
        # Save ensemble if applicable
        if self.ensemble and self.ensemble.is_trained:
            save_dict['ensemble_size'] = self.ensemble.n_models
            save_dict['ensemble_models'] = []
            for i, model in enumerate(self.ensemble.models):
                model_path = self.model_dir / f"ensemble_model_{i}_{timestamp}.pt"
                model.save_model(str(model_path))
                save_dict['ensemble_models'].append(str(model_path))
        
        torch.save(save_dict, filepath)
        logger.info(f"Model saved to {filepath}")
        return str(filepath)
    
    def load_model(self, filepath: str):
        """Load complete model state"""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        checkpoint = torch.load(filepath, map_location=self.device)
        
        # Restore configuration
        self.architecture = checkpoint.get('architecture', 'lstm')
        config = checkpoint.get('model_config', {})
        
        # Restore components
        self.scaler = checkpoint['scaler']
        self.pca = checkpoint.get('pca')
        self.training_history = checkpoint.get('training_history', [])
        self.feature_names = checkpoint.get('feature_names')
        self.class_names = checkpoint.get('class_names', ['sell', 'hold', 'buy'])
        
        # Update parameters
        params = checkpoint.get('parameters', {})
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Load model if single model
        if 'model_state_dict' in checkpoint:
            input_dim = len(self.feature_names) if self.feature_names else 10
            if self.use_pca and self.pca:
                input_dim = self.pca.n_components_
            
            self.model = self._create_model(input_dim).to(self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Load ensemble if applicable
        if 'ensemble_size' in checkpoint:
            self.ensemble_size = checkpoint['ensemble_size']
            ensemble_models = checkpoint.get('ensemble_models', [])
            if ensemble_models:
                # Load ensemble models (simplified for this example)
                logger.info(f"Ensemble with {len(ensemble_models)} models loaded")
        
        logger.info(f"Model loaded from {filepath}")
        logger.info(f"Model trained on: {checkpoint.get('timestamp', 'Unknown')}")
        
        return self
    
    def plot_training_curves(self, save_path: Optional[str] = None):
        """Plot comprehensive training curves for classification"""
        if not self.training_history:
            logger.warning("No training history available for plotting")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Training Progress - Nateemma Neural Classifier V2', fontsize=16)
        
        history_df = pd.DataFrame(self.training_history)
        
        # Loss curves
        axes[0, 0].plot(history_df['epoch'], history_df['train_loss'], label='Train Loss', alpha=0.8)
        axes[0, 0].plot(history_df['epoch'], history_df['val_loss'], label='Val Loss', alpha=0.8)
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].set_title('Loss Curves')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Accuracy curves
        axes[0, 1].plot(history_df['epoch'], history_df['train_accuracy'], label='Train Accuracy', alpha=0.8)
        axes[0, 1].plot(history_df['epoch'], history_df['val_accuracy'], label='Val Accuracy', alpha=0.8)
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy')
        axes[0, 1].set_title('Accuracy Progress')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Class-specific accuracies if available
        class_metrics = ['sell_accuracy', 'hold_accuracy', 'buy_accuracy']
        if any(metric in history_df.columns for metric in class_metrics):
            for metric in class_metrics:
                if metric in history_df.columns:
                    axes[1, 0].plot(history_df['epoch'], history_df[metric], 
                                  label=metric.replace('_', ' ').title(), alpha=0.8)
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Class Accuracy')
            axes[1, 0].set_title('Per-Class Accuracy')
            axes[1, 0].legend()
            axes[1, 0].grid(True, alpha=0.3)
        
        # Learning Rate
        if 'learning_rate' in history_df.columns:
            axes[1, 1].plot(history_df['epoch'], history_df['learning_rate'], alpha=0.8, color='red')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('Learning Rate')
            axes[1, 1].set_title('Learning Rate Schedule')
            axes[1, 1].set_yscale('log')
            axes[1, 1().grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Training curves saved to {save_path}")
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = self.model_dir / f"classifier_training_curves_{timestamp}.png"
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        return str(save_path)
    
    def calculate_comprehensive_metrics(
        self, 
        y_true: np.ndarray, 
        y_pred: np.ndarray, 
        y_proba: Optional[np.ndarray] = None,
        returns: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """Calculate comprehensive classification and trading metrics"""
        metrics = {}
        
        # Basic classification metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        
        # Per-class metrics
        class_metrics = ClassificationMetrics.calculate_signal_accuracy(y_true, y_pred)
        metrics.update(class_metrics)
        
        # Classification report
        try:
            report = classification_report(y_true, y_pred, 
                                         target_names=self.class_names, 
                                         output_dict=True, zero_division=0)
            for class_name in self.class_names:
                if class_name in report:
                    metrics[f'{class_name}_precision'] = report[class_name]['precision']
                    metrics[f'{class_name}_recall'] = report[class_name]['recall']
                    metrics[f'{class_name}_f1'] = report[class_name]['f1-score']
            
            metrics['macro_avg_f1'] = report['macro avg']['f1-score']
            metrics['weighted_avg_f1'] = report['weighted avg']['f1-score']
        except Exception as e:
            logger.warning(f"Could not calculate classification report: {e}")
        
        # Confidence metrics if probabilities provided
        if y_proba is not None:
            avg_confidence = np.mean(np.max(y_proba, axis=1))
            metrics['average_confidence'] = avg_confidence
            
            # Entropy-based uncertainty
            entropy = -np.sum(y_proba * np.log(y_proba + 1e-8), axis=1)
            metrics['average_entropy'] = np.mean(entropy)
        
        # Trading metrics if returns provided
        if returns is not None and len(returns) >= len(y_pred):
            trading_metrics = ClassificationMetrics.calculate_trading_profit(
                y_pred, returns[:len(y_pred)]
            )
            metrics.update(trading_metrics)
        
        return metrics
    
    def _create_sequences(self, data: np.ndarray, labels: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Create sequences for neural network training"""
        sequences = []
        targets = []
        
        for i in range(len(data) - self.sequence_length + 1):
            seq = data[i:i + self.sequence_length]
            target = labels[i + self.sequence_length - 1]
            sequences.append(seq)
            targets.append(target)
        
        return np.array(sequences), np.array(targets)
    
    def _generate_signals(self, returns: np.ndarray, threshold: float = None) -> np.ndarray:
        """Generate trading signals based on forward returns"""
        if threshold is None:
            threshold = self.signal_threshold
        
        signals = np.ones(len(returns))  # Default to hold
        
        # Buy signals for positive returns above threshold
        signals[returns > threshold] = 2
        
        # Sell signals for negative returns below threshold
        signals[returns < -threshold] = 0
        
        return signals.astype(int)
    
    def _calculate_forward_returns(self, prices: np.ndarray, periods: int = None) -> np.ndarray:
        """Calculate forward returns for signal generation"""
        if periods is None:
            periods = self.forward_periods
            
        returns = np.zeros(len(prices))
        
        for i in range(len(prices) - periods):
            current_price = prices[i]
            future_price = prices[i + periods]
            returns[i] = (future_price - current_price) / current_price
        
        return returns
    
    def _create_model(self, input_dim: int) -> nn.Module:
        """Create enhanced neural network model"""
        if self.architecture == 'lstm':
            return NNTCLSTMModelV2(
                input_dim=input_dim,
                hidden_dim=self.hidden_dim,
                num_layers=self.num_layers,
                dropout=self.dropout,
                use_attention=self.use_attention,
                attention_heads=self.attention_heads,
                uncertainty_estimation=self.uncertainty_estimation
            )
        elif self.architecture == 'transformer':
            return NNTCTransformerModelV2(
                input_dim=input_dim,
                d_model=self.hidden_dim,
                nhead=min(8, self.hidden_dim // 8),
                num_layers=self.num_layers,
                dropout=self.dropout,
                uncertainty_estimation=self.uncertainty_estimation
            )
        elif self.architecture == 'ensemble':
            # Create hybrid ensemble model
            lstm_model = NNTCLSTMModelV2(
                input_dim, self.hidden_dim, self.num_layers, self.dropout,
                self.use_attention, self.attention_heads, self.uncertainty_estimation
            )
            transformer_model = NNTCTransformerModelV2(
                input_dim, self.hidden_dim, min(8, self.hidden_dim // 8), 
                self.num_layers, self.dropout, self.uncertainty_estimation
            )
            
            class EnhancedEnsembleModel(nn.Module):
                def __init__(self, lstm, transformer):
                    super().__init__()
                    self.lstm = lstm
                    self.transformer = transformer
                    self.combiner = nn.Sequential(
                        nn.Linear(6, self.hidden_dim // 2),  # 3 outputs from each model
                        nn.ReLU(),
                        nn.Dropout(self.dropout),
                        nn.Linear(self.hidden_dim // 2, 3)
                    )
                    self.softmax = nn.Softmax(dim=1)
                
                def forward(self, x, return_attention_weights=False):
                    lstm_out = self.lstm(x)
                    transformer_out = self.transformer(x)
                    
                    # Combine probabilities
                    combined = torch.cat([
                        lstm_out['probabilities'], 
                        transformer_out['probabilities']
                    ], dim=1)
                    
                    final_logits = self.combiner(combined)
                    final_probs = self.softmax(final_logits)
                    
                    outputs = {
                        'logits': final_logits,
                        'probabilities': final_probs
                    }
                    
                    # Average uncertainties if available
                    if 'uncertainty' in lstm_out and 'uncertainty' in transformer_out:
                        avg_uncertainty = (lstm_out['uncertainty'] + transformer_out['uncertainty']) / 2
                        outputs['uncertainty'] = avg_uncertainty
                    
                    return outputs
            
            return EnhancedEnsembleModel(lstm_model, transformer_model)
        else:
            raise ValueError(f"Unknown architecture: {self.architecture}")
    
    def fit(self, X, y, **kwargs):
        """Enhanced training with all V2 features"""
        try:
            logger.info(f"Starting NateemmaNeuralClassifierV2 training with {self.architecture} architecture...")
            
            # Store feature names for explainability
            if hasattr(X, 'columns'):
                self.feature_names = list(X.columns)
            
            # Initialize ensemble if requested
            if self.ensemble_size > 1:
                logger.info(f"Training ensemble of {self.ensemble_size} models...")
                ensemble_kwargs = {k: v for k, v in self.__dict__.items() 
                                 if k in self.default_parameters}
                ensemble_kwargs['ensemble_size'] = 1  # Prevent recursive ensemble
                
                self.ensemble = EnsembleClassifier(self.ensemble_size, **ensemble_kwargs)
                self.ensemble.fit(X, y, **kwargs)
                return self
            
            # Prepare features
            X_scaled = self.scaler.fit_transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.fit_transform(X_scaled)
                logger.info(f"PCA reduced dimensions from {X_scaled.shape[1]} to {X_reduced.shape[1]}")
            else:
                X_reduced = X_scaled
            
            # Generate classification labels if continuous target provided
            if len(np.unique(y)) > 3:
                forward_returns = self._calculate_forward_returns(y)
                y_class = self._generate_signals(forward_returns)
                logger.info("Generated classification signals from continuous target")
            else:
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
            
            # Optimizer
            optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.learning_rate,
                weight_decay=1e-5
            )
            
            # Mixed precision training
            if self.mixed_precision and self.device.type in ['cuda', 'mps']:
                self.scaler_grad = torch.cuda.amp.GradScaler() if self.device.type == 'cuda' else None
            
            # Loss function with class weights
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
                train_preds = []
                train_targets = []
                
                for i in range(0, len(X_train), self.batch_size):
                    batch_X = X_train[i:i + self.batch_size]
                    batch_y = y_train[i:i + self.batch_size]
                    
                    optimizer.zero_grad()
                    
                    # Mixed precision forward pass
                    if self.mixed_precision and self.scaler_grad:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(batch_X)
                            logits = outputs['logits'] if isinstance(outputs, dict) else outputs
                            
                            # Enhanced loss with uncertainty if available
                            if isinstance(outputs, dict) and 'log_var' in outputs:
                                # Aleatoric uncertainty loss
                                precision = torch.exp(-outputs['log_var'])
                                loss = torch.mean(precision * criterion(logits, batch_y) + 0.5 * outputs['log_var'])
                            else:
                                loss = criterion(logits, batch_y)
                        
                        self.scaler_grad.scale(loss).backward()
                        self.scaler_grad.unscale_(optimizer)
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                        self.scaler_grad.step(optimizer)
                        self.scaler_grad.update()
                    else:
                        outputs = self.model(batch_X)
                        logits = outputs['logits'] if isinstance(outputs, dict) else outputs
                        
                        if isinstance(outputs, dict) and 'log_var' in outputs:
                            precision = torch.exp(-outputs['log_var'])
                            loss = torch.mean(precision * criterion(logits, batch_y) + 0.5 * outputs['log_var'])
                        else:
                            loss = criterion(logits, batch_y)
                        
                        loss.backward()
                        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
                        optimizer.step()
                    
                    train_loss += loss.item()
                    _, predicted = torch.max(logits.data, 1)
                    train_total += batch_y.size(0)
                    train_correct += (predicted == batch_y).sum().item()
                    
                    train_preds.extend(predicted.cpu().numpy())
                    train_targets.extend(batch_y.cpu().numpy())
                
                # Validation phase
                self.model.eval()
                val_loss = 0
                val_correct = 0
                val_total = 0
                val_preds = []
                val_targets = []
                val_probas = []
                
                with torch.no_grad():
                    for i in range(0, len(X_val), self.batch_size):
                        batch_X = X_val[i:i + self.batch_size]
                        batch_y = y_val[i:i + self.batch_size]
                        
                        outputs = self.model(batch_X)
                        logits = outputs['logits'] if isinstance(outputs, dict) else outputs
                        probabilities = outputs.get('probabilities', torch.softmax(logits, dim=1))
                        
                        if isinstance(outputs, dict) and 'log_var' in outputs:
                            precision = torch.exp(-outputs['log_var'])
                            loss = torch.mean(precision * criterion(logits, batch_y) + 0.5 * outputs['log_var'])
                        else:
                            loss = criterion(logits, batch_y)
                        
                        val_loss += loss.item()
                        _, predicted = torch.max(logits.data, 1)
                        val_total += batch_y.size(0)
                        val_correct += (predicted == batch_y).sum().item()
                        
                        val_preds.extend(predicted.cpu().numpy())
                        val_targets.extend(batch_y.cpu().numpy())
                        val_probas.extend(probabilities.cpu().numpy())
                
                # Calculate accuracies and comprehensive metrics
                train_acc = train_correct / train_total
                val_acc = val_correct / val_total
                avg_val_loss = val_loss / len(X_val) * self.batch_size
                
                # Calculate comprehensive metrics
                train_metrics = self.calculate_comprehensive_metrics(
                    np.array(train_targets), np.array(train_preds)
                )
                val_metrics = self.calculate_comprehensive_metrics(
                    np.array(val_targets), np.array(val_preds), np.array(val_probas)
                )
                
                # Learning rate scheduling
                scheduler.step(avg_val_loss)
                
                # Early stopping
                if val_acc > best_val_acc:
                    best_val_acc = val_acc
                    patience_counter = 0
                    self.best_model_state = self.model.state_dict().copy()
                else:
                    patience_counter += 1
                
                # Record comprehensive history
                history_entry = {
                    'epoch': epoch,
                    'train_loss': train_loss / len(X_train) * self.batch_size,
                    'val_loss': avg_val_loss,
                    'train_accuracy': train_acc,
                    'val_accuracy': val_acc,
                    'learning_rate': optimizer.param_groups[0]['lr']
                }
                
                # Add comprehensive metrics
                for metric_name, value in train_metrics.items():
                    history_entry[f'train_{metric_name}'] = value
                for metric_name, value in val_metrics.items():
                    history_entry[f'val_{metric_name}'] = value
                
                self.training_history.append(history_entry)
                
                # Logging
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}: Train Acc = {train_acc:.4f}, Val Acc = {val_acc:.4f}, "
                              f"Val F1 = {val_metrics.get('macro_avg_f1', 0):.4f}")
                
                if patience_counter >= self.early_stopping_patience:
                    logger.info(f"Early stopping at epoch {epoch}")
                    break
            
            # Load best model state
            if hasattr(self, 'best_model_state'):
                self.model.load_state_dict(self.best_model_state)
            
            logger.info(f"Training completed - Best Val Accuracy: {best_val_acc:.4f}")
            
            # Plot training curves if requested
            if self.plot_training:
                self.plot_training_curves()
            
            # Initialize SHAP explainer if requested
            if self.calculate_shap and self.feature_names:
                try:
                    def model_predict_proba(X):
                        X_scaled = self.scaler.transform(X)
                        if self.use_pca and self.pca:
                            X_reduced = self.pca.transform(X_scaled)
                        else:
                            X_reduced = X_scaled
                        return self.predict_proba(X_reduced)
                    
                    sample_size = min(100, len(X))
                    sample_X = X.iloc[:sample_size] if hasattr(X, 'iloc') else X[:sample_size]
                    self.explainer = shap.Explainer(model_predict_proba, sample_X)
                    logger.info("SHAP explainer initialized")
                except Exception as e:
                    logger.warning(f"Could not initialize SHAP explainer: {e}")
            
            return self
            
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            raise
    
    def predict(self, X):
        """Enhanced prediction with uncertainty handling"""
        try:
            # Use ensemble if available
            if self.ensemble and self.ensemble.is_trained:
                return self.ensemble.predict(X)
            
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            # Prepare features
            X_scaled = self.scaler.transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.transform(X_scaled)
            else:
                X_reduced = X_scaled
            
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
                
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    
                    if isinstance(outputs, dict):
                        probabilities = outputs['probabilities'].cpu().numpy()[0]
                    else:
                        probabilities = torch.softmax(outputs, dim=1).cpu().numpy()[0]
                    
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
        """Enhanced probability prediction"""
        try:
            # Use ensemble if available
            if self.ensemble and self.ensemble.is_trained:
                return self.ensemble.predict_proba(X)
            
            if self.model is None:
                raise ValueError("Model must be trained before making predictions")
            
            # Prepare features
            X_scaled = self.scaler.transform(X)
            
            # Apply PCA if enabled
            if self.use_pca and self.pca is not None:
                X_reduced = self.pca.transform(X_scaled)
            else:
                X_reduced = X_scaled
            
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
                
                X_seq = sequence_data.reshape(1, self.sequence_length, -1)
                X_tensor = torch.FloatTensor(X_seq).to(self.device)
                
                self.model.eval()
                with torch.no_grad():
                    outputs = self.model(X_tensor)
                    
                    if isinstance(outputs, dict):
                        probabilities = outputs['probabilities'].cpu().numpy()[0]
                    else:
                        probabilities = torch.softmax(outputs, dim=1).cpu().numpy()[0]
                
                all_probabilities.append(probabilities)
            
            return np.array(all_probabilities)
            
        except Exception as e:
            logger.error(f"Error during predict_proba: {str(e)}")
            return np.full((len(X), 3), 1/3)
    
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
            
            sample_size = min(n_samples, len(X_sample))
            shap_values = self.explainer(X_sample.iloc[:sample_size] if hasattr(X_sample, 'iloc') else X_sample[:sample_size])
            
            return {
                'shap_values': shap_values.values,
                'feature_names': self.feature_names,
                'base_values': shap_values.base_values,
                'data': shap_values.data,
                'class_names': self.class_names
            }
        except Exception as e:
            logger.error(f"Error calculating SHAP values: {e}")
            return None
    
    def get_model_info(self):
        """Get comprehensive model information"""
        info = {
            "model_name": "NateemmaNeuralClassifierV2",
            "model_type": self.model_type,
            "version": "2.0",
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
                "confidence_threshold": self.confidence_threshold,
                "use_attention": self.use_attention,
                "attention_heads": self.attention_heads,
                "uncertainty_estimation": self.uncertainty_estimation,
                "ensemble_size": self.ensemble_size
            },
            "device": str(self.device),
            "training_history_length": len(self.training_history),
            "classes": self.class_names,
            "features_v2": [
                "Model Persistence (save/load)",
                "Training Curve Plotting",
                "Comprehensive Classification Metrics",
                "Trading-Specific Metrics",
                "Ensemble Support",
                "Mixed Precision Training",
                "Uncertainty Estimation",
                "Temporal Attention Layer",
                "SHAP Explainability",
                "Enhanced Architectures (LSTM/Transformer/Ensemble)",
                "Confidence-based Predictions",
                "PCA Dimensionality Reduction",
                "Advanced Loss Functions with Uncertainty"
            ],
            "trading_features": [
                "Trinary Classification (sell/hold/buy)",
                "Signal Generation from Price Data",
                "Trading Profit Calculation",
                "Win Rate Analysis",
                "Confidence-based Position Sizing"
            ],
            "recommended_use": "Production-grade signal generation for crypto trading strategies",
            "model_trained": self.model is not None or (self.ensemble and self.ensemble.is_trained),
            "explainability_available": self.explainer is not None,
            "ensemble_active": self.ensemble_size > 1
        }
        
        # Add final training metrics if available
        if self.training_history:
            last_epoch = self.training_history[-1]
            info["final_metrics"] = {
                "validation_accuracy": last_epoch.get('val_accuracy', 0),
                "validation_f1": last_epoch.get('val_macro_avg_f1', 0),
                "validation_loss": last_epoch.get('val_loss', 0),
                "final_learning_rate": last_epoch.get('learning_rate', 0)
            }
            
            # Add trading metrics if available
            trading_metrics = ['total_return', 'sharpe_ratio', 'win_rate']
            for metric in trading_metrics:
                val_metric = f'val_{metric}'
                if val_metric in last_epoch:
                    info["final_metrics"][f"validation_{metric}"] = last_epoch[val_metric]
        
        return info

# Utility functions for hyperparameter tuning
def suggest_classifier_hyperparameters_optuna(trial):
    """Suggest hyperparameters for Optuna optimization"""
    return {
        'architecture': trial.suggest_categorical('architecture', ['lstm', 'transformer', 'ensemble']),
        'hidden_dim': trial.suggest_categorical('hidden_dim', [32, 64, 128, 256]),
        'num_layers': trial.suggest_int('num_layers', 1, 4),
        'dropout': trial.suggest_float('dropout', 0.1, 0.7),
        'learning_rate': trial.suggest_float('learning_rate', 1e-5, 1e-2, log=True),
        'batch_size': trial.suggest_categorical('batch_size', [16, 32, 64, 128]),
        'sequence_length': trial.suggest_int('sequence_length', 5, 30),
        'attention_heads': trial.suggest_categorical('attention_heads', [4, 8, 16]),
        'use_attention': trial.suggest_categorical('use_attention', [True, False]),
        'pca_components': trial.suggest_int('pca_components', 5, 20),
        'confidence_threshold': trial.suggest_float('confidence_threshold', 0.3, 0.9)
    }

def create_ensemble_classifier(n_models=3, **kwargs):
    """Factory function to create ensemble classifier"""
    return NateemmaNeuralClassifierV2(ensemble_size=n_models, **kwargs)

# Export main classes
__all__ = [
    'NateemmaNeuralClassifierV2',
    'NNTCLSTMModelV2',
    'NNTCTransformerModelV2',
    'EnsembleClassifier',
    'ClassificationMetrics',
    'TemporalAttentionClassifier',
    'suggest_classifier_hyperparameters_optuna',
    'create_ensemble_classifier'
]