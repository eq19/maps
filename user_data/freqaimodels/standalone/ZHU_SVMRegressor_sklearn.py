import logging
from typing import Any, Dict, Tuple

import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame
from sklearn.svm import SVR  # Updated import

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class ZHU_SVMRegressor_sklearn(BaseRegressionModel):
    """
    User-created prediction model using Support Vector Machine (SVM) regressor.
    This class inherits from BaseRegressionModel and is customized to use the
    SVR from scikit-learn for model training and prediction.
    The SVR is versatile and effective for a variety of regression tasks.
    """

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        X = data_dictionary["train_features"].to_numpy()
        y = data_dictionary["train_labels"].to_numpy()[:, 0]

        # No need for LabelEncoder in regression tasks
        # Instantiate the SVR model with provided training parameters
        model = SVR(**self.model_training_parameters)

        # Fit the model to the training data
        model.fit(X=X, y=y)

        return model

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> Tuple[DataFrame, npt.NDArray[np.float_]]:
        pred_df, dk.do_predict = super().predict(unfiltered_df, dk, **kwargs)

        # No need for LabelEncoder in regression tasks
        # Predictions are already continuous values

        return pred_df, dk.do_predict

