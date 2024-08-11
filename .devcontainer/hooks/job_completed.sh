#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nFinal Space\n$hr"
df -h

if [ -d /mnt/disks/platform/usr/bin ]; then
  
  echo -e "\n$hr\nFinal Cloud\n$hr"
  /mnt/disks/platform/usr/bin/gcloud info
  
  echo -e "\n$hr\nFinal Network\n$hr"
  /mnt/disks/platform/usr/bin/docker network inspect bridge

fi

echo -e "\njob completed"
HEADER="Accept: application/vnd.github+json"
echo ${GITHUB_ACCESS_TOKEN} | gh auth login --with-token
TOTAL_COUNT=$(gh api -H "${HEADER}" /repos/${GITHUB_REPOSITORY}/actions/runners --jq '.total_count')
RUNNER_ID=$(gh api -H "${HEADER}" /repos/${GITHUB_REPOSITORY}/actions/runners --jq '.runners.[].id')
#if (( $TOTAL_COUNT != 0 )); then gh api --method DELETE -H "${HEADER}" /repos/${GITHUB_REPOSITORY}/actions/runners/${RUNNER_ID}; fi 
