#!/usr/bin/env bash

iree-compile \
  --iree-input-type=mhlo \
  --iree-hal-target-backends=llvm-cpu \
  add_model/saved_model.pb \
  -o add_module.vmfb
#iree-run-module --help

cat $ARTIFACT
curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
