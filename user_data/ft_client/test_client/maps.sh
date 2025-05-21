#!/usr/bin/env bash

#lscpu | grep Flags
iree-run-module \
  --module=add_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --output=json | jq '{
    "serving_default": {
      "result": [
        [.real[0], .imag[0]],
        [.real[1], .imag[1]],
        [.real[2], .imag[2]],
        [.real[3], .imag[3]],
        [.real[4], .imag[4]],
        [.real[5], .imag[5]],
        [.real[6], .imag[6]],
        [.real[7], .imag[7]],
        [.real[8], .imag[8]],
        [.real[9], .imag[9]],
        [.real[10], .imag[10]],
        [.real[11], .imag[11]],
        [.real[12], .imag[12]]
      ]
    }
  }'

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
