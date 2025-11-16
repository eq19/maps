import numpy
import indicator

x = numpy.arange(27, dtype=numpy.float64)
print(x)

y = indicator.tensorflow_shift(x, 2)
print(y)

y = indicator.tensorflow_shift(x, 0)
print(y)

y = indicator.tensorflow_shift(x, -2)
print(y)

y = indicator.tensorflow_shift(x, 2, axis=0)
print(y)

y = indicator.tensorflow_shift(x, 0, axis=0)
print(y)

y = indicator.tensorflow_shift(x, -2, axis=0)
print(y)

x = numpy.arange(27, dtype=numpy.float64).reshape((3, 3, 3))
print(x)

y = indicator.tensorflow_shift(x, 1, axis=1)
print(y)

y = indicator.tensorflow_shift(x, 0, axis=1)
print(y)

y = indicator.tensorflow_shift(x, -1, axis=1)
print(y)

y = indicator.tensorflow_shift(x, 2, axis=1)
print(y)

y = indicator.tensorflow_shift(x, 0, axis=1)
print(y)

y = indicator.tensorflow_shift(x, -2, axis=1)
print(y)
