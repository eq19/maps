#!/bin/bash

# Path to your config.json
CONFIG_FILE="/home/runner/config.json"

# Extract Telegram bot token and chat ID from config.json
TELEGRAM_BOT_TOKEN=$(jq -r '.telegram.token' "$CONFIG_FILE")
TELEGRAM_CHAT_ID=$(jq -r '.telegram.chat_id' "$CONFIG_FILE")

# Ensure jq and configurations are valid
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Please install it and try again."
    exit 1
fi

if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]]; then
    echo "Telegram bot token or chat ID is missing in config.json."
    exit 1
fi

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
done

# Handle graceful termination
trap "echo 'Terminating...'; exit" SIGINT SIGTERM

wait
