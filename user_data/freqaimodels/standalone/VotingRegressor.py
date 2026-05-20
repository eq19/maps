import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)


class VotingRegressor(BaseRegressionModel):
    """
    FreqAI-compatible Voting Regressor
    - Safe param filtering
    - Proper FreqAI pipeline
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}

    # 🔥 Reusable param filter
    def _filter_params(self, model_class, params: Dict[str, Any]) -> Dict[str, Any]:
        valid_params = model_class().get_params().keys()
        return {k: v for k, v in params.items() if k in valid_params}

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit voting model
        """

        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # 🔥 Normalize labels
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

        lr_params = {}

        # -----------------------------
        # FILTERED CONFIG PARAMS
        # -----------------------------
        rf_params.update(self._filter_params(RandomForestRegressor, self.model_training_parameters))
        gb_params.update(self._filter_params(GradientBoostingRegressor, self.model_training_parameters))
        lr_params.update(self._filter_params(LinearRegression, self.model_training_parameters))

        # Initialize models
        self.base_models['rf'] = RandomForestRegressor(**rf_params)
        self.base_models['gb'] = GradientBoostingRegressor(**gb_params)
        self.base_models['lr'] = LinearRegression(**lr_params)

        # Train all models
        for name, model in self.base_models.items():
            model.fit(X, y)

        return self

    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs):
        """
        Predict using average voting
        """

        # 🔥 Use FreqAI pipeline (NOT filter_features)
        dk.find_features(unfiltered_df)
        X = dk.data_dictionary["prediction_features"]

        predictions = []

        for name, model in self.base_models.items():
            pred = np.asarray(model.predict(X)).reshape(-1)
            predictions.append(pred)

        # Average predictions
        final_pred = np.mean(predictions, axis=0)

        # Ensure 2D
        final_pred = final_pred.reshape(-1, 1)

        # ✅ Correct label mapping
        pred_df = pd.DataFrame(final_pred, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=np.int_)

        return pred_df, do_predict
