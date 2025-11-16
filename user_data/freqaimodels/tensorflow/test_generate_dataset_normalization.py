import numpy
import generate_dataset

x = numpy.arange(27, dtype=numpy.float64).reshape((3, 3, 3))
print(x)

y = generate_dataset.window_nomalization(x, version='v1')
print(y)

y = generate_dataset.window_nomalization(x, version='v2')
print(y)

y = generate_dataset.window_nomalization(x, version='absolute_first')
print(y)

y = generate_dataset.window_nomalization(x, version='absolute_previous')
print(y)

y = generate_dataset.window_nomalization(x, version='minmax')
print(y)

y = generate_dataset.window_nomalization(x, version='minmax_scale')
print(y)

y = generate_dataset.window_nomalization(x, version='minmax_scale_range')
print(y)

y = generate_dataset.window_nomalization(x, version='zscore')
print(y)

y = generate_dataset.window_nomalization(x, version='zscore_robust')
print(y)
