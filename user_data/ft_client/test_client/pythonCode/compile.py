import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"  # Still important for CPU targets

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
    try:
        model = AddModule()
        tf.saved_model.save(
            model,
            "add_model",
            tags=["serve"],
            signatures={
                "serving_default": model.add.get_concrete_function(
                    tf.TensorSpec([None], tf.float32),
                    tf.TensorSpec([None], tf.float32))
            }
        )
        
        # Double verification
        loaded = tf.saved_model.load("add_model", tags=["serve"])
        assert "serving_default" in loaded.signatures

        iree_tf_compiler.compile_saved_model(
            "add_model",
            exported_names=["serving_default"],
            output_file="add_module.vmfb",
            target_backends=["llvm-cpu"],
            import_type="SIGNATURE_DEF",
            saved_model_tags="serve"
        )
        print("Compilation successful")
    except Exception as e:
        print(f"Failed: {str(e)}")
        raise

if __name__ == "__main__":
    export_model()
