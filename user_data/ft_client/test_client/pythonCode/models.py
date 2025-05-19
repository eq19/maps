import tensorflow as tf
from iree.compiler.tf import compile_saved_model  # From iree-tools-tf

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    
    # 1. Save as a SavedModel
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )
    
    # 2. Compile directly from the SavedModel directory to VMFB
    compile_saved_model(
        saved_model_dir="add_model",
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        exported_names=["serving_default"]
    )
    
    print("Successfully compiled to: add_module.vmfb")

if __name__ == "__main__":
    export_model()
