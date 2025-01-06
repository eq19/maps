#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Ref: https://github.com/ccxt/ccxt/blob/4.4.40/python/ccxt/async_support/indodax.py#L195

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nTEST ENV\n$hr"
printenv

echo -e "\n$hr\nTEST CLIENT\n$hr"
python user_data/ft_client/test_client/test_client.py
        
echo -e "\n$hr\nTEST NOTIFICATION\n$hr"
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
CONFIG=user_data/config_examples/config_indodax.example.json

echo -e "\n$hr\nTEST DOWNLOAD DATA\n$hr"
freqtrade download-data --config $CONFIG --timeframes 1m 15m
echo -e "\n$hr\nLIST DOWNLOAD DATA\n$hr"
freqtrade list-data --config $CONFIG

echo -e "\n$hr\nTEST BACKTEST\n$hr"
freqtrade backtesting --config $CONFIG
echo -e "\n$hr\nBACKTEST RESULTS\n$hr"
ls -alR user_data/backtest_results
echo -e "\n$hr\nSHOW BACKTEST\n$hr"
freqtrade backtesting-show --config $CONFIG
echo -e "\n$hr\nBACKTEST ANALYSIS\n$hr"
freqtrade backtesting-analysis --config $CONFIG

#freqtrade edge --config $CONFIG
#freqtrade hyperopt --config $CONFIG
#freqtrade hyperopt-list --config $CONFIG
#freqtrade hyperopt-show --config $CONFIG
#freqtrade list-markets --config $CONFIG
#freqtrade list-pairs --config $CONFIG
#freqtrade list-strategies --config $CONFIG
#freqtrade list-freqaimodels --config $CONFIG
#freqtrade list-timeframes --config $CONFIG
#freqtrade show-trades --config $CONFIG
#freqtrade test-pairlist --config $CONFIG
#freqtrade convert-db --config $CONFIG
#freqtrade install-ui --config $CONFIG
#freqtrade plot-dataframe --config $CONFIG
#freqtrade plot-profit --config $CONFIG
#freqtrade webserver --config $CONFIG
#freqtrade strategy-updater --config $CONFIG
#freqtrade lookahead-analysis --config $CONFIG
#freqtrade recursive-analysis --config $CONFIG

#sed -i "s|your_exchange_key|$ACCESS_API|g" $CONFIG
#sed -i "s|your_exchange_secret|$ACCESS_KEY|g" $CONFIG
#sed -i "s|your_telegram_chat_id|$MESSAGE_API|g" $CONFIG
#sed -i "s|your_telegram_token|$MESSAGE_TOKEN|g" $CONFIG

#gh secret set CONFIG_JSON < $CONFIG
#rm -rf $CONFIG
