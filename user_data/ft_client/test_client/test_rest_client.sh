#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='------------------------------------------------------------------------------------'
SCORE=100
FEE=0.003322
TIMEFRAMES='1m 15m'
STRATEGY=/home/runner/user_data/strategies/fibbo.json
EDGEFILE=user_data/config_examples/config_edge.example.json
CONFIG=user_data/config_examples/config_exchange.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERPY=/home/runner/venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

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

echo -e "\n$hr\nTEST ENVIRONMENT\n$hr"
printenv

hyperopt() {

  # Load JSON and filter by given ID
  HYPERFILE=user_data/config_examples/config_hyperopt.example.json
  jq -c --argjson ids "[$(echo "$*" | sed 's/ /,/g')]" '.pipelines[] | select(.id as $id | $ids | index($id))' $HYPERFILE | while read -r pipeline; do
    id=$(echo "$pipeline" | jq -r '.id')
    days=$(echo "$pipeline" | jq -r '.days')
    epochs=$(echo "$pipeline" | jq -r '.epochs')

    end_date=$(date +"%Y%m%d")
    start_date=$(date -d "$days days ago" +"%Y%m%d")
    timerange="$start_date-$end_date"

    spaces=$(echo "$pipeline" | jq -r '.spaces | join(" ")')  # Space-separated
    all_losses=($(jq -r --arg loss "$hyperopt_loss" '[.built_in[], .custom_built[]] | map(select(. != $loss)) | [$loss] + . | .[]' $HYPERFILE))

    for losses in "${all_losses[@]}"; do
      hyperopt_loss=$(echo "$pipeline" | jq -r '.hyperopt_loss')
    done

    echo -e "\n$hr\nID: $id 👉 Running $losses | Spaces: $spaces | Days: $days | Epochs: $epochs\n$hr"
    freqtrade hyperopt --fee=$FEE --timerange ${start_date}-${end_date} --epochs ${epochs} -j 4 \
      --spaces ${spaces} --ignore-missing-spaces --hyperopt-loss ${hyperopt_loss} \
      --enable-protections --analyze-per-epoch  --random-state ${id} \
      --logfile /dev/null > /dev/null 2>&1
    freqtrade hyperopt-list

    echo -e "\n$hr\nRERUN BACKTEST\n$hr"
    freqtrade backtesting --help
    rm -rf /home/runner/user_data/backtest_results/*
    freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections
  
    calculate_score
    NEW_SCORE=$SCORE
    echo "NEW SCORE: $NEW_SCORE"

    if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )); then
      cat $STRATEGY
      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
         https://api.github.com/repos/$TARGET_REPOSITORY/actions/variables/PARAMS_JSON \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")"

      python user_data/ft_client/test_client/app.py output.txt
      cat user_data/ft_client/test_client/results/output.txt

      curl -s -X POST \
        -H "Authorization: Bearer ${BEARER}" \
        -H "Content-Type: application/json" \
          https://us-central1-feedmapping.cloudfunctions.net/function \
        --data @${STRATEGY} | jq '.'
    fi
  done
}

calculate_score() {

  # Unzip the latest backtest result file
  local dir="/home/runner/user_data/backtest_results"
  local latest_zip=$(ls -t "$dir/backtest-result-"*.zip | head -n 1)
  if [[ -z "$latest_zip" ]]; then
     echo "No ZIP file found in $dir"
      return 1
  fi
  unzip -q "$latest_zip" -d "$dir"  # -q for quiet mode

  # Find the latest JSON file (excluding .meta.json)
  local json_file=$(ls -t "$dir/backtest-result-"*.json | grep -v '.meta.json' | head -n 1)
  if [[ -z "$json_file" ]]; then
    echo "No JSON file found in $dir"
    return 1
  fi

  # Extract JSON data for the given strategy key
  local json_data=$(jq ".strategy_comparison[] | select(.key==\"fibbo\")" "$json_file")
  if [[ -z "$json_data" ]]; then
    echo "No data found for key: $key"
    return 1
  else
    echo "$json_data" | jq .
    rm -rf $dir/*
  fi

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
  SCORE=$(echo "scale=2; $winrate_score + $profit_total_score + $profit_factor_score + $max_drawdown_score + $trade_count_score" | bc)
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

else
#elif [[ "${RERUN_RUNNER}" != "true" ]]; then

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
  cat $STRATEGY > /tmp/store.json
  rm -rf /home/runner/user_data/backtest_results/*
  freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protections

  calculate_score
  OLD_SCORE=$SCORE
  echo "SCORE: $OLD_SCORE"

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt/#solving-a-mystery
  freqtrade hyperopt --help && freqtrade list-hyperoptloss && hyperopt $ID

  #echo -e "\n$hr\nANALYSIS\n$hr"
  #freqtrade backtesting-analysis --help
  #freqtrade lookahead-analysis
  #freqtrade recursive-analysis
  #freqtrade backtesting-analysis --timerange="$TB" --indicator-list all
  jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json
  
  #echo -e "\n$hr\nAI MODELS\n$hr"
  #freqtrade list-freqaimodels --help
  #freqtrade list-freqaimodels

#else

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

  git config --global user.name eq19
  git config --global user.email eq19@users.noreply.github.com

  rm -rf *.json freqtrade_pid.txt freqtrade.log /tmp/wiki /tmp/dummy
  rm -rf /home/runner/user_data/build_helpers /home/runner/user_data/hyperopt*
  git clone https://eq19:$GH_TOKEN@github.com/$TARGET_REPOSITORY.wiki.git /tmp/wiki

  if [[ ! -d /tmp/wiki/_user ]]; then
    git clone https://eq19:$GH_TOKEN@github.com/eq19/eq19.wiki.git /tmp/dummy
    rm -rf /tmp/wiki/* /tmp/dummy/.git && mv -f /tmp/dummy/* /tmp/wiki/
  fi
  
  cd /tmp/wiki
  rm -rf _user && mv -f /home/runner/user_data _user
  find _user/strategies -mindepth 1 -type d -exec rm -rf {} +
  git add . && git commit --allow-empty -m "update params" && git push

fi
