#!/usr/bin/env bash
#
# Structure: Cell Types
# Ref: https://www.freqtrade.io/
# Ref: https://strat.ninja/ranking.php
#
hr='----------------------------------------------------------------------------------'
FEE=0.003322
TIMEFRAMES='15m 1h'
[[ -z "${SCORE+x}" ]] && SCORE=100
STRATEGY=user_data/strategies/fibbo.json
HYPEROPT_PARAM=user_data/strategies/hyperopt_params.json
CONFIG=user_data/config_examples/config_full.example.json
EDGEFILE=user_data/config_examples/config_edge.example.json
PAIRFILE=user_data/config_examples/config_pairlist.example.json
HYPERFILE=user_data/config_examples/config_hyperopt.example.json
EXCHANGE_FILE=user_data/config_examples/config_exchange.example.json
HYPERPY=venv/lib/python3.11/site-packages/freqtrade/optimize/hyperopt_tools.py

# Define the backtesting duration (in days)
BACKTESTING_DURATION=1  # In months. Adjust as per your strategy

# Today's date in the required format (YYYYMMDD)
TODAY=$(date -u +%Y%m%d)
YESTERDAY=$(date -u -d "yesterday" +%Y%m%d)

# 30 days ago in the required format
EARLIEST_DATE=$(date -u -d "3 months ago" +%Y%m%d)

# Backtesting start date in the required format (earliest_date + sliding window)
BACKTESTING_START=$(date -u -d "$EARLIEST_DATE + $BACKTESTING_DURATION months" +%Y%m%d)

# Time range for downloading data
TD="$EARLIEST_DATE-$TODAY"

# Time range for backtesting
TB="$BACKTESTING_START-$TODAY"

# Print the timeranges
echo "Download Timerange: $TD"
echo "Backtesting Timerange: $TB"
cat $CONFIG > user_data/config.json

# ENVIRONMENT
export PATH="venv/bin:$PATH"
export PYTHONPATH="user_data/strategies:$PYTHONPATH"

hyperopt() {

  # Extract clean list of hyperoptloss classes
  hyperopts=$(printf '%s\n' "$(freqtrade list-hyperoptloss --one-column)" | jq -R . | jq -s .)
  
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
      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$(jq -n \
          --argjson hyperopts "$hyperopts" \
          --arg runId "$GITHUB_RUN_ID" \
          --arg ref "$DEFAULT_BRANCH" \
          --arg score "$SCORE" \
          --arg epochs "$epochs" \
          --arg freqai "$FREQAIMODEL" \
          '{ref: $ref, inputs: {
           matrix_json: (
             {
               score: $score,
               run_id: $runId,
               epochs: $epochs,
               freqai: $freqai,
               hyperopts: $hyperopts
             } | @json
           )
         }}')" \
       "https://api.github.com/repos/$GITHUB_REPOSITORY/actions/workflows/matrix.yml/dispatches"
      gh variable list | grep -q "HYPEROPT" && HYPEROPT=$(gh variable get HYPEROPT)
      epochs=$((epochs * 2))
    fi

    # Disable protections if 'all' or 'protection' is in the spaces
    spaces=$(echo "$pipeline" | jq -r '.spaces | join(" ")')  # Space-separated
    if [[ "$spaces" =~ (^|[[:space:]])(all|protection)($|[[:space:]]) ]]; then
        enable_protections=""
        prot="disable"
    else
        enable_protections="--enable-protections"
        prot="enable"
    fi

    echo -e "\n$hr\nID: $id 👉 Running ${HYPEROPT:-$loss} | Days: $days\nSpaces: $spaces | Epochs: $epochs | Protection: $prot\n$hr"
    freqtrade hyperopt --timerange ${start_date}-${end_date} --hyperopt-loss ${HYPEROPT:-$loss} -j 4 \
      --spaces ${spaces} --ignore-missing-spaces --epochs ${epochs} --fee=$FEE \
      ${enable_protections} --analyze-per-epoch --random-state ${id} \
      --freqaimodel $FREQAIMODEL --logfile /dev/null > /dev/null 2>&1 
      #--print-json
    freqtrade hyperopt-list

    echo -e "\n$hr\nRERUN BACKTEST\n$hr"
    freqtrade backtesting --help
    #rm -rf user_data/backtest_results/*
    freqtrade backtesting --freqaimodel $FREQAIMODEL --fee=$FEE --timerange="$TB" --enable-protections
  
    calculate_score
    NEW_SCORE=$SCORE
    OLD_SCORE=$(gh variable get SCORE)

    if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )); then
      cat $STRATEGY
      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
         https://api.github.com/repos/$( [[ "$GITHUB_JOB" == "lexering" ]] && echo "$TARGET_REPOSITORY" || echo "$GITHUB_REPOSITORY" )/actions/variables/PARAMS_JSON
      gh variable set HYPEROPT --body "${HYPEROPT:-$loss}" && gh variable set SCORE --body "${NEW_SCORE}" && gh variable set JOB --body "${GITHUB_JOB}"
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

  local json_data=$(jq ".strategy_comparison[] | select(.key==\"Fibbo\")" "$json_file")
  if [[ -z "$json_data" ]]; then
    echo "No data found for key: Fibbo"
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
  local cagr=$(echo "$json_data" | jq -r '.cagr')
  local expectancy=$(echo "$json_data" | jq -r '.expectancy')
  local sharpe=$(echo "$json_data" | jq -r '.sharpe')
  local sortino=$(echo "$json_data" | jq -r '.sortino')

  if [[ -z "$winrate" || -z "$profit_mean_pct" || -z "$profit_total_pct" || -z "$max_drawdown_account" || -z "$trades" ]]; then
    echo "Missing one or more required values."
    return 1
  fi

  if (( $(echo "$trades == 0" | bc -l) || $(echo "$profit_total_pct == 0" | bc -l) )); then
    SCORE=0.00
    return
  fi

  [[ $(echo "$profit_mean_pct > 0.25" | bc -l) -eq 1 ]] && profit_mean_pct=0.25
  [[ $(echo "$cagr > 1.0" | bc -l) -eq 1 ]] && cagr=1.0
  [[ $(echo "$expectancy > 1.0" | bc -l) -eq 1 ]] && expectancy=1.0
  [[ $(echo "$profit_total_pct > 200" | bc -l) -eq 1 ]] && profit_total_pct=200

  [[ $(echo "$profit_mean_pct < 0" | bc -l) -eq 1 ]] && profit_mean_pct=0
  [[ $(echo "$profit_total_pct < 0" | bc -l) -eq 1 ]] && profit_total_pct=0
  [[ $(echo "$cagr < 0" | bc -l) -eq 1 ]] && cagr=0
  [[ $(echo "$expectancy < 0" | bc -l) -eq 1 ]] && expectancy=0

  local winrate_score=$(echo "$winrate * 25" | bc -l)
  local profit_mean_score=$(echo "$profit_mean_pct * 100" | bc -l)
  local profit_total_score=$(echo "$profit_total_pct * 0.1" | bc -l)
  local cagr_score=$(echo "$cagr * 10" | bc -l)
  local expectancy_score=$(echo "$expectancy * 5" | bc -l)

  local drawdown_score
  if (( $(echo "$max_drawdown_account == 0" | bc -l) )); then
    drawdown_score=10
  elif (( $(echo "$max_drawdown_account < 5" | bc -l) )); then
    drawdown_score=7
  elif (( $(echo "$max_drawdown_account < 10" | bc -l) )); then
    drawdown_score=5
  elif (( $(echo "$max_drawdown_account < 20" | bc -l) )); then
    drawdown_score=2
  else
    drawdown_score=0
  fi

  local trade_score=0
  if (( $(echo "$trades > 2000" | bc -l) )); then
    trade_score=5
  fi

  local bonus=0
  if (( $(echo "$sharpe > 1.0" | bc -l) )); then
    bonus=$(echo "$bonus + 2" | bc)
  fi
  if (( $(echo "$sortino > 1.0" | bc -l) )); then
    bonus=$(echo "$bonus + 2" | bc)
  fi
  if (( $(echo "$sortino < 0" | bc -l) )); then
    bonus=$(echo "$bonus - 3" | bc)
  fi

  SCORE=$(echo "$winrate_score + $profit_mean_score + $profit_total_score + $cagr_score + $expectancy_score + $drawdown_score + $trade_score + $bonus" | bc -l)

  # 🔻 Apply penalties for low trade count
  if (( $(echo "$trades < 3" | bc -l) )); then
    SCORE=0
  elif (( $(echo "$trades < 10" | bc -l) )); then
    SCORE=$(echo "$SCORE * 0.25" | bc -l)
  elif (( $(echo "$trades < 20" | bc -l) )); then
    SCORE=$(echo "$SCORE * 0.5" | bc -l)
  elif (( $(echo "$trades < 30" | bc -l) )); then
    SCORE=$(echo "$SCORE * 0.75" | bc -l)
  fi

  SCORE=$(printf "%.2f" "$SCORE")

  echo ""
  echo "📈 Strategy Summary for 'Fibbo'"
  echo "---------------------------------"
  echo "🧮 SCORE: $SCORE"
  echo "💰 Total Profit: $profit_total_pct%"
  echo "📊 Winrate: $winrate"
  echo "🔁 Trades: $trades"
  echo "📉 Max Drawdown: $max_drawdown_account%"
  echo "📈 CAGR: $cagr"
  echo "📦 Expectancy: $expectancy"
  echo "📌 Sharpe: $sharpe"
  echo "📌 Sortino: $sortino"

  echo ""
  echo "🔍 Behavior Profile:"
  if (( $(echo "$profit_total_pct > 100" | bc -l) && $(echo "$trades > 1000" | bc -l) )); then
    echo "✅ High-profit and active trading strategy"
  elif (( $(echo "$profit_total_pct > 100" | bc -l) )); then
    echo "⚖️ High-profit but with fewer trades – consider increasing volume"
  elif (( $(echo "$profit_total_pct < 20" | bc -l) && $(echo "$trades > 1000" | bc -l) )); then
    echo "⚠️ Active trading but low profitability – review signal precision"
  elif (( $(echo "$max_drawdown_account > 20" | bc -l) )); then
    echo "🛑 Risky strategy with high drawdown – requires protection tuning"
  else
    echo "📌 Balanced strategy – decent trade-off between risk and return"
  fi

}

if [[ "$1" != "hyperopt" ]]; then

  echo -e "\n$hr\nLIST EXCHANGES\n$hr"
  freqtrade list-exchanges --help
  freqtrade list-exchanges

  echo -e "\n$hr\nLIST MARKETS\n$hr"
  freqtrade list-markets --help
  freqtrade list-markets

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

    echo -e "\n$hr\nAI MODELS\n$hr"
    freqtrade list-freqaimodels --help
    freqtrade list-freqaimodels

    echo -e "\n$hr\nAI TRADES\n$hr"
    freqtrade trade --help && echo "Starting freqtrade trade..."
    nohup freqtrade trade --dry-run --freqaimodel $FREQAIMODEL --fee=$FEE > freqtrade.log 2>&1 &
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
  pairs=$(gh variable get PAIRS)
  #jq --slurpfile new_edge $EDGEFILE '.edge = $new_edge[0].edge' $CONFIG > config.json
  jq '.pairlists = [{"method": "StaticPairList"}]' $PAIRFILE > tmp.json && mv tmp.json $PAIRFILE
  jq --argjson pairs "$pairs" '.exchange.pair_whitelist = $pairs' "$EXCHANGE_FILE" > config.tmp && mv config.tmp "$EXCHANGE_FILE"

  if [[ "$SCORE" == "100" ]]; then
    echo -e "\n$hr\nRUN BACKTEST\n$hr"
    freqtrade backtesting --help
    cat $STRATEGY > /tmp/store.json
    #rm -rf user_data/backtest_results/*
    #freqtrade backtesting --fee=$FEE --timerange="$TB"
    freqtrade backtesting --freqaimodel $FREQAIMODEL --fee=$FEE --timerange="$TB" --enable-protections

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
  if [[ "$GITHUB_JOB" == "lexering" ]]; then
    if [[ "$OLD_SCORE" == "100" ]]; then
      gh workflow run "main.yml"
    else
      gh variable set SCORE --body "${SCORE}"
    fi
  fi

  echo -e "\n$hr\nRUN HYPEROPT\n$hr"
  #Ref: https://www.freqtrade.io/en/stable/hyperopt
  freqtrade hyperopt --help
  hyperopt $ID

  #echo -e "\n$hr\nANALYSIS\n$hr"
  #freqtrade backtesting-analysis --help
  #freqtrade lookahead-analysis
  #freqtrade recursive-analysis
  #freqtrade backtesting-analysis --timerange="$TB" --indicator-list all
  #jq --slurpfile new_pairlists $PAIRFILE '.pairlists = $new_pairlists[0].pairlists' $CONFIG > config.json
  
  #echo -e "\n$hr\nPLOT DATAFRAME\n$hr"
  #freqtrade plot-dataframe
  #freqtrade plot-profit --timerange="$TB"

  rm -rf *.json freqtrade_pid.txt freqtrade.log /tmp/wiki /tmp/dummy
  rm -rf user_data/build_helpers user_data/hyperopt*

fi
