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
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERFILE=user_data/config_examples/config_hyperopt.example.json
FREQAI_FILE=user_data/config_examples/config_freqai.example.json
EXCHANGE_FILE=user_data/config_examples/config_exchange.example.json
HYPERPY=venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

# Download vs Backtesting
EARLIEST_DATE=$(date -u -d "3 months ago" +%Y%m%d)
BACKTESTING_START=$(date -u -d "1 months ago" +%Y%m%d)

# Time range
TD="$EARLIEST_DATE-$TODAY"
TB="$BACKTESTING_START-$TODAY"

# Print the timeranges
HYPEROPT=${MATRIX_INPUT:-$(gh variable get HYPEROPT)}
FREQAI_MODEL=${MATRIX_INPUT:-$(gh variable get FREQAIMODEL)}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/functions.sh"
cat $CONFIG > user_data/config.json

# ENVIRONMENT
export PATH="venv/bin:$PATH"
export PYTHONPATH="user_data/strategies:user_data/freqaimodels:$PYTHONPATH"

if [[ "$1" != "Hyperopt" &&  "$1" != "FreqAI" ]]; then

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

    if [[ "$RUN_MODE" == "Hyperopt" ]]; then
      freqtrade list-hyperoptloss --help
      freqtrade list-hyperoptloss
    elif [[ "$RUN_MODE" == "FreqAI" ]]; then
      freqtrade list-freqaimodels --help
      freqtrade list-freqaimodels \
        --freqaimodel-path user_data/freqaimodels/resources \
        --freqaimodel-path user_data/freqaimodels/tradeflow \
        --freqaimodel-path user_data/freqaimodels/torch_models \
        --freqaimodel-path user_data/freqaimodels/tensorflow_models
       fi

    echo -e "\n$hr\nDOWNLOAD PAIRS ($TD)\n$hr"
    freqtrade download-data --help
    freqtrade test-pairlist --one-column 2>/dev/null | tail -n +2 | jq -R . | jq -s . > pairs.json
    freqtrade download-data --pairs-file pairs.json --timeframes $TIMEFRAMES --timerange="$TD" --verbose
    gh variable set PAIRS --body "$(cat pairs.json)"
  fi

elif [[ "$1" == "Hyperopt" ]]; then

  echo -e "\n$hr\nLIST DATA ($TIMEFRAMES)\n$hr"
  freqtrade list-data --help
  freqtrade list-data

  OLD_SCORE=$SCORE
  export CALCULATION="false"
  pairs=$(gh variable get PAIRS)
  jq '.freqai.enabled = false' "$FREQAI_FILE" > freqai.tmp && mv freqai.tmp "$FREQAI_FILE"
  jq '.pairlists = [{"method": "StaticPairList"}]' $PAIRFILE > tmp.json && mv tmp.json $PAIRFILE  
  jq --argjson pairs "$pairs" '.exchange.pair_whitelist = $pairs' "$EXCHANGE_FILE" > config.tmp && mv config.tmp "$EXCHANGE_FILE"

  if [[ "$GITHUB_JOB" == "lexering" ]]; then

    echo -e "\n$hr\nRUN BACKTEST ($TB) without FREQAI_MODEL\n$hr" && freqtrade backtesting --help
    #freqtrade backtesting --fee=$FEE --enable-dynamic-pairlist --freqai-backtest-live-models
    freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

    calculate_score
    if [[ "$SCORE" == "100" ]]; then
      gh workflow run "main.yml"
    else
      if [[ "$CALCULATION" != "false" ]]; then
        if [[ "$OLD_SCORE" == "100" ]]; then       
          gh variable set SCORE --body "${SCORE}"
        elif (( $(echo "$SCORE > $OLD_SCORE" | bc -l) )); then
          cat $STRATEGY
          gh variable set SCORE --body "${SCORE}"
        fi
        export CALCULATION="false"
      fi
    fi

  fi

  echo -e "\n$hr\nRUN HYPEROPT ($EARLIEST_DATE-$BACKTESTING_START) without FREQAI_MODEL\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt
  SCORE=$(gh variable get SCORE)
  freqtrade hyperopt --help
  OLD_SCORE=$SCORE            
  hyperopt $ID

elif [[ "$1" == "FreqAI" ]]; then

  freqai $ID

fi
