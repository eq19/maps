uhh#!/usr/bin/env bash
#
# Structure: Cell Types – Modulo 6
# Ref: https://www.freqtrade.io/en/stable/utils/#list-freqai-models
# Ref: https://medium.com/@shanejones/how-i-set-up-freqtrade-a287db8966f
# Ref: https://github.com/ccxt/ccxt/blob/4.4.40/python/ccxt/async_support/indodax.py#L195
#
hr='------------------------------------------------------------------------------------'
CONFIG=user_data/config_examples/config_indodax.example.json
#CONFIG=user_data/config_examples/config_indodax.freqai.json

# Define the backtesting duration (in days)
BACKTESTING_DURATION=7  # Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)

# 30 days ago in the required format
EARLIEST_DATE=$(date -u -d "90 days ago" +%Y%m%d)

# Backtesting start date in the required format (earliest_date + sliding window)
BACKTESTING_START=$(date -u -d "$EARLIEST_DATE + $BACKTESTING_DURATION days" +%Y%m%d)

# Time range for downloading data
TD="$EARLIEST_DATE-$TODAY"

# Time range for backtesting
TB="$BACKTESTING_START-$TODAY"

# Print the timeranges
echo "Download Timerange: $TD"
echo "Backtesting Timerange: $TB"

echo -e "\n$hr\nTEST ENV\n$hr"
printenv

if [[ "$1" == "listing" ]]; then

  freqtrade list-exchanges
  #freqtrade edge --config $CONFIG
  #freqtrade hyperopt --config $CONFIG
  #freqtrade hyperopt-list --config $CONFIG
  #freqtrade hyperopt-show --config $CONFIG
  freqtrade list-markets --config $CONFIG
  #freqtrade list-pairs --config $CONFIG
  #freqtrade list-strategies --config $CONFIG
  #freqtrade list-freqaimodels --config $CONFIG
  #freqtrade show-trades --config $CONFIG
  #freqtrade convert-db --config $CONFIG
  #freqtrade install-ui --config $CONFIG
  #freqtrade plot-dataframe --config $CONFIG
  #freqtrade plot-profit --config $CONFIG
  #freqtrade webserver --config $CONFIG
  #freqtrade strategy-updater --config $CONFIG
  #freqtrade lookahead-analysis --config $CONFIG
  #freqtrade recursive-analysis --config $CONFIG

else

  echo -e "\n$hr\nTEST CLIENT\n$hr"
  python user_data/ft_client/test_client/test_client.py
        
  #echo -e "\n$hr\nSHOW CONFIG\n$hr"
  #freqtrade show-config --help
  #freqtrade show-config --config $CONFIG

  #echo -e "\n$hr\nTEST PAIR LIST\n$hr"
  #freqtrade test-pairlist --help
  #freqtrade test-pairlist --config $CONFIG

  echo -e "\n$hr\nTEST DOWNLOAD DATA\n$hr"
  freqtrade download-data --help
  #freqtrade download-data --config $CONFIG
  #freqtrade download-data --config $CONFIG --timeframes 1m 15m 30m 1h 1d
  freqtrade download-data --config $CONFIG --timeframes 1m 15m 30m 1h 1d --timerange="$TD"

  echo -e "\n$hr\nLIST DOWNLOAD DATA\n$hr"
  freqtrade list-data --help
  freqtrade list-data --config $CONFIG

  echo -e "\n$hr\nTEST BACKTEST\n$hr"
  freqtrade backtesting --help
  freqtrade backtesting --config $CONFIG --fee 0.003322 --timerange="$TB" --export signals
  #freqtrade backtesting --config $CONFIG --freqaimodel LightGBMRegressor --timerange="$TB" --export signals

  #echo -e "\n$hr\nBACKTEST RESULTS\n$hr"
  #ls -alR user_data/backtest_results

  #echo -e "\n$hr\nSHOW BACKTEST\n$hr"
  #freqtrade backtesting-show --help
  #freqtrade backtesting-show --config $CONFIG

  echo -e "\n$hr\nBACKTEST ANALYSIS\n$hr"
  freqtrade backtesting-analysis --help
  freqtrade backtesting-analysis --config $CONFIG --timerange="$TB" --indicator-list all

  echo -e "\n$hr\nBACKTEST AI TRADES\n$hr"
  #freqtrade trade --help

  #sed -i "s|your_exchange_key|$ACCESS_API|g" $CONFIG
  #sed -i "s|your_exchange_secret|$ACCESS_KEY|g" $CONFIG
  #sed -i "s|your_telegram_chat_id|$MESSAGE_API|g" $CONFIG
  #sed -i "s|your_telegram_token|$MESSAGE_TOKEN|g" $CONFIG

  #freqtrade trade --config $CONFIG --freqaimodel LightGBMRegressor
  #gh secret set CONFIG_JSON < $CONFIG
  #rm -rf $CONFIG
 
fi
