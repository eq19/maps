from pandas import DataFrame
import numpy as np

from .base_adapter import BaseAdapter


class NeuralAdapter(BaseAdapter):

    def fit(self, data_dictionary, dk, **kwargs):
        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # reshape if needed
        X = np.array(X)
        y = np.array(y)

        self.model.fit(X, y, epochs=10, verbose=0)

        return self.model

    def predict(self, unfiltered_df, dk, **kwargs):
        dk.find_features(unfiltered_df)

        X = np.array(dk.data_dictionary["prediction_features"])

        preds = self.model.predict(X)

        if len(preds.shape) == 1:
            preds = preds.reshape(-1, 1)

        pred_df = DataFrame(preds, columns=dk.label_list)

        do_predict = np.ones(len(pred_df), dtype=int)

        return pred_df, do_predict
