import tensorflow as tf

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    tf.saved_model.save(model, "add_model", signatures=model.add)
