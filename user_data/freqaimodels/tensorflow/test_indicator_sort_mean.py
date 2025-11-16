import numpy
import indicator

x = numpy.arange(27, dtype=numpy.float64)
print(x)

y = indicator.sort_mean(x, 9, 18)
print(y)

x = numpy.arange(27, dtype=numpy.float64)
print(x)

y = indicator.profit_long(x, 9)
print(y)

y = indicator.sort_mean(y, 3, 6)
print(y)
