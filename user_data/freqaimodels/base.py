"""
Base FreqAI Model Class
=======================

This module provides the base class for all FreqAI models.
All custom models should inherit from BaseFreqAIModel.
"""

import logging
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from sklearn.base import BaseEstimator
import joblib
import os
from datetime import datetime
# Import with error handling - using absolute imports
import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from utils.logging_utils import LoggingMixin, log_model_operation
except ImportError:
    # Fallback logging mixin
    class LoggingMixin:
        def _setup_logging(self):
            pass
        def _log_error(self, error, message):
            print(f"Error: {message} - {error}")
        def _log_data_validation(self, X, y):
            pass
    
    def log_model_operation(operation):
        def decorator(func):
            return func
        return decorator

try:
    from utils.validation_utils import validate_input, validate_output, data_quality_report, model_health_check
except ImportError:
    # Fallback validation functions
    def validate_input(X, y=None):
        if X is None or len(X) == 0:
            raise ValueError("Input data is empty or None")
    
    def validate_output(y_pred, expected_shape=None):
        if y_pred is None or len(y_pred) == 0:
            raise ValueError("Output data is empty or None")
    
    def data_quality_report(X, y=None):
        return {"status": "basic_validation_passed"}
    
    def model_health_check(model):
        return {"status": "basic_health_check_passed"}

logger = logging.getLogger(__name__)


class BaseFreqAIModel(BaseEstimator, ABC, LoggingMixin):
    """
    Base class for all FreqAI models.
    
    This class provides common functionality for:
    - Model training and prediction
    - Feature importance calculation
    - Model persistence
    - Performance metrics
    - Hyperparameter optimization
    - Comprehensive logging
    """
    
    model_type = "base"
    default_parameters = {}
    
    def __init__(self, **kwargs):
        """Initialize the base model with parameters"""
        self.model = None
        self.is_trained = False
        self.feature_names = None
        self.scaler = None
        self.parameters = {**self.default_parameters, **kwargs}
        self.training_history = []
        self.model_path = None
        
    @abstractmethod
    @log_model_operation("fit")
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'BaseFreqAIModel':
        """Train the model on the given data"""
        pass
    
    @abstractmethod
    @log_model_operation("predict")
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions on new data"""
        pass
    
    def fit_predict(self, X: np.ndarray, y: np.ndarray, **kwargs) -> np.ndarray:
        """Fit the model and return predictions"""
        self.fit(X, y, **kwargs)
        return self.predict(X)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get feature importance scores if available"""
        if hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            return np.abs(self.model.coef_)
        else:
            logger.warning("Feature importance not available for this model")
            return None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get comprehensive model information and health check"""
        info = {
            "model_type": self.model_type,
            "is_trained": self.is_trained,
            "parameters": self.parameters,
            "feature_names": self.feature_names,
            "training_history": self.training_history,
            "model_path": self.model_path
        }
        # Add health check
        info["health_check"] = model_health_check(self)
        return info
    
    def save_model(self, path: str) -> None:
        """Save the trained model to disk with logging"""
        try:
            if not self.is_trained:
                raise ValueError("Cannot save untrained model")
            
            os.makedirs(os.path.dirname(path), exist_ok=True)
            joblib.dump(self, path)
            self.model_path = path
            
            # Log successful save
            self._setup_logging()
            self.logger.info(f"Model successfully saved to {path}")
            
        except Exception as e:
            self._log_error(e, f"Model save failed for path: {path}")
            raise
    
    def load_model(self, path: str) -> None:
        """Load a trained model from disk with logging"""
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Model file not found: {path}")
            
            loaded_model = joblib.load(path)
            self.__dict__.update(loaded_model.__dict__)
            self.model_path = path
            
            # Log successful load
            self._setup_logging()
            self.logger.info(f"Model successfully loaded from {path}")
            
        except Exception as e:
            self._log_error(e, f"Model load failed for path: {path}")
            raise
    
    def validate_data(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> None:
        """Validate input data with comprehensive logging and validation utils"""
        try:
            # Use validation utility
            validate_input(X, y)
            # Log successful validation
            self._log_data_validation(X, y)
            # Log data quality report
            report = data_quality_report(X, y)
            self.logger.info(f"Data quality report: {report}")
        except Exception as e:
            # Log validation error
            self._log_error(e, "Data validation failed")
            raise
    
    def preprocess_features(self, X: np.ndarray) -> np.ndarray:
        """Preprocess features before training/prediction with logging"""
        try:
            original_shape = X.shape
            original_nan_count = np.sum(np.isnan(X))
            original_inf_count = np.sum(np.isinf(X))
            
            # Handle NaN values
            if np.any(np.isnan(X)):
                self._setup_logging()
                self.logger.warning(f"NaN values found in features ({original_nan_count} values), filling with 0")
                X = np.nan_to_num(X, nan=0.0)
            
            # Handle infinite values
            if np.any(np.isinf(X)):
                self._setup_logging()
                self.logger.warning(f"Infinite values found in features ({original_inf_count} values), clipping")
                X = np.clip(X, -1e6, 1e6)
            
            # Log preprocessing results
            if original_nan_count > 0 or original_inf_count > 0:
                self._setup_logging()
                self.logger.info(f"Preprocessing completed - Original shape: {original_shape}, NaN fixed: {original_nan_count}, Inf fixed: {original_inf_count}")
            
            return X
            
        except Exception as e:
            self._log_error(e, "Feature preprocessing failed")
            raise
    
    def calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """Calculate performance metrics with logging and output validation"""
        try:
            from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
            
            # Validate output
            validate_output(y_pred, expected_shape=y_true.shape)
            metrics = {
                "mse": mean_squared_error(y_true, y_pred),
                "rmse": np.sqrt(mean_squared_error(y_true, y_pred)),
                "mae": mean_absolute_error(y_true, y_pred),
                "r2": r2_score(y_true, y_pred)
            }
            
            # Log metrics
            self._setup_logging()
            self.logger.info(f"Performance metrics calculated: {metrics}")
            
            return metrics
            
        except Exception as e:
            self._log_error(e, "Metrics calculation failed")
            raise
    
    def update_training_history(self, metrics: Dict[str, float]) -> None:
        """Update training history with new metrics"""
        self.training_history.append({
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics
        })
    
    def get_optimal_parameters(self) -> Dict[str, Any]:
        """Get optimal parameters based on training history"""
        if not self.training_history:
            return self.parameters
        
        # Find best performing iteration
        best_iteration = max(self.training_history, 
                           key=lambda x: x["metrics"].get("r2", -np.inf))
        return best_iteration.get("parameters", self.parameters)
    
    def __repr__(self) -> str:
        """String representation of the model"""
        return f"{self.__class__.__name__}({self.parameters})"
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        return f"{self.__class__.__name__} - {self.model_type} model"


class ModelFactory:
    """Factory class for creating model instances"""
    
    @staticmethod
    def create_model(model_name: str, **kwargs) -> BaseFreqAIModel:
        """Create a model instance by name"""
        from . import get_model_class
        
        try:
            model_class = get_model_class(model_name)
            return model_class(**kwargs)
        except Exception as e:
            logger.error(f"Failed to create model {model_name}: {e}")
            raise
    
    @staticmethod
    def list_models() -> list:
        """List all available models"""
        from . import list_available_models
        return list_available_models()
    
    @staticmethod
    def get_model_info(model_name: str) -> Dict[str, Any]:
        """Get information about a specific model"""
        from . import get_model_info
        return get_model_info(model_name) 