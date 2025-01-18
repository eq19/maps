#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
FEE=0.003322
STRATEGY=ichiV1
TIMEFRAME='15m 1h 1d'
CONFIG=user_data/config_examples/config_indodax.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json

# Define the backtesting duration (in days)
BACKTESTING_DURATION=30  # Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

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

  echo -e "\n$hr\nLIST EXCHANGES\n$hr"
  freqtrade list-exchanges -- help
  freqtrade list-exchanges

  #freqtrade show-trades --config $CONFIG
  #freqtrade convert-db --config $CONFIG
  #freqtrade install-ui --config $CONFIG
  #freqtrade webserver --config $CONFIG

  echo -e "\n$hr\nSHOW PAIRS\n$hr"
  freqtrade list-pairs --help
  freqtrade list-pairs --config $CONFIG

  echo -e "\n$hr\nSTRATEGIES\n$hr"
  freqtrade list-strategies --help
  freqtrade list-strategies --config $CONFIG
  #freqtrade strategy-updater --config $CONFIG

else

  echo -e "\n$hr\nTEST CLIENT\n$hr"
  python user_data/ft_client/test_client/test_client.py
        
  sed -i "s|ichi|$STRATEGY|g" $CONFIG
  
  echo -e "\n$hr\nTEST DOWNLOAD\n$hr"
  freqtrade download-data --help
  #freqtrade download-data --config $CONFIG
  #freqtrade download-data --config $CONFIG --timeframes 1m 15m 30m 1h 1d
  freqtrade download-data --config $CONFIG --timeframes $TIMEFRAME --timerange="$TD"

  echo -e "\n$hr\nLIST DATA\n$hr"
  freqtrade list-data --help
  freqtrade list-data --config $CONFIG

  echo -e "\n$hr\nRUN BACKTESTING\n$hr"
  freqtrade backtesting --help
  freqtrade backtesting --config $CONFIG --fee=$FEE --timerange="$TB" --export signals
  #freqtrade backtesting --config $CONFIG --freqaimodel LightGBMRegressor --timerange="$TB" --export signals

  sed -i "s|$STRATEGY|ichiV1_Marius|g" $CONFIG

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  freqtrade hyperopt --help
  freqtrade hyperopt-list --config $CONFIG
  freqtrade hyperopt-show --config $CONFIG
  #Ref: https://www.freqtrade.io/en/stable/hyperopt/#solving-a-mystery
  freqtrade hyperopt --config $CONFIG --fee=$FEE --hyperopt-loss SharpeHyperOptLossDaily

  echo -e "\n$hr\nSHOW EDGE\n$hr"
  freqtrade edge --help
  freqtrade edge --config $CONFIG --fee=$FEE

  echo -e "\n$hr\nRERUN BACKTEST\n$hr"
  freqtrade backtesting --help
  freqtrade backtesting --config $CONFIG --fee=$FEE

  #echo -e "\n$hr\nANALYSIS\n$hr"
  #freqtrade backtesting-analysis --help
  #freqtrade lookahead-analysis --config $CONFIG
  #freqtrade recursive-analysis --config $CONFIG
  #freqtrade backtesting-analysis --config $CONFIG --timerange="$TB" --indicator-list all

  #echo -e "\n$hr\nAI MODELS\n$hr"
  #freqtrade list-freqaimodels --help
  #freqtrade list-freqaimodels --config $CONFIG

  echo -e "\n$hr\nAI TRADES\n$hr"
  freqtrade trade --help
  cd /home/runner
  jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json

  #gh secret set CONFIG_JSON < config.json
  sed -i "s|your_exchange_key|$ACCESS_API|g" config.json
  sed -i "s|your_exchange_secret|$ACCESS_KEY|g" config.json
  sed -i "s|your_telegram_chat_id|$MESSAGE_API|g" config.json
  sed -i "s|your_telegram_token|$MESSAGE_TOKEN|g" config.json

  #freqtrade trade --freqaimodel LightGBMRegressor
  freqtrade trade --dry-run --fee=$FEE
  #freqtrade trade
  rm -rf *.json

  #echo -e "\n$hr\nPLOT DATAFRAME\n$hr"
  #freqtrade plot-dataframe --config $CONFIG
  #freqtrade plot-profit --config $CONFIG --timerange="$TB"

fi
