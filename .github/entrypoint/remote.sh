#!/usr/bin/env bash

deploy_remote() {
  echo -e "Deploying to $1 on branch gh-pages"
  REMOTE_REPO="https://${ACTOR}:${TOKEN}@github.com/$1.git"

  git config --global user.name "${ACTOR}"
  git config --global user.email "${ACTOR}@users.noreply.github.com"

  git clone -b gh-pages --single-branch ${REMOTE_REPO} &>/dev/null
  cd "$(basename "${REMOTE_REPO}" .git)" && rm -rf *

  mv -v ${GITHUB_WORKSPACE}/_site/* . && touch .nojekyll && git add .
  git commit -m "jekyll build from cction ${GITHUB_SHA}"
  git push -u origin gh-pages
}
