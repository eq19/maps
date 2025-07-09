#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
FEE=0.003322
[[ -z "${SCORE+x}" ]] && SCORE=100
STRATEGY=user_data/strategies/fibbo.json
HYPEROPT_PARAM=user_data/strategies/hyperopt_params.json
EDGEFILE=user_data/config_examples/config_edge.example.json
CONFIG=user_data/config_examples/config_exchange.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERFILE=user_data/config_examples/config_hyperopt.example.json
HYPERPY=venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

# Define the backtesting duration (in days)
BACKTESTING_DURATION=2  # Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

# 30 days ago in the required format
EARLIEST_DATE=$(date -u -d "13 days ago" +%Y%m%d)

# Backtesting start date in the required format (earliest_date + sliding window)
BACKTESTING_START=$(date -u -d "$EARLIEST_DATE + $BACKTESTING_DURATION days" +%Y%m%d)

# Time range for downloading data
TD="$EARLIEST_DATE-$TODAY"

# Time range for backtesting
TB="$BACKTESTING_START-$TODAY"

# Print the timeranges
echo "Download Timerange: $TD"
echo "Backtesting Timerange: $TB"

#echo -e "\n$hr\nTEST ENVIRONMENT\n$hr"
export PATH="venv/bin:$PATH"
#printenv

hyperopt() {

  # Load JSON and filter by given ID
  jq -c --argjson ids "[$(echo "$*" | sed 's/ /,/g')]" '.pipelines[] | select(.id as $id | $ids | index($id))' $HYPERFILE | while read -r pipeline; do
    end_date=$(date +"%Y%m%d")
    days=$(echo "$pipeline" | jq -r '.days')
    start_date=$(date -d "$days days ago" +"%Y%m%d")

    id=$(echo "$pipeline" | jq -r '.id')
    epochs=$(echo "$pipeline" | jq -r '.epochs')
    loss=$(echo "$pipeline" | jq -r '.hyperopt_loss')

    # dispatch only for main workflow 
    if [[ "$GITHUB_JOB" == "lexering" ]]; then
      spaces=$(echo "$pipeline" | jq -r '.spaces[]')  # One space per line
    fi

    # empty spaces if unset
    for space in ${spaces:-}; do
      # Extract params as raw JSON
      #params=$(jq -c --arg key "$space" '.span[$key]' "$HYPEROPT_PARAM")
      params=$(jq -r --arg key "$space" '.. | objects | select(has("span")) | .span[$key] | keys' "$HYPEROPT_PARAM")
  
      if [[ "$params" == "null" ]]; then
        echo "Warning: No params found for space '$space'"
        continue
      fi

      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$(jq -n \
          --arg ref "$DEFAULT_BRANCH" \
          --argjson params "$params" \
          --arg runId "$GITHUB_RUN_ID" \
          --arg score "$SCORE" \
          --arg epochs "$epochs" \
          --arg space "$space" \
          --arg loss "$loss" \
          '{ref: $ref, inputs: {
           matrix_json: (
             {
               loss: $loss,
               space: $space,
               score: $score,
               run_id: $runId,
               epochs: $epochs,
               params: $params
             } | @json
           )
         }}')" \
       "https://api.github.com/repos/$GITHUB_REPOSITORY/actions/workflows/matrix.yml/dispatches"
    done

    [[ "$GITHUB_JOB" == "lexering" ]] && epochs=$((epochs * 10))
    spaces=$(echo "$pipeline" | jq -r '.spaces | join(" ")')  # Space-separated

    # Disable protections if 'all' or 'protection' is in the spaces
    if [[ "$spaces" =~ (^|[[:space:]])(all|protection)($|[[:space:]]) ]]; then
        enable_protections=""
        prot="disable"
    else
        enable_protections="--enable-protections"
        prot="enable"
    fi

    echo -e "\n$hr\nID: $id 👉 Running $loss\nSpaces: $spaces | Days: $days | Epochs: $epochs | Protection: $prot\n$hr"
    freqtrade hyperopt --timerange ${start_date}-${end_date} --epochs ${epochs} -j 4 \
      --spaces ${spaces} --ignore-missing-spaces --hyperopt-loss ${loss} \
      ${enable_protections} --analyze-per-epoch --random-state ${id} \
      --fee=$FEE --logfile /dev/null > /dev/null 2>&1 #--print-json
    freqtrade hyperopt-list

    echo -e "\n$hr\nRERUN BACKTEST\n$hr"
    freqtrade backtesting --help
    #rm -rf user_data/backtest_results/*
    freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections
  
    calculate_score
    NEW_SCORE=$SCORE
    echo "NEW SCORE: $NEW_SCORE"
    OLD_SCORE=$(gh variable get SCORE)

    if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )); then
      cat $STRATEGY
      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
         https://api.github.com/repos/$( [[ "$GITHUB_JOB" == "lexering" ]] && echo "$TARGET_REPOSITORY" || echo "$GITHUB_REPOSITORY" )/actions/variables/PARAMS_JSON
      gh variable set SCORE --body "${NEW_SCORE}" && gh variable set JOB --body "${GITHUB_JOB}"
    elif (( $(echo "$NEW_SCORE < $OLD_SCORE" | bc -l) )); then
      if [[ "$GITHUB_JOB" == "lexering" ]] && [[ "$(gh variable get JOB)" != "lexering" ]]; then 
        gh workflow run "main.yml"
      fi
    fi
  done
}

calculate_score() {
  sleep 5
  local dir="user_data/backtest_results"
  local latest_zip=$(ls -t "$dir/backtest-result-"*.zip 2>/dev/null | head -n 1)
  if [[ -z "$latest_zip" ]]; then
    echo "No ZIP file found in $dir"
    return 1
  fi
  unzip -q "$latest_zip" -d "$dir"

  local json_file=$(ls -t "$dir/backtest-result-"*.json | grep -v '.meta.json' | head -n 1)
  if [[ -z "$json_file" ]]; then
    echo "No JSON file found in $dir"
    return 1
  fi

  local json_data=$(jq ".strategy_comparison[] | select(.key==\"fibbo\")" "$json_file")
  if [[ -z "$json_data" ]]; then
    echo "No data found for key: fibbo"
    return 1
  else
    echo "$json_data" | jq .
    rm -rf "$dir"/*
  fi

  local winrate=$(echo "$json_data" | jq -r '.winrate')
  local profit_mean_pct=$(echo "$json_data" | jq -r '.profit_mean_pct')
  local profit_total_pct=$(echo "$json_data" | jq -r '.profit_total_pct')
  local max_drawdown_account=$(echo "$json_data" | jq -r '.max_drawdown_account')
  local trades=$(echo "$json_data" | jq -r '.trades')

  # Sanity check
  if [[ -z "$winrate" || -z "$profit_mean_pct" || -z "$profit_total_pct" || -z "$max_drawdown_account" || -z "$trades" ]]; then
    echo "Missing one or more required values."
    return 1
  fi

  # Cap values
  profit_mean_pct=$(echo "$profit_mean_pct > 0.25" | bc -l) && [[ "$profit_mean_pct" -eq 1 ]] && profit_mean_pct=0.25
  local winrate_score=$(echo "$winrate * 25" | bc -l)
  local profit_per_trade_score=$(echo "$profit_mean_pct * 100" | bc -l)
  if (( $(echo "$profit_per_trade_score > 25" | bc -l) )); then
    profit_per_trade_score=25
  fi
  local profit_total_score=$(echo "$profit_total_pct / 2" | bc -l)

  # Prevent division by zero
  local drawdown_ratio_score
  if (( $(echo "$max_drawdown_account == 0" | bc -l) )); then
    drawdown_ratio_score=20
  else
    drawdown_ratio_score=$(echo "$profit_total_pct / ($max_drawdown_account * 100)" | bc -l)
    if (( $(echo "$drawdown_ratio_score > 20" | bc -l) )); then
      drawdown_ratio_score=20
    fi
  fi

  local trade_count_score=0
  if (( $(echo "$trades > 2000" | bc -l) )); then
    trade_count_score=5
  fi

  # Total score
  SCORE=$(echo "$winrate_score + $profit_per_trade_score + $profit_total_score + $drawdown_ratio_score + $trade_count_score" | bc -l)
  SCORE=$(printf "%.2f" "$SCORE")
}

if [[ "$1" == "listing" ]]; then

  echo -e "\n$hr\nLIST EXCHANGES\n$hr"
  freqtrade list-exchanges --help
  freqtrade list-exchanges

  #freqtrade show-trades
  #freqtrade convert-db 
  #freqtrade install-ui
  #freqtrade webserver

  echo -e "\n$hr\nTEST PAIRLIST\n$hr"
  freqtrade test-pairlist --help
  #freqtrade test-pairlist --one-column --print-json

else
#elif [[ "${RERUN_RUNNER}" != "true" ]]; then

  echo -e "\n$hr\nTEST CCXT\n$hr"
  python user_data/ft_client/test_client/test_client.py

  echo -e "\n$hr\nSTRATEGIES\n$hr"
  freqtrade list-strategies --help
  freqtrade list-strategies
  #freqtrade list-strategies --recursive-strategy-search
  #freqtrade strategy-updater

  echo -e "\n$hr\nLIST DATA\n$hr"
  freqtrade list-data --help
  freqtrade list-data

  #echo -e "\n$hr\nSHOW EDGE\n$hr"
  #freqtrade edge --help
  #jq --slurpfile new_edge $EDGEFILE '.edge = $new_edge[0].edge' $CONFIG > config.json
  #freqtrade edge --fee=$FEE

  if [[ "$SCORE" == "100" ]]; then
    echo -e "\n$hr\nRUN BACKTEST\n$hr"
    freqtrade backtesting --help
    cat $STRATEGY > /tmp/store.json
    #rm -rf user_data/backtest_results/*
    #freqtrade backtesting --fee=$FEE --timerange="$TB"
    freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

    # Scoring breakdown:
    # Winrate: 25 pts
    # Profit per trade: 25 pts
    # Total profit: 25 pts
    # Drawdown ratio: 20 pts
    # Trade count bonus (capped): 5 pts
    calculate_score
    gh variable set JOB --body "${GITHUB_JOB}"
  fi
  
  OLD_SCORE=$SCORE
  echo "SCORE: $OLD_SCORE"
  if [[ "$OLD_SCORE" != "100" ]]; then
    gh variable set SCORE --body "${SCORE}"
  else
    [[ "$GITHUB_JOB" == "lexering" ]] && gh workflow run "main.yml"
    exit 1
  fi

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt
  freqtrade hyperopt --help

  # Get list of available hyperopt classes
  hyperopts=$(freqtrade list-hyperoptloss | sed -n '/Available hyperopt classes/,/positional arguments:/p' | \
    grep -vE "Available hyperopt classes|positional arguments" | awk '{$1=$1};1')

  # Convert to JSON array
  json_array=$(printf '%s\n' "$hyperopts" | jq -R . | jq -s .)

  # Wrap into GitHub Actions matrix format
  jq -n --argjson hyperopts "$json_array" '{ hyperopt: $hyperopts }'
  
  freqtrade list-hyperoptloss --one-column && hyperopt $ID

  #echo -e "\n$hr\nANALYSIS\n$hr"
  #freqtrade backtesting-analysis --help
  #freqtrade lookahead-analysis
  #freqtrade recursive-analysis
  #freqtrade backtesting-analysis --timerange="$TB" --indicator-list all
  jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json
  
  echo -e "\n$hr\nAI MODELS\n$hr"
  freqtrade list-freqaimodels --help
  #freqtrade list-freqaimodels

#else

  echo -e "\n$hr\nAI TRADES\n$hr"
  freqtrade trade --help

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

  rm -rf *.json freqtrade_pid.txt freqtrade.log /tmp/wiki /tmp/dummy
  rm -rf user_data/build_helpers user_data/hyperopt*

fi
