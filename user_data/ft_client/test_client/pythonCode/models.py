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
    tf.saved_model.save(
        model,
        export_dir="add_model",
        signatures=model.add.get_concrete_function()
    )

if __name__ == "__main__":
    export_model()
