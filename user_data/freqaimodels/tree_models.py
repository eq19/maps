"""
Tree-based Models for FreqAI (FINAL FIXED VERSION)
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

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

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
# 1. CatBoost
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

        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

        self.model = None
        self.is_trained = False

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = _to_numpy(data["train_features"])
        y = _to_numpy(data["train_labels"]).ravel()

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        self.model = cb.CatBoostRegressor(**self.parameters)

        if len(X) > 100:
            split = int(0.8 * len(X))

            self.model.fit(
                X[:split],
                y[:split],
                eval_set=(X[split:], y[split:]),
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
# 2. LightGBM (SAFE VERSION)
# =========================
class EnhancedLightGBMRegressor(BaseFreqAIModel):

    model_type = "tree_based"

    default_parameters = {
        "objective": "regression",
        "learning_rate": 0.05,
        "n_estimators": 100,
        "num_leaves": 31,
        "verbosity": -1,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not LIGHTGBM_AVAILABLE:
            raise ImportError("pip install lightgbm")

        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

        self.model = None
        self.is_trained = False

    def _prepare(self, X):
        if isinstance(X, pd.DataFrame):
            X = X.copy()
            for col in X.columns:
                if X[col].dtype == "object":
                    X[col] = pd.to_numeric(X[col], errors="coerce")
            X = X.fillna(0)
            return X.values
        return np.array(X)

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = self._prepare(data["train_features"])
        y = self._prepare(data["train_labels"]).ravel()

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        self.model = lgb.LGBMRegressor(**self.parameters)

        try:
            if len(X) > 100:
                split = int(0.8 * len(X))

                self.model.fit(
                    X[:split],
                    y[:split],
                    eval_set=[(X[split:], y[split:])],
                    eval_metric="rmse",
                )
            else:
                self.model.fit(X, y)

        except TypeError:
            logger.warning("LightGBM fallback (no eval_set support)")
            self.model.fit(X, y)

        self.is_trained = True
        return self

    def predict(self, X, dk=None):
        if not self.is_trained:
            raise ValueError("Model not trained")
        return self.model.predict(self._prepare(X))

    def get_feature_importance(self):
        if self.is_trained:
            return self.model.feature_importances_
        return None


# =========================
# 3. XGBoost
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

        self.parameters = self.default_parameters.copy()
        self.parameters.update(kwargs.get("model_parameters", {}))

        self.model = None
        self.is_trained = False

    def fit(self, data: Dict, dk: Any, **kwargs):
        X = _to_numpy(data["train_features"])
        y = _to_numpy(data["train_labels"]).ravel()

        self.feature_names = [f"feature_{i}" for i in range(X.shape[1])]

        self.model = xgb.XGBRegressor(**self.parameters)

        if len(X) > 100:
            split = int(0.8 * len(X))

            self.model.fit(
                X[:split],
                y[:split],
                eval_set=[(X[split:], y[split:])],
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
            return self.model.feature_importances_
        return None
