#!/usr/bin/env bash

tensorflow-export-stablehlo \
  --saved_model_dir=add_model \
  --output_file=add_model.mlir
  
iree-compile \
  --iree-input-type=stablehlo \
  --iree-hal-target-backends=llvm-cpu \
  add_model.mlir \
  -o add_module.vmfb
  
iree-run-module \
  --module=add_module.vmfb \
  --function=add \
  --input=2.0 \
  --input=3.0

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
