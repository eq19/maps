import logging
from typing import Any, Dict, Tuple
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import numpy.typing as npt
from pandas import DataFrame
from sklearn.ensemble import ExtraTreesClassifier # Changed from RandomForestClassifier to ExtraTreesClassifier
from sklearn.preprocessing import LabelEncoder
from pandas.api.types import is_integer_dtype

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class ZHU_sklearn_ExtraTreesClassifier(BaseClassifierModel):
    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        X = data_dictionary["train_features"].to_numpy()
        y = data_dictionary["train_labels"].to_numpy()[:, 0]

        le = LabelEncoder()
        if not is_integer_dtype(y):
            y = pd.Series(le.fit_transform(y), dtype="int64")

        if self.freqai_info.get('data_split_parameters', {}).get('test_size', 0.1) == 0:
            eval_set = None
        else:
            test_features = data_dictionary["test_features"].to_numpy()
            test_labels = data_dictionary["test_labels"].to_numpy()[:, 0]

            if not is_integer_dtype(test_labels):
                test_labels = pd.Series(le.transform(test_labels), dtype="int64")

            eval_set = [(test_features, test_labels)]

        train_weights = data_dictionary["train_weights"]

        model = ExtraTreesClassifier(**self.model_training_parameters) # Changed from RandomForestClassifier to ExtraTreesClassifier
        model.fit(X=X, y=y, sample_weight=train_weights)
        
        if eval_set:
            logger.info("Score: %s", model.score(eval_set[0][0], eval_set[0][1]))

        return model

    def predict(self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
        (pred_df, dk.do_predict) = super().predict(unfiltered_df, dk, **kwargs)

        le = LabelEncoder()
        label = dk.label_list[0]
        labels_before = list(dk.data['labels_std'].keys())
        labels_after = le.fit_transform(labels_before).tolist()
        pred_df[label] = le.inverse_transform(pred_df[label].astype(int))
        pred_df = pred_df.rename(columns={labels_after[i]: labels_before[i] for i in range(len(labels_before))})

        return (pred_df, dk.do_predict)

