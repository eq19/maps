#!/bin/bash

# Define the function to send a Telegram message
send_telegram_message() {
    local message="$1"
    local bot_token="$WARNING_BOT_TOKEN"
    local chat_id="$TELEGRAM_CHAT_ID"
    
    # https://www.freqtrade.io/en/stable/faq/#how-do-i-search-the-bot-logs-for-something
    curl -s -X POST "https://api.telegram.org/bot$bot_token/sendMessage" \
        -d chat_id="$chat_id" \
        -d text="$message" > /dev/null
}

# Run the log monitoring command in the background
tail -f /mnt/disks/deeplearning/var/log/apt/freqtrade.log | \
grep --line-buffered -iE "WARNING|ERROR" | \
while read -r line; do
    send_telegram_message "$line"
done &

# Keep the script running
while true; do
    sleep 3600
done

# Handle graceful termination
trap "echo 'Terminating...'; exit" SIGINT SIGTERM
