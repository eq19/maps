from abc import ABC
from pandas import DataFrame
import numpy as np
from typing import Any, Tuple
from numpy.typing import NDArray

from user_data.freqaimodels.base.freqai_interface import IFreqaiModel


class BaseAdapter(IFreqaiModel, ABC):

    def __init__(self, config, model):
        super().__init__(config)
        self.model = model

    def train(self, unfiltered_df: DataFrame, pair: str, dk, **kwargs) -> Any:
        # Standard FreqAI pipeline
        dk.find_features(unfiltered_df)
        dk.find_labels(unfiltered_df)

        return self.fit(dk.data_dictionary, dk)

    def fit(self, data_dictionary, dk, **kwargs) -> Any:
        raise NotImplementedError

    def predict(
        self, unfiltered_df: DataFrame, dk, **kwargs
    ) -> Tuple[DataFrame, NDArray[np.int_]]:
        raise NotImplementedError
