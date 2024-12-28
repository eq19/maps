#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

cd ${{ github.workspace }}
python user_data/ft_client/test_client/test_client.py
        
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
freqtrade trade --config user_data/config_examples/config_indodax.example.json
