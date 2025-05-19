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
    mlir_bytes = compile_saved_model(
        "add_model",
        output_format="mlir-ir",
        target_backends=["llvm-cpu"],
        import_only=True
    )
    with open("add_model.mlir", "wb") as f:
        f.write(mlir_bytes)
    
    # 3. Compile to VM FlatBuffer format
    compile_saved_model(
        "add_model",
        output_file="add_module.vmfb",
        target_backends=["llvm-cpu"],
        import_only=True  # Only imports to MLIR without full compilation
    )
    
    print("Successfully exported:")
    print("- MLIR: add_model.mlir")
    print("- Compiled module: add_module.vmfb")

if __name__ == "__main__":
    export_model()
