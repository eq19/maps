import typing
import numpy
import tensorflow_probability
from numpy import ndarray

from numba_wrapper import numba
from tensorflow_wrapper import tensorflow

@numba.jit(inline='always')
def _generate_answer(price: ndarray, threshold: float = 0.01, enum_unknown: int = -1, enum_up: int = 1,
                     enum_down: int = 0) -> ndarray:

    result_answer = numpy.empty(len(price), dtype='int64')

    for i in range(len(price)):
        price_entry = price[i]
        answer = enum_unknown

        for j in range(1, len(price)):
            if i + j > len(price) - 1:
                break

            price_current = price[i + j]

            if price_current / price_entry > (1 + threshold):
                answer = enum_up
                break

            elif price_current / price_entry < (1 - threshold):
                answer = enum_down
                break

        result_answer[i] = answer

        if answer == enum_unknown:
            for j in range(i, len(price)):
                result_answer[j] = enum_unknown
            break

    return (result_answer, result_answer != -1)

@numba.jit(inline='always')
def _generate_window(a: ndarray, mask: ndarray, window: int = 200, exclude_nan: bool = False) -> (ndarray, ndarray):

    if len(a) != len(mask):
        raise Exception

    if len(a) < window:
        raise Exception

    if len(a.shape) != 2:
        raise Exception

    if window < 1:
        raise Exception

    if exclude_nan:
        for i in range(len(a)):
            mask[i] &= ~numpy.isnan(a[i]).any()

    length: int = 0
    mask_window = numpy.empty(len(a), dtype='bool')

    for i in range(window - 1):
        mask_window[i] = False

    for i in range(window - 1, len(a)):
        status = True

        for j in range(window):
            if not mask[i - j]:
                status = False
                break

        if status:
            mask_window[i] = True
            length += 1
        else:
            mask_window[i] = False

    result = numpy.empty((length, window, a.shape[1]), dtype=a.dtype)
    index = 0

    for i in range(window - 1, len(a)):
        if mask_window[i]:
            result[index] = a[i + 1 - window:i + 1]
            index += 1

    return (result, mask_window)

@numba.jit(inline='always')
def _make_divisible(number: int, divisor: int) -> int:
    return number - (number % divisor)

@tensorflow.jit
def _window_nomalization(input_a: ndarray, threshold_scale: typing.Optional[float]) -> ndarray:

    if len(input_a.shape) != 3:
        raise Exception

    window_maximum = tensorflow.numpy.amax(input_a, axis=1)
    if threshold_scale is not None:
        window_maximum *= (1 + threshold_scale)
    window_maximum = tensorflow.numpy.repeat(window_maximum, input_a.shape[1], axis=0)
    window_maximum = tensorflow.numpy.reshape(window_maximum, input_a.shape)

    window_minimum = tensorflow.numpy.amin(input_a, axis=1)
    if threshold_scale is not None:
        window_minimum *= (1 - threshold_scale)
    window_minimum = tensorflow.numpy.repeat(window_minimum, input_a.shape[1], axis=0)
    window_minimum = tensorflow.numpy.reshape(window_minimum, input_a.shape)

    result = (input_a - window_minimum) / (window_maximum - window_minimum)
    return result

@tensorflow.jit
def _window_nomalization_v2(input_a: ndarray) -> tensorflow.numpy.ndarray:

    if len(input_a.shape) != 3:
        raise Exception

    window_index0 = tensorflow.numpy.repeat(input_a[:, 0], input_a.shape[1], axis=0)
    window_index0 = tensorflow.numpy.reshape(window_index0, input_a.shape)

    with numpy.errstate(divide='ignore'):
        result = tensorflow.numpy.where(window_index0 != 0., input_a / window_index0, numpy.nan)

    return result

@tensorflow.jit
def _nomalization_absolute_first(x: tensorflow.numpy.ndarray, axis: int = None) -> tensorflow.numpy.ndarray:
    x_0 = tensorflow.numpy.rollaxis(x, axis)[0]  # https://stackoverflow.com/questions/31363704/numpy-index-on-a-variable-axis
    x_0 = tensorflow.numpy.expand_dims(x_0, axis=axis)
    x_0 = tensorflow.numpy.absolute(x_0)
    y = tensorflow.numpy.where(x_0 != 0., x / x_0, numpy.nan)
    return y

import indicator

@tensorflow.jit
def _nomalization_absolute_previous(x: tensorflow.numpy.ndarray, axis: int = None) -> tensorflow.numpy.ndarray:
    x_previous = indicator.tensorflow_shift(x, 1, axis=axis)
    x_previous = tensorflow.numpy.absolute(x_previous)
    y = x / x_previous
    y = tensorflow.numpy.where(tensorflow.numpy.logical_or(tensorflow.numpy.isnan(y), tensorflow.numpy.isinf(y)), 1., y)
    return y

@tensorflow.jit
def _nomalization_minmax(x: tensorflow.numpy.ndarray, axis: int = None) -> tensorflow.numpy.ndarray:
    x_min = tensorflow.numpy.min(x, axis=axis, keepdims=True)
    x_max = tensorflow.numpy.max(x, axis=axis, keepdims=True)
    y = (x - x_min) / (x_max - x_min)
    return y

@tensorflow.jit
def _nomalization_minmax_scale(x: tensorflow.numpy.ndarray, scale: float, axis: int = None) -> tensorflow.numpy.ndarray:
    x_min = tensorflow.numpy.min(x, axis=axis, keepdims=True) * (1 - scale)
    x_max = tensorflow.numpy.max(x, axis=axis, keepdims=True) * (1 + scale)
    y = (x - x_min) / (x_max - x_min)
    return y

@tensorflow.jit
def _nomalization_minmax_scale_range(x: tensorflow.numpy.ndarray, scale: float, axis: int = None) -> tensorflow.numpy.ndarray:
    x_min = tensorflow.numpy.min(x, axis=axis, keepdims=True)
    x_max = tensorflow.numpy.max(x, axis=axis, keepdims=True)
    x_scale = (x_max - x_min) * scale
    x_min = x_min - x_scale
    x_max = x_max + x_scale
    y = (x - x_min) / (x_max - x_min)
    return y

@tensorflow.jit
def _nomalization_zscore(x: tensorflow.numpy.ndarray, axis: int = None) -> tensorflow.numpy.ndarray:
    x_mean = tensorflow.numpy.mean(x, axis=axis, keepdims=True)
    x_std = tensorflow.numpy.std(x, axis=axis, keepdims=True)
    y = (x - x_mean) / x_std
    return y

@tensorflow.jit
def _nomalization_zscore_robust(x: tensorflow.numpy.ndarray, axis: int = None) -> tensorflow.numpy.ndarray:
    x_quantile = tensorflow_probability.stats.quantiles(x, num_quantiles=4, axis=axis, interpolation='linear', keepdims=True)
    x_scale_robust = (x - x_quantile[2]) / (x_quantile[3] - x_quantile[1])
    y = x_scale_robust * 1.3489
    return y

@tensorflow.jit
def window_nomalization(x: tensorflow.numpy.ndarray, version: str = 'minmax_scale') -> tensorflow.numpy.ndarray:

    if len(x.shape) != 3:
        raise Exception

    if x.shape[1] < 2:
        raise Exception

    if version == 'v1':
        x = _window_nomalization(x, threshold_scale=0.005)
    elif version == 'v2':
        x = _window_nomalization_v2(x)
    elif version == 'absolute_first':
        x = _nomalization_absolute_first(x, axis=1)
    elif version == 'absolute_previous':
        x = _nomalization_absolute_previous(x, axis=1)
    elif version == 'minmax':
        x = _nomalization_minmax(x, axis=1)
    elif version == 'minmax_scale':
        x = _nomalization_minmax_scale(x, scale=0.005, axis=1)
    elif version == 'minmax_scale_range':
        x = _nomalization_minmax_scale_range(x, scale=0.01, axis=1)
    elif version == 'zscore':
        x = _nomalization_zscore(x, axis=1)
    elif version == 'zscore_robust':
        x = _nomalization_zscore_robust(x, axis=1)
    else:
        raise Exception

    return x

def generate_dataset(x: ndarray, x_mask: ndarray, y: ndarray, y_mask: ndarray, window: int, batch_size: int = 200,
                     split_ratio: float = 0.8, train_include_test: bool = False, enable_window_nomalization: bool = False,
                     encode_onehot: bool = False) -> (ndarray, ndarray, ndarray, ndarray):

    if len(x.shape) != 2:
        raise Exception

    if len(x_mask.shape) != 1:
        raise Exception

    if len(y.shape) != 2:
        raise Exception

    if len(y_mask.shape) != 1:
        raise Exception

    if not len(x) == len(x_mask) == len(y) == len(y_mask):
        raise Exception

    if window < 1:
        raise Exception

    if batch_size < 2:
        raise Exception

    if not 0 <= split_ratio <= 1:
        raise Exception

    y_mask &= ~numpy.isnan(y).any(axis=1)
    x, x_mask = _generate_window(x, (x_mask & y_mask), window=window, exclude_nan=True)
    y = y[x_mask]

    if len(x) != len(y):
        raise Exception

    if enable_window_nomalization:
        x = window_nomalization(x)

    if encode_onehot:
        y = tensorflow.keras.utils.to_categorical(y)

    length = _make_divisible(len(x), batch_size)
    x, y = x[-length:], y[-length:]

    # length_train = _make_divisible(length * split_ratio, batch_size)
    length_train = int(_make_divisible(length * split_ratio, batch_size))

    if train_include_test:
        x_train, y_train = x[:], y[:]
        x_test, y_test = x[length_train:], y[length_train:]

    else:
        x_train, y_train = x[:length_train], y[:length_train]
        x_test, y_test = x[length_train:], y[length_train:]

    return (x_train, y_train, x_test, y_test)

def generate_dataset_predict(x: ndarray, x_mask: ndarray, window: int, batch_size: int = 200,
                             enable_window_nomalization: bool = False) -> (ndarray, ndarray):

    if len(x.shape) != 2:
        raise Exception

    if len(x_mask.shape) != 1:
        raise Exception

    if not len(x) == len(x_mask):
        raise Exception

    if window < 1:
        raise Exception

    if batch_size < 2:
        raise Exception

    x, x_mask = _generate_window(x, x_mask, window=window, exclude_nan=True)

    if enable_window_nomalization:
        x = window_nomalization(x)

    return (x, x_mask)
