import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"  # Critical for CPU-only environments

import tensorflow as tf
from iree.compiler.tools import compile_file

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
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

    # Direct compilation
    compile_file(
        "add_model",
        input_type="tf_saved_model",
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        exported_names=["serving_default"]
    )

    print("Successfully compiled to add_module.vmfb")

if __name__ == "__main__":
    export_model()
