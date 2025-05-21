import os
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["MLIR_CRASH_REPRODUCER_DIRECTORY"] = "1"

import tensorflow as tf
from iree.compiler.tools import tf as tfc

class ComplexModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([13], tf.float32),
    ])
    def compute(self, a):
        # Pure complex number operation
        return tf.complex(a, a)  # a + ai

def export_model():
    model = ComplexModule()
    tf.saved_model.save(
        model,
        export_dir="complex_model",
        signatures={"serving_default": model.compute}
    )

    tfc.compile_saved_model(
        "complex_model",
        saved_model_tags={"serve"},
        import_type="SIGNATURE_DEF",
        target_backends=["llvm-cpu"],
        output_file="complex_module.vmfb",
        exported_names=["serving_default"],
        extra_args=[
            "--iree-input-demote-i64-to-i32",
            "--iree-llvmcpu-target-cpu=generic"
        ]
    )
    print("Model compiled to complex_module.vmfb")

if __name__ == "__main__":
    export_model()
