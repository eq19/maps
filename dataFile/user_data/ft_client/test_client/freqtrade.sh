#!/bin/bash

# Function to send a message to Telegram
send_telegram_message() {
    local log_type=$1
    local message=$2
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="[$log_type] $message" > /dev/null
}

# Monitor the log files and send updates to Telegram
tail -f /home/runner/supervisord.log | while read line; do
    send_telegram_message "CONF" "$line"
done

# Send updates to Telegram in batches
logs=""
tail -f /var/log/freqtrade.log | while read line; do
    logs+="$line\n"
    if [[ $(echo "$logs" | wc -l) -ge 10 ]]; then
        send_telegram_message "LOGS" "$logs"
        logs=""
    fi
done

# Keep the script running
while true; do
    sleep 3600
done

# Handle graceful termination
trap "echo 'Terminating...'; exit" SIGINT SIGTERM
