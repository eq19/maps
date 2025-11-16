import os
import pickle
import sys

import keras_model
from keras_device import scope
from tensorflow_wrapper import tensorflow

# @tensorflow.jit()
def loss_custom(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    batch_size = y_pred.shape[0]
    y_true = tensorflow.cast(y_true, y_pred.dtype)

    # print(y_pred)
    # print(y_true)

    if y_pred.shape != (batch_size, 3):
        raise Exception(y_pred.shape)
    if y_true.shape != (batch_size, 2):
        raise Exception(y_true.shape)

    # y_pred_index_maximum = tensorflow.numpy.argmax(y_pred, axis=1)
    # y_true_index_maximum = tensorflow.numpy.argmax(y_true, axis=1)

    # print(y_pred_index_maximum)
    # print(y_true_index_maximum)

    point_zero = y_pred[:, 2:]

    # print(point_zero)

    y_pred = y_pred[:, :2]

    # print(y_pred)

    y_difference = y_true - y_pred

    # print(y_difference)

    # mask_zero = tensorflow.numpy.repeat((y_pred_index_maximum == 2), 2).reshape(batch_size, 2)

    # print(mask_zero)

    # point_plus = y_pred[~mask_zero & (y_difference > 0)]
    # point_minus = -y_pred[mask_zero | (y_difference < 0)]
    point_plus = y_pred[y_difference > 0]
    point_minus = y_pred[y_difference < 0]

    # print(point_plus)
    # print(point_minus)

    fee = 0.002

    # loss = batch_size - tensorflow.numpy.sum(point_plus) + tensorflow.numpy.sum(point_minus) * 1.05
    # loss = batch_size - tensorflow.numpy.sum(point_plus) + tensorflow.numpy.sum(point_minus) - tensorflow.numpy.sum(point_zero) * 0
    loss = batch_size - (tensorflow.numpy.sum(point_plus) * (1 - fee)) + (tensorflow.numpy.sum(point_minus) * (1 + fee)) - tensorflow.numpy.sum(point_zero) * 0
    return loss

print(loss_custom(tensorflow.numpy.array([[1, 0], [1, 0], [1, 0]]), tensorflow.numpy.array([[0.1, 0.3, 0.6], [0.1, 0.6, 0.3], [0.6, 0.3, 0.1]])))
# assert loss_custom(tensorflow.numpy.array([[1, 0], [1, 0], [1, 0]]), tensorflow.numpy.array([[0.1, 0.3, 0.6], [0.1, 0.6, 0.3], [0.6, 0.3, 0.1]])) == 3.4

def reverse_direction(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    batch_size = y_pred.shape[0]
    y_true = tensorflow.cast(y_true, y_pred.dtype)

    if y_pred.shape != (batch_size, 3):
        raise Exception(y_pred.shape)
    if y_true.shape != (batch_size, 2):
        raise Exception(y_true.shape)

    y_pred_index_maximum = tensorflow.numpy.argmax(y_pred, axis=1)
    y_true_index_maximum = tensorflow.numpy.argmax(y_true, axis=1)

    # mask0 = (y_true_index_maximum == y_pred_index_maximum) & (y_true_index_maximum == 0)
    # ratio0 = tensorflow.numpy.count_nonzero(mask0) / len(y_true_index_maximum)

    mask0 = (y_true_index_maximum != y_pred_index_maximum) & (y_pred_index_maximum != 2)
    ratio0 = tensorflow.numpy.count_nonzero(mask0) / len(y_true_index_maximum)
    return ratio0

print(reverse_direction(tensorflow.numpy.array([[1, 0], [1, 0], [1, 0]]), tensorflow.numpy.array([[0.1, 0.3, 0.6], [0.1, 0.6, 0.3], [0.6, 0.3, 0.1]])))

def ratio2(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    batch_size = y_pred.shape[0]
    y_true = tensorflow.cast(y_true, y_pred.dtype)

    if y_pred.shape != (batch_size, 3):
        raise Exception(y_pred.shape)
    if y_true.shape != (batch_size, 2):
        raise Exception(y_true.shape)

    y_pred_index_maximum = tensorflow.numpy.argmax(y_pred, axis=1)
    y_true_index_maximum = tensorflow.numpy.argmax(y_true, axis=1)
    mask = y_pred_index_maximum == 2
    ratio = tensorflow.numpy.count_nonzero(mask) / len(y_true_index_maximum)
    return ratio

@tensorflow.jit()
def accuracy60(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    y_true = tensorflow.cast(y_true, y_pred.dtype)

    y_pred_index_maximum = tensorflow.numpy.argmax(y_pred, axis=1)
    y_true_index_maximum = tensorflow.numpy.argmax(y_true, axis=1)
    y_pred_maximum = tensorflow.numpy.amax(y_pred, axis=1)

    mask = (y_pred_index_maximum == y_true_index_maximum) & (y_pred_maximum > 0.60)
    ratio = tensorflow.numpy.count_nonzero(mask) / y_true_index_maximum.shape[0]
    return ratio

print(accuracy60(tensorflow.numpy.array([[1, 0], [1, 0], [1, 0]]), tensorflow.numpy.array([[0.1, 0.3, 0.95], [0.1, 0.95, 0.3], [0.95, 0.3, 0.1]])))

@tensorflow.jit()
def reverse_direction60(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    y_true = tensorflow.cast(y_true, y_pred.dtype)

    y_pred_index_maximum = tensorflow.numpy.argmax(y_pred, axis=1)
    y_true_index_maximum = tensorflow.numpy.argmax(y_true, axis=1)
    y_pred_maximum = tensorflow.numpy.amax(y_pred, axis=1)

    mask = (y_true_index_maximum != y_pred_index_maximum) & (y_pred_maximum > 0.60)
    ratio = tensorflow.numpy.count_nonzero(mask) / y_true_index_maximum.shape[0]
    return ratio

@tensorflow.jit()
def error_absolute_maximum(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor) -> tensorflow.Tensor:
    result = tensorflow.numpy.amax(tensorflow.numpy.absolute(y_true - y_pred))
    return result

_rate_entry = 0.03
_rate_exit_profit = 0.02
_rate_exit_loss = 0.001

if _rate_exit_profit > _rate_entry or _rate_exit_loss > _rate_entry:
    raise Exception

if _rate_entry <= 0 or _rate_exit_profit <= 0 or _rate_exit_loss <= 0:
    raise Exception

@tensorflow.jit()
def ratio_entry(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry) -> tensorflow.Tensor:
    mask = (y_pred > (1 + rate_entry)) | (y_pred < (1 - rate_entry))
    result = tensorflow.numpy.count_nonzero(mask) / y_pred.shape[0]
    return result

@tensorflow.jit()
def ratio_exit_profit(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry,
                      rate_exit_profit: float = _rate_exit_profit) -> tensorflow.Tensor:
    mask_a = (((y_pred > (1 + rate_entry)) & (y_true > (1 + rate_exit_profit)))
              | ((y_pred < (1 - rate_entry)) & (y_true < (1 - rate_exit_profit))))
    mask_b = (y_pred > (1 + rate_entry)) | (y_pred < (1 - rate_entry))
    result = tensorflow.numpy.count_nonzero(mask_a) / tensorflow.numpy.count_nonzero(mask_b)
    result = tensorflow.numpy.nan_to_num(result)
    return result

@tensorflow.jit()
def ratio_hold(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry,
               rate_exit_profit: float = _rate_exit_profit, rate_exit_loss: float = _rate_exit_loss) -> tensorflow.Tensor:
    mask_a = (((y_pred > (1 + rate_entry)) & ((1 - rate_exit_loss) < y_true) & (y_true < (1 + rate_exit_profit)))
              | ((y_pred < (1 - rate_entry)) & ((1 + rate_exit_loss) > y_true) & (y_true > (1 - rate_exit_profit))))
    mask_b = (y_pred > (1 + rate_entry)) | (y_pred < (1 - rate_entry))
    result = tensorflow.numpy.count_nonzero(mask_a) / tensorflow.numpy.count_nonzero(mask_b)
    result = tensorflow.numpy.nan_to_num(result)
    return result

@tensorflow.jit()
def ratio_exit_loss(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry,
                    rate_exit_loss: float = _rate_exit_loss) -> tensorflow.Tensor:
    mask_a = (((y_pred > (1 + rate_entry)) & (y_true < (1 - rate_exit_loss)))
              | ((y_pred < (1 - rate_entry)) & (y_true > (1 + rate_exit_loss))))
    mask_b = (y_pred > (1 + rate_entry)) | (y_pred < (1 - rate_entry))
    result = tensorflow.numpy.count_nonzero(mask_a) / tensorflow.numpy.count_nonzero(mask_b)
    result = tensorflow.numpy.nan_to_num(result)
    return result

@tensorflow.jit()
def percent(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry) -> tensorflow.Tensor:
    mask_a = y_pred > (1 + rate_entry)
    mask_b = y_pred < (1 - rate_entry)

    sum_long = tensorflow.numpy.sum(y_true[mask_a] - 1)
    sum_short = tensorflow.numpy.sum(-(y_true[mask_b] - 1))
    result = (sum_long + sum_short) * 100
    return result

@tensorflow.jit()
def percent_loss(y_true: tensorflow.Tensor, y_pred: tensorflow.Tensor, rate_entry: float = _rate_entry) -> tensorflow.Tensor:
    mask_a = (y_pred > (1 + rate_entry)) & (y_true < 1)
    mask_b = (y_pred < (1 - rate_entry)) & (y_true > 1)

    sum_long = tensorflow.numpy.sum(y_true[mask_a] - 1)
    sum_short = tensorflow.numpy.sum(-(y_true[mask_b] - 1))
    result = (sum_long + sum_short) * 100
    return result

enable_cache = False
cachefile = 'cache.pickle'

if enable_cache and os.path.exists(cachefile):
    with open(cachefile, 'rb') as cachehandle:
        print(f'Using cached result from \'{cachefile}\'')
        result = pickle.load(cachehandle)
else:
    from load_data import load_data
    result = load_data(window=400, return_column_feature=True)

    if enable_cache:
        with open(cachefile, 'wb') as cachehandle:
            print(f'Saving result to cache \'{cachefile}\'')
            pickle.dump(result, cachehandle)

x_train, y_train, x_test, y_test, column_feature = result

print(column_feature)

print(x_train.shape, x_test.shape)
print(x_train)

print(y_train.shape, y_test.shape)
print(y_train)

import numpy
print(numpy.mean(numpy.absolute(y_train), axis=0))
print(numpy.mean(numpy.absolute(y_test), axis=0))

window = x_train.shape[1]
feature = x_train.shape[2]
output_class = y_train.shape[1]

with scope():
    # data_train = strategy.experimental_distribute_dataset(data_train)
    # data_test = strategy.experimental_distribute_dataset(data_test)

    try:
        model = tensorflow.keras.models.load_model('./model')
    except OSError as error:
        print(f'Model has not found: {error}')
        input_shape = [window, feature]        
        model = keras_model.create_model(input_shape, output_class)

    # steps_per_epoch = len(x_test) // batch_size
    # log.info(f'steps_per_epoch: {steps_per_epoch}')

    # learning_rate_schedule = tensorflow.keras.optimizers.schedules.InverseTimeDecay(
        # 0.001, decay_steps=steps_per_epoch * 1000, decay_rate=1, staircase=False
    # )

    # learning_rate=1e-6 learning_rate=learning_rate_schedule
    # accuracy accuracy60 ratio2 reverse_direction reverse_direction60
    # loss_custom steps_per_execution=len(x_test) // 200
    model.compile(optimizer=tensorflow.optimizers.SGD(), loss='mean_absolute_error', metrics=[error_absolute_maximum,
                  ratio_entry, ratio_exit_profit, ratio_hold, ratio_exit_loss, percent, percent_loss])
    model.summary()

    # https://github.com/tensorflow/tensorflow/blob/master/tensorflow/python/keras/backend.py#L1794-L1815
    parameter_trainable = tensorflow.numpy.sum([tensorflow.numpy.prod(i.shape.as_list()) for i in model.trainable_weights])
    print(f'parameter_trainable:{parameter_trainable}')

    early_stopping = tensorflow.keras.callbacks.EarlyStopping(monitor='loss', patience=10, mode='min',  # baseline=0.01,
                                                              start_from_epoch=20)
    try:
        # data_train batch_size data_test
        history = model.fit(x_train, y_train, batch_size=200, epochs=300, validation_data=(x_test, y_test),
                            callbacks=[early_stopping])

    except KeyboardInterrupt:
        print('\nPaused: KeyboardInterrupt')

    if False:
        model.save('./model')

sys.exit()
