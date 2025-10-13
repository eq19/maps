#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='----------------------------------------------------------------------------------'
CONTAINER="mydb"
APP="freqtrade_live"
DOCKER="/mnt/disks/deeplearning/usr/bin/docker"
FILE_PATH="/home/runner/data_live/logs/freqtrade.log"

echo -e "\n$hr\nFinal Space\n$hr"
df -h

set_monitor() {
  # Max retries
  max_retries=10
  # Interval between checks (10 retries in 10 minutes -> 60s each)
  interval=60

  for ((i=1; i<=max_retries; i++)); do
    echo "Check $i of $max_retries..."

    if $DOCKER exec mydb test -f "$FILE_PATH"; then
      $DOCKER exec mydb supervisorctl start monitor_freqtrade
      $DOCKER exec mydb service cron start

      echo -e "\n$hr\nMemory Usage\n$hr"
      $DOCKER exec mydb free -h

      echo -e "\n$hr\njob completed ✅"
      exit 0
    fi

    if [ $i -lt $max_retries ]; then
      wait=$((i * interval))
      sleep $wait
    fi
  done
}

if [ -d /mnt/disks/deeplearning/usr/local/sbin ]; then

  echo -e "\n$hr\nDocker images\n$hr"
  $DOCKER image ls

  echo -e "\n$hr\nNetwork images\n$hr"
  $DOCKER network inspect bridge

  RERUN_RUNNER=$(curl -s \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')

  REMOVE_REPOSITORY=$(curl -s \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/REMOVE_REPOSITORY" | jq -r '.value')

  TARGET_REPOSITORY=$(curl -s \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/TARGET_REPOSITORY" | jq -r '.value')

  echo -e "\n$hr\nStart Network\n$hr"
  $DOCKER exec mydb supervisorctl reread
  $DOCKER exec mydb supervisorctl update
  if [[ "$RERUN_RUNNER" == "true" ]]; then
    echo "🚀 Run all applications upon the given configuration."
    $DOCKER exec mydb supervisorctl start freqtrade_dry
    $DOCKER exec mydb supervisorctl start freqtrade_live
    set_monitor

  #Check if ✅ $APP is running inside $CONTAINER
  elif $DOCKER ps --format '{{.Names}}' | grep -q "^${CONTAINER}$" && \
    $DOCKER exec "$CONTAINER" supervisorctl status "$APP" | grep -q "RUNNING"; then

    if [[ "$CONTAINER_NAME" == "runner1" ]]; then
      $DOCKER exec runner2 /home/runner/scripts/exitpoint.sh $REMOVE_REPOSITORY $TARGET_REPOSITORY
    elif [[ "$CONTAINER_NAME" == "runner2" ]]; then
      $DOCKER exec runner1 /home/runner/scripts/exitpoint.sh $REMOVE_REPOSITORY $TARGET_REPOSITORY
    fi

  else
    # Optionally restart:
    # docker start "$CONTAINER" && docker exec "$CONTAINER" supervisorctl start "$APP"
    echo "🌀 Rerun all applications upon the updated configuration."
    $DOCKER exec mydb supervisorctl start freqtrade_dry
    $DOCKER exec mydb supervisorctl start freqtrade_live
    set_monitor
  fi
fi
