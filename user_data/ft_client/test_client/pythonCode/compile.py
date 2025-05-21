import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["MLIR_CRASH_REPRODUCER_DIRECTORY"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"  # For debugging

import tensorflow as tf
from iree.compiler.tools import tf as tfc

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([10], tf.float32),  # Single input tensor
    ])
    def add(self, a):
        # Return complex value a + ia
        return tf.complex(a, a)  # Creates complex numbers with real=a, imag=a

def export_model():
    # Save model
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    # Compile with minimal required flags
    tfc.compile_saved_model(
        "add_model",
        saved_model_tags={"serve"},
        import_type="SIGNATURE_DEF",
        target_backends=["llvm-cpu"],
        output_file="add_module.vmfb",
        exported_names=["serving_default"],
        extra_args=[
            # Essential flags for IREE 3.5.0rc
            "--iree-input-demote-i64-to-i32",
            "--iree-flow-enable-pad-handling",
            "--iree-llvmcpu-target-cpu=generic"
        ]
    )

    print("Successfully compiled model")

if __name__ == "__main__":
    export_model()
