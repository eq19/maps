import numpy
import indicator

x = numpy.arange(27, dtype=numpy.float64)
print(x)
y = indicator.tensorflow_numpy_mean(x, where=(x < 9))
print(y)
