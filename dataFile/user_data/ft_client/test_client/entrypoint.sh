#!/usr/bin/env bash

# Start Freqtrade in the background
if [ -d /mnt/disks/deeplearning ]; then
  echo "Deeplearning exists. Proceeding...";
  /mnt/disks/deeplearning/usr/bin/gcloud auth application-default print-access-token > /tmp/token || { echo "Failed to get token"; exit 1; };
  TOKEN=$(cat /tmp/token)
  curl -H "Authorization: Bearer $TOKEN" \
    "https://secretmanager.googleapis.com/v1/projects/feedmapping/secrets/freqtrade-config/versions/latest:access" | \
    jq -r '.payload.data' | base64 --decode > /home/runner/config.json
  freqtrade trade &
  docker-entrypoint.sh postgres
else
  "Deeplearning is not found.";
  docker-entrypoint.sh postgres
fi

# Start PostgreSQL in the foreground
exec docker-entrypoint.sh postgres
#exec supervisord -c /etc/supervisor/supervisord.conf
