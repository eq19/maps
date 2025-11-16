from tensorflow_wrapper import tensorflow

class RelativePosition(tensorflow.keras.layers.Layer):
    def __init__(self):
        super(RelativePosition, self).__init__()

    def build(self, input_shape):
        n = input_shape[1]
        x, y = tensorflow.meshgrid(tensorflow.range(n), tensorflow.range(n))
        self.mask = tensorflow.Variable(initial_value=tensorflow.math.greater(x, y), trainable=False)

    # @tensorflow.jit
    def _f(self, a):
        x, y = tensorflow.meshgrid(a, a)
        x = tensorflow.math.subtract(x, y)
        x = tensorflow.boolean_mask(x, self.mask)
        # x = tensorflow.ensure_shape(x, [self.n * (self.n - 1) // 2])
        return x

    # @tensorflow.jit
    def call(self, inputs):
        x = tensorflow.map_fn(fn=self._f, elems=inputs)
        n = inputs.shape[1]
        x = tensorflow.ensure_shape(x, [inputs.shape[0], n * (n - 1) // 2])
        return x

@tensorflow.jit
def relative_position(inputs):
    n = inputs.shape[-1]
    x_mask, y_mask = tensorflow.meshgrid(tensorflow.range(n), tensorflow.range(n))
    mask = tensorflow.math.greater(x_mask, y_mask)
    x, y = tensorflow.meshgrid(inputs, inputs)
    x = tensorflow.math.subtract(x, y)
    x = tensorflow.boolean_mask(x, mask)
    x = tensorflow.ensure_shape(x, [n * (n - 1) // 2])
    return x

class SimpleDense(tensorflow.keras.layers.Layer):
    def __init__(self, units=32):
        super(SimpleDense, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(name='w', shape=(input_shape[-1], self.units),
                                 initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight(name='b', shape=(self.units,),
                                 initializer='random_normal',
                                 trainable=True)

    def call(self, inputs):
        return tensorflow.matmul(inputs, self.w) + self.b

class DenseNotTainable(tensorflow.keras.layers.Layer):
    def __init__(self, units):
        super(DenseNotTainable, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(name='w', shape=(input_shape[-1], self.units),
                                 initializer='random_normal',
                                 trainable=False)
        self.b = self.add_weight(name='b', shape=(self.units,),
                                 initializer='random_normal',
                                 trainable=False)

    def call(self, inputs):
        return tensorflow.matmul(inputs, self.w) + self.b

class DenseAverage(tensorflow.keras.layers.Layer):
    def __init__(self, units=32):
        super(DenseAverage, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(name='w', shape=(input_shape[-1], self.units),
                                 initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight(name='b', shape=(self.units,),
                                 initializer='random_normal',
                                 trainable=True)

    def call(self, inputs):
        x = tensorflow.matmul(inputs, self.w)
        s = tensorflow.reduce_sum(self.w, axis=0)
        x /= s
        x += self.b
        return x

class DenseBatchNormalization(tensorflow.keras.layers.Layer):
    def __init__(self, units=32):
        super(DenseBatchNormalization, self).__init__()
        self.units = units
        self.bn = tensorflow.keras.layers.BatchNormalization()

    def build(self, input_shape):
        self.w = self.add_weight(name='w', shape=(input_shape[-1], self.units),
                                 initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight(name='b', shape=(self.units,),
                                 initializer='random_normal',
                                 trainable=True)

    def call(self, inputs):
        w2 = self.bn(self.w)
        x = tensorflow.matmul(inputs, w2)
        x += self.b
        return x

class DenseBlock(tensorflow.keras.layers.Layer):
    def __init__(self):
        super(DenseBlock, self).__init__()
        self.layer_1 = tensorflow.keras.layers.Dense(2)
        self.layer_2 = tensorflow.keras.layers.Activation('relu')
        self.layer_3 = tensorflow.keras.layers.Dense(256)
        self.layer_4 = tensorflow.keras.layers.BatchNormalization()
        self.layer_5 = tensorflow.keras.layers.Activation('relu')
        self.layer_6 = tensorflow.keras.layers.Dense(256)
        self.layer_7 = tensorflow.keras.layers.BatchNormalization()
        self.layer_8 = tensorflow.keras.layers.Activation('relu')
        self.layer_9 = tensorflow.keras.layers.Dense(2)

    def call(self, inputs):
        x = self.layer_1(inputs)
        x = self.layer_2(x)
        x = self.layer_3(x)
        x = self.layer_4(x)
        x = self.layer_5(x)
        x = self.layer_6(x)
        x = self.layer_7(x)
        x = self.layer_8(x)
        x = self.layer_9(x)
        return x

class DenseBlockSkip(tensorflow.keras.layers.Layer):
    def __init__(self, n, n_internal):
        super(DenseBlockSkip, self).__init__()
        self.layer_1 = tensorflow.keras.layers.BatchNormalization()
        self.layer_2 = tensorflow.keras.layers.Activation('relu')
        self.layer_3 = tensorflow.keras.layers.Dense(n_internal)
        self.layer_4 = tensorflow.keras.layers.BatchNormalization()
        self.layer_5 = tensorflow.keras.layers.Activation('relu')
        self.layer_6 = tensorflow.keras.layers.Dense(n_internal)
        self.layer_7 = tensorflow.keras.layers.BatchNormalization()
        self.layer_8 = tensorflow.keras.layers.Activation('relu')
        self.layer_9 = tensorflow.keras.layers.Dense(n)

    def call(self, inputs):
        x = self.layer_1(inputs)
        x = self.layer_2(x)
        x = self.layer_3(x)
        x = self.layer_4(x)
        x = self.layer_5(x)
        x = self.layer_6(x)
        x = self.layer_7(x)
        x = self.layer_8(x)
        x = self.layer_9(x)
        x += inputs
        return x

class CustomModel(tensorflow.keras.Model):
    def __init__(self):
        super(CustomModel, self).__init__()
        self.layer_1 = tensorflow.keras.layers.Conv1D(16, kernel_size=200)
        self.layer_2 = tensorflow.keras.layers.Flatten()
        self.layer_3 = tensorflow.keras.layers.RelativePosition(n=16)
        self.layer_4 = tensorflow.keras.layers.Flatten()
        self.layer_5 = tensorflow.keras.layers.Dense(64)
        self.layer_6 = tensorflow.keras.layers.Activation('relu')
        self.layer_7 = tensorflow.keras.layers.BatchNormalization()
        self.layer_8 = tensorflow.keras.layers.Dense(2)
        self.layer_9 = tensorflow.keras.layers.Activation('softmax')

    def call(self, inputs):
        x = self.layer_1(inputs)
        x = self.layer_2(x)
        x = self.layer_3(x)
        x = self.layer_4(x)
        x = self.layer_5(x)
        x = self.layer_6(x)
        x = self.layer_7(x)
        x = self.layer_8(x)
        x = self.layer_9(x)
        return x

def create_model(input_shape: list, output_class: int) -> tensorflow.keras.models.Model:
    if output_class < 1:
        raise Exception

    inputs = tensorflow.keras.layers.Input(shape=input_shape)

    '''
    x = tensorflow.keras.layers.Flatten()(inputs)
    b1 = DenseBlock()(x)
    b2 = DenseBlock()(x)
    b3 = DenseBlock()(x)
    b4 = DenseBlock()(x)
    b5 = DenseBlock()(x)
    b6 = DenseBlock()(x)
    b7 = DenseBlock()(x)
    b8 = DenseBlock()(x)
    b9 = DenseBlock()(x)
    b10 = DenseBlock()(x)
    b11 = DenseBlock()(x)
    x = tensorflow.keras.layers.Concatenate()([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11])
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    x = tensorflow.keras.layers.Activation('softmax')(x)
    '''

    '''
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    x = tensorflow.keras.layers.Activation('softmax')(x)
    '''

    '''
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(256)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    x = tensorflow.keras.layers.Activation('softmax')(x)
    '''

    '''
    n = 4
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(output_class * n ** 4)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n ** 3)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n ** 2)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    '''
    n = 4
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = DenseNotTainable(output_class * n ** 4)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = DenseNotTainable(output_class * n ** 3)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = DenseNotTainable(output_class * n ** 2)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = DenseNotTainable(output_class * n)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    '''
    n = 4
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(output_class * n ** 4, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n ** 3, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n ** 2, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class * n, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    '''
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = DenseNotTainable(128)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = DenseNotTainable(128)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = DenseNotTainable(128)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    n = 128
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(n, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(n, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(n, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(n, trainable=False)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)

    '''
    x = tensorflow.keras.layers.GRU(64)(inputs)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(16)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    '''
    n = 128
    n_internal = 64
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(n)(x)
    x = DenseBlockSkip(n, n_internal)(x)
    x = DenseBlockSkip(n, n_internal)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    '''

    model = tensorflow.keras.models.Model(inputs=inputs, outputs=x)

    # for i in model.layers[:-1]:
    #     i.trainable = False

    '''
    x = tensorflow.keras.layers.Flatten()(inputs)
    x = tensorflow.keras.layers.Dense(2)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(128)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(16)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    x = tensorflow.keras.layers.Activation('softmax')(x)
    '''

    '''
    x = tensorflow.keras.layers.Conv1D(32, kernel_size=3)(inputs)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.MaxPooling1D(pool_size=2)(x)
    x = tensorflow.keras.layers.Conv1D(64, kernel_size=3)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.MaxPooling1D(pool_size=2)(x)
    x = tensorflow.keras.layers.Conv1D(128, kernel_size=3)(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.MaxPooling1D(pool_size=2)(x)
    x = tensorflow.keras.layers.Flatten()(x)
    x = tensorflow.keras.layers.Dense(16)(x)
    x = tensorflow.keras.layers.BatchNormalization()(x)
    x = tensorflow.keras.layers.Activation('relu')(x)
    x = tensorflow.keras.layers.Dense(output_class)(x)
    x = tensorflow.keras.layers.Activation('softmax')(x)
    '''

    '''
    x = Flatten()(inputs)
    x = SimpleDense(1250)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SimpleDense(1250)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SimpleDense(2)(x)
    x = Activation('softmax')(x)
    model = Model(inputs=inputs, outputs=x)
    '''

    '''
    x = Flatten()(inputs)
    x = DenseAverage(1250)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = DenseAverage(1250)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SimpleDense(2)(x)
    x = Activation('softmax')(x)
    model = Model(inputs=inputs, outputs=x)
    '''

    '''
    x = Flatten()(inputs)
    x = DenseBatchNormalization(2048)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = DenseBatchNormalization(64)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = SimpleDense(2)(x)
    x = Activation('softmax')(x)
    model = Model(inputs=inputs, outputs=x)
    '''

    return model
