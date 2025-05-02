#!/usr/bin/env bash
#
ls -al $WORKSPACE

cat $WORKSPACE/user_data/ft_client/test_client/results/output.txt
ARTIFACT=$WORKSPACE/user_data/ft_client/test_client/results/orgs.json

curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
