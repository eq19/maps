#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Ref: https://github.com/ccxt/ccxt/blob/4.4.40/python/ccxt/async_support/indodax.py#L195

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nTEST CCXT\n$hr"

#cd ${{ github.workspace }}/user_data/build_helpers && ./install_ta-lib.sh > /dev/null 2>&1
python user_data/ft_client/test_client/test_client.py
        
echo -e "\n$hr\nTEST CHAT\n$hr"
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
freqtrade trade --config user_data/config_examples/config_indodax.example.json
