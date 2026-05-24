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

restart_mydb() {

  echo -e "\n$hr\nRestart mydb container\n$hr"
  $DOCKER restart mydb

  echo "Waiting container stabilization..."
  sleep 20

  $DOCKER exec mydb supervisorctl reread
  $DOCKER exec mydb supervisorctl update

  $DOCKER exec mydb supervisorctl start postgres || true
  $DOCKER exec mydb supervisorctl start freqtrade_dry || true
  $DOCKER exec mydb supervisorctl start freqtrade_live || true
  set_monitor

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

  if [[ "$RERUN_RUNNER" == "true" ]]; then

    echo "🚀 Start all applications."

    $DOCKER exec mydb supervisorctl reread
    $DOCKER exec mydb supervisorctl update

    $DOCKER exec mydb supervisorctl start postgres || true
    $DOCKER exec mydb supervisorctl start freqtrade_dry || true
    $DOCKER exec mydb supervisorctl start freqtrade_live || true

    set_monitor

  #Check if ✅ freqtrade_live is running
  elif $DOCKER exec mydb supervisorctl status freqtrade_live | grep -q "RUNNING"; then

    echo -e "\n$hr\nStart Network\n$hr"

    if [[ "$CONTAINER_NAME" == "runner1" ]]; then
      $DOCKER exec runner2 /home/runner/scripts/exitpoint.sh "$REMOVE_REPOSITORY" "$TARGET_REPOSITORY"
    elif [[ "$CONTAINER_NAME" == "runner2" ]]; then
      $DOCKER exec runner1 /home/runner/scripts/exitpoint.sh "$REMOVE_REPOSITORY" "$TARGET_REPOSITORY"
    fi

    echo "🌀 Reload all application's configs upon the updated configuration."
    restart_mydb

  else

    echo "🏃 Rerun all applications upon the given configuration."
    restart_mydb

  fi
fi
