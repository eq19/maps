#!/bin/bash

# Run IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Debug: Show raw output
echo "---- RAW IREE OUTPUT ----"
echo "$RAW_OUTPUT"
echo "-------------------------"

# Extract the hex data after "13xcf64="
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[0-9A-F]+' | tr -d ' ')

# Debug: Show extracted hex
echo "Extracted HEX: $HEX_DATA"
echo "Length: ${#HEX_DATA} characters"

# Verify length (should be 13 numbers * 16 chars = 208)
if [ ${#HEX_DATA} -ne 208 ]; then
    echo "Error: Expected 208 hex chars, got ${#HEX_DATA}"
    exit 1
fi

# Run decoder
./user_data/ft_client/test_client//decoder "$HEX_DATA"

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
