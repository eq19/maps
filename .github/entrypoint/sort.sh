#!/usr/bin/env bash

edit_file () {

  while ((i++)); IFS=' ' read -ra SORT; do

    T+=("${SORT[0]}")
    R+=("${SORT[1]}")
    A+=("${SORT[2]}")
    C+=("${SORT[3]}")
    K+=("${SORT[4]}")
    I+=("${SORT[5]}")
    N+=("${SORT[6]}")
    G+=("${SORT[7]}")

  done < ${RUNNER_TEMP}/spin.txt

  while ((j++)); IFS=' ' read -ra SORT; do

    SPIN="$((i+j-1))"
    SPIN+=" ${SORT[0]}"
    SPIN+=" ${SORT[1]}"
    SPIN+=" ${SORT[2]}"
    SPIN+=" ${SORT[3]}"
    
    echo "${SPIN} ${SORT[0]}" >> ${RUNNER_TEMP}/spin.txt

  done < $1

}

FILE=${1##*_} && NAME=${FILE%.*}
[[ $(($NAME + 0)) < 3 ]] && edit_file $1

