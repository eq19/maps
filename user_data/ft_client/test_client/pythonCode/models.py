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
    
    # Option 1: Try standard pipeline first
    try:
        mlir_text = tf.mlir.experimental.convert_function(
            concrete_fn,
            pass_pipeline='tf-standard-pipeline'
        )
        
        # Convert to StableHLO format if needed
        if 'tf.' in mlir_text:  # If output contains TensorFlow ops
            import subprocess
            with open("temp_tf.mlir", "w") as f:
                f.write(mlir_text)
            
            # Convert TF dialect to StableHLO
            subprocess.run([
                "mlir-opt", "temp_tf.mlir",
                "--tf-to-hlo-pipeline",
                "-o", "add_model_stablehlo.mlir"
            ], check=True)
            
            with open("add_model_stablehlo.mlir", "r") as f:
                mlir_text = f.read()
    
    except Exception as e:
        print(f"Standard pipeline failed: {e}")
        # Option 2: Fallback to XLA export
        try:
            from tensorflow.compiler.mlir.tensorflow import translate
            mlir_text = translate.tf_function_to_mlir(
                concrete_fn,
                pass_pipeline='tf-standard-pipeline'
            )
        except Exception as e:
            print(f"XLA export failed: {e}")
            raise

    # Save final MLIR
    with open("add_model_stablehlo.mlir", "w") as f:
        f.write(mlir_text)
    
    print(f"Successfully exported to: add_model_stablehlo.mlir")

if __name__ == "__main__":
    export_model()
