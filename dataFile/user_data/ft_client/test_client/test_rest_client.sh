yg#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
FEE=0.003322
STRATEGY=ichiV1
TIMEFRAMES='1m 15m'
EDGEFILE=user_data/config_examples/config_edge.example.json
CONFIG=user_data/config_examples/config_exchange.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERPY=/home/runner/venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

# Define the backtesting duration (in days)
BACKTESTING_DURATION=6  # Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

# 30 days ago in the required format
EARLIEST_DATE=$(date -u -d "9 days ago" +%Y%m%d)

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

  #freqtrade show-trades
  #freqtrade convert-db 
  #freqtrade install-ui
  #freqtrade webserver

  echo -e "\n$hr\nTEST PAIRLIST\n$hr"
  freqtrade test-pairlist --help
  freqtrade test-pairlist --one-column --print-json

  echo -e "\n$hr\nSTRATEGIES\n$hr"
  freqtrade list-strategies --help
  freqtrade list-strategies
  #freqtrade strategy-updater

else

  echo -e "\n$hr\nTEST CCXT\n$hr"
  python user_data/ft_client/test_client/test_client.py

  echo -e "\n$hr\nTEST DOWNLOAD\n$hr"
  freqtrade download-data --help
  freqtrade download-data --timeframes $TIMEFRAMES --timerange="$TD"

  echo -e "\n$hr\nLIST DATA\n$hr"
  freqtrade list-data --help
  freqtrade list-data

  #echo -e "\n$hr\nSHOW EDGE\n$hr"
  #freqtrade edge --help
  #jq --slurpfile new_edge $EDGEFILE '.edge = $new_edge[0].edge' $CONFIG > config.json
  #freqtrade edge --fee=$FEE

  echo -e "\n$hr\nRUN BACKTESTING\n$hr"
  freqtrade backtesting --help
  freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  freqtrade hyperopt --help
  #freqtrade hyperopt-list
  #freqtrade hyperopt-show
  #Ref: https://www.freqtrade.io/en/stable/hyperopt/#solving-a-mystery
  #freqtrade hyperopt --hyperopt-loss SharpeHyperOptLossDaily -e 500
  freqtrade hyperopt --fee=$FEE --timerange="$TB" --spaces all --random-state 42 -e 30

  echo -e "\n$hr\nRERUN HYPEROPT\n$hr"
  freqtrade hyperopt --fee=$FEE --timerange="$TB" --spaces all --random-state 42 \
    -e 300 --hyperopt-loss ProfitDrawDownHyperOptLoss --log-level CRITICAL > /dev/null 2>&1

  echo -e "\n$hr\nRERUN BACKTEST\n$hr"
  freqtrade backtesting --help
  freqtrade backtesting --fee=$FEE --timerange="$TB" --export signals

  if [[ -f /home/runner/user_data/strategies/$STRATEGY.json ]]; then
    PARAMS=.github/entrypoint/artifact/python/src/params/spaces.json
    git clone https://eq19:$TOKEN@github.com/eq19/eq19.git /tmp/eq19
    cat /home/runner/user_data/strategies/$STRATEGY.json > /tmp/eq19/$PARAMS

    cd /tmp/eq19
    git config --global user.name eq19
    git config --global user.email eq19@users.noreply.github.com
    git add . && git commit --allow-empty -m "update params" && git push
    cd /home/runner && rm -rf /tmp/eq19
  fi

  #echo -e "\n$hr\nANALYSIS\n$hr"
  #freqtrade backtesting-analysis --help
  #freqtrade lookahead-analysis
  #freqtrade recursive-analysis
  #freqtrade backtesting-analysis --timerange="$TB" --indicator-list all
  jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json
  
  #echo -e "\n$hr\nAI MODELS\n$hr"
  #freqtrade list-freqaimodels --help
  #freqtrade list-freqaimodels

  echo -e "\n$hr\nAI TRADES\n$hr"
  freqtrade trade --help

  #sed -i "s|your_exchange_key|$ACCESS_API|g" config.json
  #sed -i "s|your_exchange_secret|$ACCESS_KEY|g" config.json
  #sed -i "s|your_telegram_chat_id|$MESSAGE_API|g" config.json
  #sed -i "s|your_telegram_token|$MESSAGE_TOKEN|g" config.json

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

  #echo -e "\n$hr\nPLOT DATAFRAME\n$hr"
  #freqtrade plot-dataframe
  #freqtrade plot-profit --timerange="$TB"

  rm -rf *.json freqtrade_pid.txt freqtrade.log
  
fi
