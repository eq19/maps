#!/bin/bash

# Max retries
max_retries=10
# Interval between checks (600s / 10 = 60s each)
interval=60

for ((i=1; i<=max_retries; i++)); do

    echo "Check $i of $max_retries..."
    HEADER="Accept: application/vnd.github+json"
    RESPONSE=$(gh api -H "${HEADER}" repos/$REPO_NAME/actions/runners)
    TOTAL_COUNT=$(gh api -H "${HEADER}" /repos/$REPO_NAME/actions/runners --jq '.total_count')
    STATUS=$(echo "$RESPONSE" | jq -r --arg NAME "$RUNNER_TITLE" '.runners[] | select(.name == $NAME).status')

    # Replace this with your condition
    if [[ ! "$TOTAL_COUNT" -eq 0 ]] && [[ "$STATUS" != "offline" ]]; then
        echo "Condition fulfilled ✅"
        exit 0
    fi

    # If not fulfilled and not the last try, wait
    if [ $i -lt $max_retries ]; then
        sleep $interval
    fi
done

# If condition never fulfilled after retries, run fallback command
echo "Condition not fulfilled after $max_retries checks ❌"
gh workflow run "main.yml" --repo $REPO_NAME
