#!/usr/bin/env bash

# Default workspace
WORKSPACE="/home/runner"

# Check if the Deep Learning disk exists
if [ -d "/mnt/disks/deeplearning" ]; then
  WORKSPACE="/mnt/disks/deeplearning/home/runner"
  
  # Ensure user_data directory is initialized
  freqtrade create-userdir --userdir "$WORKSPACE/user_data"
  
  # Authenticate with Google Cloud and get access token
  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { 
    echo "Failed to get token"; 
    exit 1; 
  }
  TOKEN=$(cat /tmp/token)

  # Fetch Freqtrade config (uncomment if needed)
  # curl -H "Authorization: Bearer $TOKEN" \
  #     "https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
  #     jq -r '.payload.data' | base64 --decode > $WORKSPACE/config.json
fi

# Ensure `config.json` exists and update Telegram settings
if [ ! -f "$WORKSPACE/config.json" ]; then
  jq '.telegram.enabled = true' /home/runner/config.json > "$WORKSPACE/config.json"
  rm -f /home/runner/config.json

  sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" "$WORKSPACE/config.json"
  sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" "$WORKSPACE/config.json"
fi

# Move user_data to the correct workspace (only if different)
if [ -d "/home/runner/user_data" ] && [ "$WORKSPACE/user_data" != "/home/runner/user_data" ]; then
  mv -f /home/runner/user_data "$WORKSPACE/user_data" 2>/dev/null || {
    echo "Move failed, falling back to copy."
    cp -r /home/runner/user_data/* "$WORKSPACE/user_data/"
    rm -rf /home/runner/user_data
  }
fi

# Ensure /freqtrade points to the correct workspace
ln -sfn "$WORKSPACE" /freqtrade
cd /freqtrade

# Start supervisord (only if NOT inside devcontainer setup)
if [ -z "$DEVCONTAINER" ]; then
  exec supervisord -c /etc/supervisor/supervisord.conf &
fi

# Execute the main process
exec "$@"
