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
pwd
id

echo -e "\n$hr\nOperation System\n$hr"
cat /etc/os-release

echo -e "\n$hr\nDisk Structure\n$hr"
df -h

echo -e "\n$hr\nService Status\n$hr"
service --status-all

echo -e "\n$hr\nSupervisor\n$hr"
apt-cache show supervisor

echo -e "\n$hr\nEnvironment\n$hr"
printenv | sort

echo -e "\n$hr\nExecutables\n$hr"
find ${PATH//:/ } -maxdepth 1 -executable | sort

if [ -d /mnt/disks/Linux/usr/local/sbin ]; then
  
  echo -e "\n$hr\n"
  find /mnt/disks/Linux -maxdepth 3 -executable | sort 
  
  #echo -e "\n$hr\nPackage List\n$hr"
  #/mnt/disks/Linux/usr/bin/dpkg -l | sort

  #echo -e "\n$hr\nPython Modules\n$hr"
  #/mnt/disks/Linux/usr/bin/python3 -c 'help("modules")'

  #echo -e "\n$hr\nLocate Python\n$hr" 
  #find /mnt/disks/Linux -type d -name '*python*' | sort

  #echo -e "\n$hr\nTensorflow\n$hr"
  #find /mnt/disks/Linux -type d -name "tensorflow*" | sort

  #echo -e "\n$hr\nLocate Requirements\n$hr" 
  #locate requirements.txt
  #echo -e "\n$hr\n"
  #find /mnt/disks/Linux -type f -name "requirements*.txt" | sort

  #echo -e "\n$hr\nDockerfile\n$hr"
  #find / -type f -name "Dockerfile" | sort

  #echo -e "\n$hr\nLocate SQL\n$hr" 
  #find /mnt/disks/Linux -type f -name "*.sql" | sort

  echo -e "\n$hr\nWorkdir\n$hr"
  ls -alR /home/runner/_w

fi        
