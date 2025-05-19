#!/usr/bin/env bash

# Look for the dialect declaration (should contain 'stablehlo')
head -n 50 add_model_stablehlo.mlir

#iree-compile \
#  --iree-input-type=stablehlo \
#  --iree-hal-target-backends=llvm-cpu \
#  --iree-llvmcpu-target-cpu-features=host \
#  --iree-global-optimization-opt-level=0 \
#  --mlir-print-ir-after-all \
#  --mlir-print-ir-after-failure \
#  add_model_stablehlo.mlir \
#  -o add_module.vmfb
  
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
