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
