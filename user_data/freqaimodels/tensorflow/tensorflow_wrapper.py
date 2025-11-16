import os

xla_flags = []
if False:
    xla_flags.append('--xla_dump_to=/tmp/tensorflow/xla')
    xla_flags.append('--xla_dump_hlo_as_text')

os.environ['XLA_FLAGS'] = ' '.join(xla_flags)
print(f'XLA_FLAGS=\'{os.environ["XLA_FLAGS"]}\'')


tf_xla_flags = []
tf_xla_flags.append('--tf_xla_auto_jit=2')
if False:
    tf_xla_flags.append('--tf_xla_cpu_global_jit')
if False:
    # ISSUE https://github.com/tensorflow/tensorflow/issues/57649
    tf_xla_flags.append('--tf_xla_persistent_cache_directory=/tmp/tensorflow/cache')
if False:
    tf_xla_flags.append('--tf_xla_clustering_debug')

os.environ['TF_XLA_FLAGS'] = ' '.join(tf_xla_flags)
print(f'TF_XLA_FLAGS=\'{os.environ["TF_XLA_FLAGS"]}\'')

if False:
    os.environ['TF_DUMP_GRAPH_PREFIX'] = '/tmp/tensorflow/graph'
    print(f'TF_DUMP_GRAPH_PREFIX=\'{os.environ["TF_DUMP_GRAPH_PREFIX"]}\'')

import tensorflow

if not callable(getattr(tensorflow, 'jit', None)):
    def jit(*args, **kwargs):
        if 'jit_compile' not in kwargs:
            kwargs['jit_compile'] = True

        if 'autograph' not in kwargs:
            kwargs['autograph'] = False

        if 'reduce_retracing' not in kwargs and False:
            kwargs['reduce_retracing'] = True

        return tensorflow.function(*args, **kwargs)

    tensorflow.jit = jit

else:
    raise Exception

tensorflow.numpy = tensorflow.experimental.numpy

if False:
    tensorflow.numpy.experimental_enable_numpy_behavior()

# https://stackoverflow.com/questions/20926909/python-check-if-function-exists-without-running-it
if not callable(getattr(tensorflow.numpy, 'nan_to_num', None)):
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/lib/type_check.py#L404-L521
    def nan_to_num(x, nan=0., posinf=None, neginf=None):
        posinf = tensorflow.numpy.inf
        neginf = -tensorflow.numpy.inf
        x = tensorflow.numpy.where(tensorflow.numpy.isnan(x), nan, x)
        x = tensorflow.numpy.where(tensorflow.numpy.isposinf(x), posinf, x)
        x = tensorflow.numpy.where(tensorflow.numpy.isneginf(x), neginf, x)
        return x

    tensorflow.numpy.nan_to_num = nan_to_num

else:
    raise Exception

if not callable(getattr(tensorflow.numpy, 'rollaxis', None)):
    # https://github.com/numpy/numpy/blob/main/numpy/core/numeric.py#L1245-L1332
    @tensorflow.jit
    def rollaxis(a, axis, start=0):
        n = len(a.shape)
        # axis = normalize_axis_index(axis, n)
        if start < 0:
            start += n
        if not (0 <= start < n + 1):
            msg = "'%s' arg requires %d <= %s < %d, but %d was passed in"
            raise Exception(msg % ('start', -n, 'start', n + 1, start))
        if axis < start:
            start -= 1
        if axis == start:
            return a[...]
        axes = list(range(0, n))
        axes.remove(axis)
        axes.insert(start, axis)
        return tensorflow.numpy.transpose(a, axes)

    tensorflow.numpy.rollaxis = rollaxis

else:
    raise Exception

# https://numpy.org/doc/stable/reference/constants.html#numpy.nan
if getattr(tensorflow.numpy, 'nan', None) is None:
    import numpy
    tensorflow.numpy.nan = numpy.nan

else:
    raise Exception
