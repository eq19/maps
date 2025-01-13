#!/usr/bin/env bash

# Check the Deeplearning 
if [ -d /mnt/disks/deeplearning ]; then
  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { echo "Failed to get token"; exit 1; };
  TOKEN=$(cat /tmp/token)
  curl -H "Authorization: Bearer $TOKEN" \
    "https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
    jq -r '.payload.data' | base64 --decode > /home/runner/config.json
else
  "Deeplearning is not found.";
fi

# Run PostgreSQL (autostart) and Freqtrade (cpu low)
exec supervisord -c /etc/supervisor/supervisord.conf
