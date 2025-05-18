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
    
    # 1. Save as SavedModel
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures={"serving_default": model.add}
    )
    
    # 2. Convert to MLIR using public API
    mlir_text = tf.mlir.experimental.convert_function(
        model.add.get_concrete_function(),
        pass_pipeline='tf-standard-pipeline'
    )
    
    # 3. Save MLIR
    with open("add_model.mlir", "w") as f:
        f.write(mlir_text)

if __name__ == "__main__":
    export_model()
