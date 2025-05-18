import tensorflow as tf
from iree.compiler.tools import tf as iree_tf

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    iree_tf.compile_saved_model(
        saved_model_dir="add_model",
        output_file="add_model.mlir",
        import_only=True
    )
