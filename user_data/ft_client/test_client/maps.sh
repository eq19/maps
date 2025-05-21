#!/bin/bash

# Run the IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract the hex data after "13xcf64="
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[^ ]+')

# Hex to Float conversion using pure bash
hex_to_float() {
    local hex=$1
    # Reverse byte order (little-endian to big-endian)
    local reversed=$(echo "$hex" | sed -r 's/(..)(..)(..)(..)/\4\3\2\1/')
    # Convert to binary IEEE 754 float
    local sign=$((0x${reversed:0:1} >> 3))
    local exponent=$(( (0x${reversed:0:2} & 0x7F) << 1 | 0x${reversed:2:1} >> 7 ))
    local mantissa=$(( (0x${reversed:2:1} & 0x7F) << 16 | 0x${reversed:3:1} << 8 ))
    exponent=$((exponent - 127))
    printf "%.1f" $(echo "scale=2; (-1)^$sign * (1 + $mantissa/8388608) * 2^$exponent" | bc)
}

# Decode each complex number
echo "Decoded complex numbers:"
i=1
for chunk in $HEX_DATA; do
    # Process real and imaginary parts
    REAL_HEX=${chunk:0:8}
    IMAG_HEX=${chunk:8:8}
    
    # Hex to float conversion
    REAL=$(hex_to_float "$REAL_HEX")
    IMAG=$(hex_to_float "$IMAG_HEX")
    
    # Format output
    printf "[%02d] (r%s + i%sj)\n" $i "$REAL" "$IMAG"
    i=$((i+1))
done

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
