#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
FEE=0.003322
STRATEGY=fibbo
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

hyperopt() {
    local timerange=$1
    local epochs=$2
    local loss=$3
    shift 3
    local spaces="$@"

    # Calculate start_date and end_date
    local end_date=$(date +"%Y%m%d")  # Today’s date
    local start_date=$(date -d "-${days} days" +"%Y%m%d")  # `days` ago

    # Run Freqtrade hyperopt with calculated timerange
    freqtrade hyperopt --timerange ${start_date}-${end_date} --epochs ${epochs} -j 4 \
      --spaces ${spaces} --ignore-missing-spaces --hyperopt-loss ${loss} \
      --analyze-per-epoch  --random-state 42 --logfile /dev/null > /dev/null 2>&1
}

calculate_score() {
  local json_file="$1"
  local key="$2"

  # Extract JSON data for the given strategy key
  local json_data=$(jq ".strategy_comparison[] | select(.key==\"$key\")" "$json_file")

  # Extract values
  local winrate=$(echo "$json_data" | jq -r '.winrate')
  local profit_total_pct=$(echo "$json_data" | jq -r '.profit_total_pct')
  local profit_sum=$(echo "$json_data" | jq -r '.profit_sum')
  local profit_total=$(echo "$json_data" | jq -r '.profit_total')
  local max_drawdown_account=$(echo "$json_data" | jq -r '.max_drawdown_account')
  local trade_count=$(echo "$json_data" | jq -r '.trades')

  # Prevent division by zero in profit factor calculation
  if (( $(echo "$profit_sum == $profit_total" | bc -l) )); then
      profit_factor=1
  else
      profit_factor=$(echo "scale=4; $profit_sum / ($profit_sum - $profit_total)" | bc)
  fi

  # Adjusted Winrate (subtracting drawdown)
  adjusted_winrate=$(echo "scale=4; $winrate - $max_drawdown_account" | bc)

  # Score Calculation
  winrate_score=$(echo "scale=4; $winrate * 100 * 0.3" | bc)
  profit_total_score=$(echo "scale=4; $profit_total_pct * 2" | bc)
  profit_factor_score=$(echo "scale=4; ($profit_factor - 1) * 200" | bc)
  max_drawdown_score=$(echo "scale=4; (10 - ($max_drawdown_account * 100)) * 2" | bc)
  trade_count_score=$(echo "scale=4; ($trade_count / 200) * 10" | bc)

  # Total Score Calculation
  total_score=$(echo "scale=2; $winrate_score + $profit_total_score + $profit_factor_score + $max_drawdown_score + $trade_count_score" | bc)

  # Return total score
  echo "$total_score"
}

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

elif [[ "${RERUN_RUNNER}" != "true" ]]; then

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

  echo -e "\n$hr\nRUN BACKTEST\n$hr"
  freqtrade backtesting --help
  rm -rf /home/runner/user_data/backtest_results/*
  freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

  cd /home/runner/user_data/backtest_results
  unzip $(ls -t backtest-result-*.zip | head -n 1) > /dev/null 2>&1
  LATEST_JSON=$(ls -t backtest-result-*.json | grep -v '.meta.json' | head -n 1)
  echo $(jq '.strategy_comparison' $LATEST_JSON)
  OLD_SCORE=$(calculate_score "$LATEST_JSON" "fibbo")
  echo $OLD_SCORE && cd /home/runner

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  freqtrade hyperopt --help
  #Ref: https://www.freqtrade.io/en/stable/hyperopt/#solving-a-mystery
  #freqtrade hyperopt -e 10 --fee=$FEE --timerange="$TB" --disable-param-export \
    #--spaces roi stoploss trailing protection trades --ignore-missing-spaces \
    #--analyze-per-epoch --random-state 42

  LOGURU_LEVEL=ERROR freqtrade hyperopt -e 500 --fee=$FEE --timerange="$TB" \
    --spaces buy sell --ignore-missing-spaces --analyze-per-epoch \
    --hyperopt-loss ProfitDrawDownHyperOptLoss --random-state 42 \
    --logfile /dev/null > /dev/null 2>&1

  # Step 1: Optimize buy, sell, and ROI logic
  #hyperopt 30 100 SharpeHyperOptLoss buy sell roi

  # Step 2: Optimize ROI, protection, and trailing for profit management
  #hyperopt 60 500 ShortTradeDurHyperOptLoss roi protection trailing

  # Step 3: Optimize protection, stoploss, and trade parameters
  #hyperopt 90 1000 OnlyProfitHyperOptLoss protection stoploss trades

  # Step 4: Refine protection, stoploss, and trailing parameters for risk management
  #hyperopt 120 1500 MaxDrawDownHyperOptLoss protection stoploss trailing

  # Step 5: Comprehensive optimization with all parameters
  #hyperopt 180 2500 ExpectancyHyperOptLoss all
  freqtrade hyperopt-list
  freqtrade hyperopt-show

  echo -e "\n$hr\nRERUN BACKTEST\n$hr"
  rm -rf /home/runner/user_data/backtest_results/*
  freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

  cd /home/runner/user_data/backtest_results
  unzip $(ls -t backtest-result-*.zip | head -n 1) > /dev/null 2>&1
  LATEST_JSON=$(ls -t backtest-result-*.json | grep -v '.meta.json' | head -n 1)
  echo $(jq '.strategy_comparison' $LATEST_JSON)
  NEW_SCORE=$(calculate_score "$LATEST_JSON" "fibbo")
  echo $NEW_SCORE && cd /home/runner

  LOGURU_LEVEL=ERROR freqtrade hyperopt -e 500 --fee=$FEE --timerange="$TB" \
    --spaces roi stoploss trailing protection trades --ignore-missing-spaces \
    --analyze-per-epoch --random-state 42 --logfile /dev/null > /dev/null 2>&1

  echo -e "\n$hr\nRERUN HYPEROPT\n$hr"
  freqtrade hyperopt-list
  freqtrade hyperopt-show

  echo -e "\n$hr\nFINAL BACKTEST\n$hr"
  rm -rf /home/runner/user_data/backtest_results/*
  freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

  cd /home/runner/user_data/backtest_results
  unzip $(ls -t backtest-result-*.zip | head -n 1) > /dev/null 2>&1
  LATEST_JSON=$(ls -t backtest-result-*.json | grep -v '.meta.json' | head -n 1)
  echo $(jq '.strategy_comparison' $LATEST_JSON)
  NEW_SCORE=$(calculate_score "$LATEST_JSON" "fibbo")
  echo $NEW_SCORE && cd /home/runner

  if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )); then
    PARAMS=.github/entrypoint/artifact/python/src/params/spaces.json
    git clone https://eq19:$TOKEN@github.com/eq19/eq19.git /tmp/eq19
    cat /home/runner/user_data/strategies/$STRATEGY.json > /tmp/eq19/$PARAMS
    #gh variable set RERUN_RUNNER --body "true"

    cd /tmp/eq19
    git config --global user.name eq19
    git config --global user.email eq19@users.noreply.github.com
    git add . && git commit --allow-empty -m "update params" && git push

    git clone --single-branch --branch gh-pages $REMOTE_REPO gh-pages && cd gh-pages
    git add . && git commit --allow-empty -m "RERUN_RUNNER due to job update" && git push
    #cd /home/runner && rm -rf /tmp/eq19
    exit 1
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

else

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
