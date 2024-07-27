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
echo "build 10011"
pwd
id

echo -e "\n$hr\nService Status\n$hr"
service --status-all

echo -e "\n$hr\nOperation System\n$hr"
cat /etc/os-release

echo -e "\n$hr\nSupervisor\n$hr"
apt-cache show supervisor

echo -e "\n$hr\nLocate Initdb\n$hr"
locate python

echo -e "\n$hr\nEnvironment\n$hr"
printenv

echo -e "\n$hr\nDB Cluster\n$hr"
#/etc/init.d/postgresql restart

echo -e "\n$hr\nDisk Structure\n$hr"
df -h

echo -e "\n$hr\nExecutables\n$hr"
find ${PATH//:/ } -maxdepth 1 -executable | sort
find /mnt/disks/Linux/bin -maxdepth 1 -executable | sort
find /mnt/disks/Linux/sbin -maxdepth 1 -executable | sort
find /mnt/disks/Linux/usr/bin -maxdepth 1 -executable | sort
find /mnt/disks/Linux/usr/local/bin -maxdepth 1 -executable | sort
find /mnt/disks/Linux/usr/local/sbin -maxdepth 1 -executable | sort
find /mnt/disks/Linux/usr/sbin -maxdepth 1 -executable | sort

echo -e "\n$hr\nDockerfile\n$hr"
#find / -type f -name "Dockerfile"

echo -e "\n$hr\nTensorflow\n$hr"
