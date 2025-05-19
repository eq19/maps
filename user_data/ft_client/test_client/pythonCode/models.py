import tensorflow as tf
from iree.compiler.tools.tf import tf_saved_model_to_stablehlo
from iree.compiler.api import compile_str
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
        stablehlo = tf_saved_model_to_stablehlo(
            saved_model_dir="add_model",
            exported_names=["serving_default"]
        )

        compile_str(
            stablehlo,
            input_type="stablehlo_xla",
            target_backends=["llvm-cpu"],
            output_file="add_module.vmfb"
        )

    print("Compiled successfully to add_module.vmfb")

if __name__ == "__main__":
    export_model()
