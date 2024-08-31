#!/usr/bin/env bash

# root
echo -e "\n$hr\nROOT PROFILES\n$hr"
echo "/root"
[[ "$(whoami)" == "root" ]] && ls -alL /root || sudo bash -c 'ls -alL /root'

# root ssh
echo -e "\n$hr\nSSH FILES\n$hr"
echo "/root/.ssh"
mkdir /root/.ssh
[[ "$(whoami)" == "root" ]] && ls -alL /root/.ssh || sudo bash -c 'ls -alL /root/.ssh'

# git/config
cd ${WORKING_DIR}
echo -e "\n$hr\nGIT PROFILES\n$hr"
ls -al .git

echo -e "\n$hr\nGIT CPNFIG\n$hr"
chown -R $(whoami) .git/config
git config --unset http.https://github.com/.extraheader
git config --unset-all http.https://github.com/.extraheader
git config --global --unset http.https://github.com/.extraheader
git config --system --unset http.https://github.com/.extraheader
git submodule update --init --recursive
git submodule foreach --recursive git fetch
git submodule foreach 'git fetch origin; git checkout $(git rev-parse --abbrev-ref HEAD); git reset --hard origin/$(git rev-parse --abbrev-ref HEAD); chown -R $(whoami) .git; chmod -R +x .git; git config --unset http.https://github.com/.extraheader; git config --unset-all http.https://github.com/.extraheader; git config --global --unset http.https://github.com/.extraheader; git config --system --unset http.https://github.com/.extraheader;git submodule update --recursive; git clean -dfx'

cat .git/config

# environtment
echo -e "\n$hr\nENVIRONTMENT\n$hr"
printenv | sort

# Generate a Gemfile.lock
# $ docker run --rm -v "$PWD":/usr/src/app -w /usr/src/app combos/ruby_node:3_16 bundle install
