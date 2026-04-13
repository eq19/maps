import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


class StackingRegressor(BaseRegressionModel):
    """
    FreqAI-compatible Stacking Regressor
    - Safe parameter handling
    - Robust label handling (DataFrame / Series / ndarray)
    - Backtest-safe
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # 🔥 CRITICAL FIX: normalize labels
        y = np.asarray(y).reshape(-1)

        # -----------------------------
        # SAFE PARAM MERGE
        # -----------------------------
        rf_params = {
            "n_estimators": 50,
            "max_depth": 8,
            "random_state": 42,
        }
        rf_params.update(self.model_training_parameters)

        gb_params = {
            "n_estimators": 50,
            "max_depth": 6,
            "random_state": 42,
        }
        gb_params.update(self.model_training_parameters)

        # Initialize base models
        self.base_models['rf'] = RandomForestRegressor(**rf_params)
        self.base_models['gb'] = GradientBoostingRegressor(**gb_params)

        meta_features = []

        # Generate meta-features
        for name, model in self.base_models.items():
            try:
                cv_pred = cross_val_predict(model, X, y, cv=3)
            except Exception as e:
                logger.warning(f"{name} CV failed, fallback to direct fit. Error: {e}")
                model.fit(X, y)
                cv_pred = model.predict(X)

            meta_features.append(cv_pred)

        meta_features = np.column_stack(meta_features)

        # Train base models fully
        for name, model in self.base_models.items():
            model.fit(X, y)

        # Train meta learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, y)

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        # Standard FreqAI pipeline
        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        base_predictions = []

        for name, model in self.base_models.items():
            pred = model.predict(X)

            # Ensure 1D
            pred = np.asarray(pred).reshape(-1)

            base_predictions.append(pred)

        meta_features = np.column_stack(base_predictions)

        final_pred = self.meta_learner.predict(meta_features)

        # Ensure 2D for FreqAI
        final_pred = np.asarray(final_pred).reshape(-1, 1)

        # Use correct label names
        pred_df = pd.DataFrame(final_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
