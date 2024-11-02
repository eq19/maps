#!/usr/bin/env bash

gh gist clone 0ce5848f7ad62dc46dedfaa430069857 $1/identition/span1
gh gist clone b32915925d9d365e2e9351f0c4ed786e $1/identition/span2
gh gist clone 88d09204b2e5986237bd66d062406fde $1/identition/span3
gh gist clone 8cab5e72d52ecb338a2f2187082a1699 $1/identition/span4
gh gist clone 54600a56d20163c2da8910dd804ec406 $1/identition/span5
gh gist clone f1af4317b619154719546e615aaa2155 $1/identition/span6
gh gist clone 6c89c3b0f109e0ead561a452720d1ebf $1/identition/span7
gh gist clone f21abd90f8d471390aad23d6ecc90d6d $1/identition/span8
gh gist clone 6e2fcc2138be6fb68839a3ede32f0525 $1/identition/span9
gh gist clone b541275ab7deda356feef32d600e44d8 $1/identition/span10
gh gist clone 80c8098f16f3e6ca06893b17a02d910e $1/identition/span11
gh gist clone 4ffc4d02579d5cfd336a553c6da2f267 $1/identition/span12

gh gist clone f78d4470250720fb18111165564d555f $1/exponentiation/span13
gh gist clone 765ddc69e339079a5a64b56c1d46e00f $1/exponentiation/span14
gh gist clone b9f901cda16e8a11dd24ee6b677ca288 $1/exponentiation/span15
gh gist clone dc30497160f3389546d177da901537d9 $1/exponentiation/span16
gh gist clone e84a0961dc7636c01d5953d19d65e30a $1/exponentiation/span17
gh gist clone e9832026b5b78f694e4ad22c3eb6c3ef $1/exponentiation/span18

find $1 -type f -name "README.md" -exec rm -rf {} \;
rm -rf ${RUNNER_TEMP}/README.md && mv -f ${RUNNER_TEMP}/wikidir/README.md ${RUNNER_TEMP}/README.md && cp -R ${RUNNER_TEMP}/wikidir/* $1

rm -rf ${RUNNER_TEMP}/spin.txt && touch ${RUNNER_TEMP}/spin.txt
find $1 -type f -name 'spin_*.txt' | sort -n -t _ -k 2  | while ((i++)); IFS= read -r f; do sort.sh $f $i; done

rm -rf ${RUNNER_TEMP}/Sidebar.md && cp $1/_Sidebar.md ${RUNNER_TEMP}/Sidebar.md
sed -i 's/0. \[\[//g' ${RUNNER_TEMP}/Sidebar.md && sed -i 's/\]\]//g' ${RUNNER_TEMP}/Sidebar.md

find $1 -iname '*.md' -print0 | sort -zn | xargs -0 -I '{}' front.sh '{}'
cat ${RUNNER_TEMP}/spin.txt
