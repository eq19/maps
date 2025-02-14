#!/bin/bash

# Define the function to send a Telegram message
send_telegram_message() {
    local message="$1"
    local bot_token="$WARNING_BOT_TOKEN"
    local chat_id="$TELEGRAM_CHAT_ID"

    # Ensure required environment variables are set
    if [[ -z "$bot_token" || -z "$chat_id" ]]; then
        echo "Error: WARNING_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables are not set."
        exit 1
    fi

    # Send the message via Telegram API
    curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
        -d chat_id="$chat_id" \
        -d text="$message" > /dev/null
}

# Check if the log file exists
if [[ ! -f "/mnt/disks/deeplearning/var/log/apt/freqtrade.log" ]]; then
    echo "Error: Log file not found at /mnt/disks/deeplearning/var/log/apt/freqtrade.log"
    exit 1
fi

# Run the log monitoring command in the background
tail -f "/mnt/disks/deeplearning/var/log/apt/freqtrade.log" | \
grep --line-buffered -iE "WARNING|ERROR" | \
while read -r line; do
    send_telegram_message "$line"
done

# Capture the background process PID for later termination
TAIL_PID=$!

# Keep the script running
#while true; do sleep 3600; done

# Handle graceful termination
trap "echo 'Terminating...'; kill $TAIL_PID; exit" SIGINT SIGTERM
