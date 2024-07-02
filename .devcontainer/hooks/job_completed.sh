#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

CREDENTIAL=${INPUT_TOKEN}
[[ "${OWNER}" != "${USER}" ]] && CREDENTIAL=${INPUT_OWNER}
REMOTE_REPO="https://${ACTOR}:${CREDENTIAL}@github.com/${OWNER}/$1.git"
#git init --initial-branch=master > /dev/null && git remote add origin ${REMOTE_REPO}
#git add . && git commit -m "jekyll build" > /dev/null && git push --force ${REMOTE_REPO} master:gh-pages

echo 'job completed'
