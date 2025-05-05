#!/usr/bin/env bash
#

cat user_data/ft_client/test_client/results/output.txt
ARTIFACT=user_data/ft_client/test_client/results/orgs.json

curl -s -X POST \
  -H "Authorization: Bearer ${BEARER}" \
  -H "Content-Type: application/json" \
  https://us-central1-feedmapping.cloudfunctions.net/function \
  --data @${ARTIFACT} | jq '.'

curl -L -s -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$GITHUB_REPOSITORY/actions/variables/ORGS_JSON \
  -d "$(jq -n '{name:"ORGS_JSON", value:$value}' --arg value "$(cat "$ARTIFACT")")"
