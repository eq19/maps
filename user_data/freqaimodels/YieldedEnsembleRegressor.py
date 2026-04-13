import logging
import numpy as np
import pandas as pd
from typing import Any, Dict

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


class YieldedEnsembleRegressor(BaseRegressionModel):
    """
    FreqAI-safe weighted ensemble regressor
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models = {}
        self.weights = {}

    def _clean_params(self, allowed_keys):
        return {
            k: v for k, v in self.model_training_parameters.items()
            if k in allowed_keys
        }

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # ✅ Normalize y
        if isinstance(y, pd.DataFrame):
            y = y.values
        elif isinstance(y, pd.Series):
            y = y.values

        if len(y.shape) == 1:
            y = y.reshape(-1, 1)

        y_flat = y.ravel()

        # ✅ Clean params
        rf_params = self._clean_params({"n_estimators", "max_depth", "random_state"})
        lr_params = self._clean_params({})

        # Models
        self.models['rf'] = RandomForestRegressor(
            random_state=42,
            **rf_params
        )

        self.models['lr'] = LinearRegression(**lr_params)

        # Train
        for model in self.models.values():
            model.fit(X, y_flat)

        # Equal weights
        self.weights = {
            name: 1.0 / len(self.models)
            for name in self.models
        }

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):

        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        predictions = []

        for name, model in self.models.items():
            pred = model.predict(X)
            predictions.append(pred * self.weights[name])

        ensemble_pred = np.sum(predictions, axis=0)

        # ✅ Ensure 2D
        if len(ensemble_pred.shape) == 1:
            ensemble_pred = ensemble_pred.reshape(-1, 1)

        # ✅ Correct output
        pred_df = pd.DataFrame(ensemble_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
