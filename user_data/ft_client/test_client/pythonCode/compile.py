import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"  # For debugging

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([10], tf.float32),  # Fixed shape instead of [None]
        tf.TensorSpec([10], tf.float32),  # Fixed shape instead of [None]
    ])
    def add(self, a, b):
        return a + b

def export_model():
    # Save model
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    # Compile with additional legalization passes
    iree_tf_compiler.compile_saved_model(
        "add_model",
        exported_names=["serving_default"],
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        import_type="SIGNATURE_DEF",
        saved_model_tags={"serve"},
        extra_args=[
            "--iree-flow-enable-padding",
            "--iree-flow-demote-i64-to-i32",
            "--iree-llvmcpu-enable-pad-handling"
        ]
    )

    print("Successfully compiled to add_module.vmfb")

if __name__ == "__main__":
    export_model()
