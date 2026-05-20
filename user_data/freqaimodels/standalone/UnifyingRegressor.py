import logging
import numpy as np
import pandas as pd
from typing import Any, Dict

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


class UnifyingRegressor(BaseRegressionModel):
    """
    FreqAI-compatible Unifying Regressor (simple stacking with holdout logic)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None

    # ================================
    # 🔧 PARAM FILTER
    # ================================
    def _filter_params(self, allowed):
        return {
            k: v for k, v in self.model_training_parameters.items()
            if k in allowed
        }

    # ================================
    # 🧠 FIT
    # ================================
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # 🔥 FIX: convert y safely
        if isinstance(y, pd.DataFrame):
            y = y.values

        if y.ndim == 2 and y.shape[1] == 1:
            y = y.ravel()

        # 🔥 FIX: safe params
        rf_params = self._filter_params(['n_estimators', 'max_depth'])
        lr_params = self._filter_params([])

        # Initialize models
        self.base_models['rf'] = RandomForestRegressor(
            random_state=42,
            **rf_params
        )

        self.base_models['lr'] = LinearRegression(**lr_params)

        # Train base models
        base_predictions = []

        for model in self.base_models.values():
            model.fit(X, y)

            pred = model.predict(X)
            if pred.ndim == 1:
                pred = pred.reshape(-1, 1)

            base_predictions.append(pred)

        # Create meta-features
        meta_features = np.column_stack(base_predictions)

        # Train meta learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, y)

        return self

    # ================================
    # 🔮 PREDICT
    # ================================
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        # 🔥 FIX: standard FreqAI pipeline
        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        base_predictions = []

        for model in self.base_models.values():
            pred = model.predict(X)

            if pred.ndim == 1:
                pred = pred.reshape(-1, 1)

            base_predictions.append(pred)

        # Meta-features
        meta_features = np.column_stack(base_predictions)

        final_pred = self.meta_learner.predict(meta_features)

        # 🔥 CRITICAL FIX: match labels
        if final_pred.ndim == 1:
            final_pred = final_pred.reshape(-1, 1)

        pred_df = pd.DataFrame(final_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
