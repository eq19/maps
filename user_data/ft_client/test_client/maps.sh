#!/bin/bash

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
./float_decoder "$RAW_OUTPUT"

#cat $ARTIFACT
#if curl -s -X POST -H "Authorization: Bearer ${BEARER}" -H "Content-Type: application/json" https://us-central1-marketleader.cloudfunctions.net/function --data @${ARTIFACT} | jq '.' > $HYPEROPT_PARAM; then
  #cat $HYPEROPT_PARAM
#else
  #exit 1
#fi

# Show the first part of your JSON file
head -50 user_data/ft_client/test_client/results/orgs.json

# Or use jq to pretty print and show structure
cat user_data/ft_client/test_client/results/orgs.json | jq '. | type'
cat user_data/ft_client/test_client/results/orgs.json | jq 'if type=="array" then "Array with \(length) items" else "Object with keys: \(keys)" end'

curl -s -X POST -H "Authorization: Bearer ${BEARER}" -H "Content-Type: application/json" https://us-central1-marketleader.cloudfunctions.net/function -d @$ARTIFACT > $HYPEROPT_PARAM
cat $HYPEROPT_PARAM
