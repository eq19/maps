#!/usr/bin/env bash

iree-compile --iree-input-type=torch --iree-hal-target-backends=llvm-cpu \
  add_model.pt -o add_module.vmfb
#iree-run-module --help

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
