#!/bin/bash

# Function to send a message to Telegram
send_telegram_message() {
    local message=$1
    # https://www.freqtrade.io/en/stable/faq/#how-do-i-search-the-bot-logs-for-something
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="$message" > /dev/null
}

# Monitor the log files and send updates to Telegram
# https://www.freqtrade.io/en/2023.11/advanced-setup/#logging-to-syslog
tail -f /var/log/freqtrade.log | while read line; do
    send_telegram_message "$line"
done &

# Keep the script running
while true; do
    sleep 3600
done

# Handle graceful termination
trap "echo 'Terminating...'; exit" SIGINT SIGTERM
