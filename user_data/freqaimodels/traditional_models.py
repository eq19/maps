"""
Traditional Machine Learning Models for FreqAI
=============================================

This module contains traditional ML models optimized for trading:
- Linear Regression: Simple linear models
- Random Forest: Ensemble of decision trees
- SVR: Support Vector Regression
- KNN: K-Nearest Neighbors

These models are particularly good for:
- Baseline performance comparison
- Interpretable results
- Fast training and prediction
- Feature importance analysis
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.preprocessing import StandardScaler

# Traditional ML models
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

# Fix the import to use absolute import
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

import warnings

logger = logging.getLogger(__name__)


class LinearRegressionModel(BaseFreqAIModel):
    """
    Linear Regression for FreqAI
    
    Simple linear regression model that can serve as a baseline
    for more complex models.
    
    Advantages:
    - Fast training and prediction
    - Interpretable coefficients
    - Good baseline performance
    - Low computational cost
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "fit_intercept": True,
        "copy_X": True,
        "n_jobs": None,
        "positive": False
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'LinearRegressionModel':
        """Train the linear regression model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize and train model
        self.model = LinearRegression(**self.parameters)
        self.model.fit(X_scaled, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"Linear Regression model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get linear regression coefficients"""
        if self.is_trained and hasattr(self.model, 'coef_'):
            return np.abs(self.model.coef_)
        return None


class RandomForestRegressor(BaseFreqAIModel):
    """
    Random Forest Regressor for FreqAI
    
    Random Forest is an ensemble method that combines multiple decision trees
    to improve prediction accuracy and reduce overfitting.
    
    Advantages:
    - Robust to overfitting
    - Feature importance analysis
    - Handles non-linear relationships
    - Good performance on financial data
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "n_estimators": 100,
        "criterion": "squared_error",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "bootstrap": True,
        "random_state": 42,
        "n_jobs": -1,
        "verbose": 0
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'RandomForestRegressor':
        """Train the random forest model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Initialize and train model
        self.model = RandomForestRegressor(**self.parameters)
        self.model.fit(X, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"Random Forest model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        return self.model.predict(X)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get random forest feature importance"""
        if self.is_trained and hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None


class SVR(BaseFreqAIModel):
    """
    Support Vector Regression for FreqAI
    
    SVR is a powerful regression method that can handle non-linear
    relationships using kernel functions.
    
    Advantages:
    - Handles non-linear relationships
    - Robust to outliers
    - Kernel flexibility
    - Good generalization
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "kernel": "rbf",
        "C": 1.0,
        "epsilon": 0.1,
        "gamma": "scale",
        "tol": 1e-3,
        "max_iter": -1,
        "verbose": False
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'SVR':
        """Train the SVR model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize and train model
        self.model = SVR(**self.parameters)
        self.model.fit(X_scaled, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"SVR model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)


class KNeighborsRegressor(BaseFreqAIModel):
    """
    K-Nearest Neighbors Regressor for FreqAI
    
    KNN is a simple but effective method that predicts based on
    the average of the k nearest neighbors.
    
    Advantages:
    - Simple and interpretable
    - No training required
    - Good for local patterns
    - Non-parametric
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "n_neighbors": 5,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
        "p": 2,
        "metric": "minkowski",
        "metric_params": None,
        "n_jobs": None
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'KNeighborsRegressor':
        """Train the KNN model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize and train model
        self.model = KNeighborsRegressor(**self.parameters)
        self.model.fit(X_scaled, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"KNN model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)


class RidgeRegressor(BaseFreqAIModel):
    """
    Ridge Regression for FreqAI
    
    Ridge regression adds L2 regularization to linear regression,
    which helps prevent overfitting.
    
    Advantages:
    - Regularization prevents overfitting
    - Handles multicollinearity
    - Fast training and prediction
    - Interpretable coefficients
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "alpha": 1.0,
        "fit_intercept": True,
        "copy_X": True,
        "max_iter": None,
        "tol": 1e-4,
        "solver": "auto",
        "random_state": None
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'RidgeRegressor':
        """Train the ridge regression model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Initialize and train model
        self.model = Ridge(**self.parameters)
        self.model.fit(X_scaled, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"Ridge Regression model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get ridge regression coefficients"""
        if self.is_trained and hasattr(self.model, 'coef_'):
            return np.abs(self.model.coef_)
        return None


class ExtraTreesRegressor(BaseFreqAIModel):
    """
    Extra Trees Regressor for FreqAI
    
    Extra Trees is an ensemble method similar to Random Forest but
    with additional randomization in the tree building process.
    
    Advantages:
    - More randomization than Random Forest
    - Often better generalization
    - Feature importance analysis
    - Robust to noise
    """
    
    model_type = "traditional_ml"
    default_parameters = {
        "n_estimators": 100,
        "criterion": "squared_error",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "bootstrap": False,
        "random_state": 42,
        "n_jobs": -1,
        "verbose": 0
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'ExtraTreesRegressor':
        """Train the extra trees model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Initialize and train model
        self.model = ExtraTreesRegressor(**self.parameters)
        self.model.fit(X, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"Extra Trees model trained with {X.shape[0]} samples, {X.shape[1]} features")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        return self.model.predict(X)
    
    def get_feature_importance(self) -> Optional[np.ndarray]:
        """Get extra trees feature importance"""
        if self.is_trained and hasattr(self.model, 'feature_importances_'):
            return self.model.feature_importances_
        return None


class TraditionalModelUtils:
    """Utility class for traditional ML models"""
    
    @staticmethod
    def get_optimal_hyperparameters(model_type: str, data_size: int) -> Dict[str, Any]:
        """Get optimal hyperparameters based on data size"""
        if model_type == "random_forest":
            if data_size < 1000:
                return {"n_estimators": 50, "max_depth": 5, "min_samples_split": 5}
            elif data_size < 10000:
                return {"n_estimators": 100, "max_depth": 10, "min_samples_split": 2}
            else:
                return {"n_estimators": 200, "max_depth": 15, "min_samples_split": 2}
        
        elif model_type == "svr":
            if data_size < 1000:
                return {"C": 0.1, "epsilon": 0.2, "gamma": "scale"}
            elif data_size < 10000:
                return {"C": 1.0, "epsilon": 0.1, "gamma": "scale"}
            else:
                return {"C": 10.0, "epsilon": 0.05, "gamma": "scale"}
        
        elif model_type == "knn":
            if data_size < 1000:
                return {"n_neighbors": 3, "weights": "uniform"}
            elif data_size < 10000:
                return {"n_neighbors": 5, "weights": "uniform"}
            else:
                return {"n_neighbors": 7, "weights": "distance"}
        
        return {}
    
    @staticmethod
    def analyze_model_complexity(model) -> Dict[str, Any]:
        """Analyze model complexity"""
        if hasattr(model, 'n_estimators'):
            return {
                "n_estimators": model.n_estimators,
                "max_depth": model.max_depth,
                "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None
            }
        elif hasattr(model, 'support_vectors_'):
            return {
                "n_support_vectors": len(model.support_vectors_),
                "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None
            }
        else:
            return {
                "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None
            }
    
    @staticmethod
    def create_model_comparison(models: list, X: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """Compare multiple models on the same dataset"""
        results = {}
        
        for model in models:
            if not model.is_trained:
                model.fit(X, y)
            
            y_pred = model.predict(X)
            metrics = model.calculate_metrics(y, y_pred)
            results[model.__class__.__name__] = metrics
        
        return results 