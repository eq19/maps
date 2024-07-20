#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Action https://github.com/${REPO}/actions/runs/${RUN}

hr='------------------------------------------'

echo -e "\n$hr\nGroups\n$hr"
getent group

echo -e "\n$hr\nAll users\n$hr"
getent passwd

echo -e "\n$hr\nIdentity\n$hr"
whoami
echo "build 10003"
pwd
id

echo -e "\n$hr\nService Status\n$hr"
service --status-all

echo -e "\n$hr\nSupervisor\n$hr"
apt-cache show supervisor

echo -e "\n$hr\nLocate Initdb\n$hr"
locate initdb

echo -e "\n$hr\nEnvironment\n$hr"
printenv

echo -e "\n$hr\nDB Cluster\n$hr"
/etc/init.d/postgresql restart
