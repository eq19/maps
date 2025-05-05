#!/usr/bin/env bash
#

cat user_data/ft_client/test_client/results/output.txt
ARTIFACT=user_data/ft_client/test_client/results/orgs.json

curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'
