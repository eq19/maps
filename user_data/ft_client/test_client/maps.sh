#!/usr/bin/env bash

iree-run-module \
  --module=add_module.vmfb \
  --function=serving_default \
  --input="10xf32=[1,2,3,4,5,6,7,8,9,10]" \
  --input="10xf32=[2,3,4,5,6,7,8,9,10,11]"
  
cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
