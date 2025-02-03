#!/usr/bin/env bash

# Default workspace
WORKSPACE="/home/runner"

# Check if the Deep Learning exists
if [ -d "/mnt/disks/deeplearning" ]; then
  WORKSPACE="/mnt/disks/deeplearning/home/runner"
  exec supervisord -c /etc/supervisor/supervisord.conf
  freqtrade create-userdir --userdir $WORKSPACE/user_data/

  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { echo "Failed to get token"; exit 1; };
  TOKEN=$(cat /tmp/token)
  #curl -H "Authorization: Bearer $TOKEN" \
    #"https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
    #jq -r '.payload.data' | base64 --decode > $CONFIG
fi

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
  cp /home/runner/config.json $WORKSPACE/config.json
  sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" $WORKSPACE/config.jsom
  sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" $WORKSPACE/config.json
  jq '.telegram.enabled = true' $CONFIG > tmp.json && mv tmp.json $CONFIG
fi

# Change to the correct working directory
ln -sfn "$WORKSPACE" /freqtrade
cd /freqtrade

# Execute the container's main process
exec "$@"
