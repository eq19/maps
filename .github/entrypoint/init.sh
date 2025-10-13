#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

hr='----------------------------------------------------------------------------------'

set_config() {
  echo -e "\n$hr\nCONFIG\n$hr"
  cat /home/runner/work/_actions/eq19/eq19/v2/.github/templates/jekyll_config.yml > $RUNNER_TEMP/_config.yml
  export PATH=/home/runner/work/_actions/eq19/eq19/v2/.github/entrypoint:$PATH && bash artifact.sh

  cat $RUNNER_TEMP/orgs.json > $1/user_data/ft_client/test_client/results/orgs.json
  gh variable set JEKYLL_CONFIG --body "$(cat $RUNNER_TEMP/_config.yml)"

  PARAMS_DRY=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_DRY" | jq -r '.value')
  PARAMS_LIVE=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_LIVE" | jq -r '.value')
  PARAMS_JSON=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_JSON" | jq -r '.value')
  echo "${PARAMS_JSON}" | jq '.' > $1/user_data/strategies/fibbo.json

  if jq empty < $1/user_data/strategies/fibbo.json; then
    echo -e "\n$hr\nPARAMETERS\n$hr"
    cat $1/user_data/strategies/fibbo.json
    gh variable set PARAMS_DRY --repo ${TARGET_REPOSITORY} --body "${PARAMS_DRY}"
    gh variable set PARAMS_LIVE --repo ${TARGET_REPOSITORY} --body "${PARAMS_LIVE}"
    gh variable set PARAMS_JSON --repo ${TARGET_REPOSITORY} --body "${PARAMS_JSON}"
    gh variable set REMOVE_REPOSITORY --repo ${TARGET_REPOSITORY} --body "${GITHUB_REPOSITORY}"
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

export MAP_BRANCH=$(curl -s -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/eq19/maps | jq -r .default_branch)
export DEFAULT_BRANCH=$(curl -s -H "Authorization: token $GH_TOKEN" \
  https://api.github.com/repos/$GITHUB_REPOSITORY | jq -r .default_branch)
export FREQAIMODEL_DRY=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/FREQAIMODEL" | jq -r '.value')
export FREQAIMODEL_LIVE=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/FREQAIMODEL" | jq -r '.value')
export RERUN_RUNNER=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')
export TARGET_REPOSITORY=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/TARGET_REPOSITORY" | jq -r '.value')


echo 'RERUN_RUNNER='${RERUN_RUNNER} >> ${GITHUB_ENV}
echo 'DEFAULT_BRANCH='${DEFAULT_BRANCH} >> ${GITHUB_ENV}
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
    gh workflow run "main.yml"

  else

    if [[ ! -f $RUNNER_TEMP/_config.yml ]]; then set_config $1; fi
    if [[ "$(yq '.repository' $RUNNER_TEMP/_config.yml)" != "$TARGET_REPOSITORY" ]]; then
      echo "$(yq '.repository' $RUNNER_TEMP/_config.yml) != $TARGET_REPOSITORY"
      gh workflow run "main.yml"
    else
      HEADER="Accept: application/vnd.github+json"
      RESPONSE=$(gh api -H "${HEADER}" repos/$TARGET_REPOSITORY/actions/runners)
      STATUS=$(echo "$RESPONSE" | jq -r --arg NAME "$RUNNER_TITLE" '.runners[] | select(.name == $NAME).status')

      if [[ "$STATUS" == "offline" ]]; then
        RUNNER_ID=$(gh api -H "${HEADER}" /repos/$TARGET_REPOSITORY/actions/runners --jq '.runners.[].id')
        gh api --method DELETE -H "${HEADER}" /repos/$TARGET_REPOSITORY/actions/runners/${RUNNER_ID}
      fi
    fi

    cd $GITHUB_WORKSPACE
    mv -f $1/pythonCode $1/user_data/ft_client/test_client/
    gcc -Wall -Wextra $1/gccCode/src/decoder.c -o float_decoder

    #Ref: https://github.com/tsoding/JelloVM
    javac -d $1/user_data/ft_client/test_client $1/javaCode/Main.java

    rm -rf .dockerignore user_data && mv -f $1/user_data .
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

  # Configuration
  NONCE=$(date +%s)
  METHOD="getInfo"
  MAX_RETRIES=3
  DIRS=(
    "data_dry"
    "data_live"
    "user_data"
  )
  FILES=(
    "strategies/fibbo.py"
    "strategies/__init__.py"
    "strategies/utils/__init__.py"
    "strategies/utils/indodax_patch.py"
  )
  PARAMS="method=${METHOD}&nonce=${NONCE}"
  DOCKER="/mnt/disks/deeplearning/usr/bin/docker"
  BASE_URL="https://raw.githubusercontent.com/eq19/maps/$MAP_BRANCH/user_data"
  SIGNATURE=$(echo -n "$PARAMS" | openssl sha512 -hmac "$API_SECRET" | cut -d' ' -f2)
  BALANCE=$(curl -s -X POST -H "Key: $API_KEY" -H "Sign: $SIGNATURE" -d "method=$METHOD" -d "nonce=$NONCE" "https://indodax.com/tapi/")
  ASSET_COUNT=$(echo "$BALANCE" | jq -r '.return.balance | to_entries | map(select(.value != 0 and .value != "0")) | length')

  for DIR_PATH in "${DIRS[@]}"; do
    for REL_PATH in "${FILES[@]}"; do
      DOWNLOAD_URL="$BASE_URL/$REL_PATH"
      DEST_PATH="/home/runner/$DIR_PATH/$REL_PATH"

      # Ensure parent directory exists (no file existence check)
      $DOCKER exec mydb mkdir -p "$(dirname "$DEST_PATH")"
      $DOCKER exec mydb rm -rf "$(dirname "$DEST_PATH")/strategies/__pycache__"
      $DOCKER exec mydb rm -rf "$(dirname "$DEST_PATH")/strategies/utils/__pycache__"

      # Download with retries (always overwrite
      for attempt in $(seq 1 $MAX_RETRIES); do
        echo "⌛ [Attempt $attempt/$MAX_RETRIES] Downloading: $REL_PATH"
    
        if $DOCKER exec mydb curl -sf -o "$DEST_PATH" "$DOWNLOAD_URL"; then
          if $DOCKER exec mydb test -s "$DEST_PATH"; then
            echo "✅ [SUCCESS] Downloaded: $DEST_PATH"
            break
          else
            echo "⚠️ [WARNING] Empty file (retrying...)"
          fi
        else
          echo "⚠️ [WARNING] Download failed (retrying...)"
        fi

        # Final attempt failure
        if [ "$attempt" -eq "$MAX_RETRIES" ]; then
          echo "❌ [ERROR] Failed to download: $REL_PATH" >&2
          exit 1
        fi
        sleep 2
      done
    done
  done

  # Setup freqtrade config.json
  CONF="/etc/supervisor/supervisord.conf"
  CONFIG="/home/runner/user_data/config.json"
  CONFIG_DRY="/home/runner/data_dry/config.json"
  CONFIG_LIVE="/home/runner/data_live/config.json"
  SUPERVISORD_CONF="$BASE_URL/ft_client/supervisord.conf"
  CONFIG_BASIC="$BASE_URL/config_examples/config_basic.example.json"
  CONFIG_PAIRLIST="$BASE_URL/config_examples/config_pairlist.example.json"
  CONFIG_EXCHANGE="$BASE_URL/config_examples/config_exchange.example.json"
  HYPEROPT_PARAM="/home/runner/user_data/strategies/hyperopt_params.json"
  EXCHANGE_PARAM="/home/runner/user_data/config_examples/config_exchange.example.json"
  PAIRLIST_PARAM="/home/runner/user_data/config_examples/config_pairlist.example.json"

  set -euo pipefail  # Strict error handling
  $DOCKER exec mydb rm -rf "$CONFIG"
  if $DOCKER exec mydb curl -sf -o "$CONFIG" "$CONFIG_BASIC"; then
    $DOCKER exec mydb sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" $CONFIG
    $DOCKER exec mydb sed -i "s|config_examples|/home/runner/user_data/config_examples|g" $CONFIG

    $DOCKER exec mydb ls -al /home/runner/user_data
    WALLET=$(echo $BALANCE | jq '.return.balance.idr')
    if [[ "${ASSET_COUNT}" == "1" ]]; then echo $WALLET; fi
  
    $DOCKER exec mydb bash -c "jq '.telegram.enabled = true' $CONFIG > $CONFIG_DRY"
    $DOCKER exec mydb bash -c "jq '.telegram.enabled = true' $CONFIG > $CONFIG_LIVE"
    #$DOCKER exec mydb bash -c "jq '.telegram.enabled = true | .dry_run = false' $CONFIG > $CONFIG_LIVE"

    $DOCKER exec mydb sed -i "s|tradesv3|tradesv3_dry|g" $CONFIG_DRY
    $DOCKER exec mydb sed -i "s|tradesv3|tradesv3_live|g" $CONFIG_LIVE
    $DOCKER exec mydb sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" $CONFIG_DRY
    $DOCKER exec mydb sed -i "s|your_telegram_token|$TRADING_BOT_TOKEN|g" $CONFIG_LIVE

    $DOCKER exec mydb curl -sf -o "$CONF" "$SUPERVISORD_CONF"
    $DOCKER exec mydb sed -i "s|FREQAIMODEL_DRY|$FREQAIMODEL_DRY|g" $CONF
    $DOCKER exec mydb sed -i "s|FREQAIMODEL_LIVE|$FREQAIMODEL_LIVE|g" $CONF

    $DOCKER exec mydb curl -sf -o "$PAIRLIST_PARAM" "$CONFIG_PAIRLIST"
    $DOCKER exec mydb curl -sf -o "$EXCHANGE_PARAM" "$CONFIG_EXCHANGE"
    $DOCKER exec mydb sed -i "s|your_exchange_key|$API_KEY|g" $EXCHANGE_PARAM
    $DOCKER exec mydb sed -i "s|your_exchange_secret|$API_SECRET|g" $EXCHANGE_PARAM

    $DOCKER exec mydb sed -i "s|TELEGRAM_CHAT_ID|$TELEGRAM_CHAT_ID|g" /freqtrade.sh
    $DOCKER exec mydb sed -i "s|WARNING_BOT_TOKEN|$WARNING_BOT_TOKEN|g" /freqtrade.sh

    echo "🚀 All files updated (forced overwrite)!"
  fi

  $DOCKER exec mydb bash -c \
    "curl -s -H 'Authorization: token $GH_TOKEN' -H 'Accept: application/vnd.github.v3+json' \
    https://api.github.com/repos/$GITHUB_REPOSITORY/actions/variables/PARAMS_DRY \
    | jq -r '.value' > /home/runner/data_dry/strategies/fibbo.json"
  $DOCKER exec mydb bash -c \
    "curl -s -H 'Authorization: token $GH_TOKEN' -H 'Accept: application/vnd.github.v3+json' \
    https://api.github.com/repos/$GITHUB_REPOSITORY/actions/variables/PARAMS_LIVE \
    | jq -r '.value' > /home/runner/data_live/strategies/fibbo.json"

  # Get the config value and save to file.json
  curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/ORGS_JSON" \
    | jq -r '.value' > _data/orgs.json
  curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/JEKYLL_CONFIG" \
    | jq -r '.value' > _config.yml

  $DOCKER exec mydb cat $HYPEROPT_PARAM
  $DOCKER exec mydb cp $HYPEROPT_PARAM /home/runner/data_dry/strategies/hyperopt_params.json
  $DOCKER exec mydb cp $HYPEROPT_PARAM /home/runner/data_live/strategies/hyperopt_params.json

  $DOCKER exec mydb ls -alR /home/runner/data_dry
  $DOCKER exec mydb ls -alR /home/runner/data_live

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
