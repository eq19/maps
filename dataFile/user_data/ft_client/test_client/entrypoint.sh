#!/usr/bin/env bash


if [ -f /home/runner/config.json ]; then
  #sed -i "s|your_exchange_key|${ACCESS_API}|g" $CONFIG
  #sed -i "s|your_exchange_secret|${ACCESS_KEY}|g" $CONFIG
fi

# Check the Deeplearning 
if [ -d /mnt/disks/deeplearning ]; then
  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { echo "Failed to get token"; exit 1; };
  TOKEN=$(cat /tmp/token)
  #curl -H "Authorization: Bearer $TOKEN" \
    #"https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
    #jq -r '.payload.data' | base64 --decode > $CONFIG

else
  "Deeplearning is not found.";
fi

# Run PostgreSQL (autostart)
#sudo service supervisor start
exec supervisord -c /etc/supervisor/supervisord.conf

#!/bin/bash

# Default workspace
WORKSPACE="/home/runner"
CONFIG=/home/runner/config.json

# Check if the Deep Learning workspace exists
if [ -d "/mnt/disks/deeplearning/home/runner" ]; then
  WORKSPACE="/mnt/disks/deeplearning/home/runner"
  sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" $WORKSPACE/config.jsom
  sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" $WORKSPACE/config.json
  jq '.telegram.enabled = true' $CONFIG > tmp.json && mv tmp.json $CONFIG
fi

# Ensure the workspace exists
mkdir -p "$WORKSPACE"

# Move `user_data` to the correct workspace, with a fallback
if [ ! -d "$WORKSPACE/user_data" ]; then
    if mv -f /home/runner/user_data "$WORKSPACE/user_data" 2>/dev/null; then
        echo "Moved user_data to $WORKSPACE successfully."
    else
        echo "Move failed, falling back to copy."
        cp -r /home/runner/user_data "$WORKSPACE/user_data" && rm -rf /home/runner/user_data
    fi
fi

# Ensure `config.json` is in the correct workspace
if [ ! -f "$WORKSPACE/config.json" ]; then
    cp /home/runner/config.json "$WORKSPACE/config.json"
fi

# Create a symbolic link for Freqtrade (avoid conflict with GitHub Actions)
if [ -z "$GITHUB_ACTIONS" ]; then
    ln -sfn "$WORKSPACE" /freqtrade
fi

# Change to the correct working directory
cd "$WORKSPACE"

# Execute the container's main process
exec "$@"
