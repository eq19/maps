import logging
from typing import Any, Dict, Tuple

import numpy
import pandas
from freqtrade.exceptions import OperationalException
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

import TensorFlowBase
import generate_dataset
import keras_model
from load_data import column_feature, column_label
from tensorflow_wrapper import tensorflow

log = logging.getLogger(__name__)

class TensorFlowRegression(TensorFlowBase.TensorFlowBase):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self.CONV_WIDTH = 400

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen) -> Any:
        dataframe = data_dictionary['unfiltered_df']

        for i in dk.label_list:
            if dataframe[i].dtype != 'float64':
                raise OperationalException

        n_features = len(dk.training_features_list)
        n_labels = len(dk.label_list)

        # batch_size = self.freqai_info.get('batch_size', 200)
        batch_size = 200
        input_dims = [self.CONV_WIDTH, n_features]

        feature = dataframe[column_feature(dataframe)].to_numpy(dtype='float32')
        feature_mask = (dataframe['volume'] > 0).to_numpy(dtype='bool')

        label = dataframe[column_label(dataframe)].to_numpy(dtype='float32')
        label_mask = numpy.full(len(label), True, dtype='bool')

        x_train, y_train, x_test, y_test = (
            generate_dataset.generate_dataset(feature, feature_mask, label, label_mask, window=self.CONV_WIDTH,
                                              batch_size=batch_size, split_ratio=0.90, train_include_test=True,
                                              enable_window_nomalization=True)
        )

        if len(x_train) == 0 or len(x_test) == 0:
            raise Exception

        dataset_train = tensorflow.data.Dataset.from_tensor_slices((x_train, y_train))
        # dataset_test = tensorflow.data.Dataset.from_tensor_slices((x_test, y_test))

        dataset_train = dataset_train.batch(batch_size, drop_remainder=True)
        # dataset_test = dataset_test.batch(batch_size, drop_remainder=True)

        model = self.get_init_model(dk.pair)

        if model is None:
            log.info('Creating a new model.')

            input_shape = input_dims
            output_class = n_labels
            model = keras_model.create_model(input_shape, output_class)

            model.compile(
                optimizer=tensorflow.optimizers.SGD(),
                loss='mean_absolute_error',
                metrics=[],
            )
            model.summary()
            # max_epochs = 50
            max_epochs = 200

        else:
            log.info('Updating the old model.')
            max_epochs = 10

        # early_stopping = tensorflow.keras.callbacks.EarlyStopping(monitor='loss', patience=10, mode='min', start_from_epoch=20)

        # model.fit(dataset_train, epochs=max_epochs, shuffle=False, callbacks=[early_stopping])
        model.fit(dataset_train, epochs=max_epochs, shuffle=False)
        return model

    def predict(self, unfiltered_dataframe: pandas.DataFrame, dk: FreqaiDataKitchen, first=True
                ) -> Tuple[pandas.DataFrame, pandas.DataFrame]:

        dataframe = unfiltered_dataframe
        feature = dataframe[column_feature(dataframe)]

        # print(feature.to_markdown())
        # print(feature.shape)

        if first:
            log.info('First')
            x, x_mask = generate_dataset.generate_dataset_predict(x=feature.to_numpy(dtype='float32'),
                                                                  x_mask=numpy.full(len(feature), True, dtype='bool'),
                                                                  window=self.CONV_WIDTH, batch_size=200,
                                                                  enable_window_nomalization=True)

            print(x)
            prediction = self.model.predict(x)

        else:
            log.info('Not first')
            data = feature
            # data = tensorflow.expand_dims(data, axis=0)
            print(data.shape)
            prediction = self.model(data, training=False)

        print(prediction)
        print(prediction.shape)

        pred_df = pandas.DataFrame(prediction, columns=dk.label_list)
        do_predict = numpy.ones(len(pred_df))
        return (pred_df, do_predict)
