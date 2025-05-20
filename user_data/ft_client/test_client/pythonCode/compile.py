import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"  # Disable GPU support
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"    # Save intermediate files for debugging

import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
        tf.TensorSpec([None], tf.float32),  # Dynamic shape
    ])
    def add(self, a, b):
        return a + b

def export_model():
    # Save the model with dynamic shapes
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
            # Dynamic shape support
            "--iree-flow-enable-dynamic-shaping",
            "--iree-stream-resource-index-bits=32",
            
            # Required optimizations
            "--iree-flow-enable-pad-handling",
            "--iree-input-demote-i64-to-i32",
            
            # Additional flags for dynamic shapes
            "--iree-opt-const-eval=false",
            "--iree-opt-const-expr-hoisting=false"
        ]
    )

    print("Successfully compiled dynamic shape model to add_module.vmfb")

if __name__ == "__main__":
    export_model()
