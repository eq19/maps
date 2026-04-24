#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='----------------------------------------------------------------------------------'
FEE=0.003322
TIMEFRAMES='15m 1h'

STRATEGY=user_data/strategies/fibbo.json
HYPEROPT_PARAM=user_data/strategies/hyperopt_params.json
CONFIG=user_data/config_examples/config_basic.example.json
EDGEFILE=user_data/config_examples/config_edge.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERFILE=user_data/config_examples/config_hyperopt.example.json
EXCHANGE_FILE=user_data/config_examples/config_exchange.example.json
HYPERPY=venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

# Define the starting point of backtesting duration (in months)
BACKTESTING_DURATION=2  # In weeks. Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

# 30 days ago in the required format
EARLIEST_DATE=$(date -u -d "3 weeks ago" +%Y%m%d)

# Backtesting start date in the required format (earliest_date + sliding window)
BACKTESTING_START=$(date -u -d "$EARLIEST_DATE + $BACKTESTING_DURATION weeks" +%Y%m%d)

# Time range
TD="$EARLIEST_DATE-$TODAY"
TB="$BACKTESTING_START-$TODAY"

# Print the timeranges
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/functions.sh"
cat $CONFIG > user_data/config.json

# ENVIRONMENT
export PATH="venv/bin:$PATH"
export PYTHONPATH="user_data/strategies:user_data/freqaimodels:$PYTHONPATH"

if [[ "$GITHUB_JOB" == "lexering" ]]; then
  gh variable set JOB --body "${GITHUB_JOB}"
      
  # Read FreqAI models into an array
  mapfile -t MODELS < <(freqtrade list-freqaimodels --one-column | grep -v -E '^\s*$|INFO|matplotlib')
  CURRENT="${FREQAI_MODEL}"

  if [[ "$CURRENT" == "false" ]]; then
    # Set CURRENT to first model
    export FREQAI_MODEL="${MODELS[0]}"
    export FREQAI_NEXT="${MODELS[1]}"
    [[ "$REDUCE_EPOCH" == "false" ]] && export SCORE=100
  else
    # Find index of CURRENT in list
    index=-1
    for i in "${!MODELS[@]}"; do
      if [[ "${MODELS[$i]}" == "$CURRENT" ]]; then
        index=$i
        break
      fi
    done

    if [[ $index -lt 0 ]]; then
      echo "Current model '$CURRENT' not found in list!"
      exit 1
    fi

    # If not last element → NEXT = next model
    if (( index < ${#MODELS[@]} - 1 )); then
      export FREQAI_NEXT="${MODELS[$((index + 1))]}"
    else
      # Last model → NEXT = false
      export FREQAI_NEXT="false"
    fi
  fi
fi

if [[ "$1" != "hyperopt" ]]; then

  echo -e "\n$hr\nTEST CCXT\n$hr"
  python user_data/ft_client/test_client/test_client.py

  if [[ "$GITHUB_JOB" == "lexering" ]]; then
    #freqtrade show-trades
    #freqtrade convert-db 
    #freqtrade install-ui
    #freqtrade webserver

    #echo -e "\n$hr\nLIST MARKETS\n$hr"
    #freqtrade list-markets --help
    #freqtrade list-markets

    #echo -e "\n$hr\nLIST EXCHANGES\n$hr"
    #freqtrade list-exchanges --help
    #freqtrade list-exchanges

    echo -e "\n$hr\nSTRATEGIES\n$hr"
    freqtrade list-strategies --help
    freqtrade list-strategies
    #freqtrade list-strategies --recursive-strategy-search
    #freqtrade strategy-updater

    echo -e "\n$hr\nDOWNLOAD PAIRS\n$hr"
    freqtrade download-data --help
    freqtrade test-pairlist --one-column 2>/dev/null | tail -n +2 | jq -R . | jq -s . > pairs.json
    freqtrade download-data --pairs-file pairs.json --timeframes $TIMEFRAMES --timerange="$TD" --verbose
  fi

else

  echo -e "\n$hr\nLIST DATA\n$hr"
  echo "Download Timerange: $TD"
  echo "Backtesting Timerange: $TB"
  freqtrade list-data --help
  freqtrade list-data

  #echo -e "\n$hr\nSHOW EDGE\n$hr"
  #freqtrade edge --help
  pairs=$(gh variable get PAIRS)
  #jq --slurpfile new_edge $EDGEFILE '.edge = $new_edge[0].edge' $CONFIG > config.json
  jq '.pairlists = [{"method": "StaticPairList"}]' $PAIRFILE > tmp.json && mv tmp.json $PAIRFILE
  jq --argjson pairs "$pairs" '.exchange.pair_whitelist = $pairs' "$EXCHANGE_FILE" > config.tmp && mv config.tmp "$EXCHANGE_FILE"

  OLD_SCORE=$SCORE
  export CALCULATION="false"
  if [[ "$GITHUB_JOB" == "lexering" ]]; then
    echo -e "\n$hr\nAI TRADES with $FREQAI_MODEL\n$hr"
    nohup freqtrade trade --dry-run --freqaimodel $FREQAI_MODEL --fee=$FEE > freqtrade.log 2>&1 &
    echo $! > freqtrade_pid.txt

    # Open descriptor to log stream
    exec 3< <(tail -f freqtrade.log)

    while read -r LOGLINE <&3; do
      echo "$LOGLINE"
      # Stop if Freqtrade has entered RUNNING state
      #if [[ "$LOGLINE" == *"state='RUNNING'"* ]]; then
      if [[ "$LOGLINE" == *"Done training"* ]]; then
       echo "Stopping freqtrade trade..."
        PID=$(cat freqtrade_pid.txt)
        kill -SIGTERM $PID
        echo "freqtrade trade stopped."
        break
      fi
    done

    echo -e "\n$hr\nRUN BACKTEST with $FREQAI_MODEL\n$hr"
    freqtrade backtesting --help
    cat $STRATEGY > /tmp/store.json
    freqtrade backtesting --freqaimodel $FREQAI_MODEL --fee=$FEE --timerange="$TB" --enable-protections

    calculate_score
    if [[ "$SCORE" == "100" ]]; then
      gh workflow run "main.yml"
    else
      if [[ "$CALCULATION" != "false" ]]; then
        if [[ "$OLD_SCORE" == "100" ]]; then       
          gh variable set SCORE --body "${SCORE}"
          gh variable set FREQAIMODEL --body "${FREQAI_MODEL}"                 
        elif (( $(echo "$SCORE > $OLD_SCORE" | bc -l) )); then
          gh variable set SCORE --body "${SCORE}"
          gh variable set FREQAIMODEL --body "${FREQAI_MODEL}"                 
        fi
        export CALCULATION="false"
      fi
    fi

  fi
  echo -e "\n$hr\nRUN HYPEROPT with $FREQAI_MODEL\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt
  SCORE=$(gh variable get SCORE)
  freqtrade hyperopt --help
  OLD_SCORE=$SCORE            
  hyperopt $ID
fi
