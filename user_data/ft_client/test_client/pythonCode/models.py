import tensorflow as tf
from iree.compiler.tf import compile_module  # From iree-tools-tf

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    
    # 1. Convert directly to IREE-compatible format
    compiled_module = compile_module(
        model,
        target_backends=["llvm-cpu"],
        output_file="add_module.vmfb",  # Direct to final compiled format
        input_type="auto",  # Automatically detect input type
        export_only=False  # Perform full compilation
    )
    
    # 2. Also save the intermediate MLIR (optional)
    mlir_text = compile_module(
        model,
        target_backends=["llvm-cpu"],
        output_file=None,  # Get MLIR as string
        input_type="auto",
        export_only=True  # Only export to MLIR
    )
    with open("add_model.mlir", "w") as f:
        f.write(mlir_text)
    
    print("Successfully compiled to:")
    print("- Binary: add_module.vmfb")
    print("- MLIR: add_model.mlir")

if __name__ == "__main__":
    export_model()
