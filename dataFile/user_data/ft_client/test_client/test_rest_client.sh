#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

cd ${GITHUB_WORKSPACE}/user_data/config_examples
sed -i "s|your_exchange_key|${ACCESS_API}|g" *.json
sed -i "s|your_exchange_secret|${ACCESS_KEY}|g" *.json
sed -i "s|your_telegram_chat_id|${MESSAGE_API}|g" *.json
sed -i "s|your_telegram_token|${MESSAGE_TOKEN}|g" *.json

cd ${GITHUB_WORKSPACE}
python user_data/ft_client/test_client/test_client.py
        
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
freqtrade trade --config user_data/config_examples/config_indodax.example.json
