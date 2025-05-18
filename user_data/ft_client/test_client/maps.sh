#!/usr/bin/env bash

# Step 1: Convert TensorFlow SavedModel to MLIR
iree-import-tf \
  --savedmodel_dir=add_model \
  --output_file=add_model.mlir

# Step 2: Compile MLIR to IREE's VMFB (executable binary format)
iree-compile \
  --iree-input-type=stablehlo \
  --iree-hal-target-backends=llvm-cpu \
  add_model.mlir \
  -o add_module.vmfb

#iree-run-module --help

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
