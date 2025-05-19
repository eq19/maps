#!/bin/bash

MAX_RETRIES=10
RETRY_DELAY=100  # seconds
RUNNER_URL="https://github.com/$1"
GH_API_URL="https://api.github.com/repos/$1/actions/runners"

# Function to check if runner is online using GitHub API
check_runner_online() {
  local AUTH="Authorization: Bearer $GITHUB_ACCESS_TOKEN"
  local VERSION="X-GitHub-Api-Version: 2022-11-28"
  local ACCEPT="Accept: application/vnd.github+json"
    
  echo "Checking runner status via GitHub API..."
    
  RESPONSE=$(curl -s -L -H "$AUTH" -H "$VERSION" -H "$ACCEPT" "$GH_API_URL")
  if [ $? -ne 0 ]; then
    echo "Error: Failed to query GitHub API"
    return 1
  fi
    
  STATUS=$(echo "$RESPONSE" | jq -r --arg NAME "$RUNNER_NAME" '.runners[] | select(.name == $NAME).status')
  if [ $? -ne 0 ]; then
    echo "Error: Failed to parse API response"
    return 1
  fi
    
  if [ "$STATUS" == "online" ]; then
    echo "Runner is online according to GitHub API"
    return 0
  else
    echo "Runner status: ${STATUS:-unknown}"
    return 1
  fi
}

# Function to register the runner
register_runner() {
  # Stop the runner through supervisor
  echo "Stopping runner..."
  supervisorctl stop runner || true

  # Forcefully remove old configuration
  if [ -f .runner ]; then
    echo "Forcefully removing old runner configuration"
    rm -f .env
    rm -f .runner
    rm -f .credentials
    rm -f .credentials_rsaparams
    rm -rf _diag $RUNNER_WORK_DIRECTORY
  fi

  # Register with new token
  echo "Exchanging the GitHub Access Token with a Runner Token (scope: repos)..."
  _PROTO="$(echo "${RUNNER_URL}" | grep :// | sed -e's,^\(.*://\).*,\1,g')"
  _URL="$(echo "${RUNNER_URL/${_PROTO}/}")"
  _PATH="$(echo "${_URL}" | grep / | cut -d/ -f2-)"

  RUNNER_TOKEN="$(curl -XPOST -fsSL \
    -H "Authorization: token ${GITHUB_ACCESS_TOKEN}" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${_PATH}/actions/runners/registration-token" \
    | jq -r '.token')"

  if [ -z "$RUNNER_TOKEN" ]; then
    echo "Failed to get registration token"
    exit 1
  fi

  echo "Registering new runner..."
  ./config.sh \
    --url "$RUNNER_URL" \
    --token "$RUNNER_TOKEN" \
    --name "$RUNNER_NAME" \
    --work "$RUNNER_WORK_DIRECTORY" \
    $CONFIG_OPTS \
    --replace \
    --unattended

  # Restart the runner through supervisor
  echo "Starting runner..."
  supervisorctl start runner
}

if [[ -z $RUNNER_TOKEN && -z $GITHUB_ACCESS_TOKEN ]]; then
  echo "Error : You need to set RUNNER_TOKEN (or GITHUB_ACCESS_TOKEN) environment variable."
  exit 1
fi

if [[ -z $RUNNER_NAME ]]; then
  echo "RUNNER_NAME environment variable is not set, using '${HOSTNAME}'."
  export RUNNER_NAME=${HOSTNAME}
fi

if [[ -z $RUNNER_WORK_DIRECTORY ]]; then
  echo "RUNNER_WORK_DIRECTORY environment variable is not set, using '_work'."
  export RUNNER_WORK_DIRECTORY="_work"
fi

if [[ -z $RUNNER_REPLACE_EXISTING ]]; then
  export RUNNER_REPLACE_EXISTING="true"
fi

CONFIG_OPTS=""
if [ "$(echo $RUNNER_REPLACE_EXISTING | tr '[:upper:]' '[:lower:]')" == "true" ]; then
  export CONFIG_OPTS="--replace"
fi

if [[ -n $RUNNER_LABELS ]]; then
  export CONFIG_OPTS="${CONFIG_OPTS} --labels ${RUNNER_LABELS}"
fi

# Change to runner directory
cd /home/runner || { echo "Failed to cd to /home/runner"; exit 1; }

# Main execution with retries
retry_count=0
while [ $retry_count -lt $MAX_RETRIES ]; do
  echo "Attempt $((retry_count + 1)) of $MAX_RETRIES"
    
  register_runner
    
  echo "Waiting $RETRY_DELAY seconds for runner to initialize..."
  sleep $RETRY_DELAY
    
  if check_runner_online; then
    echo "Runner successfully registered and online"
    exit 0
  else
    echo "Runner failed to come online"
    ((retry_count++))
  fi
done

echo "ERROR: Failed to bring runner online after $MAX_RETRIES attempts"
