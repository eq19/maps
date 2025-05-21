#!/bin/bash

# Run IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract hex data
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[^ ]+')

# IEEE 754 hex-to-float decoder in pure bash
hex_to_float() {
    local hex=$1
    # Convert hex to binary (32 bits)
    local bin=$(echo "ibase=16; obase=2; ${hex^^}" | bc | awk '{printf "%32s", $0}' | tr ' ' '0')
    
    # Extract components
    local sign=${bin:0:1}
    local exponent=${bin:1:8}
    local mantissa=${bin:9:23}
    
    # Convert to decimal
    local sign_val=$(( sign == "0" ? 1 : -1 ))
    local exponent_val=$(( 2#$exponent - 127 ))
    local mantissa_val=$(( 2#$mantissa ))
    
    # Calculate final value
    echo "$sign_val * (1 + $mantissa_val/8388608) * 2^$exponent_val" | bc -l | awk '{printf "%.1f", $0}'
}

# Decode each complex number
echo "Decoded complex numbers:"
i=1
for chunk in $HEX_DATA; do
    # Split into real/imaginary parts
    REAL_HEX=${chunk:0:8}
    IMAG_HEX=${chunk:8:8}
    
    # Decode floats (requires bc)
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
