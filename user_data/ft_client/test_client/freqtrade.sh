#!/bin/bash

# Define the function to send a Telegram message
LOG_FILE="/home/runner/data_live/logs/freqtrade.log"
rm -rf $LOG_FILE.* /home/runner/data_dry/logs/freqtrade.log.*

send_telegram_message() {
    local message="$1"
    local chat_id="TELEGRAM_CHAT_ID"
    local bot_token="WARNING_BOT_TOKEN"

    # Send the message via Telegram API
    curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
        -d chat_id="$chat_id" \
        -d text="$message" > /dev/null
}

# Check if the log file exists
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file not found at $LOG_FILE"
    exit 1
fi

# Monitor the entire log file and then continue monitoring new lines
cat "$LOG_FILE" | grep --line-buffered -iE "WARNING|ERROR|✅|⏳|📦|🔁|🔄|📎|🧾|🛠️|🔧|💤|⚠️|⛔" | while read -r line; do
    send_telegram_message "$line"
done

# Keep the freqtrade running using earlyoom
service earlyoom status > /dev/null 2>&1 || service earlyoom start

# Run the log monitoring command in the background
tail -f "$LOG_FILE" | grep --line-buffered -iE "WARNING|ERROR|✅|⏳|📦|🔁|🔄|📎|🧾|🛠️|🔧|💤|⚠️|⛔" | while read -r line; do
    send_telegram_message "$line"
done

# Capture the background process PID for later termination
TAIL_PID=$!

# Handle graceful termination
trap "echo 'Terminating...'; kill $TAIL_PID; exit" SIGINT SIGTERM
