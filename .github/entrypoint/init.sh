#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

hr='------------------------------------------------------------------------------------'

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git config --global --add safe.directory "${GITHUB_WORKSPACE}"
#[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.autocrlf true
[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.safecrlf false
       
git config --global credential.helper store
echo "https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com" > ~/.git-credentials

TARGET_REPO="https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com/${TARGET_REPOSITORY}.git"
REMOTE_REPO="https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

API_URL="https://api.github.com/users/eq19/events/public"
LATEST_COMMIT=$(curl -s $API_URL | jq ".[0].payload.commits[0].message")
if [[ $? -eq 0 ]]; then
  if [[ -z "$LATEST_COMMIT" ]]; then
    echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
  elif [[ "$LATEST_COMMIT" == null ]]; then
    echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
  else
     echo 'LATEST_COMMIT='$LATEST_COMMIT >> ${GITHUB_ENV}
  fi
else
  echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
fi

if [[ "${JOB_ID}" == "1" ]]; then
   
  cd "${GITHUB_WORKSPACE}" && rm -rf .github
  cp -r /home/runner/work/_actions/eq19/eq19/v1/.github .
  chown -R "$(whoami)" .github

  git remote set-url origin ${REMOTE_REPO}        
  git add . && git commit -m "update workflows" && git push
  if [ $? -eq 0 ]; then exit 1; fi

fi

echo -e "\n$hr\nENVIRONTMENT\n$hr"
echo 'TARGET_REPO='${TARGET_REPO} >> ${GITHUB_ENV}
echo 'REMOTE_REPO='${REMOTE_REPO} >> ${GITHUB_ENV}
printenv | sort

echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
