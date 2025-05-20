import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),  # Dynamic dimension
        tf.TensorSpec([None], tf.float32),  # Dynamic dimension
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

    # Compile with UPDATED dynamic shape support
    iree_tf_compiler.compile_saved_model(
        "add_model",
        exported_names=["serving_default"],
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        import_type="SIGNATURE_DEF",
        saved_model_tags={"serve"},
        extra_args=[
            # Current dynamic shape support in IREE 3.5.0+
            "--iree-input-demote-i64-to-i32",
            "--iree-flow-enable-pad-handling",
            
            # New way to handle dynamic shapes
            "--iree-stream-resource-index-bits=32",
            "--iree-opt-const-expr-hoisting=false",
            
            # Enable dynamic dim support
            "--iree-opt-const-eval=false"
        ]
    )

    print("Successfully compiled dynamic shape model")

if __name__ == "__main__":
    export_model()
