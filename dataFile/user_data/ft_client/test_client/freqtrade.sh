#!/bin/bash

# Path to your config.json
CONFIG_FILE="/home/runner/config.json"

# Extract Telegram bot token and chat ID from config.json
TELEGRAM_BOT_TOKEN=$(jq -r '.telegram.token' "$CONFIG_FILE")
TELEGRAM_CHAT_ID=$(jq -r '.telegram.chat_id' "$CONFIG_FILE")

# Function to send a message to Telegram
send_telegram_message() {
    local log_type=$1
    local message=$2
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d chat_id="${TELEGRAM_CHAT_ID}" \
    -d text="[$log_type] $message" > /dev/null
}

# Monitor the log files and send updates to Telegram
tail -f /var/log/freqtrade.log | while read line; do
    send_telegram_message "$line"
done

wait
