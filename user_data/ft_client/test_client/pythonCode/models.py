import tensorflow as tf

class AddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([None], tf.float32),
        tf.TensorSpec([None], tf.float32),
    ])
    def add(self, a, b):
        return a + b

def export_model():
    model = AddModule()
    concrete_fn = model.add.get_concrete_function()
    
    # 1. Save as SavedModel (optional, for reference)
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )
    
    # 2. Convert directly to StableHLO format
    mlir_text = tf.mlir.experimental.convert_function(
        concrete_fn,
        pass_pipeline='tf-stablehlo-pipeline'  # Changed to StableHLO pipeline
    )
    
    # 3. Save MLIR
    with open("add_model_stablehlo.mlir", "w") as f:
        f.write(mlir_text)
    
    print("Successfully exported to StableHLO MLIR: add_model_stablehlo.mlir")

if __name__ == "__main__":
    export_model()
