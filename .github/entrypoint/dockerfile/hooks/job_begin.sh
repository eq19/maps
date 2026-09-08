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

freqtrade_total_profit() {
  local PORT="$1"
  local MODE="$2"
  local USER="YourUsername"
  local PASS="YourPassword"
  local CONTAINER="mydb"
  
  # Get daily profit
  local DAILY
  DAILY=$(curl -s -u "$USER:$PASS" \
    "http://172.17.0.1:${PORT}/api/v1/daily" \
    | jq '[.data[].abs_profit // 0] | add // 0')
  
  # Get open profit
  local OPEN
  OPEN=$(curl -s -u "$USER:$PASS" \
    "http://172.17.0.1:${PORT}/api/v1/status" \
    | jq '[.[].profit_abs // 0] | add // 0')
  
  # Calculate total and set as global variable
  declare -g TOTAL
  TOTAL=$(echo "$DAILY + $OPEN" | bc -l)
  
  echo "Port      : $PORT ($MODE)"
  echo "Weekly PnL: $DAILY IDR"
  echo "Open PnL  : $OPEN IDR"
  echo "------------------------"
  echo "TOTAL     : $TOTAL IDR"
}

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
  RERUN_RUNNER=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
    "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/RERUN_RUNNER" | jq -r '.value')

  for ((i=1; i<=max_retries; i++)); do
    echo "Check $i of $max_retries..."

    if $DOCKER ps --format '{{.Names}}' | grep -wq "^mydb$"; then
      if [[ "$RERUN_RUNNER" == "true" ]]; then
        $DOCKER stop mydb
        echo "Waiting container stabilization..."
        sleep 20
        $DOCKER start mydb
      fi
      echo -e "\nCondition fulfilled ✅"

      echo -e "\n$hr\nDeepLearning Final Cloud\n$hr" && /mnt/disks/deeplearning/usr/bin/gcloud info
      echo -e "\n$hr\n" && /mnt/disks/deeplearning/usr/bin/gcloud info --run-diagnostics
  
      echo -e "\n$hr\nDeepLearning Docker info\n$hr" && $DOCKER info
      echo -e "\n$hr\n" && $DOCKER container ls -a

      # Setup freqtrade userdir for dry mode
      if ! $DOCKER exec mydb test -d "/home/runner/data_dry"; then
        $DOCKER exec mydb bash -c 'freqtrade create-userdir --userdir /home/runner/data_dry 2>/dev/null'
        $DOCKER exec mydb bash -c 'rm -rf /home/runner/data_dry/freqaimodels /home/runner/data_dry/ft_client'
        $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/freqaimodels /home/runner/data_dry/'
        $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/ft_client /home/runner/data_dry/'
      elif $DOCKER exec mydb supervisorctl status freqtrade_dry | grep -q "RUNNING"; then
        echo -e "\n$hr\nTotal Profit Dry-run vs Live Mode\n$hr"
        freqtrade_total_profit 8081 Dry
        TOTAL1=$TOTAL
      fi

      # Setup freqtrade userdir for live mode
      if ! $DOCKER exec mydb test -d "/home/runner/data_live"; then
        $DOCKER exec mydb bash -c 'freqtrade create-userdir --userdir /home/runner/data_live 2>/dev/null'
        $DOCKER exec mydb bash -c 'rm -rf /home/runner/data_live/freqaimodels /home/runner/data_live/ft_client'
        $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/freqaimodels /home/runner/data_live/'
        $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/ft_client /home/runner/data_live/'
      elif $DOCKER exec mydb supervisorctl status freqtrade_live | grep -q "RUNNING"; then
        echo -e "\n$hr\n"
        freqtrade_total_profit 8082 Live
        TOTAL2=$TOTAL

        if [ -n "$TOTAL1" ] && [ -n "$TOTAL2" ] && \
          [ $(echo "$TOTAL1 > 0" | bc) -eq 1 ] && \
          [ $(echo "$TOTAL1 > $TOTAL2" | bc) -eq 1 ]; then
          echo "Dry-run is better than Live mode"
          $DOCKER exec mydb supervisorctl stop freqtrade_dry || true
          $DOCKER exec mydb supervisorctl stop freqtrade_live || true
          $DOCKER exec mydb supervisorctl stop freqtrade_monitor || true

          $DOCKER exec mydb mv /home/runner/data_dry /home/runner/data_dry_
          $DOCKER exec mydb mv /home/runner/data_live /home/runner/data_live_
          $DOCKER exec mydb mv /home/runner/data_dry_ /home/runner/data_live
          $DOCKER exec mydb mv /home/runner/data_live_ /home/runner/data_dry

          # Directory "models" need to remain its zip files
          $DOCKER exec mydb mv /home/runner/data_dry/models /home/runner/data_dry_/models
          $DOCKER exec mydb mv /home/runner/data_live/models /home/runner/data_live_/models
          $DOCKER exec mydb mv /home/runner/data_dry_/models /home/runner/data_live/models
          $DOCKER exec mydb mv /home/runner/data_live_/models /home/runner/data_dry/models

          #$DOCKER exec mydb bash -c "find /home/runner/data_dry/models -type f -exec sed -i 's/data_live/data_dry/g' {} +"
          #$DOCKER exec mydb bash -c "find /home/runner/data_live/models -type f -exec sed -i 's/data_dry/data_live/g' {} +"

          $DOCKER exec mydb bash -c 'for folder in /home/runner/tradesv3_dry.*; do mv "$folder" "${folder/tradesv3_dry/tradesv3_dry_}"; done'
          $DOCKER exec mydb bash -c 'for folder in /home/runner/tradesv3_live.*; do mv "$folder" "${folder/tradesv3_live/tradesv3_live_}"; done'
          $DOCKER exec mydb bash -c 'for folder in /home/runner/tradesv3_dry_.*; do mv "$folder" "${folder/tradesv3_dry_/tradesv3_live}"; done'
          $DOCKER exec mydb bash -c 'for folder in /home/runner/tradesv3_live_.*; do mv "$folder" "${folder/tradesv3_live_/tradesv3_dry}"; done'
        else
          echo "Dry-run is not better than Live mode"
          $DOCKER exec mydb supervisorctl stop freqtrade_dry || true
          $DOCKER exec mydb bash -c 'rm -rf /home/runner/data_dry /home/runner/tradesv3_dry.*'
          $DOCKER exec mydb bash -c 'freqtrade create-userdir --userdir /home/runner/data_dry 2>/dev/null'
          $DOCKER exec mydb bash -c 'rm -rf /home/runner/data_dry/freqaimodels /home/runner/data_dry/ft_client'
          $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/freqaimodels /home/runner/data_dry/'
          $DOCKER exec mydb bash -c 'cp -a /home/runner/user_data/ft_client /home/runner/data_dry/'
        fi

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
