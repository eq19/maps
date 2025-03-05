#!/usr/bin/env bash

git config --global user.name "${GITHUB_ACTOR}"
git config --global --add safe.directory "${GITHUB_WORKSPACE}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

#git config --global credential.helper store
#echo "https://${GITHUB_ACTOR}:${GITHUB_ACCESS_TOKEN}@github.com" > ~/.git-credentials

echo 'REMOTE_REPO="https://${GITHUB_ACTOR}:${GITHUB_ACCESS_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"' >> ${GITHUB_ENV}
COMMIT=$(curl -s "https://api.github.com/users/eq19/events/public" | jq ".[0].payload.commits[0].message")

# Remove double quotes using parameter expansion
echo 'LATEST_COMMIT="${COMMIT//\"/}"' >> ${GITHUB_ENV}
