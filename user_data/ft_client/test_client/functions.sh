#!/usr/bin/env bash
#
# Function: Calculate Score
#

calculate_score() {

  # Scoring breakdown:

  # Profit Block (40%)
    # profit_total   = 20%
    # profit_mean    = 10%
    # winrate        = 10%

  # Risk Block (30%)
    # max_drawdown_account = 15%
    # calmar               = 10%
    # sharpe               = 5%

  # Quality Block (30%)
    # expectancy_ratio = 10%
    # profit_factor    = 10%
    # sortino          = 5%
    # sqn              = 5%

  # Optional
    # cagr as bonus (0 - 5)%
    # trades as penalties if lower than 100

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
  local profit_mean=$(echo "$json_data" | jq -r '.profit_mean')
  local profit_mean_pct=$(echo "$json_data" | jq -r '.profit_mean_pct')
  local profit_total_pct=$(echo "$json_data" | jq -r '.profit_total_pct')
  local max_drawdown_account=$(echo "$json_data" | jq -r '.max_drawdown_account')
  local trades=$(echo "$json_data" | jq -r '.trades')
  local sqn=$(echo "$json_data" | jq -r '.sqn')
  local cagr=$(echo "$json_data" | jq -r '.cagr')
  local calmar=$(echo "$json_data" | jq -r '.calmar')
  local expectancy=$(echo "$json_data" | jq -r '.expectancy')
  local expectancy_ratio=$(echo "$json_data" | jq -r '.expectancy_ratio')
  local profit_factor=$(echo "$json_data" | jq -r '.profit_factor')
  local sharpe=$(echo "$json_data" | jq -r '.sharpe')
  local sortino=$(echo "$json_data" | jq -r '.sortino')

  if [[ -z "$winrate" || -z "$profit_mean" || -z "$profit_total_pct" || -z "$max_drawdown_account" || -z "$trades" ]]; then
    echo "Missing one or more required values."
    return 1
  fi

  if (( $(echo "$trades == 0" | bc -l) || $(echo "$profit_total_pct == 0" | bc -l) )); then
    SCORE=0.00
    return
  fi

  echo -e "\n"
  echo "📈 Strategy Summary for 'Fibbo'"
  echo "---------------------------------"

  local profit_total_score=$(echo "$profit_total_pct * 1" | bc -l)
  [[ $(echo "$profit_total_pct < 0" | bc -l) -eq 1 ]] && profit_total_score=0
  [[ $(echo "$profit_total_pct > 20" | bc -l) -eq 1 ]] && profit_total_score=20
  echo "💰 1.1 Profit Total: $profit_total_pct% (score: $(printf "%.2f" "$profit_total_score") of 20)"

  [[ $(echo "$profit_mean < 0" | bc -l) -eq 1 ]] && profit_mean=0
  local profit_mean_score=$(echo "
    scale=6

    t = sqrt($trades / 200)
    e = $expectancy_ratio / 0.1

    pm = $profit_mean / 0.02
    if (pm > 1) {
      pm_factor = 1
    } else {
      pm_factor = pm
    }

    pf = $profit_factor / 2
    if (pf > 1) {
      pf_factor = 1
    } else {
      pf_factor = pf
    }

    w = 10 * t * e * pm_factor * pf_factor

    if (w > 10) {
      10
    } else {
      w
    }
    " | bc -l)

  echo "💰 1.2 Profit Mean: $profit_mean_pct% (score: $(printf "%.2f" "$profit_mean_score") of 10)"

  WINRATE=$(echo "$winrate * 100" | bc -l)
  WINRATE=$(printf "%.2f" "$WINRATE")

  local winrate_score=$(echo "$winrate * 10" | bc -l)
  echo "📊 1.3 Winrate: $WINRATE% (score: $(printf "%.2f" "$winrate_score") of 10)"

  local profit=$(echo "$profit_total_score + $profit_mean_score + $winrate_score" | bc -l)
  echo "📊 Profit Block: $(printf "%.2f" "$profit") of 40"
  echo -e "\n"

  local dd_score=$(echo "
    scale=6

    dd = $max_drawdown_account * 100

    if (dd < 2) {
      13 + (2 - dd)
    } else if (dd < 5) {
      10 + (5 - dd)
    } else if (dd < 10) {
      7 + (10 - dd) * (3 / 5)
    } else if (dd < 20) {
      4 + (20 - dd) * (3 / 10)
    } else if (dd < 30) {
      2 + (30 - dd) * (2 / 10)
    } else {
      0
    }
  " | bc -l)

  local DRAWDOWN=$(echo "$max_drawdown_account * 100" | bc -l)
  if (( $(echo "$DRAWDOWN > 15" | bc -l) )); then
    dd_score=$(echo "$dd_score * 0.7" | bc -l)
  fi

  DRAWDOWN=$(printf "%.2f" "$DRAWDOWN")
  echo "📉 2.1 Max Drawdown: $DRAWDOWN% (score: $dd_score of 15)"

  local sharpe_score=$(echo "
    scale=6
    s = $sharpe

    if (s < 1) {
      2 * s
    } else if (s < 3) {
      2 + (s - 1) * 3
    } else if (s < 5) {
      8 + (s - 3)
    } else {
      10
    }
  " | bc -l) 

  local calmar_score=$(echo "
    scale=6
    c = $calmar

    if (c < 0.5) {
      c * 2
    } else if (c < 1) {
      1 + (c - 0.5) * 2
    } else if (c < 2) {
      2 + (c - 1)
    } else if (c < 3) {
      3 + (c - 2)
    } else if (c < 5) {
      4 + (c - 3) * 0.5
    } else {
      5
    }
  " | bc -l)

  echo "📌 2.2 Sharpe: $sharpe (score: $sharpe_score of 10)"
  echo "📌 2.3 Calmar: $calmar (score: $calmar_score of 5)"

  local risk=$(echo "$dd_score + $sharpe_score + $calmar_score" | bc -l)
  echo "📊 Risk Block: $(printf "%.2f" "$risk") of 30"
  echo -e "\n"

  local expectancy_score=$(echo "
    scale=6
    e = $expectancy_ratio

    if (e < 0.02) {
      e * 100
    } else if (e < 0.05) {
      2 + (e - 0.02) * (2 / 0.03)
    } else if (e < 0.1) {
      4 + (e - 0.05) * (2 / 0.05)
    } else if (e < 0.2) {
      6 + (e - 0.1) * (2 / 0.1)
    } else if (e < 0.3) {
      8 + (e - 0.2) * (2 / 0.1)
    } else {
      10
    }
  " | bc -l)

  local profit_factor_score=$(echo "
    scale=6
    p = $profit_factor

    if (p < 1) {
      0
    } else if (p < 1.2) {
      (p - 1) * (3 / 0.2)
    } else if (p < 1.5) {
      3 + (p - 1.2) * (2 / 0.3)
    } else if (p < 2) {
      5 + (p - 1.5) * (2 / 0.5)
    } else if (p < 3) {
      7 + (p - 2) * 2
    } else {
      10
    }
  " | bc -l)

  local sortino_score=$(echo "
    scale=6
    s = $sortino

    if (s < 1) {
      s
    } else if (s < 3) {
      1 + (s - 1)
    } else if (s < 6) {
      3 + (s - 3) * (2/3)
    } else {
      5
    }
  " | bc -l)

  local sqn_score=$(echo "
    scale=6
    s = $sqn

    if (s < 1) {
      s
    } else if (s < 2) {
      1 + (s - 1)
    } else if (s < 3) {
      2 + (s - 2)
    } else if (s < 5) {
      3 + (s - 3) * 0.5
    } else {
      5
    }
  " | bc -l)

  echo "📦 3.1 Expectancy: $expectancy_ratio (score: $expectancy_score of 10)"
  echo "📦 3.2 Profit Factor: $profit_factor (score: $profit_factor_score of 10)"
  echo "📌 3.3 Sortino: $sortino (score: $sortino_score of 5)"
  echo "📌 3.4 SQN: $sqn (score: $sqn_score of 5)"

  local quality=$(echo "$expectancy_score + $profit_factor_score + $sortino_score + $sqn_score" | bc -l)
  echo "📊 Quality Block: $(printf "%.2f" "$quality") of 30"
  echo -e "\n"
  
  local cagr_score=$(echo "
    scale=6
    c = $cagr

    if (c < 5) {
      c / 5
    } else if (c < 15) {
      1 + (c - 5) * (1 / 10)
    } else if (c < 30) {
      2 + (c - 15) * (1 / 15)
    } else if (c < 60) {
      3 + (c - 30) * (1 / 30)
    } else if (c < 100) {
      4 + (c - 60) * (1 / 40)
    } else {
      5
    }
  " | bc -l)

  if (( $(echo "$cagr > 200" | bc -l) )); then
    cagr_score=$(echo "$cagr_score * 0.7" | bc -l)
  fi
  echo "📈 CAGR: $cagr (score: $cagr_score)"

  # 🔻 Apply penalties for low trade count
  SCORE=$(echo "$profit + $risk + $quality + $cagr_score" | bc -l)
  if (( $(echo "$trades < 200" | bc -l) )); then
    echo "🔁 Trades: $trades (penalties applied to $(printf "%.2f" "$SCORE"))"
    SCORE=$(echo "$SCORE * $trades / 200" | bc -l)
  fi

  SCORE=$(printf "%.2f" "$SCORE")
  echo "🧮 SCORE: $SCORE"
  CALCULATION="true"

  echo -e "\n"
  echo "🔍 Behavior Profile:"
  if (( $(echo "$profit_total_pct > 100" | bc -l) && $(echo "$trades > 1000" | bc -l) )); then
    echo "✅ High-profit and active trading strategy"
  elif (( $(echo "$profit_total_pct > 100" | bc -l) )); then
    echo "⚖️ High-profit but with fewer trades – consider increasing volume"
  elif (( $(echo "$profit_total_pct < 20" | bc -l) && $(echo "$trades > 1000" | bc -l) )); then
    echo "⚠️ Active trading but low profitability – review signal precision"
  elif (( $(echo "$max_drawdown_account > 0.20" | bc -l) )); then
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
