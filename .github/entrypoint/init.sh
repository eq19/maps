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
COMMIT=$(curl -s $API_URL | jq -r 'map(select(.type == "PushEvent")) | .[0].payload.commits[0].message')

# Remove double quotes using parameter expansion
LATEST_COMMIT="${COMMIT//\"/}"

if [[ -z "$LATEST_COMMIT" ]] || [[ "$LATEST_COMMIT" == "null" ]]; then
  echo 'LATEST_COMMIT="update by workspace"' >> ${GITHUB_ENV}
else
  echo 'LATEST_COMMIT='$LATEST_COMMIT >> ${GITHUB_ENV}
fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then

  echo -e "\n$hr\nENVIRONTMENT\n$hr"
  echo 'TARGET_REPO='${TARGET_REPO} >> ${GITHUB_ENV}
  echo 'REMOTE_REPO='${REMOTE_REPO} >> ${GITHUB_ENV}

  if [[ -f /home/runner/_site/_config.yml ]]; then
    cat /home/runner/_site/_config.yml
    FOLDER=$(yq '.span' /home/runner/_site/_config.yml)
    export FOLDER=$(eval echo $FOLDER)
  elif [[ -f /home/runner/_site/.env ]]; then
    set -a && . /home/runner/_site/.env && set +a
  fi
  printenv | sort

fi

echo -e "\n$hr\nWORKSPACE\n$hr"
RERUN_RUNNER=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')

if [[ "${JOBS_ID}" == "1" ]]; then

  cd ${GITHUB_WORKSPACE} && rm -rf .github
  cp -r /home/runner/work/_actions/eq19/eq19/v2/.github .
  chown -R "$(whoami)" .github

  git remote set-url origin ${REMOTE_REPO}        
  git add . && git commit -m "update workflows" --quiet && git push --quiet

  if [[ $? -eq 0 ]]; then

    git clone --single-branch --branch gh-pages $REMOTE_REPO gh-pages && cd gh-pages
    git add . && git commit --allow-empty -m "rerun due to job update" && git push
    exit 1

  else

    PARAMS_JSON=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_JSON" | jq -r '.value')
    echo "${PARAMS_JSON}" | jq '.' > $1/user_data/strategies/fibbo.json

    if jq empty < $1/user_data/strategies/fibbo.json; then
      cat $1/user_data/strategies/fibbo.json
    else
      echo "Invalid JSON"
    fi

    cd $1 && javac -d user_data/ft_client/test_client javaCode/Main.java
    cd ${GITHUB_WORKSPACE} && rm -rf user_data && mv -f $1/user_data . && ls -al .
    if [[ "${RERUN_RUNNER}" != "false" ]]; then gh variable set RERUN_RUNNER --body "false"; fi

  fi

elif [[ "${JOBS_ID}" == "2" ]]; then

  ls -alR ${GITHUB_WORKSPACE}

elif [[ "${JOBS_ID}" == "3" ]]; then

  cd /home/runner/_site && rm -rf README.md docs && gist.sh ${BASE} $(pwd)

  if [[ "${WIKI}" != "${BASE}" ]]; then
    find . -type d -name "${FOLDER}" -prune -exec sh -c 'gist.sh ${WIKI} "$1"' sh {} \;
  fi

else

  cd ${RUNNER_TEMP//\\//} && rm -rf gh-source
  git clone --single-branch --branch gh-source $TARGET_REPO gh-source
  
  cd ${GITHUB_WORKSPACE//\\//}
  find -not -path "./.git/*" -not -name ".git" -delete

  rm -rf ${RUNNER_TEMP//\\//}/gh-source/.git
  shopt -s dotglob && mv -f ${RUNNER_TEMP//\\//}/gh-source/* . && ls -lR .

fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then
  echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
fi
