#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# Ref: https://github.com/ccxt/ccxt/blob/4.4.40/python/ccxt/async_support/indodax.py#L195

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nTEST CLIENT\n$hr"

#cd ${{ github.workspace }}/user_data/build_helpers && ./install_ta-lib.sh > /dev/null 2>&1
python user_data/ft_client/test_client/test_client.py
        
echo -e "\n$hr\nTEST NOTIFICATION\n$hr"
#Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
#freqtrade trade --config user_data/config_examples/config_indodax.example.json
#freqtrade list-pairs --config user_data/config_examples/config_indodax.example.json
#freqtrade backtesting         Backtesting module.
#freqtrade backtesting-show    Show past Backtest results
#freqtrade backtesting-analysis Backtest Analysis module.
#freqtrade edge                Edge module.
#freqtrade hyperopt            Hyperopt module.
#freqtrade hyperopt-list       List Hyperopt results
#freqtrade hyperopt-show       Show details of Hyperopt results
#freqtrade list-exchanges      Print available exchanges.
#freqtrade list-markets        Print markets on exchange.
#freqtrade list-pairs          Print pairs on exchange.
#freqtrade list-strategies     Print available strategies.
#freqtrade list-freqaimodels   Print available freqAI models.
#freqtrade list-timeframes     Print available timeframes for the exchange.
#freqtrade show-trades         Show trades.
#freqtrade test-pairlist       Test your pairlist configuration.
#freqtrade convert-db          Migrate database to different system
#freqtrade install-ui          Install FreqUI
#freqtrade plot-dataframe      Plot candles with indicators.
#freqtrade plot-profit         Generate plot showing profits.
#freqtrade webserver           Webserver module.
#freqtrade strategy-updater    updates outdated strategy files to the current version
#freqtrade lookahead-analysis  Check for potential look ahead bias.
#freqtrade recursive-analysis  Check
