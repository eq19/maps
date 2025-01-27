#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
FEE=0.003322
STRATEGY=ichiV1
#TIMEFRAMES='1m 5m'
TIMEFRAMES='15m 1h 1d'
CONFIG=user_data/config_examples/config_indodax.example.json
PARAMS=user_data/config_examples/config_params.example.json
EDGEFILE=user_data/config_examples/config_edge.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERPY=/home/runner/venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

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

echo -e "\n$hr\nTEST ENVIRONMENT\n$hr"
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

  echo -e "\n$hr\nTEST CCXT\n$hr"
  python user_data/ft_client/test_client/test_client.py

  echo -e "\n$hr\nTEST DOWNLOAD\n$hr"
  freqtrade download-data --help
  #sed -i "s|ichi|$STRATEGY|g" $CONFIG
  #freqtrade download-data --config $CONFIG
  #freqtrade download-data --config $CONFIG --timerange="$TD"
  freqtrade download-data --config $CONFIG --timeframes $TIMEFRAMES --timerange="$TD"

  echo -e "\n$hr\nLIST DATA\n$hr"
  freqtrade list-data --help
  freqtrade list-data --config $CONFIG

  #echo -e "\n$hr\nSHOW EDGE\n$hr"
  #freqtrade edge --help
  #sed -i "s|ichi|ichiV1_Marius|g" $CONFIG
  #jq --slurpfile new_edge $EDGEFILE '.edge = $new_edge[0].edge' $CONFIG > config.json
  #freqtrade edge --fee=$FEE

  echo -e "\n$hr\nRUN BACKTESTING\n$hr"
  freqtrade backtesting --help
  [[ ! -f user_data/strategies/$STRATEGY.json ]] && mv -f $PARAMS user_data/strategies/$STRATEGY.json
  freqtrade backtesting --config $CONFIG --fee=$FEE --timerange="$TB" --export signals
  #freqtrade backtesting --config $CONFIG --freqaimodel LightGBMRegressor --timerange="$TB" --export signals

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  freqtrade hyperopt --help
  #freqtrade hyperopt-list --config $CONFIG
  #freqtrade hyperopt-show --config $CONFIG
  #Ref: https://www.freqtrade.io/en/stable/hyperopt/#solving-a-mystery
  #sed -i "s|if params.get(FTHYPT_FILEVERSION, 1) >= 2 and not config.get(\"disableparamexport\", False):|logger.warning(f'{params.get(FTHYPT_FILEVERSION, 1)} and {config.get(\"disableparamexport\", False)}')|g" $HYPERPY
  #sed -i "s|# Export parameters ...|logger.warning(f'{HyperoptTools.get_strategy_filename(config, strategy_name)}')|g" $HYPERPY && cat $HYPERPY
  freqtrade hyperopt --config $CONFIG -e 10 --fee=$FEE --hyperopt-loss SharpeHyperOptLossDaily

  echo -e "\n$hr\nRERUN BACKTEST\n$hr"
  cat user_data/strategies/$STRATEGY.json
  echo -e "\n$hr\n" && freqtrade backtesting --help
  freqtrade backtesting --config $CONFIG --fee=$FEE --timerange="$TB" --export signals

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
  #sed -i "s|ichiV1_Marius|$STRATEGY|g" $CONFIG
  sed -i "s|your_exchange_key|$ACCESS_API|g" $CONFIG
  sed -i "s|your_exchange_secret|$ACCESS_KEY|g" $CONFIG
  sed -i "s|your_telegram_chat_id|$MESSAGE_API|g" $CONFIG
  sed -i "s|your_telegram_token|$MESSAGE_TOKEN|g" $CONFIG

  cd /home/runner
  jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json
  #gh secret set CONFIG_JSON < config.json

  echo "Starting freqtrade trade..."
  #freqtrade trade --freqaimodel LightGBMRegressor
  nohup freqtrade trade --dry-run --fee=$FEE > freqtrade.log 2>&1 &
  echo $! > freqtrade_pid.txt
  tail -f freqtrade.log | while read LOGLINE
  do
    echo "$LOGLINE"
    if [[ "${LOGLINE}" == *"state='RUNNING'"* ]]; then
      echo "Stopping freqtrade trade..."
      PID=$(cat freqtrade_pid.txt)
      kill -SIGTERM $PID
      echo "freqtrade trade stopped."
      break
    fi
  done  
  rm -rf *.json freqtrade_pid.txt freqtrade.log

  #echo -e "\n$hr\nPLOT DATAFRAME\n$hr"
  #freqtrade plot-dataframe --config $CONFIG
  #freqtrade plot-profit --config $CONFIG --timerange="$TB"

fi
