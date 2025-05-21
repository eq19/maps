#!/bin/bash

# Run IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract and clean hex data
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[0-9A-F]+' | tr -d ' ' | tr -d '\n')

# IEEE 754 Hex to Float Decoder
hex_to_float() {
    local hex=$1
    # Convert to binary (32 bits)
    local bin=$(echo "obase=2; ibase=16; ${hex^^}" | bc | awk '{printf "%32s", $0}' | tr ' ' '0')
    
    # Extract components
    local sign=${bin:0:1}
    local exponent=${bin:1:8}
    local mantissa=${bin:9:23}
    
    # Calculate decimal values
    local sign_val=$(( sign == "0" ? 1 : -1 ))
    local exponent_val=$(( 2#$exponent - 127 ))
    local mantissa_val=$(( 2#$mantissa ))
    
    # Final calculation
    echo "scale=2; $sign_val * (1 + $mantissa_val/8388608) * 2^$exponent_val" | bc -l | awk '{printf "%.1f", $0}'
}

# Decode each complex number
echo "Decoded complex numbers:"
for i in {1..13}; do
    offset=$(( (i-1)*16 ))
    chunk=${HEX_DATA:$offset:16}
    
    REAL_HEX=${chunk:0:8}
    IMAG_HEX=${chunk:8:8}
    
    REAL=$(hex_to_float "$REAL_HEX")
    IMAG=$(hex_to_float "$IMAG_HEX")
    
    printf "[%02d] (r%s + i%sj)\n" $i "$REAL" "$IMAG"
done

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
