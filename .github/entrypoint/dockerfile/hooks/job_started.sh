#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Action https://github.com/${REPO}/actions/runs/${RUN}

hr='----------------------------------------------------------------------------------'

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

  # Max retries
  max_retries=10
  # Interval between checks (10 retries in 10 minutes -> 60s each)
  interval=60

  # Path to docker binary
  DOCKER="/mnt/disks/deeplearning/usr/bin/docker"

  for ((i=1; i<=max_retries; i++)); do
    echo "Check $i of $max_retries..."

    if $DOCKER ps --format '{{.Names}}' | grep -wq "^mydb$"; then
      echo -e "\nCondition fulfilled ✅"

      echo -e "\n$hr\nDeepLearning Final Cloud\n$hr" && /mnt/disks/deeplearning/usr/bin/gcloud info
      echo -e "\n$hr\n" && /mnt/disks/deeplearning/usr/bin/gcloud info --run-diagnostics
  
      echo -e "\n$hr\nDeepLearning Docker info\n$hr" && $DOCKER info
      echo -e "\n$hr\n" && $DOCKER container ls -a

      # Setup freqtrade userdir for dry mode
      if ! $DOCKER exec mydb test -d "/home/runner/data_dry"; then
        $DOCKER exec mydb freqtrade create-userdir --userdir /home/runner/data_dry
        $DOCKER exec mydb mkdir -p /home/runner/data_dry/strategies/utils
      elif $DOCKER exec mydb supervisorctl status freqtrade_dry | grep -q "RUNNING"; then
        $DOCKER exec mydb supervisorctl stop freqtrade_dry || true
      fi

      # Setup freqtrade userdir for live mode
      if ! $DOCKER exec mydb test -d "/home/runner/data_live"; then
        $DOCKER exec mydb freqtrade create-userdir --userdir /home/runner/data_live
        $DOCKER exec mydb mkdir -p /home/runner/data_live/strategies/utils
      elif $DOCKER exec mydb supervisorctl status freqtrade_live | grep -q "RUNNING"; then
        $DOCKER exec mydb supervisorctl stop freqtrade_live || true
        $DOCKER exec mydb supervisorctl stop monitor_freqtrade || true to 
      fi

      exit 0
    fi

    if [ $i -lt $max_retries ]; then
      wait=$((i * interval))
      sleep $wait
    fi
  done

  echo "Condition not fulfilled after $max_retries checks ❌"
  gh workflow run "main.yml" --repo "$REPOSITORY" --raw-field "REMOVE_RUNNER=true"

fi
