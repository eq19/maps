#!/usr/bin/env bash

rm -rf ${RUNNER_TEMP}/*dir

WIKI=https://github.com/$2/$1.wiki.git
BASE=https://github.com/eq19/eq19.github.io.wiki.git

#git ls-remote ${WIKI} > /dev/null 2>&1
#if [[ $? == 0 ]]; then git clone $WIKI ${RUNNER_TEMP}/workdir;
#else git clone $BASE ${RUNNER_TEMP}/workdir && rm -rf ${RUNNER_TEMP}/workdir/Home.md; fi
#gh release view --json name,body,tagName --jq '.body' -R eq19/feed
#mv -f ${RUNNER_TEMP}/workdir/virtual /maps/_includes/virtual && mkdir ${RUNNER_TEMP}/gistdir

gh gist clone 0ce5848f7ad62dc46dedfaa430069857 ${RUNNER_TEMP}/gistdir/identition/span1
gh gist clone b32915925d9d365e2e9351f0c4ed786e ${RUNNER_TEMP}/gistdir/identition/span2
gh gist clone 88d09204b2e5986237bd66d062406fde ${RUNNER_TEMP}/gistdir/identition/span3
gh gist clone 8cab5e72d52ecb338a2f2187082a1699 ${RUNNER_TEMP}/gistdir/identition/span4
gh gist clone 54600a56d20163c2da8910dd804ec406 ${RUNNER_TEMP}/gistdir/identition/span5
gh gist clone f1af4317b619154719546e615aaa2155 ${RUNNER_TEMP}/gistdir/identition/span6
gh gist clone 6c89c3b0f109e0ead561a452720d1ebf ${RUNNER_TEMP}/gistdir/identition/span7
gh gist clone f21abd90f8d471390aad23d6ecc90d6d ${RUNNER_TEMP}/gistdir/identition/span8
gh gist clone 6e2fcc2138be6fb68839a3ede32f0525 ${RUNNER_TEMP}/gistdir/identition/span9
gh gist clone b541275ab7deda356feef32d600e44d8 ${RUNNER_TEMP}/gistdir/identition/span10
gh gist clone 80c8098f16f3e6ca06893b17a02d910e ${RUNNER_TEMP}/gistdir/identition/span11
gh gist clone 4ffc4d02579d5cfd336a553c6da2f267 ${RUNNER_TEMP}/gistdir/identition/span12

gh gist clone f78d4470250720fb18111165564d555f ${RUNNER_TEMP}/gistdir/exponentiation/span13
gh gist clone 765ddc69e339079a5a64b56c1d46e00f ${RUNNER_TEMP}/gistdir/exponentiation/span14
gh gist clone b9f901cda16e8a11dd24ee6b677ca288 ${RUNNER_TEMP}/gistdir/exponentiation/span15
gh gist clone dc30497160f3389546d177da901537d9 ${RUNNER_TEMP}/gistdir/exponentiation/span16
gh gist clone e84a0961dc7636c01d5953d19d65e30a ${RUNNER_TEMP}/gistdir/exponentiation/span17
gh gist clone e9832026b5b78f694e4ad22c3eb6c3ef ${RUNNER_TEMP}/gistdir/exponentiation/span18

rm -rf ${RUNNER_TEMP}/spin.txt && touch ${RUNNER_TEMP}/spin.txt
find ${RUNNER_TEMP}/gistdir -type f -name "README.md" -exec rm -rf {} \;

git clone $BASE ${RUNNER_TEMP}/workdir
mv -f ${RUNNER_TEMP}/workdir/Home.md ${RUNNER_TEMP}/workdir/README.md
find ${RUNNER_TEMP}/gistdir -type f -name 'spin_*.txt' | sort -n -t _ -k 2  | while ((i++)); IFS= read -r f; do sort.sh $f $i; done

if [[ "${WIKI}" != "${BASE}" ]]; then
  git clone $WIKI ${RUNNER_TEMP}/wikidir
  mv -f ${RUNNER_TEMP}/wikidir/Home.md ${RUNNER_TEMP}/wikidir/README.md
  echo $3
  find ${RUNNER_TEMP}/gistdir -type d -name "$3" -prune -exec sh -c 'wiki.sh "$1"' sh {} \;
fi
