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
    - Safe param filtering per model
    - Robust label handling
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None

    # 🔥 KEY FUNCTION: filter params per model
    def _filter_params(self, model_class, params: Dict[str, Any]) -> Dict[str, Any]:
        valid_params = model_class().get_params().keys()
        return {k: v for k, v in params.items() if k in valid_params}

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # Normalize labels
        y = np.asarray(y).reshape(-1)

        # -----------------------------
        # DEFAULT PARAMS
        # -----------------------------
        rf_params = {
            "n_estimators": 50,
            "max_depth": 8,
            "random_state": 42,
        }

        gb_params = {
            "n_estimators": 50,
            "max_depth": 6,
            "random_state": 42,
        }

        # -----------------------------
        # FILTERED CONFIG PARAMS
        # -----------------------------
        rf_extra = self._filter_params(RandomForestRegressor, self.model_training_parameters)
        gb_extra = self._filter_params(GradientBoostingRegressor, self.model_training_parameters)

        rf_params.update(rf_extra)
        gb_params.update(gb_extra)

        # Initialize models safely
        self.base_models['rf'] = RandomForestRegressor(**rf_params)
        self.base_models['gb'] = GradientBoostingRegressor(**gb_params)

        meta_features = []

        # Generate meta-features
        for name, model in self.base_models.items():
            try:
                cv_pred = cross_val_predict(model, X, y, cv=3)
            except Exception as e:
                logger.warning(f"{name} CV failed, fallback to fit. Error: {e}")
                model.fit(X, y)
                cv_pred = model.predict(X)

            meta_features.append(cv_pred)

        meta_features = np.column_stack(meta_features)

        # Train base models
        for model in self.base_models.values():
            model.fit(X, y)

        # Train meta learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, y)

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        base_predictions = []

        for model in self.base_models.values():
            pred = np.asarray(model.predict(X)).reshape(-1)
            base_predictions.append(pred)

        meta_features = np.column_stack(base_predictions)

        final_pred = self.meta_learner.predict(meta_features)
        final_pred = np.asarray(final_pred).reshape(-1, 1)

        pred_df = pd.DataFrame(final_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
