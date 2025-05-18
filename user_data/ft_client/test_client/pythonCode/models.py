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
    
    # Save as SavedModel
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures=model.add.get_concrete_function()
    )
    
    # Convert to MLIR
    converter = tf.lite.TFLiteConverter.from_saved_model("add_model")
    converter.target_spec.supported_ops = [
        tf.lite.OpsSet.TFLITE_BUILTINS,
        tf.lite.OpsSet.SELECT_TF_OPS
    ]
    tflite_model = converter.convert()
    
    # Save MLIR (TFLite flatbuffer)
    with open('add_model.mlir', 'wb') as f:
        f.write(tflite_model)

if __name__ == "__main__":
    export_model()
