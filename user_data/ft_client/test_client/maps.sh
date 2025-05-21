#!/bin/bash

# Run the IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract the hex data after "13xcf64="
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[^ ]+')

# Simplified hex-to-float decoder using awk only
hex_to_float() {
    echo "$1" | awk '{
        # Convert little-endian hex to float (simplified)
        split($0, bytes, /../)
        sign = (strtonum("0x" bytes[4]) > 127 ? -1 : 1
        exponent = (strtonum("0x" bytes[4] "%128")*2 + int(strtonum("0x" bytes[3])/128)
        mantissa = (strtonum("0x" bytes[3] "%128")*65536 + strtonum("0x" bytes[2])*256 + strtonum("0x" bytes[1])
        printf "%.1f", sign * (2^(exponent-127)) * (1 + mantissa/8388608)
    }'
}

# Decode each complex number
echo "Decoded complex numbers:"
i=1
for chunk in $HEX_DATA; do
    # Split into real and imag parts
    REAL_HEX=${chunk:0:8}
    IMAG_HEX=${chunk:8:8}
    
    # Decode using awk
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
