#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------'

if [ -d /opt/hostedtoolcache ]; then
  
  echo -e "\n$hr\nFinal Agent\n$hr"
  ls -al /opt/hostedtoolcache

fi

echo "\njob completed"
echo -e "\n$hr\nFinal Space\n$hr"
df -h
