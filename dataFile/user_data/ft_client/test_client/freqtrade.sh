#!/bin/bash

# Function to send a message to Telegram
send_telegram_message() {
    local message=$1
    # Set timezone to Jakarta and get the current timestamp
    local timestamp=$(TZ='Asia/Jakarta' date +"%Y-%m-%d %H:%M:%S")
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="[${timestamp}] $message" > /dev/null
}

# Monitor the log files and send updates to Telegram in batches
logs=""
tail -f /var/log/freqtrade.log | while read line; do
    logs+="$line\n"
    if [[ $(echo "$logs" | wc -l) -ge 10 ]]; then
        send_telegram_message "$logs"
        logs=""
    fi
done &  # Run the monitoring loop in the background

# Keep the script running
while true; do
    sleep 3600
done

# Handle graceful termination
trap "echo 'Terminating...'; exit" SIGINT SIGTERM
