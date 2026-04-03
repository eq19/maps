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

  # Print results
  echo "FREQAI_MODEL=${FREQAI_MODEL}"
  echo "FREQAI_NEXT=${FREQAI_NEXT}"
fi

if [[ "$1" != "hyperopt" ]]; then

  #echo -e "\n$hr\nLIST EXCHANGES\n$hr"
  #freqtrade list-exchanges --help
  #freqtrade list-exchanges

  #echo -e "\n$hr\nLIST MARKETS\n$hr"
  #freqtrade list-markets --help
  #freqtrade list-markets

  echo -e "\n$hr\nSTRATEGIES\n$hr"
  freqtrade list-strategies --help
  freqtrade list-strategies
  #freqtrade list-strategies --recursive-strategy-search
  #freqtrade strategy-updater

  #freqtrade show-trades
  #freqtrade convert-db 
  #freqtrade install-ui
  #freqtrade webserver

  echo -e "\n$hr\nTEST PAIRLIST\n$hr"
  freqtrade test-pairlist --help
  #freqtrade test-pairlist --one-column --print-json

  if [[ "$GITHUB_JOB" == "lexering" ]]; then
    echo -e "\n$hr\nTEST CCXT\n$hr"
    python user_data/ft_client/test_client/test_client.py

    echo -e "\n$hr\nAI TRADES with $FREQAI_MODEL\n$hr"
    freqtrade trade --help && echo "Starting freqtrade trade..."
    nohup freqtrade trade --dry-run --freqaimodel $FREQAI_MODEL --fee=$FEE > freqtrade.log 2>&1 &
    echo $! > freqtrade_pid.txt

    # Open descriptor to log stream
    exec 3< <(tail -f freqtrade.log)

    inside_pairs_block=false
    full_pairs_line=""

    while read -r LOGLINE <&3; do
      echo "$LOGLINE"

      # Detect the start of pair whitelist
      if [[ "$LOGLINE" == *"Whitelist with"* && "$LOGLINE" == *"pairs:"* ]]; then
        inside_pairs_block=true
        full_pairs_line="$LOGLINE"
        # Check if closing bracket already present
        if [[ "$LOGLINE" == *"]" ]]; then
          inside_pairs_block=false
        fi
        continue
      fi

      # Collect remaining lines if pair list is split
      if $inside_pairs_block; then
        full_pairs_line+="$LOGLINE"
        if [[ "$LOGLINE" == *"]" ]]; then
          inside_pairs_block=false
        fi
      fi

      # Stop if Freqtrade has entered RUNNING state
      if [[ "$LOGLINE" == *"state='RUNNING'"* ]]; then
        echo "Stopping freqtrade trade..."
        PID=$(cat freqtrade_pid.txt)
        kill -SIGTERM $PID
        echo "freqtrade trade stopped."
        break
      fi
    done

    # Extract the JSON from the full_pairs_line
    pairs=$(echo "$full_pairs_line" | sed -n "s/.*pairs: \(\[.*\]\).*/\1/p" | tr -d '\n' | sed "s/'/\"/g")

    # Validate and update config
    if [[ -z "$pairs" ]]; then
      echo "❌ No pairs found in the log. Last line was:"
      echo "$full_pairs_line"
    else
      jq --argjson pairs "$pairs" '.exchange.pair_whitelist = $pairs' "$EXCHANGE_FILE" > config.tmp && mv config.tmp "$EXCHANGE_FILE"
      echo "✅ Updated pair whitelist in $EXCHANGE_FILE"
      gh variable set PAIRS --body "$pairs"
    fi

    echo -e "\n$hr\nDOWNLOAD PAIRS\n$hr"
    freqtrade download-data --help
    freqtrade download-data --timeframes $TIMEFRAMES --timerange="$(date -u -d "3 months ago" +%Y%m%d)-$(date -u +%Y%m%d)" --verbose
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

  export CALCULATION="false"
  if [[ "$SCORE" == "100" ]]; then
    FREQAIMODEL=$(gh variable get FREQAIMODEL)
    echo -e "\n$hr\nRUN BACKTEST with $FREQAIMODEL\n$hr"
    freqtrade backtesting --help
    cat $STRATEGY > /tmp/store.json
    #rm -rf user_data/backtest_results/*
    freqtrade backtesting --freqaimodel $FREQAIMODEL --fee=$FEE --timerange="$TB" --enable-protections
    calculate_score
  fi
  
  OLD_SCORE=$SCORE
  if [[ "$GITHUB_JOB" == "lexering" ]]; then
    if [[ "$OLD_SCORE" == "100" ]]; then
      gh workflow run "main.yml"
    else
      if [[ "$CALCULATION" != "false" ]]; then
        gh variable set SCORE --body "${SCORE}"
        export CALCULATION="false"
      fi
    fi
  fi

  echo -e "\n$hr\nRUN HYPEROPT with $FREQAI_MODEL\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt
  freqtrade hyperopt --help
  hyperopt $ID
fi
