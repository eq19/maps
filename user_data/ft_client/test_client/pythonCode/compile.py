import os
os.environ["IREE_LLVMAOT_DISABLE_NVPTX"] = "1"
os.environ["MLIR_CRASH_REPRODUCER_DIRECTORY"] = "1"
os.environ["IREE_SAVE_TEMPS"] = "/tmp/iree"

import tensorflow as tf
from iree.compiler.tools import tf as tfc

class ComplexAddModule(tf.Module):
    @tf.function(input_signature=[
        tf.TensorSpec([13], tf.float32),
    ])
    def add(self, a):
        # Create complex numbers using tf.complex (documentation-style)
        complex_numbers = tf.complex(a, a)  # a + ai
        # Convert to explicit real/imag pairs for IREE compatibility
        return tf.stack([tf.math.real(complex_numbers), 
                        tf.math.imag(complex_numbers)], axis=1)

def export_model():
    # Create and save the model
    model = ComplexAddModule()
    tf.saved_model.save(
        model,
        export_dir="complex_add_model",
        signatures={"serving_default": model.add}
    )

    # Compile with standard flags
    tfc.compile_saved_model(
        "complex_add_model",
        saved_model_tags={"serve"},
        import_type="SIGNATURE_DEF",
        target_backends=["llvm-cpu"],
        output_file="complex_add_module.vmfb",
        exported_names=["serving_default"],
        extra_args=[
            "--iree-input-demote-i64-to-i32",
            "--iree-flow-enable-pad-handling",
            "--iree-llvmcpu-target-cpu=generic",
            "--iree-stream-resource-index-bits=64",
            "--iree-vm-target-index-bits=64"
        ]
    )
    print("Model compiled successfully to complex_add_module.vmfb")

def test_model():
    # Test the model (optional)
    import numpy as np
    from iree.runtime import load_vm_flatbuffer_file, system_setup
    
    ctx = system_setup()
    vm_module = load_vm_flatbuffer_file("complex_add_module.vmfb", driver="local-task", ctx=ctx)
    
    input_data = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13], dtype=np.float32)
    result = vm_module["serving_default"](input_data)
    
    print("\nTest output:")
    for i, (real, imag) in enumerate(result):
        print(f"[r{real:.1f}, i{imag:.1f}]")

if __name__ == "__main__":
    export_model()
    test_model()  # Optional: Comment out if you only want to compile
