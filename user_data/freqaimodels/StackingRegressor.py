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
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # Ensure y is 2D
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)

        # Initialize base models
        self.base_models['rf'] = RandomForestRegressor(
            n_estimators=50,
            max_depth=8,
            random_state=42,
            **self.model_training_parameters
        )

        self.base_models['gb'] = GradientBoostingRegressor(
            n_estimators=50,
            max_depth=6,
            random_state=42,
            **self.model_training_parameters
        )

        meta_features = []

        # Generate meta-features
        for name, model in self.base_models.items():
            try:
                cv_pred = cross_val_predict(model, X, y.ravel(), cv=3)
            except Exception:
                # fallback (multi-target or incompatible)
                model.fit(X, y)
                cv_pred = model.predict(X)

            meta_features.append(cv_pred)

        meta_features = np.column_stack(meta_features)

        # Train base models fully
        for model in self.base_models.values():
            model.fit(X, y.ravel())

        # Train meta learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, y.ravel())

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        # Standard FreqAI feature pipeline
        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        base_predictions = []

        for model in self.base_models.values():
            pred = model.predict(X)
            base_predictions.append(pred)

        meta_features = np.column_stack(base_predictions)

        final_pred = self.meta_learner.predict(meta_features)

        # Ensure 2D
        if len(final_pred.shape) == 1:
            final_pred = final_pred.reshape(-1, 1)

        # 🔥 KEY FIX: Use dk.label_list
        pred_df = pd.DataFrame(final_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
