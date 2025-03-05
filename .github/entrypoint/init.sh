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
LATEST_COMMIT=$(curl -s $API_URL | jq -r 'map(select(.type == "PushEvent")) | .[0].payload.commits[0].message')

if [[ -z "$LATEST_COMMIT" ]] || [[ "$LATEST_COMMIT" == "null" ]]; then
  echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
else
  echo 'LATEST_COMMIT='$LATEST_COMMIT >> ${GITHUB_ENV}
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

echo -e "\n$hr\nWORKSPACE\n$hr"
if [[ "${JOB_ID}" == "1" ]]; then

  cd ${GITHUB_WORKSPACE} && rm -rf .github
  cp -r /home/runner/work/_actions/eq19/eq19/v1/.github .
  chown -R "$(whoami)" .github

  git remote set-url origin ${REMOTE_REPO}        
  git add . && git commit -m "update workflows" --quiet && git push --quiet
  if [ $? -eq 0 ]; then
    git clone --single-branch --branch gh-pages $REMOTE_REPO gh-pages && cd gh-pages
    git add . && git commit --allow-empty -m "rerun due to job update" && git push
    exit 1
  else
    mv -f $1/dataFile/user_data ${GITHUB_WORKSPACE}/
    cd ${GITHUB_WORKSPACE} && ls -al ${GITHUB_WORKSPACE}
  fi

elif [[ "${JOB_ID}" == "2" ]]; then

  ls -alR ${GITHUB_WORKSPACE}

elif [[ "${JOB_ID}" == "3" ]]; then

  cat /home/runner/_site/_config.yml
  gist.sh ${TARGET_REPOSITORY} ${FOLDER}

  find ${RUNNER_TEMP}/gistdir -type d -name .git -prune -exec rm -rf {} \;
  mv -f ${RUNNER_TEMP}/workdir/* /home/runner/_site/

  rm -rf ${RUNNER_TEMP}/Sidebar.md && cp _Sidebar.md ${RUNNER_TEMP}/Sidebar.md
  sed -i 's/0. \[\[//g' ${RUNNER_TEMP}/Sidebar.md && sed -i 's/\]\]//g' ${RUNNER_TEMP}/Sidebar.md

  cd /home/runner/_site && cp -R ${RUNNER_TEMP}/gistdir/* . && ls -lR .

else

  cd ${RUNNER_TEMP//\\//} && rm -rf gh-source
  git clone --single-branch --branch gh-source $TARGET_REPO gh-source
  
  cd ${GITHUB_WORKSPACE//\\//}
  #find -not -path "./.git/*" -not -name ".git" | grep git
  find -not -path "./.git/*" -not -name ".git" -delete

  rm -rf ${RUNNER_TEMP//\\//}/gh-source/.git
  shopt -s dotglob && mv -f ${RUNNER_TEMP//\\//}/gh-source/* . && ls -lR .

fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then
  echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
fi
