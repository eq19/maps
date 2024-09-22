#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6
# https://www.hexspin.com/proof-of-confinement/

set_target() {
  
  # Get Structure
  if [[ $2 == *"github.io"* ]]; then
    [[ -n "$CELL" ]] && SPIN=$(( $CELL * 13 ))
    if [[ "${OWNER}" == "eq19" ]]; then
      echo "maps, feed, lexer, parser, syntax, grammar" > ${RUNNER_TEMP}/pinned_repos
    else
      QUERY='{"query":"{\n organization(login: \"'${OWNER}'\") {\n pinnedItems(first: 6, types: REPOSITORY) {\n nodes {\n ... on Repository {\n name\n }\n }\n }\n }\n}"'
      curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/pinned_repos
      sed -i "1s|^|maps, feed, lexer, parser, syntax, grammar, |" ${RUNNER_TEMP}/pinned_repos
    fi
    IFS=', '; array=($(cat ${RUNNER_TEMP}/pinned_repos))
  else
    gh api -H "${HEADER}" /user/orgs  --jq '.[].login' | sort -uf | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/user_orgs
    IFS=', '; array=($(cat ${RUNNER_TEMP}/user_orgs))
    echo "[" > ${RUNNER_TEMP}/orgs.json
    for ((i=0; i < ${#array[@]}; i++)); do
      QUERY='{"query":"{\n organization(login: \"'${array[$i]}'\") {\n pinnedItems(first: 6, types: REPOSITORY) {\n nodes {\n ... on Repository {\n name\n }\n }\n }\n }\n}"'
      IFS=', '; pr=($(curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g"))
      gh api -H "${HEADER}" /orgs/${array[$i]} | jq '. +
        {"key1": ["maps","feed","lexer","parser","syntax","grammar"]} +
        {"key2": ["'${pr[0]}'","'${pr[1]}'","'${pr[2]}'","'${pr[3]}'","'${pr[4]}'","'${pr[5]}'"]}' >> ${RUNNER_TEMP}/orgs.json
      if [[ "$i" -lt "${#array[@]}-1" ]]; then echo "," >> ${RUNNER_TEMP}/orgs.json; fi
    done
    echo "]" >> ${RUNNER_TEMP}/orgs.json
  fi
  
  # Iterate the Structure
  printf -v array_str -- ',,%q' "${array[@]}"
  if [[ ! "${array_str},," =~ ",,$1,," ]]; then
    SPAN=0; echo ${array[0]}
  elif [[ "${array[-1]}" == "$1" ]]; then
    SPAN=${#array[@]}; echo $2 | sed "s|${OWNER}.github.io|${ENTRY}.github.io|g"
    if [[ -n "$CELL" ]]; then
      if [[ "${ENTRY}" == "eq19" ]]; then
        echo "maps, feed, lexer, parser, syntax, grammar" > ${RUNNER_TEMP}/pinned_repos
      else
        QUERY='{"query":"{\n organization(login: \"'${ENTRY}'\") {\n pinnedItems(first: 6, types: REPOSITORY) {\n nodes {\n ... on Repository {\n name\n }\n }\n }\n }\n}"'
        curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/pinned_repos
        sed -i "1s|^|maps, feed, lexer, parser, syntax, grammar, |" ${RUNNER_TEMP}/pinned_repos
      fi
    fi
  else
    for ((i=0; i < ${#array[@]}; i++)); do
      if [[ "${array[$i]}" == "$1" && "$i" -lt "${#array[@]}-1" ]]; then 
        SPAN=$(( $i + 1 )); echo ${array[$SPAN]}
      fi
    done
  fi
  
  # Generate id from the Structure
  [[ -z "$SPIN" ]] && if [[ "$1" != "$2" ]]; then SPIN=0; else SPIN=13; fi
  if [[ -n "$CELL" ]]; then
    SPANPLUS=$(($SPAN + 1))
    if (( $CELL == 0 )); then MOD=7; else MOD=13; fi
    if (( $SPANPLUS == $MOD )); then 
      SPANPLUS=0
      CELLPLUS=$(($CELL + 1))
      if (( $CELLPLUS == 14 )); then CELLPLUS=0; fi
    else
      CELLPLUS=$(($CELL + 0))
    fi
    
    echo "SPIN=[${CELLPLUS}, ${SPANPLUS}]" >> ${GITHUB_ENV}
    echo "  spin: [${CELLPLUS}, ${SPANPLUS}]" >> ${RUNNER_TEMP}/_config.yml
    echo "  pinned: [$(cat ${RUNNER_TEMP}/pinned_repos)]" >> ${RUNNER_TEMP}/_config.yml
    echo "  organization: [$(cat ${RUNNER_TEMP}/user_orgs)]" >> ${RUNNER_TEMP}/_config.yml
  fi
  return $(( $SPAN + $SPIN ))
}

jekyll_build() {

  echo -e "\n$hr\nCONFIG\n$hr"
  
  [[ $1 == *"github.io"* ]] && OWNER=$2  
  echo 'TARGET_REPOSITORY='${OWNER}/$1 >> ${GITHUB_ENV}
  if [[ $1 != "eq19.github.io" ]]; then SITEID=$(( $3 + 2 )); else SITEID=1; fi

  if  [[ "${OWNER}" == "eq19" ]]; then
    sed -i "1s|^|description: An attempt to discover the Final Theory\n\n|" ${RUNNER_TEMP}/_config.yml
  else
    DESCRIPTION=$(gh api -H "${HEADER}" /orgs/${OWNER} --jq '.description')
    sed -i "1s|^|description: ${DESCRIPTION}\n\n|" ${RUNNER_TEMP}/_config.yml
  fi
  
  # Note: If you need to use a workflow run's URL from within a job, you can combine
  # these variables: $GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID
  sed -i "1s|^|action: ${REPO}/actions/runs/${RUN}\n|" ${RUNNER_TEMP}/_config.yml
  sed -i "1s|^|repository: ${OWNER}/$1\n|" ${RUNNER_TEMP}/_config.yml
  [[ $1 != *"github.io"* ]] && sed -i "1s|^|baseurl: /$1\n|" ${RUNNER_TEMP}/_config.yml
  
  sed -i "1s|^|title: eQuantum\n|" ${RUNNER_TEMP}/_config.yml
  FOLDER="span$(( 17 - $3 ))" && sed -i "1s|^|span: ${FOLDER}\n|" ${RUNNER_TEMP}/_config.yml
  sed -i "1s|^|user: ${USER}\n|" ${RUNNER_TEMP}/_config.yml

  sed -i "1s|^|id: ${SITEID}\n|" ${RUNNER_TEMP}/_config.yml
  echo 'ID='${SITEID} >> ${GITHUB_ENV}
  cat ${RUNNER_TEMP}/_config.yml
   
  echo -e "\n$hr\nSPIN\n$hr"
  gist.sh $1 ${OWNER} ${FOLDER}
  find ${RUNNER_TEMP}/gistdir -type d -name .git -prune -exec rm -rf {} \;
  
  cd ${RUNNER_TEMP}/workdir && mv -f ${RUNNER_TEMP}/_config.yml .
  rm -rf ${RUNNER_TEMP}/Sidebar.md && cp _Sidebar.md ${RUNNER_TEMP}/Sidebar.md
  sed -i 's/0. \[\[//g' ${RUNNER_TEMP}/Sidebar.md && sed -i 's/\]\]//g' ${RUNNER_TEMP}/Sidebar.md

  find . -iname '*.md' -print0 | sort -zn | xargs -0 -I '{}' front.sh '{}'
  find . -type d -name "${FOLDER}" -prune -exec sh -c 'cat ${RUNNER_TEMP}/README.md >> $1/README.md' sh {} \;
  
  echo -e "\n$hr\nWORKSPACE\n$hr"
  cp -R ${RUNNER_TEMP}/gistdir/* .
  mkdir ${RUNNER_TEMP}/workdir/_data
  mv -f ${RUNNER_TEMP}/orgs.json ${RUNNER_TEMP}/workdir/_data/orgs.json
           
}

# Get structure on gist files
PATTERN='sort_by(.created_at)|.[] | select(.public == true).files.[] | select(.filename != "README.md").raw_url'
HEADER="Accept: application/vnd.github+json" && echo ${TOKEN} | gh auth login --with-token
gh api -H "${HEADER}" "/users/eq19/gists" --jq "${PATTERN}" > ${RUNNER_TEMP}/gist_files

# Capture the string and return status
if [[ "${OWNER}" != "${USER}" ]]; then ENTRY=$(set_target ${OWNER} ${USER}); else ENTRY=$(set_target ${OWNER}); fi
CELL=$? && TARGET_REPOSITORY=$(set_target $(basename ${REPO}) ${OWNER}.github.io)
jekyll_build ${TARGET_REPOSITORY} ${ENTRY} $?
