import numpy
from sklearn.ensemble import RandomForestClassifier
from load_data import load_data

x_train, y_train, x_test, y_test = load_data()
print(x_train.shape, x_test.shape)

x_train = numpy.squeeze(x_train)
x_test = numpy.squeeze(x_test)
print(x_train.shape, x_test.shape)

model = RandomForestClassifier()
model.fit(x_train, y_train)

print(f'accuracy_train: {model.score(x_train, y_train)}')
print(f'accuracy_test: {model.score(x_test, y_test)}')
