import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor as SKRandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor as SKExtraTreesRegressor
from sklearn.svm import SVR as SKSVR
from sklearn.neighbors import KNeighborsRegressor as SKKNN

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


# =========================================================
# 🔧 COMMON SAFE UTILITIES
# =========================================================

def prepare_y(y):
    """Convert y safely for sklearn"""
    if isinstance(y, pd.DataFrame):
        y = y.values

    if len(y.shape) == 2 and y.shape[1] == 1:
        y = y.ravel()

    return y


def build_pred_df(preds, dk):
    """Build FreqAI-compatible prediction dataframe"""
    if len(preds.shape) == 1:
        preds = preds.reshape(-1, 1)

    return pd.DataFrame(preds, columns=dk.label_list)


# =========================================================
# 🔹 LINEAR REGRESSION
# =========================================================

class LinearRegressionModel(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.model = None

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        X_scaled = self.scaler.fit_transform(X)

        self.model = LinearRegression()
        self.model.fit(X_scaled, y)

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# 🔹 RIDGE REGRESSION
# =========================================================

class RidgeRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.model = None

    def fit(self, data_dictionary, dk, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        X_scaled = self.scaler.fit_transform(X)

        self.model = Ridge()
        self.model.fit(X_scaled, y)

        return self

    def predict(self, unfiltered_df, dk, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# 🔹 RANDOM FOREST
# =========================================================

class RandomForestRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None

    def fit(self, data_dictionary, dk, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        self.model = SKRandomForestRegressor(
            n_estimators=100,
            max_depth=None,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X, y)

        return self

    def predict(self, unfiltered_df, dk, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        preds = self.model.predict(X)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# 🔹 EXTRA TREES
# =========================================================

class ExtraTreesRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None

    def fit(self, data_dictionary, dk, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        self.model = SKExtraTreesRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X, y)

        return self

    def predict(self, unfiltered_df, dk, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        preds = self.model.predict(X)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# 🔹 SVR
# =========================================================

class SVR(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.model = None

    def fit(self, data_dictionary, dk, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        X_scaled = self.scaler.fit_transform(X)

        self.model = SKSVR()
        self.model.fit(X_scaled, y)

        return self

    def predict(self, unfiltered_df, dk, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict


# =========================================================
# 🔹 KNN
# =========================================================

class KNeighborsRegressor(BaseRegressionModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scaler = StandardScaler()
        self.model = None

    def fit(self, data_dictionary, dk, **kwargs):

        X = data_dictionary["train_features"]
        y = prepare_y(data_dictionary["train_labels"])

        X_scaled = self.scaler.fit_transform(X)

        self.model = SKKNN(n_neighbors=5)
        self.model.fit(X_scaled, y)

        return self

    def predict(self, unfiltered_df, dk, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)

        pred_df = build_pred_df(preds, dk)
        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
