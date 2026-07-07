#!/usr/bin/env bash
#
# Function: Backtest Score
#

calculate_score() {

  sleep 5
  local TRADES_MIN=500
  [[ "$RUN_MODE" == "FreqAI" ]] && TRADES_MIN=300

  # Scoring breakdown:

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

  json_data=$(jq ".strategy_comparison[] | select(.key==\"Fibbo\")" "$json_file")
  if [[ -z "$json_data" ]]; then
    echo "No data found for key: Fibbo"
    return 1
  else
    echo "$json_data" | jq .
    if [[ "$RUN_MODE" == "FreqAI" ]]; then
      # Search entry tags and exit reasons for "freqai" or "low_confidence"
      local found_tags=$(jq -r '.strategy.Fibbo.enter_tag_stats[]?.enter_tag, .strategy.Fibbo.exit_reasons[]?.exit_reason' "$json_file" 2>/dev/null | grep -iE 'freqai|low_confidence' || true)
  
      if [[ -n "$found_tags" ]]; then
        HAS_FREQAI_TAGS="true"
        echo "FreqAI tags detected in backtest: $(echo $found_tags | tr '\n' ' ')"
      else
        HAS_FREQAI_TAGS="false"
        echo "❌ No FreqAI tags detected in this backtest! Ignoring score."
        return 1
      fi
    fi
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
    SCORE=-100.00
    return
  fi

  echo ""
  echo "📈 Strategy Summary for 'Fibbo'"
  echo "---------------------------------"

  WINRATE=$(echo "$winrate * 100" | bc -l)
  WINRATE=$(printf "%.2f" "$WINRATE")

  local winrate_score=$(echo "
    scale=6
    w = ($winrate - 0.5) * 50
    if (w > 10) { 10 } else if (w < -10) { -10 } else { w }
  " | bc -l)
  
  echo "📊 1.1 Winrate: $WINRATE% (score: $(printf "%.2f" "$winrate_score") of 10)"

  local profit_mean_score=$(echo "
    scale=6
    pm = $profit_mean * 100 
    if (pm <= -1.0) {
      -10
    } else if (pm < 0) {
      10 * pm
    } else if (pm < 0.1) {
      1 + pm / 0.1
    } else if (pm < 0.25) {
      2 + (pm - 0.10) / 0.15 * 2
    } else if (pm < 0.50) {
      4 + (pm - 0.25) / 0.25 * 2
    } else if (pm < 0.75) {
      6 + (pm - 0.5) / 0.25 * 2
    } else if (pm < 1.00) {
      8 + (pm - 0.75) / 0.25 * 2
    } else {
      10
    }
  " | bc -l)

  echo "💰 1.2 Profit Mean: $profit_mean_pct% (score: $(printf "%.2f" "$profit_mean_score") of 10)"

  local profit_total_score=$(echo "$profit_total_pct * 0.2" | bc -l)
  [[ $(echo "$profit_total_pct < -50" | bc -l) -eq 1 ]] && profit_total_score=-10
  [[ $(echo "$profit_total_pct > 50" | bc -l) -eq 1 ]] && profit_total_score=10
  echo "💰 1.3 Profit Total: $profit_total_pct% (score: $(printf "%.2f" "$profit_total_score") of 10)"

  local profit_factor_score=$(echo "
    scale=6
    p = $profit_factor
    if (p < 0.5) {
      -10
    } else if (p < 1.0) {
      -10 * (1.0 - p) / 0.5
    } else if (p < 1.1) {
      0 + (p - 1.0) / (0.1 / 2)
    } else if (p < 1.25) {
      2 + (p - 1.1) / (0.15 / 2)
    } else if (p < 2) {
      4 + (p - 1.25) / (0.75 / 3)
    } else if (p < 3) {
      7 + (p - 2) / (1 / 3)
    } else {
      10
    }
  " | bc -l)

  echo "📦 1.4 Profit Factor: $(printf "%.2f" "$profit_factor") (score: $(printf "%.2f" "$profit_factor_score") of 10)"
  local profit=$(echo "$winrate_score + $profit_mean_score + $profit_total_score + $profit_factor_score"| bc -l)
  echo "📊 Profit Block: $(printf "%.2f" "$profit") of 40"
  echo ""

  local dd_score=$(echo "
    scale=2
    dd = $max_drawdown_account * 100
    if (dd < 0.67) {
      13 + (0.67 - dd)
    } else if (dd < 1.67) {
      10 + (1.67 - dd)
    } else if (dd < 3.33) {
      7 + (3.33 - dd) * (3 / 5)
    } else if (dd < 6.67) {
      4 + (6.67 - dd) * (3 / 10)
    } else if (dd < 10) {
      2 + (10 - dd) * (2 / 10)
    } else if (dd < 25) {
      0 - (dd - 10) * (15 / 15)
    } else {
      -15
    }
  " | bc -l)

  local DRAWDOWN=$(echo "$max_drawdown_account * 100" | bc -l)
  DRAWDOWN=$(printf "%.2f" "$DRAWDOWN")
  echo "📉 2.1 Max Drawdown: $DRAWDOWN% (score: $(printf "%.2f" "$dd_score") of 15)"

  local sharpe_score=$(echo "
    scale=6
    s = $sharpe
    if (s <= -2) {
      -10
    } else if (s < 0) {
      s * 5
    } else if (s < 1) {
      2 * s
    } else if (s < 3) {
      2 + (s - 1) * 3
    } else if (s < 5) {
      8 + (s - 3)
    } else {
      10 / (l(s) / l(5))
    }
  " | bc -l) 

  local calmar_score=$(echo "
    scale=6
    c = $calmar
    if (c <= -2.5) {
      -5
    } else if (c < 0) {
      c * 2
    } else if (c < 0.5) {
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
      5 / (l(c) / l(5))
    }
  " | bc -l)

  echo "📌 2.2 Sharpe: $(printf "%.2f" "$sharpe") (score: $(printf "%.2f" "$sharpe_score") of 10)"
  echo "📌 2.3 Calmar: $(printf "%.2f" "$calmar") (score: $(printf "%.2f" "$calmar_score") of 5)"

  local risk=$(echo "$dd_score + $sharpe_score + $calmar_score" | bc -l)
  echo "📊 Risk Block: $(printf "%.2f" "$risk") of 30"
  echo ""

  local expectancy_score=$(echo "
    scale=6
    e = $expectancy_ratio
    if (e <= -1.0) {
      -15
    } else if (e < 0) {
      e * 15
    } else if (e < 0.1) {
      0 + e / 0.1
    } else if (e < 0.25) {
      1 + (e - 0.1) / (0.15 / 2)
    } else if (e < 0.5) {
      3 + (e - 0.25) / (0.25 / 3)
    } else if (e < 1) {
      6 + (e - 0.5) / (0.5 / 4)
    } else if (e < 1.5) {
      10 + (e - 1) / (0.5 / 5)
    } else {
      15
    }
  " | bc -l)

  local sortino_score=$(echo "
    scale=6
    s = $sortino
    if (s <= -2.5) {
      -5
    } else if (s < 0) {
      s * 2
    } else if (s < 1) {
      s
    } else if (s < 3) {
      1 + (s - 1)
    } else if (s < 6) {
      3 + (s - 3) * (2/3)
    } else {
      5 / (l(s) / l(6))
    }
  " | bc -l)

  local sqn_score=$(echo "
    scale=6
    s = $sqn
    if (s <= -2) {
      -10
    } else if (s < 0) {
      s * 5
    } else if (s < 1) {
      s
    } else if (s < 2) {
      2 + (s - 1) / 0.5
    } else if (s < 3) {
      4 + (s - 2) / 0.5
    } else if (s < 5) {
      6 + (s - 3)
    } else if (s < 7) {
      8 + (s - 5)
    } else {
      10
    }
  " | bc -l)

  echo "📦 3.1 Expectancy: $(printf "%.2f" "$expectancy_ratio") (score: $(printf "%.2f" "$expectancy_score") of 15)"
  echo "📌 3.2 Sortino: $(printf "%.2f" "$sortino") (score: $(printf "%.2f" "$sortino_score") of 5)"
  echo "📌 3.3 SQN: $(printf "%.2f" "$sqn") (score: $(printf "%.2f" "$sqn_score") of 10)"

  local quality=$(echo "$expectancy_score + $sortino_score + $sqn_score" | bc -l)
  echo "📊 Quality Block: $(printf "%.2f" "$quality") of 30"
  echo ""
  
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
  echo "📈 CAGR: $(printf "%.2f" "$cagr") (score: $(printf "%.2f" "$cagr_score"))"

  # 🔻 Apply penalties for low trade count
  SCORE=$(echo "$profit + $risk + $quality + $cagr_score" | bc -l)
  if (( $(echo "$SCORE > 0" | bc -l) && $(echo "$trades < $TRADES_MIN" | bc -l) )); then
    echo "🔁 Trades: $trades (penalties applied to $(printf "%.2f" "$SCORE"))"
    SCORE=$(echo "$SCORE * $trades / $TRADES_MIN" | bc -l)
  fi

  SCORE=$(printf "%.2f" "$SCORE")
  echo "🧮 Performance: $SCORE"
  CALCULATION="true"

  echo ""
  echo "🚧 Any of these → discard or penalize heavily:"
  echo ""
  echo "  # PF < 1.0"
  echo "  # Sharpe < 0"
  echo "  # Sortino < 0"
  echo "  # Expectancy Ratio < 0"
  echo "  # Max DD > 50% (or > 40% depending on risk tolerance)"
  echo "  # Trade count < 30 (or < 50 depending on timerange and number of pairlist)"
  echo ""

  # Ensure the baseline failure properly outputs the score
  if (( $(echo "$trades >= $TRADES_MIN" | bc -l) && $(echo "$profit_factor >= 1.0" | bc -l) && $(echo "$sharpe > 0" | bc -l) && $(echo "$expectancy_ratio > 0" | bc -l) && $(echo "$sortino > 0" | bc -l) )); then
    # Passes baseline: Use the highly efficient formula (Positive Score)
    SCORE=$(echo "($expectancy_ratio * $sortino) / $max_drawdown_account" | bc -l)
    SCORE=$(echo "scale=2; ${SCORE:=0} / 100" | bc)
    SCORE=$(printf "%.2f" "$SCORE")
    echo "✅ SCORE: $SCORE"
  else
    # Fails baseline: Subtract 100 from the evaluating blocks to force a negative score
    # This keeps the relative ranking intact (e.g., -92.51 is ranked higher than -99.00)
    SCORE=$(echo "$SCORE - 100" | bc -l)
    SCORE=$(printf "%.2f" "$SCORE")
    echo "❌ SCORE: $SCORE (Failed baseline criteria)"
  fi

  echo "🔍 Behavior Profile:"
  
  # 1. 🛑 Catastrophic Risk Evaluated FIRST
  if (( $(echo "$max_drawdown_account > 0.20" | bc -l) )); then
    echo "🛑 Risky Strategy: Drawdown exceeds 20%. Prioritize stop-loss and trailing-stop optimization."
    
  # 2. 🩸 Statistical Bleeding Evaluated SECOND
  elif (( $(echo "$profit_factor < 1.0" | bc -l) )); then
    echo "🩸 Bleeding Strategy: Profit factor is < 1.0. The strategy loses more money than it makes. Review core logic."
    
  # 3. 🏆 The "Golden" Zone (High profit, active, and safe)
  elif (( $(echo "$profit_total_pct > 40" | bc -l) && $(echo "$trades > 200" | bc -l) && $(echo "$max_drawdown_account < 0.10" | bc -l) )); then
    echo "🏆 Robust Strategy: High profitability, active trading, and excellent drawdown control."
    
  # 4. 🎯 The "Sniper" Zone (Low trades, but highly accurate and profitable)
  elif (( $(echo "$trades < 100" | bc -l) && $(echo "$winrate > 0.70" | bc -l) && $(echo "$profit_factor > 2.0" | bc -l) )); then
    echo "🎯 Sniper Strategy: Highly precise but rare trades. Consider expanding pairlist or slightly relaxing entry cushions."
    
  # 5. ⚠️ The "Churn" Zone (Overtrading)
  elif (( $(echo "$trades > 500" | bc -l) && $(echo "$profit_total_pct < 15" | bc -l) )); then
    echo "⚠️ Churning Strategy: High activity but low returns. Exchange fees and slippage will likely kill this in live trading."
    
  # 6. ⚖️ The "Overfitted / Lucky" Zone (High profit, very few trades)
  elif (( $(echo "$profit_total_pct > 30" | bc -l) && $(echo "$trades < 50" | bc -l) )); then
    echo "⚖️ Unverified Outlier: High profit but very few trades. Susceptible to overfitting. Needs a longer timerange to validate."
    
  # 7. 📌 Default Catch-All
  else
    echo "📌 Balanced Strategy: Decent baseline, but requires further Hyperopt tuning to reach optimal zones."
  fi

}

hyperopt() {

  # Extract clean list of hyperoptloss classes
  hyperopts=$(printf '%s\n' "$(freqtrade list-hyperoptloss --one-column)" | jq -R . | jq -s .)
  
  # Load JSON and filter by given ID
  jq -c --argjson ids "[$(echo "$*" | sed 's/ /,/g')]" '.pipelines[] | select(.id as $id | $ids | index($id))' $HYPERFILE | while read -r pipeline; do

    days=60
    epochs=3200

    start_date=$EARLIEST_DATE
    end_date=$BACKTESTING_START

    id=$(echo "$pipeline" | jq -r '.id')
    loss=$(echo "$pipeline" | jq -r '.hyperopt_loss')

    # dispatch only for main workflow
    [[ "$REDUCE_EPOCH" != "false" ]] && epochs=$((epochs / REDUCE_EPOCH))          
    if [[ "$GITHUB_JOB" != "lexering" ]]; then
      hyperopt_loss="$HYPEROPT"
    else
      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$(jq -n \
          --argjson hyperopts "$hyperopts" \
          --arg runId "$GITHUB_RUN_ID" \
          --arg repo_id "$id" \
          --arg ref "$DEFAULT_BRANCH" \
          --arg score "$SCORE" \
          --arg reduce_epoch "$REDUCE_EPOCH" \
          '{ref: $ref, inputs: {
            RUN_MODE: "Hyperopt",
            MATRIX_JSON: (
              {
                run_id: $runId,
                repo_id: $repo_id,
                fields: $hyperopts,
                reduce_epoch: $reduce_epoch
              } | @json
            )
          }}')" \
        "https://api.github.com/repos/$GITHUB_REPOSITORY/actions/workflows/matrix.yml/dispatches"
      gh variable set JOB --body "${GITHUB_JOB}"
      hyperopt_loss="SharpeHyperOptLoss"
      epochs=$((epochs * 2))
    fi

    #spaces="buy sell entry exit roi trailing"
    spaces=$(echo "$pipeline" | jq -r '.spaces | join(" ")')  # Space-separated
 
    # Disable protections if 'all' or 'protection' is in the spaces
    if [[ "$spaces" =~ (^|[[:space:]])(all|protection)($|[[:space:]]) ]]; then
      enable_protections=""
      prot="disable"
    else
      enable_protections="--enable-protections"
      prot="enable"
    fi

    echo -e "\n$hr\nID: $id 👉 Running ${hyperopt_loss:-$loss}\nSpaces: $spaces | Days: $days | Epochs: $epochs\n$hr"
    freqtrade hyperopt --timerange ${start_date}-${end_date} --hyperopt-loss ${hyperopt_loss:-$loss} --fee=$FEE \
      --spaces ${spaces} --ignore-missing-spaces --epochs ${epochs} -j 4 --logfile /dev/null \
      --random-state ${id} ${enable_protections} > /dev/null 2>&1
    freqtrade hyperopt-list --best

    echo -e "\n$hr\nRERUN BACKTEST ($TB) without FREQAI_MODEL\n$hr" && freqtrade backtesting --help
    jq '.params |= ({enter,buy,exit,sell,roi,freqai,trailing,protection,max_open_trades,stoploss} + del(.enter,.buy,.exit,.sell,.roi,.trailing,.protection,.max_open_trades,.stoploss)) | .params.roi |= (with_entries(select(.key|startswith("roi_")|not)))' "$STRATEGY" > tmp.$$ && mv tmp.$$ "$STRATEGY"
    freqtrade backtesting --fee=$FEE --timerange="$TB" --enable-protection

    calculate_score
    NEW_SCORE=$SCORE
    OLD_SCORE=$(gh variable get SCORE)

    if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) && $(echo "$NEW_SCORE != 0" | bc -l) )); then
      cat $STRATEGY
      sed -i "s|Infinity|10|g" $STRATEGY
      sed -i 's/"max_open_trades":\s*-1/"max_open_trades": 10/g' $STRATEGY

      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
         https://api.github.com/repos/$GITHUB_REPOSITORY/actions/variables/PARAMS_JSON
 
      curl -L -s -X PATCH \
        -H "Accept: application/vnd.github+json" \
        -H "Authorization: Bearer $GH_TOKEN" \
        -H "X-GitHub-Api-Version: 2022-11-28" \
        -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
         https://api.github.com/repos/$TARGET_REPOSITORY/actions/variables/PARAMS_JSON
 
      gh variable set SCORE --body "${NEW_SCORE}"
      gh variable set HYPEROPT --body "${HYPEROPT:-$loss}"
      gh variable set HYPEROPT --body "${HYPEROPT:-$loss}" --repo "$TARGET_REPOSITORY"

      if [[ "$GITHUB_JOB" == "lexering" ]]; then
        gh workflow run "main.yml" --raw-field "RUN_MODE=FreqAI" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"   
      elif [[ "$GITHUB_JOB" != "lexering" &&  "$(gh variable get JOB)" == "lexering" ]]; then
        gh variable set JOB --body "${GITHUB_JOB}" && gh workflow run "main.yml" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
      fi
    elif (( $(echo "$NEW_SCORE < $OLD_SCORE" | bc -l) )); then
      if [[ "$GITHUB_JOB" == "lexering" ]]; then
        if [[ "$(gh variable get JOB)" != "lexering" ]]; then
          gh workflow run "main.yml"
        else
          PARAMS_JSON=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_JSON" | jq -r '.value')
          gh variable set PARAMS_JSON --repo ${TARGET_REPOSITORY} --body "${PARAMS_JSON}"
          gh workflow run "main.yml" --raw-field "RUN_MODE=FreqAI" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
        fi
      fi
    # Environment SCORE is unchanged in case calculation is failed
    elif (( $(echo "$NEW_SCORE == $OLD_SCORE" | bc -l) )); then
      if [[ "$GITHUB_JOB" == "lexering" ]]; then
        if [[ "$CALCULATION" == "false" ]]; then
          gh workflow run "main.yml"
        else
          PARAMS_JSON=$(curl -s -H "Authorization: token $GH_TOKEN" -H "Accept: application/vnd.github.v3+json" \
            "https://api.github.com/repos/${GITHUB_REPOSITORY}/actions/variables/PARAMS_JSON" | jq -r '.value')
          gh variable set PARAMS_JSON --repo ${TARGET_REPOSITORY} --body "${PARAMS_JSON}"
          gh workflow run "main.yml" --raw-field "RUN_MODE=FreqAI" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
        fi
      fi
    fi
  done

}

freqai() {
  
  # Load JSON and filter by given ID
  jq -c --argjson ids "[$(echo "$*" | sed 's/ /,/g')]" '.pipelines[] | select(.id as $id | $ids | index($id))' $HYPERFILE | while read -r pipeline; do

    days=60
    epochs=6400

    start_date=$EARLIEST_DATE
    end_date=$BACKTESTING_START

    id=$(echo "$pipeline" | jq -r '.id')
    hyperopt_loss=$(gh variable get HYPEROPT)
    loss=$(echo "$pipeline" | jq -r '.hyperopt_loss')

    # dispatch only for main workflow
    [[ "$REDUCE_EPOCH" != "false" ]] && epochs=$((epochs / REDUCE_EPOCH))          
    if [[ "$GITHUB_JOB" == "lexering" ]]; then
      # Extract clean list of hyperoptloss classes
      freqaimodels=$(printf '%s\n' "$(freqtrade list-freqaimodels --freqaimodel-path $FREQAIMODELS_PATH --one-column)" | jq -R . | jq -s .)
      curl -s -X POST \
        -H "Authorization: token $GH_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "$(jq -n \
          --argjson freqaimodels "$freqaimodels" \
          --arg runId "$GITHUB_RUN_ID" \
          --arg repo_id "$id" \
          --arg ref "$DEFAULT_BRANCH" \
          --arg score "$SCORE" \
          --arg reduce_epoch "$REDUCE_EPOCH" \
          '{ref: $ref, inputs: {
            RUN_MODE: "FreqAI",
            MATRIX_JSON: (
              {
                run_id: $runId,
                repo_id: $repo_id,
                fields: $freqaimodels,
                reduce_epoch: $reduce_epoch                
              } | @json
            )
          }}')" \
        "https://api.github.com/repos/$GITHUB_REPOSITORY/actions/workflows/matrix.yml/dispatches"
      gh variable set JOB --body "${GITHUB_JOB}"
      epochs=$((epochs * 2))

      jq '.pairlists |= map(if .method == "VolumePairList" then .number_assets = 169 else . end)' $PAIRFILE > tmp.json && mv tmp.json $PAIRFILE
      freqtrade test-pairlist --one-column 2>/dev/null | tail -n +2 | jq -R . | jq -s . > pairs.json
      freqtrade download-data --pairs-file pairs.json --timeframes $TIMEFRAMES --timerange="$TD" --verbose

    fi

    echo -e "\n$hr\nLIST DATA\n$hr"
    echo "Download Timerange: $TD"
    echo "Backtesting Timerange: $TB"
    freqtrade list-data --help
    freqtrade list-data

    pairs=$(gh variable get PAIRS)
    jq --argjson pairs "$pairs" '.exchange.pair_whitelist = $pairs' "$EXCHANGE_FILE" > config.tmp && mv config.tmp "$EXCHANGE_FILE"
    jq '.pairlists = [{"method": "StaticPairList"}]' $PAIRFILE > tmp.json && mv tmp.json $PAIRFILE

    echo -e "\n$hr\nAI TRADES with $FREQAI_MODEL\n$hr" && freqtrade trade --help
    nohup freqtrade trade -v --dry-run --freqaimodel $FREQAI_MODEL --freqaimodel-path $FREQAIMODELS_PATH --fee=$FEE > freqtrade.log 2>&1 &
    echo $! > freqtrade_pid.txt

    # Open descriptor to log stream
    exec 3< <(tail -f freqtrade.log)

    while read -r LOGLINE <&3; do
      echo "$LOGLINE"
      # Stop if Freqtrade has entered TRANING state
      if grep -qiE "throttling" <<< "$LOGLINE"; then
        echo "✅ Throttling freqtrade trade..."
        PID=$(cat freqtrade_pid.txt)
        kill -SIGTERM $PID
        echo "freqtrade trade stopped."
        break
      elif grep -qiE "traceback|object has no attribute" <<< "$LOGLINE"; then
        echo "❌ Stopping freqtrade due to error..."
        PID=$(cat freqtrade_pid.txt)
        kill -SIGTERM $PID
        echo "freqtrade trade stopped."
        exit 0
      fi
    done

    echo -e "\n$hr\nID: $id 👉 Running ${hyperopt_loss:-$loss}\nSpaces: freqai | Days: $days | Epochs: $epochs\nFreqaimodel $FREQAI_MODEL\n$hr"
    freqtrade hyperopt --timerange ${start_date}-${end_date} --hyperopt-loss ${hyperopt_loss:-$loss} --fee=$FEE \
      --spaces freqai --ignore-missing-spaces --epochs ${epochs} -j 4 --log-file hyperopt.log \
      --freqaimodel $FREQAI_MODEL --freqaimodel-path $FREQAIMODELS_PATH \
      --random-state ${id} ${enable_protections} > /dev/null 2>&1
    if [ $? -eq 0 ] && ! grep -qiE "(traceback|object has no attribute|no further splits with positive gain)" hyperopt.log; then
      freqtrade hyperopt-list --best
    else
      exit 0
    fi

    echo -e "\n$hr\nRUN BACKTEST with $FREQAI_MODEL\n$hr"
    #Ref: https://www.freqtrade.io/en/stable/backtesting
    SCORE=$(gh variable get SCORE)
    freqtrade backtesting --help
    jq '.params |= ({enter,buy,exit,sell,roi,freqai,trailing,protection,max_open_trades,stoploss} + del(.enter,.buy,.exit,.sell,.roi,.trailing,.protection,.max_open_trades,.stoploss)) | .params.roi |= (with_entries(select(.key|startswith("roi_")|not)))' "$STRATEGY" > tmp.$$ && mv tmp.$$ "$STRATEGY"
    freqtrade backtesting --freqaimodel $FREQAI_MODEL --freqaimodel-path $FREQAIMODELS_PATH --fee=$FEE --timerange="$TB" --enable-protections --log-file backtest.log
  
    # Execute calculate_score ONLY if no errors and exit code 0
    if [ $? -eq 0 ] && ! grep -qiE "(error|traceback|object has no attribute|no further splits with positive gain)" backtest.log; then

      export CALCULATION="false"
      OLD_SCORE=$SCORE            
      calculate_score
      NEW_SCORE=$SCORE

      OLD_SCORE=$(gh variable get SCORE)
      [[ "$ID" != "169" ]] && SET_INPUT="BYPASS_LEXERING" || SET_INPUT="REMOVE_RUNNER"
      if (( $(echo "$NEW_SCORE > $OLD_SCORE" | bc -l) )) && [[ "$HAS_FREQAI_TAGS" == "true" ]]; then
        cat $STRATEGY
        sed -i "s|Infinity|10|g" $STRATEGY
        sed -i 's/"max_open_trades":\s*-1/"max_open_trades": 10/g' $STRATEGY

        curl -L -s -X PATCH \
          -H "Accept: application/vnd.github+json" \
          -H "Authorization: Bearer $GH_TOKEN" \
          -H "X-GitHub-Api-Version: 2022-11-28" \
          -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
           https://api.github.com/repos/$GITHUB_REPOSITORY/actions/variables/PARAMS_JSON
 
        curl -L -s -X PATCH \
          -H "Accept: application/vnd.github+json" \
          -H "Authorization: Bearer $GH_TOKEN" \
          -H "X-GitHub-Api-Version: 2022-11-28" \
          -d "$(jq -n '{name:"PARAMS_JSON", value:$value}' --arg value "$(cat "$STRATEGY")")" \
           https://api.github.com/repos/$TARGET_REPOSITORY/actions/variables/PARAMS_JSON
 
        gh variable set SCORE --body "${NEW_SCORE}"
        gh variable set FREQAIMODEL --body "${FREQAI_MODEL}"
        gh variable set FREQAIMODEL --body "${FREQAI_MODEL}" --repo "$TARGET_REPOSITORY"

        if [[ "$GITHUB_JOB" != "lexering" ]]; then
          gh variable set JOB --body "${GITHUB_JOB}"
        else
          gh workflow run "main.yml" --raw-field "RUN_MODE=MEC30" --raw-field "$SET_INPUT=true"   
        fi
      elif (( $(echo "$NEW_SCORE < $OLD_SCORE" | bc -l) )); then
        if [[ "$GITHUB_JOB" == "lexering" ]]; then
          if [[ "$(gh variable get JOB)" != "lexering" ]]; then
            gh workflow run "main.yml" --raw-field "RUN_MODE=FreqAI" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
          else
            FREQAI_MODEL=$(gh variable get FREQAIMODEL)
            gh variable set FREQAIMODEL --body "${FREQAI_MODEL}" --repo "$TARGET_REPOSITORY"
            gh workflow run "main.yml" --raw-field "RUN_MODE=MEC30" --raw-field "$SET_INPUT=true"
          fi
        fi
      # Environment SCORE is unchanged in case calculation is failed
      elif (( $(echo "$NEW_SCORE == $OLD_SCORE" | bc -l) )); then
        if [[ "$GITHUB_JOB" == "lexering" ]]; then
          if [[ "$CALCULATION" == "false" ]]; then
            gh workflow run "main.yml" --raw-field "RUN_MODE=FreqAI" --raw-field "REDUCE_EPOCH=$REDUCE_EPOCH"
          else
            FREQAI_MODEL=$(gh variable get FREQAIMODEL)
            gh variable set FREQAIMODEL --body "${FREQAI_MODEL}" --repo "$TARGET_REPOSITORY"
            gh workflow run "main.yml" --raw-field "RUN_MODE=MEC30" --raw-field "$SET_INPUT=true"
          fi
        fi
      fi
    else
      echo "❌ Backtest failed or contained errors/warnings"
      grep -iE "(error|traceback|object has no attribute|no further splits with positive gain)" backtest.log
    fi
  done

}
