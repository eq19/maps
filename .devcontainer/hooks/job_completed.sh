#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------'

echo -e "\n$hr\nFinal Space\n$hr"
df -h

if [ -d /mnt/disks/Linux/usr/bin ]; then
  
  echo -e "\n$hr\nFinal Network\n$hr"
  /mnt/disks/Linux/usr/bin/docker network inspect bridge

fi

echo -e "\njob completed"
HEADER="Accept: application/vnd.github+json"
echo ${{ secrets.ACCESS_TOKEN }} | gh auth login --with-token
TOTAL_COUNT=$(gh api -H "${HEADER}" /repos/${REPO}/actions/runners --jq '.total_count')
RUNNER_ID=$(gh api -H "${HEADER}" /repos/${REPO}/actions/runners --jq '.runners.[].id')
if (( $TOTAL_COUNT != 0 )); then gh api --method DELETE -H "${HEADER}" /repos/${REPO}/actions/runners/${RUNNER_ID}; fi 
