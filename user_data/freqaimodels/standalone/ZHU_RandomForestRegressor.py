import logging
from typing import Any, Dict, Tuple
import pandas as pd
import numpy as np
import numpy.typing as npt
from pandas import DataFrame
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class  ZHU_RandomForestRegressor(BaseRegressionModel):
    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        X = data_dictionary["train_features"].to_numpy()
        y = data_dictionary["train_labels"].to_numpy()[:, 0]

        if self.freqai_info.get('data_split_parameters', {}).get('test_size', 0.1) == 0:
            eval_set = None
        else:
            test_features = data_dictionary["test_features"].to_numpy()
            test_labels = data_dictionary["test_labels"].to_numpy()[:, 0]
            eval_set = (test_features, test_labels)

        train_weights = data_dictionary["train_weights"]

        model = RandomForestRegressor(**self.model_training_parameters)
        model.fit(X=X, y=y, sample_weight=train_weights)

        if eval_set:
            predictions = model.predict(eval_set[0])
            mse = mean_squared_error(eval_set[1], predictions)
            r2 = r2_score(eval_set[1], predictions)
            logger.info("Evaluation Metrics - MSE: %s, R^2 Score: %s", mse, r2)

        return model

    def predict(self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
        (pred_df, dk.do_predict) = super().predict(unfiltered_df, dk, **kwargs)
        # No label encoding is needed for regression predictions
        return (pred_df, dk.do_predict)

