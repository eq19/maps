# models.py

import tensorflow as tf
import pathlib
from iree.compiler.tools.tf import tf_saved_model_to_stablehlo
from iree.compiler import compile_str

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    export_dir = "add_model"
    vmfb_file = "add_module.vmfb"

    tf.saved_model.save(
        model,
        export_dir=export_dir,
        signatures={"serving_default": model.add}
    )

    # Convert to StableHLO MLIR
    mlir_str = tf_saved_model_to_stablehlo(
        export_dir,
        exported_names=["serving_default"]
    )

    # Compile to VMFB
    vmfb_binary = compile_str(
        mlir_str,
        target_backends=["llvm-cpu"],
        input_type="stablehlo_xla"
    )

    # Write to file
    pathlib.Path(vmfb_file).write_bytes(vmfb_binary)
    print("Success: VMFB written to", vmfb_file)

if __name__ == "__main__":
    export_model()
