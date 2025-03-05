#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------------------------------------------------'

if [[ "${WIKI}" != "${BASE}" ]]; then
  rm -rf ${RUNNER_TEMP//\\//}/wikidir

  git clone $WIKI ${RUNNER_TEMP//\\//}/wikidir
  cd ${RUNNER_TEMP//\\//}/wikidir && mv -f Home.md README.md

  find . -type d -name "${FOLDER}" -prune -exec sh -c 'wiki.sh "$1"' sh {} \;
  find . -type d -name "${FOLDER}" -prune -exec sh -c 'cat ${RUNNER_TEMP//\\//}/README.md >> $1/README.md' sh {} \;
  find . -type d -name "${FOLDER}" -prune -exec sh -c 'ls -alR' sh {} \;

fi
   
#echo "action_state=yellow" | Out-File -FilePath $env:GITHUB_ENV -Append # no need for -Encoding utf8
find . -iname '*.md' -print0 | sort -zn | xargs -0 -I '{}' front.sh '{}'
cd ${GITHUB_WORKSPACE//\\//} && pwd && ls -alR .
