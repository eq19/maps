#!/bin/bash

# Run IREE module
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract ALL hex data including spaces
FULL_HEX=$(echo "$RAW_OUTPUT" | awk -F'13xcf64=' '{print $2}' | awk '{print $1}')

echo "---- DEBUG ----"
echo "Full hex with spaces: $FULL_HEX"
echo "----------------"

# Pass to C decoder (it will clean spaces)
./user_data/ft_client/test_client/decoder "$FULL_HEX"

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
