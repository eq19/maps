#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

hr='------------------------------------------------------------------------------------'

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git config --global --add safe.directory "${GITHUB_WORKSPACE}"
[[ "$RUNNER_OS" == "Windows" ]] && YQ=$(choco install yq)
[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.safecrlf false
       
git config --global credential.helper store
echo "https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com" > ~/.git-credentials

TARGET_REPO="https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com/${TARGET_REPOSITORY}.git"
REMOTE_REPO="https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"

API_URL="https://api.github.com/users/eq19/events/public"
LATEST_COMMIT=$(curl -s $API_URL | jq ".[0].payload.commits[0].message")
if [[ -z "$LATEST_COMMIT" ]] || [[ "$LATEST_COMMIT" == "null" ]]; then
  echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
else
  echo 'LATEST_COMMIT='$LATEST_COMMIT >> ${GITHUB_ENV}
fi

if [[ "${JOB_ID}" == "1" ]]; then

  cd "${GITHUB_WORKSPACE}" && rm -rf .github
  cp -r /home/runner/work/_actions/eq19/eq19/v1/.github .
  chown -R "$(whoami)" .github

  git remote set-url origin ${REMOTE_REPO}        
  git add . && git commit -m "update workflows" && git push
  if [ $? -eq 0 ]; then exit 1; fi

fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then

  echo -e "\n$hr\nENVIRONTMENT\n$hr"
  echo 'TARGET_REPO='${TARGET_REPO} >> ${GITHUB_ENV}
  echo 'REMOTE_REPO='${REMOTE_REPO} >> ${GITHUB_ENV}

  if [[ -f _config.yml ]]; then
    FOLDER=$(yq '.span' _config.yml)
    export FOLDER=$(eval echo $FOLDER)
  elif [[ -f /home/runner/_site/.env ]]; then
    set -a && . /home/runner/_site/.env && set +a
  fi
  printenv | sort

fi

if [[ "${JOB_ID}" == "3" ]]; then

  echo -e "\n$hr\nWORKSPACE\n$hr"
  gist.sh ${TARGET_REPOSITORY} ${FOLDER}

  if [[ "${WIKI}" != "${BASE}" ]]; then
    git clone $WIKI ${RUNNER_TEMP}/wikidir
    mv -f ${RUNNER_TEMP}/wikidir/Home.md ${RUNNER_TEMP}/wikidir/README.md
    find ${RUNNER_TEMP}/gistdir -type d -name "${FOLDER}" -prune -exec sh -c 'wiki.sh "$1"' sh {} \;
  fi

  find ${RUNNER_TEMP}/gistdir -type d -name .git -prune -exec rm -rf {} \;
  
  mv -f ${RUNNER_TEMP}/workdir/* /home/runner/_site/
  rm -rf ${RUNNER_TEMP}/Sidebar.md && cp _Sidebar.md ${RUNNER_TEMP}/Sidebar.md
  sed -i 's/0. \[\[//g' ${RUNNER_TEMP}/Sidebar.md && sed -i 's/\]\]//g' ${RUNNER_TEMP}/Sidebar.md

  cd /home/runner/_site && cp -R ${RUNNER_TEMP}/gistdir/* .
  find . -iname '*.md' -print0 | sort -zn | xargs -0 -I '{}' front.sh '{}'
  find . -type d -name "${FOLDER}" -prune -exec sh -c 'cat ${RUNNER_TEMP}/README.md >> $1/README.md' sh {} \;

elif [[ "${JOB_ID}" == "4" ]]; then

  echo -e "\n$hr\nWORKSPACE\n$hr"

fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then
  echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
fi
