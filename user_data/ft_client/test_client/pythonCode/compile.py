import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    # Save model (corrected parentheses)
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={
            "serving_default": model.add.get_concrete_function(
                tf.TensorSpec([None], tf.float32),
                tf.TensorSpec([None], tf.float32)
            )  # This parenthesis was missing
        }
    )

    # Compile with IREE
    iree_tf_compiler.compile_saved_model(
        "add_model",
        exported_names=["serving_default"],
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        import_type="SIGNATURE_DEF",
        saved_model_tags={"serve"}
    )

    print("Successfully compiled to add_module.vmfb")

if __name__ == "__main__":
    export_model()
