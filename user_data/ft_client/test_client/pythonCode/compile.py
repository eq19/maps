import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
    ])
    def add(self, a, b):
        # Correct broadcasting implementation
        max_length = tf.maximum(tf.shape(a)[0], tf.shape(b)[0])
        # Create a proper shape tensor [max_length] instead of scalar max_length
        output_shape = tf.stack([max_length])
        a_broadcast = tf.broadcast_to(a, output_shape)
        b_broadcast = tf.broadcast_to(b, output_shape)
        return a_broadcast + b_broadcast

def export_model():
    # Save model
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    # Compile with dynamic shape support
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
            
            # Dynamic shape support
            "--iree-stream-resource-index-bits=32",
            
            # Disable problematic optimizations
            "--iree-opt-const-expr-hoisting=false",
            "--iree-opt-const-eval=false",
            
            # Improved broadcast handling
            "--iree-flow-enable-fuse-padding-into-linalg"
        ]
    )

    print("Successfully compiled dynamic shape model")

if __name__ == "__main__":
    export_model()
