"""
Tree-based Models for FreqAI
============================

This module contains tree-based models optimized for trading:
- CatBoost: Gradient boosting with categorical features
- LightGBM: Fast gradient boosting with GPU support
- XGBoost: Extreme gradient boosting

These models are particularly good for:
- Feature importance analysis
- Handling categorical variables
- Fast training and prediction
- Robust performance on financial data
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.preprocessing import StandardScaler
import warnings

# Tree-based models with error handling
try:
    import catboost as cb
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False
    cb = None

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    lgb = None

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None

# Fix the import to use absolute import
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

logger = logging.getLogger(__name__)


class EnhancedCatboostRegressor(BaseFreqAIModel):
    """
    Enhanced CatBoost Regressor for FreqAI
    
    CatBoost is a gradient boosting algorithm that handles categorical features
    automatically and provides excellent performance on financial time series data.
    
    Advantages:
    - Automatic categorical feature handling
    - Robust to overfitting
    - Good performance on small datasets
    - Built-in feature importance
    """
    
    model_type = "tree_based"
    default_parameters = {
        "iterations": 100,
        "learning_rate": 0.05,
        "depth": 6,
        "l2_leaf_reg": 3,
        "random_strength": 1,
        "bagging_temperature": 1,
        "border_count": 254,
        "verbose": False,
        "task_type": "CPU",
        "early_stopping_rounds": 10,
        "eval_metric": "RMSE"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not CATBOOST_AVAILABLE:
            raise ImportError("CatBoost is required. Install with: pip install catboost")
        self.catboost = cb
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'EnhancedCatboostRegressor':
        """Train the CatBoost model with enhanced logging"""
        #self.validate_data(X, y)
        #X = self.preprocess_features(X)
        
        # Create CatBoost dataset
        train_data = self.catboost.Pool(X, y)
        
        # Initialize model
        self.model = self.catboost.CatBoostRegressor(**self.parameters)
        
        # Train model
        self.model.fit(train_data, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        # Log training completion
        self._setup_logging()
        self.logger.info(f"CatBoost model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray, dk: Optional[Any] = None) -> np.ndarray:
        """Make predictions"""
        if not getattr(self, "is_trained", False):
            raise ValueError("Model must be trained before making predictions")

        #X = self.preprocess_features(X)
        return self.model.predict(X)
      
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get CatBoost feature importance"""
        if self.is_trained and hasattr(self.model, 'get_feature_importance'):
            return self.model.get_feature_importance()
        return None


class EnhancedLightGBMRegressor(BaseFreqAIModel):
    """
    Enhanced LightGBM Regressor for FreqAI
    
    LightGBM is a fast gradient boosting framework that supports GPU acceleration
    and is optimized for large datasets with high-dimensional features.
    
    Advantages:
    - Fast training and prediction
    - GPU acceleration support
    - Memory efficient
    - Good for high-dimensional data
    """
    
    model_type = "tree_based"
    default_parameters = {
        "boosting_type": "gbdt",
        "objective": "regression",
        "metric": "rmse",
        "learning_rate": 0.02,
        "num_leaves": 31,
        "min_data_in_leaf": 20,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "bagging_freq": 5,
        "verbose": -1,
        "random_state": 42,
        "n_estimators": 100,
        "early_stopping_rounds": 10,
        "eval_metric": "rmse"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not LIGHTGBM_AVAILABLE:
            raise ImportError("LightGBM is required. Install with: pip install lightgbm")
        self.lightgbm = lgb
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'EnhancedLightGBMRegressor':
        """Train the LightGBM model with optimized early stopping"""
        #self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Set feature names
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        # Create validation dataset for early stopping
        if X.shape[0] > 100:  # Only use validation if we have enough data
            split_idx = int(0.8 * X.shape[0])
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            # Initialize model with early stopping
            model_params = self.parameters.copy()
            model_params.update({
                'callbacks': [self.lightgbm.early_stopping(stopping_rounds=10, verbose=False)],
                'eval_metric': 'rmse',
                'valid_sets': [(X_val, y_val)],
                'valid_names': ['validation']
            })
            
            self.model = self.lightgbm.LGBMRegressor(**model_params)
            
            # Train model with validation
            self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], **kwargs)
            
            self._setup_logging()
            self.logger.info(f"LightGBM model trained with {X_train.shape[0]} samples, {X_val.shape[0]} validation samples, {X.shape[1]} features")
        else:
            # For small datasets, train without validation
            model_params = self.parameters.copy()
            # Remove early stopping parameters for small datasets
            model_params.pop('early_stopping_rounds', None)
            model_params.pop('eval_metric', None)
            
            self.model = self.lightgbm.LGBMRegressor(**model_params)
            self.model.fit(X, y, feature_name=self.feature_names, **kwargs)
            
            self._setup_logging()
            self.logger.info(f"LightGBM model trained with {X.shape[0]} samples, {X.shape[1]} features (no validation)")
        
        self.is_trained = True
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        
        # Create DataFrame with feature names for prediction
        import pandas as pd
        X_df = pd.DataFrame(X, columns=self.feature_names)
        
        return self.model.predict(X_df)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get LightGBM feature importance"""
        if self.is_trained and hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None


class EnhancedXGBoostRegressor(BaseFreqAIModel):
    """
    Enhanced XGBoost Regressor for FreqAI
    
    XGBoost is an optimized gradient boosting library that provides excellent
    performance and scalability for machine learning tasks.
    
    Advantages:
    - Excellent performance on structured data
    - Built-in regularization
    - Cross-validation support
    - Feature importance analysis
    """
    
    model_type = "tree_based"
    default_parameters = {
        "n_estimators": 100,
        "learning_rate": 0.1,
        "max_depth": 6,
        "min_child_weight": 1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_alpha": 0,
        "reg_lambda": 1,
        "random_state": 42,
        "eval_metric": "rmse",
        "early_stopping_rounds": 10
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not XGBOOST_AVAILABLE:
            raise ImportError("XGBoost is required. Install with: pip install xgboost")
        self.xgboost = xgb
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'EnhancedXGBoostRegressor':
        """Train the XGBoost model with optimized early stopping"""
        #self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Create validation dataset for early stopping
        if X.shape[0] > 100:  # Only use validation if we have enough data
            split_idx = int(0.8 * X.shape[0])
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]
            
            # Initialize model with early stopping
            model_params = self.parameters.copy()
            model_params.update({
                'early_stopping_rounds': 10,
                'eval_metric': 'rmse'
            })
            
            self.model = self.xgboost.XGBRegressor(**model_params)
            
            # Train model with validation
            self.model.fit(X_train, y_train, eval_set=[(X_val, y_val)], verbose=False, **kwargs)
            
            self._setup_logging()
            self.logger.info(f"XGBoost model trained with {X_train.shape[0]} samples, {X_val.shape[0]} validation samples, {X.shape[1]} features")
        else:
            # For small datasets, train without validation
            model_params = self.parameters.copy()
            # Remove early stopping parameters for small datasets
            model_params.pop('early_stopping_rounds', None)
            model_params.pop('eval_metric', None)
            
            self.model = self.xgboost.XGBRegressor(**model_params)
            self.model.fit(X, y, **kwargs)
            
            self._setup_logging()
            self.logger.info(f"XGBoost model trained with {X.shape[0]} samples, {X.shape[1]} features (no validation)")
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        return self.model.predict(X)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get XGBoost feature importance"""
        if self.is_trained and hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None


class TreeModelUtils:
    """Utility class for tree-based models"""
    
    @staticmethod
    def get_optimal_hyperparameters(model_type: str, data_size: int) -> Dict[str, Any]:
        """Get optimal hyperparameters based on data size"""
        if model_type == "catboost":
            if data_size < 1000:
                return {"iterations": 50, "learning_rate": 0.1, "depth": 4}
            elif data_size < 10000:
                return {"iterations": 100, "learning_rate": 0.05, "depth": 6}
            else:
                return {"iterations": 200, "learning_rate": 0.03, "depth": 8}
        
        elif model_type == "lightgbm":
            if data_size < 1000:
                return {"n_estimators": 50, "learning_rate": 0.1, "num_leaves": 15}
            elif data_size < 10000:
                return {"n_estimators": 100, "learning_rate": 0.05, "num_leaves": 31}
            else:
                return {"n_estimators": 200, "learning_rate": 0.03, "num_leaves": 63}
        
        elif model_type == "xgboost":
            if data_size < 1000:
                return {"n_estimators": 50, "learning_rate": 0.1, "max_depth": 4}
            elif data_size < 10000:
                return {"n_estimators": 100, "learning_rate": 0.05, "max_depth": 6}
            else:
                return {"n_estimators": 200, "learning_rate": 0.03, "max_depth": 8}
        
        return {}
    
    @staticmethod
    def analyze_feature_importance(model, feature_names: Optional[list] = None) -> Dict[str, float]:
        """Analyze and return feature importance"""
        importance = model.get_feature_importance()
        if importance is None:
            return {}
        
        if feature_names is None:
            feature_names = [f"feature_{i}" for i in range(len(importance))]
        
        # Sort by importance
        feature_importance = dict(zip(feature_names, importance))
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_features)
    
    @staticmethod
    def create_ensemble(models: list, weights: Optional[list] = None) -> 'EnsembleTreeModel':
        """Create an ensemble of tree models"""
        return EnsembleTreeModel(models, weights)

class EnsembleTreeModel(BaseFreqAIModel):
    """Ensemble of tree-based models"""

    model_type = "ensemble"

    def __init__(
        self,
        config: dict,
        models: list = None,
        weights: Optional[list] = None,
        **kwargs
    ):
        # Required so Freqtrade can initialize the model
        super().__init__(config=config, **kwargs)

        # Your original parameters
        self.models = models if models else []
        self.weights = weights if weights else [1.0] * len(self.models)

        if len(self.weights) != len(self.models):
            raise ValueError("Number of weights must match number of models")

    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'EnsembleTreeModel':
        """Train all models in the ensemble"""
        for model in self.models:
            model.fit(X, y, **kwargs)

        self.is_trained = True
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make ensemble predictions"""
        if not self.is_trained:
            raise ValueError("Models must be trained before making predictions")

        predictions = []
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)

        # Weighted average
        weighted_pred = np.zeros_like(predictions[0])
        for pred, weight in zip(predictions, self.weights):
            weighted_pred += pred * weight

        return weighted_pred / sum(self.weights)
