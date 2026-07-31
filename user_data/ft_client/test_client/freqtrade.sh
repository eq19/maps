#!/bin/bash

# Define performance
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


# Define the function to send a Telegram message
send_telegram_message() {
  local message="$1"
  local chat_id="TELEGRAM_CHAT_ID"
  local bot_token="WARNING_BOT_TOKEN"

  # Send the message via Telegram API
  curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
    -d chat_id="$chat_id" \
    -d text="$message" > /dev/null
}


if supervisorctl status freqtrade_live | grep -q "RUNNING"; then

  if curl -s -u "YourUsername:YourPassword" \
    "http://172.17.0.1:8082/api/v1/show_config" \
    | jq -e '.state == "running"' >/dev/null; then

    LOG_FILE="/home/runner/data_live/logs/freqtrade.log"
    rm -rf "$LOG_FILE".* /home/runner/data_dry/logs/freqtrade.log.*

  else

    LOG_FILE="/home/runner/data_dry/logs/freqtrade.log"
    rm -rf "$LOG_FILE".* /home/runner/data_live/logs/freqtrade.log.*

  fi

else

  LOG_FILE="/home/runner/data_dry/logs/freqtrade.log"
  rm -rf "$LOG_FILE".* /home/runner/data_live/logs/freqtrade.log.*

fi

# Check if the log file exists
if [[ ! -f "$LOG_FILE" ]]; then
  echo "Error: Log file not found at $LOG_FILE"
  exit 1
fi

# Monitor the entire log file and then continue monitoring new lines
cat "$LOG_FILE" | grep --line-buffered -iE "WARNING|ERROR|✅|♻️|⏳|📦|🔁|🔂|🔄|📎|🧾|ℹ️|🛠️|🔧|💤|⚙️|⚠️|🔥|🚫|⛔|❌" | while read -r line; do
  send_telegram_message "$line"
done

# Keep the freqtrade running using earlyoom
service earlyoom status > /dev/null 2>&1 || service earlyoom start

# Run the log monitoring command in the background
tail -f "$LOG_FILE" | grep --line-buffered -iE "WARNING|ERROR|✅|♻️|⏳|📦|🔁|🔂|🔄|📎|🧾|ℹ️|🛠️|🔧|💤|⚙️|⚠️|🔥|🚫|⛔|❌" | while read -r line; do
  send_telegram_message "$line"
done

# Capture the background process PID for later termination
TAIL_PID=$!

# Handle graceful termination
trap "echo 'Terminating...'; kill $TAIL_PID; exit" SIGINT SIGTERM
