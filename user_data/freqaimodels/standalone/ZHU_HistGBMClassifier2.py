import logging
from typing import Any, Dict, Tuple

import numpy as np
import numpy.typing as npt
from pandas import DataFrame
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class ZHU_HistGBMClassifier2(BaseClassifierModel):
    """
    User created prediction model using HistGradientBoostingClassifier from scikit-learn.
    The class inherits BaseClassifierModel, which means it has full access to all Frequency AI functionality.
    """

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the HistGradientBoostingClassifier model.
        :param data_dictionary: the dictionary holding all data for train, test, labels
        :param dk: The datakitchen object for the current coin/model
        """
        X = data_dictionary["train_features"].to_numpy()
        y = data_dictionary["train_labels"].to_numpy()[:, 0]

        le = LabelEncoder()
        y_encoded = le.fit_transform(y)

        if self.freqai_info.get("data_split_parameters", {}).get("test_size", 0.1) == 0:
            eval_set = None
        else:
            test_features = data_dictionary["test_features"].to_numpy()
            test_labels = data_dictionary["test_labels"].to_numpy()[:, 0]
            test_labels_encoded = le.transform(test_labels)
            eval_set = (test_features, test_labels_encoded)

        if self.freqai_info.get("continual_learning", False):
            logger.warning(
                "Continual learning is not supported for "
                "SKLearnHistGradientBoostingClassifier, ignoring."
            )

        # Adjust class_weight to use encoded labels
        class_weight = self.model_training_parameters.get('class_weight')
        if isinstance(class_weight, dict):
            encoded_class_weight = {}
            for k, v in class_weight.items():
                if isinstance(k, str):
                    try:
                        encoded_k = le.transform([k])[0]
                    except ValueError:
                        logger.warning(f"Label {k} not found in training data, skipping from class_weight")
                        continue
                else:
                    encoded_k = k
                encoded_class_weight[encoded_k] = v

            self.model_training_parameters['class_weight'] = encoded_class_weight

        elif class_weight == 'balanced':
            self.model_training_parameters['class_weight'] = 'balanced'
        else:
            self.model_training_parameters['class_weight'] = None

        model = HistGradientBoostingClassifier(**self.model_training_parameters)
        model.fit(X=X, y=y_encoded)

        if eval_set:
            logger.info("Score: %s", model.score(eval_set[0], eval_set[1]))

        return model

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
        """
        Filter the prediction features data and predict with it.
        :param unfiltered_df: Full dataframe for the current backtest period.
        :return:
        :pred_df: dataframe containing the predictions
        :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
        data (NaNs) or felt uncertain about data (PCA and DI index)
        """
        (pred_df, dk.do_predict) = super().predict(unfiltered_df, dk, **kwargs)

        le = LabelEncoder()
        label = dk.label_list[0]
        labels_before = list(dk.data["labels_std"].keys())
        labels_after = le.fit_transform(labels_before).tolist()
        pred_df[label] = le.inverse_transform(pred_df[label].astype(int))
        pred_df = pred_df.rename(
            columns={labels_after[i]: labels_before[i] for i in range(len(labels_before))}
        )

        return (pred_df, dk.do_predict)
