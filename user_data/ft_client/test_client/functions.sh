#!/usr/bin/env bash
#
# Function: Calculate Score
#

calculate_score() {

  # Scoring breakdown:
  # Winrate: 25 pts
  # Profit per trade: 25 pts
  # Total profit: 25 pts
  # Drawdown ratio: 20 pts
  # Trade count bonus (capped): 5 pts
    
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
  [[ $(echo "$profit_total_pct > 100" | bc -l) -eq 1 ]] && profit_total_pct=100

  [[ $(echo "$profit_mean_pct < 0" | bc -l) -eq 1 ]] && profit_mean_pct=0
  [[ $(echo "$profit_total_pct < 0" | bc -l) -eq 1 ]] && profit_total_pct=0
  [[ $(echo "$cagr < 0" | bc -l) -eq 1 ]] && cagr=0
  [[ $(echo "$expectancy < 0" | bc -l) -eq 1 ]] && expectancy=0

  local winrate_score=$(echo "$winrate * 25" | bc -l)
  local profit_mean_score=$(echo "$profit_mean_pct * 100" | bc -l)
  local profit_total_score=$(echo "$profit_total_pct * 0.25" | bc -l)
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
  CALCULATION="true"

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
    [[ "$REDUCE_EPOCH" != "false" ]] && epochs=$((epochs / REDUCE_EPOCH))          
    if [[ "$GITHUB_JOB" == "lexering" ]]; then
      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$(jq -n \
          --argjson hyperopts "$hyperopts" \
          --arg runId "$GITHUB_RUN_ID" \
          --arg ref "$DEFAULT_BRANCH" \
          --arg score "$SCORE" \
          --arg freqai "$FREQAI_MODEL" \
          --arg reduce_epoch "$REDUCE_EPOCH" \
          '{ref: $ref, inputs: {
           matrix_json: (
             {
               score: $score,
               run_id: $runId,
               freqai: $freqai,
               hyperopts: $hyperopts,
               reduce_epoch: $reduce_epoch
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

    echo -e "\n$hr\nID: $id | FreqAImodel: $FREQAI_MODEL | Days: $days | Epochs: $epochs\n👉 Running ${HYPEROPT:-$loss} | Spaces: $spaces\n$hr"
    freqtrade hyperopt --timerange ${start_date}-${end_date} --hyperopt-loss ${HYPEROPT:-$loss} --freqaimodel $FREQAI_MODEL \
      --spaces ${spaces} --ignore-missing-spaces --epochs ${epochs} --fee=$FEE -j 4 \
      --random-state ${id} ${enable_protections} \
      --logfile /dev/null > /dev/null 2>&1
      #--print-json
    freqtrade hyperopt-list --best
    #cat "$STRATEGY"

    echo -e "\n$hr\nRERUN BACKTEST with $FREQAI_MODEL\n$hr"
    freqtrade backtesting --help
    #rm -rf user_data/backtest_results/*
    freqtrade backtesting --freqaimodel $FREQAI_MODEL --fee=$FEE --timerange="$TB" --enable-protections
  
    calculate_score
    NEW_SCORE=$SCORE

    OLD_SCORE=$(gh variable get SCORE)
    if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )); then
      cat $STRATEGY
      sed -i "s|Infinity|10|g" $STRATEGY
      sed -i 's/"max_open_trades":\s*-1/"max_open_trades": 10/g' $STRATEGY

      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
         https://api.github.com/repos/$( [[ "$GITHUB_JOB" == "lexering" ]] && echo "$TARGET_REPOSITORY" || echo "$GITHUB_REPOSITORY" )/actions/variables/PARAMS_JSON
      gh variable set FREQAIMODEL --body "${FREQAI_MODEL}" && gh variable set HYPEROPT --body "${HYPEROPT:-$loss}" && gh variable set SCORE --body "${NEW_SCORE}" && gh variable set JOB --body "${GITHUB_JOB}"
      if [[ "$GITHUB_JOB" != "lexering" ]]; then
        gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_MODEL" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
      else
        if [[ "$FREQAI_NEXT" != "false" ]]; then gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_NEXT"; fi      
      fi
    elif (( $(echo "$NEW_SCORE < $OLD_SCORE" | bc -l) )); then
      if [[ "$GITHUB_JOB" == "lexering" ]]; then
        if [[ "$(gh variable get JOB)" != "lexering" ]]; then
          gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_MODEL" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
        else
          if [[ "$FREQAI_NEXT" != "false" ]]; then gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_NEXT"; fi
        fi
      fi
    # Environment SCORE is unchanged in case calculation is failed
    elif (( $(echo "$NEW_SCORE == $OLD_SCORE" | bc -l) )); then
      if [[ "$GITHUB_JOB" == "lexering" ]]; then
        if [[ "$CALCULATION" != "false" ]]; then
          gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_NEXT"
        else
          gh workflow run "main.yml" --raw-field "FREQAI_MODEL=$FREQAI_MODEL" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
        fi
      fi
    fi
  done

}
