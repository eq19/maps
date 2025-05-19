#!/usr/bin/env bash

iree-run-module \
  --module=add_module.vmfb \
  --function=add \
  --input=2.0 \
  --input=3.0

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
