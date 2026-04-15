"""
Tree-based Models for FreqAI
============================
Fixed version (FreqAI compatible)
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

# Optional libs
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

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

logger = logging.getLogger(__name__)


# =========================
# Helper
# =========================
def _to_numpy(X):
    if isinstance(X, pd.DataFrame):
        return X.values
    if isinstance(X, pd.Series):
        return X.values
    return np.array(X)


# =========================
# CatBoost
# =========================
class EnhancedCatboostRegressor(BaseFreqAIModel):

    model_type = "tree_based"

    default_parameters = {
        "iterations": 100,
        "learning_rate": 0.05,
        "depth": 6,
        "verbose": False,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not CATBOOST_AVAILABLE:
            raise ImportError("pip install catboost")

        self.catboost = cb
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = _to_numpy(data["train_features"])
        y = _to_numpy(data["train_labels"])

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        self.model = self.catboost.CatBoostRegressor(**self.parameters)

        if X.shape[0] > 100:
            split = int(0.8 * len(X))
            train_pool = self.catboost.Pool(X[:split], y[:split])
            val_pool = self.catboost.Pool(X[split:], y[split:])

            self.model.fit(
                train_pool,
                eval_set=val_pool,
                early_stopping_rounds=10,
                verbose=False,
            )
        else:
            self.model.fit(X, y)

        self.is_trained = True
        return self

    def predict(self, X, dk=None):
        if not self.is_trained:
            raise ValueError("Model not trained")
        return self.model.predict(_to_numpy(X))

    def get_feature_importance(self):
        if self.is_trained:
            return self.model.get_feature_importance()
        return None


# =========================
# LightGBM
# =========================
class EnhancedLightGBMRegressor(BaseFreqAIModel):

    model_type = "tree_based"

    default_parameters = {
        "objective": "regression",
        "learning_rate": 0.05,
        "n_estimators": 100,
        "num_leaves": 31,
        "verbose": -1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not LIGHTGBM_AVAILABLE:
            raise ImportError("pip install lightgbm")

        self.lightgbm = lgb
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = _to_numpy(data["train_features"])
        y = _to_numpy(data["train_labels"])

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        self.model = self.lightgbm.LGBMRegressor(**self.parameters)

        if X.shape[0] > 100:
            split = int(0.8 * len(X))
            self.model.fit(
                X[:split],
                y[:split],
                eval_set=[(X[split:], y[split:])],
                callbacks=[self.lightgbm.early_stopping(10, verbose=False)],
            )
        else:
            self.model.fit(X, y)

        self.is_trained = True
        return self

    def predict(self, X, dk=None):
        if not self.is_trained:
            raise ValueError("Model not trained")
        return self.model.predict(_to_numpy(X))

    def get_feature_importance(self):
        if self.is_trained:
            return self.model.feature_importances_
        return None


# =========================
# XGBoost
# =========================
class EnhancedXGBoostRegressor(BaseFreqAIModel):

    model_type = "tree_based"

    default_parameters = {
        "n_estimators": 100,
        "learning_rate": 0.05,
        "max_depth": 6,
        "eval_metric": "rmse",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not XGBOOST_AVAILABLE:
            raise ImportError("pip install xgboost")

        self.xgboost = xgb
        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = _to_numpy(data["train_features"])
        y = _to_numpy(data["train_labels"])

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        if X.shape[0] > 100:
            split = int(0.8 * len(X))

            self.model = self.xgboost.XGBRegressor(**self.parameters)
            self.model.fit(
                X[:split],
                y[:split],
                eval_set=[(X[split:], y[split:])],
                verbose=False,
            )
        else:
            self.model = self.xgboost.XGBRegressor(**self.parameters)
            self.model.fit(X, y)

        self.is_trained = True
        return self

    def predict(self, X, dk=None):
        if not self.is_trained:
            raise ValueError("Model not trained")
        return self.model.predict(_to_numpy(X))

    def get_feature_importance(self):
        if self.is_trained:
            return self.model.feature_importances_
        return None


# =========================
# Ensemble
# =========================
class EnsembleTreeModel(BaseFreqAIModel):

    model_type = "ensemble"

    def __init__(self, config: dict, models=None, weights=None, **kwargs):
        super().__init__(config=config, **kwargs)

        self.models = models or []
        self.weights = weights or [1.0] * len(self.models)

        if len(self.weights) != len(self.models):
            raise ValueError("Weights must match models")

    def fit(self, data: Dict, dk: Any, **kwargs):
        for model in self.models:
            model.fit(data, dk, **kwargs)

        self.is_trained = True
        return self

    def predict(self, X, dk=None):
        if not self.is_trained:
            raise ValueError("Model not trained")

        X = _to_numpy(X)

        preds = [m.predict(X) for m in self.models]

        weighted = np.zeros_like(preds[0])
        for p, w in zip(preds, self.weights):
            weighted += p * w

        return weighted / sum(self.weights)
