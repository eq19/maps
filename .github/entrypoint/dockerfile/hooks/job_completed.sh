#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nFinal Space\n$hr"
df -h

if [ -d /mnt/disks/deeplearning/usr/local/sbin ]; then

  echo -e "\n$hr\nDocker images\n$hr"
  /mnt/disks/deeplearning/usr/bin/docker image ls

  echo -e "\n$hr\nNetwork images\n$hr"
  /mnt/disks/deeplearning/usr/bin/docker network inspect bridge

  RERUN_RUNNER=$(curl -s \
    -H "Authorization: token $GITHUB_ACCESS_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')

  TARGET_REPOSITORY=$(curl -s \
    -H "Authorization: token $GITHUB_ACCESS_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/TARGET_REPOSITORY" | jq -r '.value')

  echo -e "\n$hr\nStart Network\n$hr"
  if [[ "$RERUN_RUNNER" == "true" ]]; then
    /mnt/disks/deeplearning/usr/bin/docker exec mydb supervisorctl start freqtrade
    /mnt/disks/deeplearning/usr/bin/docker exec mydb service cron start
  else
    if [[ "$CONTAINER_NAME" == "runner1" ]]; then
      /mnt/disks/deeplearning/usr/bin/docker exec runner2 /home/runner/scripts/exitpoint.sh $TARGET_REPOSITORY
    elif [[ "$CONTAINER_NAME" == "runner2" ]]; then
      /mnt/disks/deeplearning/usr/bin/docker exec runner1 /home/runner/scripts/exitpoint.sh $TARGET_REPOSITORY
    fi
  fi

fi

echo -e "\njob completed"
