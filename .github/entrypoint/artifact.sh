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
      curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${GH_TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/pinned_repos
      sed -i "1s|^|maps, feed, lexer, parser, syntax, grammar, |" ${RUNNER_TEMP}/pinned_repos
    fi
    IFS=', '; array=($(cat ${RUNNER_TEMP}/pinned_repos))
  else
    gh api -H "${HEADER}" /user/orgs  --jq '.[].login' | sort -uf | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/user_orgs
    IFS=', '; array=($(cat ${RUNNER_TEMP}/user_orgs))
    echo "[" > ${RUNNER_TEMP}/orgs.json
    for ((i=0; i < ${#array[@]}; i++)); do
      QUERY='{"query":"{\n organization(login: \"'${array[$i]}'\") {\n pinnedItems(first: 6, types: REPOSITORY) {\n nodes {\n ... on Repository {\n name\n }\n }\n }\n }\n}"'
      IFS=', '; pr=($(curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${GH_TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g"))
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
        curl -s -X POST "${GITHUB_GRAPHQL_URL}" -H "Authorization: bearer ${GH_TOKEN}" --data-raw "${QUERY}" | jq --raw-output '.data.organization.pinnedItems.nodes[].name' | yq eval -P | sed "s/ /, /g" > ${RUNNER_TEMP}/pinned_repos
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
  
  [[ $1 == *"github.io"* ]] && OWNER=$2
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
  
  FOLDER="span$(( 19 - $SITEID ))"
  gh variable set FOLDER --body "$FOLDER"
  echo 'FOLDER='${FOLDER} >> ${RUNNER_TEMP}/.env
  
  TARGET_REPOSITORY="${OWNER}/$1"
  echo 'repo='${TARGET_REPOSITORY} >> ${GITHUB_OUTPUT}
  gh variable set TARGET_REPOSITORY --body "$TARGET_REPOSITORY"
  echo 'TARGET_REPOSITORY='${TARGET_REPOSITORY} >> ${GITHUB_ENV}

  sed -i "1s|^|title: eQuantum\n|" ${RUNNER_TEMP}/_config.yml
  sed -i "1s|^|span: ${FOLDER}\n|" ${RUNNER_TEMP}/_config.yml
  sed -i "1s|^|user: ${USER}\n|" ${RUNNER_TEMP}/_config.yml
  sed -i "1s|^|id: ${SITEID}\n|" ${RUNNER_TEMP}/_config.yml

  echo 'ID='${SITEID} >> ${GITHUB_ENV}
  cat ${RUNNER_TEMP}/_config.yml

  if [[ "${TARGET_REPOSITORY}" != *"eq19/"* ]]; then

    echo -e "\nTest Module Structure:"
    echo "1. ${OWNER}/maps → $(next_repo "${OWNER}/maps")"
    echo "2. ${OWNER}/grammar → $(next_repo "${OWNER}/grammar")"
    NEXT_REPOSITORY=$(next_repo "${OWNER}/$(yq -r '.track.pinned | .[-1]' ${RUNNER_TEMP}/_config.yml)")
    echo "3. ${OWNER}/$(yq -r '.track.pinned | .[-1]' ${RUNNER_TEMP}/_config.yml) → ${NEXT_REPOSITORY}"
    echo "4. ${NEXT_REPOSITORY} → $(next_repo "${NEXT_REPOSITORY}")"

    NEXT_REPOSITORY=$(next_repo "${TARGET_REPOSITORY}")
    gh variable set TARGET_REPOSITORY --repo $TARGET_REPOSITORY --body "$NEXT_REPOSITORY"

  fi
   
}

# Define the next repository function using jq
next_repo() {

  local target_repo="$1"
  jq -r --arg target "$target_repo" '
    ($target | split("/")) as $parts |
    $parts[0] as $org |
    $parts[1] as $repo |

    (map(.login) | index($org)) as $org_index |
    if $org_index == null then
      "Organization not found: \($org)" | halt_error(1)
    else 
      .[$org_index] as $current_org |
      (.[($org_index + 1) % length].login) as $next_org |

      if $repo == "\($org).github.io" then
        "\($org)/\($current_org.key1[0])"
      else
        ($current_org.key1 | index($repo)) as $key1_index |
        if $key1_index != null then
          if ($key1_index + 1) < ($current_org.key1 | length) then
            "\($org)/\($current_org.key1[$key1_index + 1])"
          else
            "\($org)/\($current_org.key2[0])"
          end
        else
          ($current_org.key2 | index($repo)) as $key2_index |
          if $key2_index != null then
            if ($key2_index + 1) < ($current_org.key2 | length) then
              "\($org)/\($current_org.key2[$key2_index + 1])"
            else
              "\($next_org)/\($next_org).github.io"
            end
          else
            "Repository not found: \($repo)" | halt_error(1)
          end
        end
      end
    end
  ' ${RUNNER_TEMP}/orgs.json

}

# Get structure on gist files
PATTERN='sort_by(.created_at)|.[] | select(.public == true).files.[] | select(.filename != "README.md").raw_url'
HEADER="Accept: application/vnd.github+json" #&& echo ${TOKEN} | gh auth login --with-token
gh api -H "${HEADER}" "/users/eq19/gists" --jq "${PATTERN}" > ${RUNNER_TEMP}/gist_files

# Capture the string and return status
if [[ "${OWNER}" != "${USER}" ]]; then ENTRY=$(set_target ${OWNER} ${USER}); else ENTRY=$(set_target ${OWNER}); fi
CELL=$? && TARGET_REPOSITORY=$(set_target $(basename ${REPO}) ${OWNER}.github.io)
jekyll_build ${TARGET_REPOSITORY} ${ENTRY} $?
