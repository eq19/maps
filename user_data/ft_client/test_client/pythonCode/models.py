import subprocess
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
    
    # 1. First save as SavedModel (required by compile_saved_model)
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )
    
    # 2. For MLIR export, use import_only and output_format
    subprocess.run([
        "iree-import-tf",
        "--tf-savedmodel-exported-names=serving_default",
        "--output-format=mlir-ir",
        "add_model", "-o", "add_model.mlir"
    ], check=True)
    
    # 3. Compile to VM FlatBuffer format
    compile_saved_model(
        import_only=True,
        saved_model_dir="add_model",
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        exported_names=["serving_default"]
    )
    
    print("Successfully exported:")
    print("- MLIR: add_model.mlir")
    print("- Compiled module: add_module.vmfb")

if __name__ == "__main__":
    export_model()
