import tensorflow as tf

def export_model():
    @tf.function(
        input_signature=[
            tf.TensorSpec([None], tf.float32),
            tf.TensorSpec([None], tf.float32),
        ]
    )
    def add(a, b):
        return a + b

    tf.saved_model.save(add, "add_model")
