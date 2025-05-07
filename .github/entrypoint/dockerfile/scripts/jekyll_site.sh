#!/usr/bin/env bash
# Structure: Cell Types – Modulo 6

hr='------------------------------------------------------------------------------------'

echo -e "\n$hr\nSource ⚧️ dir\n$hr"
ls -al /home/runner/_site

set -a && . /home/runner/_site/.env && set +a
cd /home/runner/_site && rm -rf .env action.yml

git config --global user.name "${GITHUB_ACTOR}"
git config --global user.email "${GITHUB_ACTOR}@users.noreply.github.com"

REMOTE_REPO="https://${GITHUB_ACTOR}:${GITHUB_ACCESS_TOKEN}@github.com/${TARGET_REPOSITORY}.git"
git remote set-url origin ${REMOTE_REPO} && git config --global --add safe.directory "/home/runner/_site"
git add . && TEST_COMMIT=$(git commit -m "${LATEST_COMMIT}")

if [[ "${TEST_COMMIT}" =~ "nothing to commit" ]] ; then
  echo -e "\n$hr\nSource Pages\n$hr"
  ls -al /home/runner/_site
else
  echo -e "\n$hr\nBuild Pages\n$hr"
  #Jekyll Quick Reference https://gist.github.com/DrOctogon/bfb6e392aa5654c63d12
  JEKYLL_GITHUB_TOKEN=${GITHUB_ACCESS_TOKEN} DISABLE_WHITELIST=true jekyll build --profile -t -p /home/runner/_site/_plugins -d /home/runner/_site/docs    
  if [[ "${TARGET_REPOSITORY}" == "eq19/eq19.github.io" ]]; then echo "www.eq19.com" > /home/runner/_site/docs/CNAME; fi
  rm -rf /home/runner/_site/docs/.nojekyll && touch /home/runner/_site/docs/.nojekyll
fi

echo -e "\n$hr\nFinal Docs\n$hr"
TOKEN=$(/mnt/disks/platform/usr/bin/gcloud auth print-identity-token)
curl -s -X POST https://us-central1-feedmapping.cloudfunctions.net/function \
  -H "Authorization: Bearer ${TOKEN}" -H "Content-Type: application/json" \
  --data @/home/runner/_site/docs/data.json | jq '.' > /home/runner/_site/_data/wiki.json
/home/runner/.github/entrypoint/remote.sh /home/runner/_site/_data/wiki.json && ls -al /home/runner/_site/docs

echo -e "\n$hr\nNext Workflow\n$hr"
cd /home/runner/_site && git fetch && git add .
git commit --allow-empty -m "${LATEST_COMMIT}" && git rebase && git push

if [[ $? -eq 0 ]]; then
  echo -e "\njobs completed"
else
  exit 1
fi
