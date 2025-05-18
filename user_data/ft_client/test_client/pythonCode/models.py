import tensorflow as tf
from stablehlo.experimental.tensorflow import export_saved_model

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    # Save the model
    model = AddModule()
    tf.saved_model.save(model, "add_model", signatures=model.add)

    # Export to StableHLO using Python API
    export_saved_model("add_model", "add_model.mlir")
