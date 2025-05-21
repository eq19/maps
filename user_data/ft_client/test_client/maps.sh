#!/usr/bin/env bash

#lscpu | grep Flags
iree-run-module \
  --module=add_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --output_format=json \
  --print_statistics=false | \
  jq -c '.output0[] | [("r"+ (.0|tostring)), ("i"+ (.1|tostring))]'

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
