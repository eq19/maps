#!/bin/bash

# Function to send a message to Telegram
send_telegram_message() {
    local message=$1
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="${message}" > /dev/null
}

# Monitor the log file and send updates to Telegram
tail -f /var/log/freqtrade.log | while read line; do
    send_telegram_message "$line"
done
