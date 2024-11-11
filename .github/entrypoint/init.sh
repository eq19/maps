#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

hr='------------------------------------------------------------------------------------'

git config --global user.name "${{ github.actor }}"
git config --global user.email "${{ github.actor }}@users.noreply.github.com"

git config --global --add safe.directory "${{ github.workspace }}"
#[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.autocrlf true
[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.safecrlf false
       
git config --global credential.helper store
echo "https://${{ github.actor }}:${{ inputs.token }}@github.com" > ~/.git-credentials

echo 'TARGET_REPO="https://${{ github.actor }}:${{ inputs.token }}@github.com/${TARGET_REPOSITORY}.git"' >> ${GITHUB_ENV}
echo 'REMOTE_REPO="https://${{ github.actor }}:${{ inputs.token }}@github.com/${{ github.repository }}.git"' >> ${GITHUB_ENV}
 
LATEST_COMMIT=$(curl -s "https://api.github.com/users/eq19/events/public" | jq ".[0].payload.commits[0].message")
if [ $? -eq 0 ]; then
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

echo -e "\n$hr\nENVIRONTMENT\n$hr"
printenv | sort

echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
