#!/usr/bin/env bash
#
ls -al $WORKSPACE

STRATEGY=$WORKSPACE/user_data/ft_client/test_client/results/output.txt
cat $STRATEGY

curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${STRATEGY} | jq '.'
