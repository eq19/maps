import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"  # Disable GPU support
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"    # Save intermediate files

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
    ])
    def add(self, a, b):
        # Explicit broadcasting to help the compiler
        a = tf.broadcast_to(a, tf.maximum(tf.shape(a)[0], tf.shape(b)[0]))
        b = tf.broadcast_to(b, tf.maximum(tf.shape(a)[0], tf.shape(b)[0]))
        return a + b

def export_model():
    # Save the model with dynamic shapes
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    # Compile with optimized settings for dynamic shapes
    iree_tf_compiler.compile_saved_model(
        "add_model",
        exported_names=["serving_default"],
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        import_type="SIGNATURE_DEF",
        saved_model_tags={"serve"},
        extra_args=[
            # Essential for dynamic shapes
            "--iree-input-demote-i64-to-i32",
            "--iree-flow-enable-pad-handling",
            
            # Improved dynamic shape support
            "--iree-stream-resource-index-bits=32",
            
            # Disable optimizations that conflict with dynamic shapes
            "--iree-opt-const-expr-hoisting=false",
            "--iree-opt-const-eval=false",
            
            # New in IREE 3.5+ for broadcasting
            "--iree-flow-enable-fuse-padding-into-linalg"
        ]
    )

    print("Successfully compiled dynamic shape model")

if __name__ == "__main__":
    export_model()
