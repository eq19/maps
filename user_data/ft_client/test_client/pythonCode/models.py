import tensorflow as tf
import os
import subprocess

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

    # Export to StableHLO using CLI
    result = subprocess.run([
        "tensorflow-export-stablehlo",
        "--saved_model_dir=add_model",
        "--output_mlir=add_model.mlir"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("Export to StableHLO failed:")
        print(result.stderr)
    else:
        print("Exported to add_model.mlir successfully.")
