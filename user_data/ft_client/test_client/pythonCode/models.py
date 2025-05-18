import tensorflow as tf
from tensorflow.python.compiler.mlir import tf2xla

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    
    # Save as SavedModel
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures=model.add.get_concrete_function()
    )
    
    # Convert to MLIR and save
    mlir_str = tf2xla.experimental.export_saved_model_to_mlir(
        "add_model",
        exported_names=["serving_default"],
        show_debug_info=False
    )
    
    with open("add_model.mlir", "w") as f:
        f.write(mlir_str)

if __name__ == "__main__":
    export_model()
