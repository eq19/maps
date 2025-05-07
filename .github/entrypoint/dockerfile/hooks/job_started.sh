#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Action https://github.com/${REPO}/actions/runs/${RUN}

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nGroups\n$hr"
getent group

echo -e "\n$hr\nService Status\n$hr"
service --status-all

echo -e "\n$hr\nOperation System\n$hr"
cat /etc/os-release

echo -e "\n$hr\nIdentity\n$hr"
whoami
id
ls -al $HOME

echo -e "\n$hr\nDisk Structure\n$hr"
df -h

echo -e "\n$hr\nSystemd Files\n$hr"
ls -al /host/etc/systemd/system

echo -e "\n$hr\nRunner 🏠 dir\n$hr"
if [ -d /home/runner/_site ]; then
  if [[ -f /home/runner/_site/.env ]]; then set -a && . /home/runner/_site/.env && set +a; fi
  rm -rf /mnt/disks/deeplearning/tmp/_site && mv -f /home/runner/_site /mnt/disks/deeplearning/tmp
  cd /mnt/disks/deeplearning/tmp/_site && rm -rf README.md docs .git .github .env .ssh .cache node-modules
fi
cd /home/runner && ls -al .

echo -e "\n$hr\nCloud-config Logs\n$hr"
curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/user-data" \
  -H "Metadata-Flavor: Google" -o cloud-config.yml
#Expected one of --config-file, --system or --docs arguments
sudo cloud-init schema --config-file cloud-config.yml
pwd && cat cloud-config.yml
echo -e "\n$hr\n"
grep -i error /host/var/log/cloud-init.log
echo -e "\n$hr\n"
cat /host/var/log/cloud-init.log
echo -e "\n$hr\n"
cat /host/var/log/cloud-init-output.log

echo -e "\n$hr\nSupervisor\n$hr"
apt-cache show supervisor

echo -e "\n$hr\nAll users\n$hr"
getent passwd

echo -e "\n$hr\nEnvironment\n$hr"
printenv | sort

echo -e "\n$hr\nPackage List\n$hr"
dpkg -l | sort

echo -e "\n$hr\nExecutables\n$hr"
find ${PATH//:/ } -maxdepth 1 -executable | sort

if [ -d /mnt/disks/deeplearning/usr/local/sbin ]; then
  
  echo -e "\n$hr\n"
  find /mnt/disks/deeplearning -maxdepth 3 -executable | sort 
  
  echo -e "\n$hr\nDeepLearning Packages\n$hr"
  /mnt/disks/deeplearning/usr/bin/dpkg -l | sort

  echo -e "\n$hr\nDeepLearning Docker info\n$hr"
  /mnt/disks/deeplearning/usr/bin/docker info
  
  echo -e "\n$hr\nDeepLearning Final Cloud\n$hr"
  /mnt/disks/deeplearning/usr/bin/gcloud info
  echo -e "\n$hr\n"
  /mnt/disks/deeplearning/usr/bin/gcloud info --run-diagnostics
  
  echo -e "\n$hr\nDeepLearning Docker containers\n$hr"
  /mnt/disks/deeplearning/usr/bin/docker container ls -a

  #echo -e "\n$hr\nDeepLearning Locate Python\n$hr" 
  #find /mnt/disks/eeplearning -type d -name '*python*' | sort

  #echo -e "\n$hr\nDeepLearning Python Modules\n$hr"
  #/mnt/disks/deeplearning/usr/bin/python3 -c 'help("modules")'

  #echo -e "\n$hr\nDeepLearning Tensorflow\n$hr"
  #find /mnt/disks/deeplearning -type d -name "tensorflow*" | sort

  #echo -e "\n$hr\nDeepLearning Locate Requirements\n$hr" 
  #locate requirements.txt
  #echo -e "\n$hr\n"
  #find /mnt/disks/deeplearning -type f -name "requirements*.txt" | sort

  #echo -e "\n$hr\nDeepLearning Dockerfile\n$hr"
  #find / -type f -name "Dockerfile" | sort

  #echo -e "\n$hr\nDeepLearning Locate Terraform\n$hr" 
  #find /mnt/disks/deeplearning -type d -name '*terraform*' | sort

fi      
