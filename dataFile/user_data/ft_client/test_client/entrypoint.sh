#!/usr/bin/env bash

CONFIG=/home/runner/user_data/config.json
if [ -f /home/runner/user_data/config.json ]; then
  #sed -i "s|your_exchange_key|${ACCESS_API}|g" $CONFIG
  #sed -i "s|your_exchange_secret|${ACCESS_KEY}|g" $CONFIG
  sed -i "s|your_telegram_token|$MONITOR_BOT_TOKEN|g" $CONFIG
  sed -i "s|your_telegram_chat_id|$TELEGRAM_CHAT_ID|g" $CONFIG
  jq '.telegram.enabled = true' $CONFIG > tmp.json && mv tmp.json $CONFIG
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
  
