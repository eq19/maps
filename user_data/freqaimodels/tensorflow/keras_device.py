import os
import tensorflow

def scope():
    # if 'POPLAR_SDK_ENABLED' in os.environ:
        # from tensorflow.python import ipu
        # ipu_config = ipu.config.IPUConfig()
        # ipu_config.auto_select_ipus = 1
        # ipu_config.configure_ipu_system()
        # strategy = ipu.ipu_strategy.IPUStrategy()
        # return strategy.scope()

    gpu = tensorflow.config.list_logical_devices('GPU')

    if len(gpu) > 1:
        strategy = tensorflow.distribute.MirroredStrategy(gpu)
        return strategy.scope()

    elif len(gpu) == 1:
        return tensorflow.device('GPU')

    return tensorflow.device('CPU')
