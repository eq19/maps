#!/usr/bin/env bash
#
git config --global user.name eq19
git config --global user.email eq19@users.noreply.github.com
git clone https://eq19:$GH_TOKEN@github.com/$TARGET_REPOSITORY.wiki.git /tmp/wiki

if [[ ! -d /tmp/wiki/_user ]]; then
  git clone https://eq19:$GH_TOKEN@github.com/eq19/eq19.wiki.git /tmp/dummy
  rm -rf /tmp/wiki/* /tmp/dummy/.git && mv -f /tmp/dummy/* /tmp/wiki/
fi
  
rm -rf /tmp/wiki/_user && mv -f user_data /tmp/wiki/_user
find /tmp/wiki/_user/strategies -mindepth 1 -type d -exec rm -rf {} +
cd /tmp/wiki && git add . && git commit --allow-empty -m "update params" && git push
