"""
Custom Models for FreqAI (FIXED VERSION)
========================================

All models are now fully compatible with FreqAI:
- Uses data_dictionary + dk interface
- Outputs (&-s_predict, do_predict)
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any
from scipy import stats

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


# =========================================================
# SMART MONEY REGRESSOR
# =========================================================
class SmartMoneyRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def _extract_features(self, X: np.ndarray) -> np.ndarray:
        features = []

        for row in X:
            if len(row) < 5:
                features.append(np.zeros(5))
                continue

            volume = row[4]
            vol_ma = np.mean(row[max(0, 4-5):4]) if len(row) > 5 else volume

            volume_ratio = volume / (vol_ma + 1e-8)
            price_change = (row[0] - row[1]) / (row[1] + 1e-8)
            momentum = (row[0] - row[2]) / (row[2] + 1e-8)
            volatility = np.std(row[:3])
            pattern = 1.0 if np.std(row) > 0.1 else 0.0

            features.append([volume_ratio, price_change, momentum, volatility, pattern])

        return np.array(features)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]

        X_feat = self._extract_features(X)

        self.model.fit(X_feat, y)
        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features_filtered, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = features_filtered.values
        X_feat = self._extract_features(X)

        preds = self.model.predict(X_feat)

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        do_predict = np.ones(len(preds), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# VOLATILITY REGRESSOR
# =========================================================
class VolatilityRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def _extract_features(self, X: np.ndarray) -> np.ndarray:
        features = []

        for row in X:
            if len(row) < 10:
                features.append(np.zeros(4))
                continue

            returns = np.diff(row) / (row[:-1] + 1e-8)

            vol = np.std(returns)
            realized = np.sqrt(np.sum(returns**2))
            clustering = np.corrcoef(np.abs(returns[:-1]), np.abs(returns[1:]))[0, 1] if len(returns) > 2 else 0
            momentum = vol - np.std(returns[:-5]) if len(returns) > 5 else 0

            features.append([vol, realized, clustering, momentum])

        return np.array(features)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]

        X_feat = self._extract_features(X)

        self.model.fit(X_feat, y)
        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features_filtered, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = features_filtered.values
        X_feat = self._extract_features(X)

        preds = self.model.predict(X_feat)

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = preds

        do_predict = np.ones(len(preds), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# MULTI-TIMEFRAME REGRESSOR
# =========================================================
class MultiTimeframeRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models = {
            "short": RandomForestRegressor(n_estimators=50, random_state=42),
            "medium": RandomForestRegressor(n_estimators=50, random_state=42),
        }
        self.weights = {"short": 0.5, "medium": 0.5}

    def _short_features(self, row):
        if len(row) < 5:
            return np.zeros(2)
        return np.array([
            (row[-1] - row[-5]) / (row[-5] + 1e-8),
            np.std(row[-5:])
        ])

    def _medium_features(self, row):
        if len(row) < 20:
            return np.zeros(2)
        return np.array([
            (row[-1] - row[-20]) / (row[-20] + 1e-8),
            np.std(row[-20:])
        ])

    def _build_features(self, X):
        short, medium = [], []

        for row in X:
            short.append(self._short_features(row))
            medium.append(self._medium_features(row))

        return np.array(short), np.array(medium)

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"].values
        y = data_dictionary["train_labels"]

        X_short, X_medium = self._build_features(X)

        self.models["short"].fit(X_short, y)
        self.models["medium"].fit(X_medium, y)

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        features_filtered, _ = dk.filter_features(
            unfiltered_df,
            dk.training_features_list,
            dk.label_list,
            training_filter=False
        )

        X = features_filtered.values
        X_short, X_medium = self._build_features(X)

        pred_short = self.models["short"].predict(X_short)
        pred_medium = self.models["medium"].predict(X_medium)

        final_pred = (
            pred_short * self.weights["short"] +
            pred_medium * self.weights["medium"]
        )

        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df["&-s_predict"] = final_pred

        do_predict = np.ones(len(final_pred), dtype=np.int_)

        return pred_df, do_predict
