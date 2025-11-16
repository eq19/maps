import numpy
import indicator

x = numpy.arange(27, dtype=numpy.float64).reshape((3, 3, 3))
print(x)
y = indicator._generate_window(x=x, window=2, x_mask=None)
print(y)

x = numpy.arange(18, dtype=numpy.float64).reshape((9, 2))
print(x)
y = indicator._generate_window(x=x, window=2, x_mask=None)
print(y)

x = numpy.full((9, 2), numpy.nan)
x[0] = [1, 2]
x[1] = [2, 3]
print(x)
y = indicator._generate_window(x=x, window=2, x_mask=None)
print(y)
