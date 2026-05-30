#!/usr/bin/env bash

ID=$1
JOBS_ID=$2
APP_PATH=$3
DIR_PATH=$4
PARAM_NAME=$5
ARTIFACT=$6
HYPEROPT_PARAM=$7

MAX_RETRIES=5
DELAY=10  # seconds
COUNT=0

# Run application
python $APP_PATH $DIR_PATH ${ID:-30} ${PARAM_NAME:-nil} ${EPOCHS:-100}

# Run IREE and capture ALL output
RAW_OUTPUT=$(iree-run-module \
  --module=complex_module.vmfb \
  --function=serving_default \
  --input="13xf32=[1,2,3,4,5,6,7,8,9,10,11,12,13]" \
  --print_statistics=false 2>&1)

# Debug: Save output to file
echo "$RAW_OUTPUT" > iree_output.txt
echo "---- RAW OUTPUT ----"
cat iree_output.txt
echo "--------------------"

# Pass to decoder
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
$SCRIPT_DIR/float_decoder "$RAW_OUTPUT"

while true; do
  #echo "Attempt $((COUNT+1))..."

  if curl -s -X POST \
    -H "Authorization: Bearer ${BEARER}" \
    -H "Content-Type: application/json" \
    https://us-central1-marketleader.cloudfunctions.net/function \
    --data @"${ARTIFACT}" | jq '.' > "${HYPEROPT_PARAM}"; then

    #echo "Request succeeded."
    [[ "$JOBS_ID" == "1" ]] && cat "${HYPEROPT_PARAM}"
    break
  fi

  COUNT=$((COUNT+1))

  if [ "$COUNT" -ge "$MAX_RETRIES" ]; then
    #echo "Failed after $MAX_RETRIES attempts."
    exit 1
  fi

  #echo "Request failed. Retrying in ${DELAY}s..."
  sleep "$DELAY"
done
