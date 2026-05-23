import logging
from typing import Any, Dict, Tuple
import numpy as np
from pandas import DataFrame
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.utils.class_weight import compute_sample_weight
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class ZHU_GradientBoostingRegressor(BaseRegressionModel):
    """
    User-created prediction model using GradientBoostingRegressor from scikit-learn.
    Inherits BaseRegressionModel to access Frequency AI functionality.
    """

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the GradientBoostingRegressor model.
        :param data_dictionary: Dictionary holding all data for train, test, labels, weights.
        :param dk: The DataKitchen object for the current coin/model.
        """
        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"].to_numpy()[:, 0]

        # Store feature columns for later use
        self.feature_columns = X.columns

        X = X.to_numpy()

        # Handle sample_weight
        sample_weight = None
        sample_weight_param = self.model_training_parameters.pop('sample_weight', None)
        if sample_weight_param == 'balanced':
            # Bin y into categories
            num_bins = 10  # Adjust the number of bins as needed
            bins = np.linspace(y.min(), y.max(), num_bins)
            y_binned = np.digitize(y, bins)
            # Compute sample weights
            sample_weight = compute_sample_weight('balanced', y_binned)
        elif sample_weight_param is not None:
            sample_weight = sample_weight_param  # Assume user provides an array-like sample_weight
        else:
            sample_weight = None

        # Initialize and fit the model
        model = GradientBoostingRegressor(**self.model_training_parameters)
        model.fit(X=X, y=y, sample_weight=sample_weight)

        # Optionally evaluate the model
        if "test_features" in data_dictionary and "test_labels" in data_dictionary:
            test_X = data_dictionary["test_features"].to_numpy()
            test_y = data_dictionary["test_labels"].to_numpy()[:, 0]
            score = model.score(test_X, test_y)
            logger.info("Model R^2 score on test set: %s", score)

        return model

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> Tuple[DataFrame, np.ndarray]:
        """
        Predict using the trained model.
        :param unfiltered_df: Full dataframe for the current backtest period.
        :param dk: The DataKitchen object for the current coin/model.
        :return:
        :pred_df: DataFrame containing the predictions.
        :do_predict: Array indicating where predictions are made.
        """
        # Prepare features for prediction
        dk.find_features(unfiltered_df)
        dk.data_dictionary["prediction_features"], _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, training_filter=False
        )

        dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
            dk.data_dictionary["prediction_features"], outlier_check=True
        )

        pred_features = dk.data_dictionary["prediction_features"]

        # Make predictions
        predictions = self.model.predict(pred_features.to_numpy())
        if self.CONV_WIDTH == 1:
            predictions = np.reshape(predictions, (-1, len(dk.label_list)))

        pred_df = DataFrame(predictions, columns=dk.label_list)

        pred_df, _, _ = dk.label_pipeline.inverse_transform(pred_df)
        if dk.feature_pipeline["di"]:
            dk.DI_values = dk.feature_pipeline["di"].di_values
        else:
            dk.DI_values = np.zeros(outliers.shape[0])
        dk.do_predict = outliers

        return pred_df, dk.do_predict

