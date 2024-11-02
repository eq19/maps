#!/usr/bin/env bash

# Restore the modification time (mtime) of all files in work tree, based on the
# date of the most recent commit that modified the file.
for f in $(git ls-files); do
  mtime=$(git log -1 --format='%at' -- "$f")
  [[ "$mtime" == "" ]] && continue
  mtime=$(date -d @"$mtime" "+%Y-%m-%dT%H:%M:%S")
  touch -d "$mtime" "$f"
done

cd ${WORKING_DIR}
git submodule update --init --recursive
git submodule foreach --recursive git fetch
git submodule foreach 'git fetch origin; git checkout $(git rev-parse --abbrev-ref HEAD); git reset --hard origin/$(git rev-parse --abbrev-ref HEAD); chown -R $(whoami) .git; chmod -R +x .git; git config --unset http.https://github.com/.extraheader; git config --unset-all http.https://github.com/.extraheader; git config --global --unset http.https://github.com/.extraheader; git config --system --unset http.https://github.com/.extraheader;git submodule update --recursive; git clean -dfx'

cd ${WORKING_DIR}/docs/_feed/parser
mv _sass ${JEKYLL_SRC}/ && ln -s ${JEKYLL_SRC}/_sass _sass
mv assets ${JEKYLL_SRC}/ && ln -s ${JEKYLL_SRC}/assets assets
mv _plugins ${JEKYLL_SRC}/ && ln -s ${JEKYLL_SRC}/_plugins _plugins
mv _layouts ${JEKYLL_SRC}/ && ln -s ${JEKYLL_SRC}/_layouts _layouts
mv _includes ${JEKYLL_SRC}/ && ln -s ${JEKYLL_SRC}/_includes _includes

cd ${WORKING_DIR}
