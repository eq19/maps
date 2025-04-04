#!/usr/bin/env bash

# Setup freqtrade config.json
CONFIG=/home/runner/user_data/config.json
if [ -f /home/runner/user_data/config.json ]; then
  #sed -i "s|your_exchange_key|${ACCESS_API}|g" $CONFIG
  #sed -i "s|your_exchange_secret|${ACCESS_KEY}|g" $CONFIG
  sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" $CONFIG
  sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" $CONFIG
  jq '.telegram.enabled = true' $CONFIG > tmp.json && mv tmp.json $CONFIG
fi

# Configure earlyoom
ARGS=/etc/default/earlyoom
if [ -f /etc/default/earlyoom ]; then
  sed -i 's|firefox|freqtrade|g' $ARGS
  sed -i 's|X|postgres|g' $ARGS
  sed -i 's|init|supervisorctl|g' $ARGS
  # EARLYOOM_ARGS="--avoid '(^|/)(init|X|sshd|firefox)$'"
  sed -i 's|# EARLYOOM_ARGS="--avoid|EARLYOOM_ARGS="-m 5 -s 20 --avoid|g' $ARGS
fi

# Check the Deeplearning 
if [ ! -d /mnt/disks/deeplearning ]; then
  echo "Deeplearning is not found."
else
  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { echo "Failed to get token"; exit 1; };
  TOKEN=$(cat /tmp/token)
  #curl -H "Authorization: Bearer $TOKEN" \
    #"https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
    #jq -r '.payload.data' | base64 --decode > $CONFIG
fi

# Check if the line already exists in the crontab
NEW_LINE="0 * * * * supervisorctl stop monitor_freqtrade && supervisorctl start monitor_freqtrade"
if ! crontab -l | grep -Fxq "$NEW_LINE"; then
  # If the line does not exist, add it
  (crontab -l 2>/dev/null; echo "$NEW_LINE") | crontab -
  echo "Crontab updated with the new line: $NEW_LINE"
else
  echo "The line already exists in the crontab. No changes made."
fi

# Run PostgreSQL (autostart)
exec supervisord -c /etc/supervisor/supervisord.conf

# Continue with the original entrypoint process
exec "$@"
