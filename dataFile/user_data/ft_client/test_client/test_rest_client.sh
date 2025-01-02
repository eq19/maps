#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Ref: https://github.com/ccxt/ccxt/blob/4.4.40/python/ccxt/async_support/indodax.py#L195

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nTEST ENV\n$hr"
printenv

echo -e "\n$hr\nTEST CLIENT\n$hr"
#cd ${{ github.workspace }}/user_data/build_helpers && ./install_ta-lib.sh > /dev/null 2>&1
python /home/runner/user_data/ft_client/test_client/test_client.py
        
echo -e "\n$hr\nTEST NOTIFICATION\n$hr"
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
CONFIG=/home/runner/config.json

freqtrade download-data --config $CONFIG --timeframes 1m 15m
freqtrade list-data --config $CONFIG
freqtrade backtesting --config $CONFIG
#freqtrade backtesting-show --config $CONFIG
#freqtrade backtesting-analysis --config $CONFIG
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
#freqtrade trade --config $CONFIG

cp $CONFIG config.json
