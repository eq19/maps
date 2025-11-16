import numpy
import indicator

x = numpy.arange(27, dtype=numpy.float64)
print(x)
y = indicator.profit_long(x, 2)
print(y)

x = numpy.arange(3, dtype=numpy.float64) + 1
print(x)
y = indicator.profit_long(x, 2)
print(y)
