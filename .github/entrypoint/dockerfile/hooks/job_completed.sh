#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

set -Eeuo pipefail

hr='----------------------------------------------------------------------------------'

DOCKER="/mnt/disks/deeplearning/usr/bin/docker"
FILE_PATH="/home/runner/data_live/logs/freqtrade.log"

echo -e "\n$hr\nFinal Space\n$hr"
df -h

set_monitor() {
  # Max retries
  max_retries=10
  # Interval between checks
  interval=60

  for ((i=1; i<=max_retries; i++)); do
    echo "Check $i of $max_retries..."

    if $DOCKER exec mydb test -f "$FILE_PATH"; then

      $DOCKER exec mydb supervisorctl start freqtrade_monitor || true
      $DOCKER exec mydb service cron start || true

      echo -e "\n$hr\nSupervisor Status\n$hr"
      $DOCKER exec mydb supervisorctl status || true

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

  #Check if ✅ target runner is exist 
  TARGET_REPOSITORY=$(curl -s \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/TARGET_REPOSITORY" | jq -r '.value')

  TOTAL_COUNT=$(curl -s \
    -H "Authorization: token $GH_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${TARGET_REPOSITORY}/actions/runners" | jq '.total_count')
  
  if [[ "$TOTAL_COUNT" -eq 0 ]]; then

    echo -e "\n$hr\nStart Network\n$hr"
    REMOVE_REPOSITORY=$(curl -s \
      -H "Authorization: token $GH_TOKEN" \
      -H "Accept: application/vnd.github.v3+json" \
      "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/REMOVE_REPOSITORY" | jq -r '.value')

    if [[ "$CONTAINER_NAME" == "runner1" ]]; then
      $DOCKER exec runner2 /home/runner/scripts/exitpoint.sh "$REMOVE_REPOSITORY" "$TARGET_REPOSITORY"
    elif [[ "$CONTAINER_NAME" == "runner2" ]]; then
      $DOCKER exec runner1 /home/runner/scripts/exitpoint.sh "$REMOVE_REPOSITORY" "$TARGET_REPOSITORY"
    fi

  fi

  echo -e "\n$hr\nRestart all applications\n$hr"
  $DOCKER exec mydb supervisorctl reread
  $DOCKER exec mydb supervisorctl update

  $DOCKER exec mydb supervisorctl start postgres || true
  $DOCKER exec mydb supervisorctl start freqtrade_dry || true
  $DOCKER exec mydb supervisorctl start freqtrade_live || true

  set_monitor

fi
