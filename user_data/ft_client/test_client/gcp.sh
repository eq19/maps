#!/bin/bash

# Max retries
max_retries=30
# Interval between checks (10 retries in 10 minutes -> 60s each)
interval=60

for ((i=1; i<=max_retries; i++)); do
    echo "Check $i of $max_retries..."

    HEADER="Accept: application/vnd.github+json"
    RESPONSE=$(gh api -H "${HEADER}" repos/$REPO_NAME/actions/runners)
    TOTAL_COUNT=$(echo "$RESPONSE" | jq '.total_count')
    STATUS=$(echo "$RESPONSE" | jq -r --arg NAME "$RUNNER_TITLE" '.runners[] | select(.name == $NAME).status')

    if [[ "$TOTAL_COUNT" -gt 0 && "$STATUS" != "offline" ]]; then
        echo "Condition fulfilled ✅"
        exit 0
    fi

    if [ $i -lt $max_retries ]; then
        sleep $interval
    fi
done

echo "Condition not fulfilled after $max_retries checks ❌"
gh workflow run "main.yml" --repo "$REPO_NAME"
