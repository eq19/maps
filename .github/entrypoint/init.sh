#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

hr='------------------------------------------------------------------------------------'

set_config() {
  echo -e "\n$hr\nCONFIG\n$hr"
  cat /home/runner/work/_actions/eq19/eq19/v2/.github/templates/jekyll_config.yml > $RUNNER_TEMP/_config.yml
  export PATH=/home/runner/work/_actions/eq19/eq19/v2/.github/entrypoint:$PATH && bash artifact.sh

  cat $RUNNER_TEMP/orgs.json > $1/user_data/ft_client/test_client/results/orgs.json
  gh variable set JEKYLL_CONFIG --body "$(cat $RUNNER_TEMP/_config.yml)"

  PARAMS_JSON=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_JSON" | jq -r '.value')
  echo "${PARAMS_JSON}" | jq '.' > $1/user_data/strategies/fibbo.json

  if jq empty < $1/user_data/strategies/fibbo.json; then
    echo -e "\n$hr\nPARAMETERS\n$hr"
    cat $1/user_data/strategies/fibbo.json
    gh variable set PARAMS_JSON --repo ${TARGET_REPOSITORY} --body "${PARAMS_JSON}"
  else
    echo "Invalid JSON"
  fi

  echo -e "\n$hr\nENVIRONTMENT\n$hr" && printenv | sort
}

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

git config --global --add safe.directory "${GITHUB_WORKSPACE}"
[[ "$RUNNER_OS" == "Windows" ]] && YQ=$(choco install yq)
[[ "$RUNNER_OS" == "Windows" ]] && git config --global core.safecrlf false
       
git config --global credential.helper store
echo "https://${GITHUB_ACTOR}:${GH_TOKEN}@github.com" > ~/.git-credentials

export RERUN_RUNNER=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')
export TARGET_REPOSITORY=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/TARGET_REPOSITORY" | jq -r '.value')
  
echo 'RERUN_RUNNER='${RERUN_RUNNER} >> ${GITHUB_ENV}
echo 'TARGET_REPOSITORY='${TARGET_REPOSITORY} >> ${GITHUB_ENV}

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

if [[ "${JOBS_ID}" == "1" ]]; then

  BASE_FOLDER="/home/runner/work/_actions/eq19/eq19/v2/.github"
  if diff -qr ${GITHUB_WORKSPACE}/.github ${BASE_FOLDER} > /dev/null; then set_config $1; fi
  cd ${GITHUB_WORKSPACE} && rm -rf .github && cp -r ${BASE_FOLDER} . && chown -R "$(whoami)" .github

  git remote set-url origin ${REMOTE_REPO}        
  CLEAN_STATUS=$(git add . && git commit -m "update workflows" --quiet && git push --quiet)

  if [[ $? -eq 0 ]]; then

    #git clone --single-branch --branch gh-pages $REMOTE_REPO gh-pages && cd gh-pages
    #git add . && git commit --allow-empty -m "rerun due to job update" && git push
    curl -s -X POST \
      -H "Authorization: token $GH_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/${GITHUB_REPOSITORY}/dispatches" \
      -d '{"event_type": "retry_workflow", "client_payload": {"original_run_id": "${GITHUB_RUN_ID}"}}'
    exit 1

  else

    if [[ ! -f $RUNNER_TEMP/_config.yml ]]; then set_config $1; fi
    if [[ "$(yq '.repository' $RUNNER_TEMP/_config.yml)" != "$TARGET_REPOSITORY" ]]; then
      echo "$(yq '.repository' $RUNNER_TEMP/_config.yml) != $TARGET_REPOSITORY"
      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "https://api.github.com/repos/${GITHUB_REPOSITORY}/dispatches" \
        -d '{"event_type": "retry_workflow", "client_payload": {"original_run_id": "${GITHUB_RUN_ID}"}}'
      exit 1
    fi

    #Ref: https://github.com/tsoding/JelloVM
    cd $1 && javac -d user_data/ft_client/test_client javaCode/Main.java

    cd $GITHUB_WORKSPACE && rm -rf user_data && mv -f $1/user_data .
    echo -e "\n$hr\nWORKSPACE\n$hr" && ls -al .

    # Fetch SHA, encode new content, and update in one step
    gh api --method PUT /repos/${TARGET_REPOSITORY}/contents/.github/workflows/main.yml \
      -f sha="$(gh api /repos/${TARGET_REPOSITORY}/contents/.github/workflows/main.yml --jq '.sha')" \
      -f message="Update file" -f content="$(base64 -w0 .github/workflows/main.yml)" > /dev/null

  fi

elif [[ "${JOBS_ID}" == "2" ]]; then

  echo -e "\n$hr\nENVIRONTMENT\n$hr" && printenv | sort
  echo -e "\n$hr\nWORKSPACE\n$hr" && ls -alR $GITHUB_WORKSPACE

  echo -e "\n$hr\nGH BRANCHES\n$hr"
  cd $RUNNER_TEMP && mkdir my-project && cd my-project && git init -q
  git remote add source "$REMOTE_REPO" && git remote add origin "$TARGET_REPO"

  # Get list of existing target branches
  existing_target_branches=$(git ls-remote --heads origin | awk -F'/' '{print $3}')

  # Fetch only gh- branches from source
  git fetch source 'refs/heads/gh-*:refs/remotes/source/gh-*'

  # Process branches
  for remote_branch in $(git branch -r | grep 'source/gh-'); do
    local_branch=${remote_branch#source/}
    
    if ! grep -q "^$local_branch$" <<< "$existing_target_branches"; then
      # New branch case
      if [[ "$local_branch" =~ ^(gh-base|gh-source|gh-pages)$ ]]; then
         git checkout -b "$local_branch" "$remote_branch" && \
         git push origin "$local_branch" && \
         echo "Successfully pushed $local_branch to target" || \
         echo "Failed to push $local_branch"
      fi
    else
      # Existing branch case
      if [[ "$local_branch" == "gh-pages" ]]; then
        git fetch origin gh-pages
        # Check if 'docs/' exists in remote
        if ! git ls-tree --name-only "origin/gh-pages" | grep -q "^docs"; then
          echo "No docs/ found - recreating gh-pages"
          # Ensure local branch exists
          if ! git show-ref --verify --quiet "refs/heads/gh-pages"; then
            git checkout -b gh-pages "$remote_branch"
          else
            git checkout gh-pages
            git reset --hard "$remote_branch"
          fi
          git push --force origin gh-pages
        fi
      fi
    fi
  done
  
elif [[ "${JOBS_ID}" == "3" ]]; then

  find -not -path "./.git/*" -not -name ".git" -delete
  shopt -s dotglob && cp -R /mnt/disks/deeplearning/tmp/_site/* .

  # Get the config value and save to file.json
  curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/ORGS_JSON" \
    | jq -r '.value' > _data/orgs.json
  curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/JEKYLL_CONFIG" \
    | jq -r '.value' > _config.yml

  echo -e "\n$hr\nCONFIG\n$hr" && cat _config.yml
  echo -e "\n$hr\nENVIRONTMENT\n$hr" && printenv | sort

  gist.sh ${BASE} $(pwd)
  if [[ "${WIKI}" != "${BASE}" ]]; then
    find . -type d -name "$(yq '.span' _config.yml)" -prune -exec sh -c 'gist.sh ${WIKI} "$1"' sh {} \;
  fi

  echo -e "\n$hr\nWORKSPACE\n$hr" && ls -alR .

else

  cd ${RUNNER_TEMP//\\//} && rm -rf gh-source
  git clone --single-branch --branch gh-source $TARGET_REPO gh-source
  
  cd ${GITHUB_WORKSPACE//\\//}
  find -not -path "./.git/*" -not -name ".git" -delete

  rm -rf ${RUNNER_TEMP//\\//}/gh-source/.git
  shopt -s dotglob && mv -f ${RUNNER_TEMP//\\//}/gh-source/* .

  echo -e "\n$hr\nCONFIG\n$hr" && cat _config.yml
  echo -e "\n$hr\nENVIRONTMENT\n$hr" && printenv | sort
  echo -e "\n$hr\nWORKSPACE\n$hr" && ls -alR .

fi

if [[ -z ${PASS} ]] || [[ "${PASS}" == "true" ]]; then
  echo -e "\n$hr\nGITHUB CONTEXT\n$hr"
fi
