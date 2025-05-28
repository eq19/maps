##!/bin/bash

#cat $ARTIFACT

# Run IREE and capture ALL output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Debug: Save output to file
echo "$RAW_OUTPUT" > iree_output.txt
echo "---- RAW OUTPUT ----"
cat iree_output.txt
echo "--------------------"

# Pass to decoder
./float_decoder "$RAW_OUTPUT"

curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
