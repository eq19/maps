import tensorflow as tf
from iree.compiler.tools import tf as iree_tf_compiler
from iree.compiler.tools import compile_str
from iree.compiler.ir import Context

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    # Save the model
    model = AddModule()
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )

    # Convert to StableHLO and compile
    with Context():
        # Step 1: Get MLIR in StableHLO dialect
        mlir_text = iree_tf_compiler.compile_saved_model(
            "add_model",
            import_type="STABLEHLO",
            exported_names=["serving_default"],
            output_format="mlir-text"
        )

        # Step 2: Compile to IREE VM bytecode
        compile_str(
            mlir_text,
            input_type="stablehlo",
            target_backends=["llvm-cpu"],
            output_file="add_module.vmfb"
        )

    print("Compiled successfully to add_module.vmfb")

if __name__ == "__main__":
    export_model()
