import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["MLIR_CRASH_REPRODUCER_DIRECTORY"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"

import tensorflow as tf
from iree.compiler.tools import tf as tfc

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([13], tf.float32),
    ])
    def add(self, a):
        # Return a dictionary with real and imag parts
        return {"result": tf.stack([a, a], axis=1)}  # Shape: [13, 2]

def export_model():
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    tfc.compile_saved_model(
        "add_model",
        saved_model_tags={"serve"},
        import_type="SIGNATURE_DEF",
        target_backends=["llvm-cpu"],
        output_file="add_module.vmfb",
        exported_names=["serving_default"],
        extra_args=[
            "--iree-input-demote-i64-to-i32",
            "--iree-flow-enable-pad-handling",
            "--iree-llvmcpu-target-cpu=generic",
            "--iree-hal-dump-output-formats=full"  # For debugging
        ]
    )

if __name__ == "__main__":
    export_model()
