#!/usr/bin/env bash

set -e
export WORKING_DIR=${PWD}
chown -R $(whoami) ${WORKING_DIR}
export hr=$(printf '=%.0s' {1..80})

# Initial default value
export TOKEN=${INPUT_TOKEN}
export ACTOR=${GITHUB_ACTOR}
export REPOSITORY=${INPUT_REPOSITORY}
export OWNER=${GITHUB_REPOSITORY_OWNER}
export BRANCH=${INPUT_BRANCH:=gh-pages}
export PROVIDER=${INPUT_PROVIDER:=github}
export BUNDLER_VER=${INPUT_BUNDLER_VER:=>=0}
export JEKYLL_BASEURL=${INPUT_JEKYLL_BASEURL:=}
export PRE_BUILD_COMMANDS=${INPUT_PRE_BUILD_COMMANDS:=}
export SCRIPT_DIR=/maps/Scripts && chmod -R +x ${SCRIPT_DIR}
export PREFIX=${WORKING_DIR}/docs/_data/ta-lib/linux/ta-lib

# https://stackoverflow.com/a/42137273/4058484
export JEKYLL_SRC=${WORKING_DIR}
export JEKYLL_GITHUB_TOKEN=${TOKEN}

if [[ "${OWNER}" == "chetabahana" ]]; then
  export JEKYLL_SRC=${WORKING_DIR}/docs
fi
export JEKYLL_CFG=${JEKYLL_SRC}/_config.yml
sed -i -e "s/eq19/${OWNER}/g" ${JEKYLL_CFG}

if [[ -z "${TOKEN}" ]]; then
  echo -e "Please set the TOKEN environment variable."
  exit 1
fi

# Pre-handle Jekyll baseurl
if [[ -n "${JEKYLL_BASEURL-}" ]]; then
  JEKYLL_BASEURL="--baseurl ${JEKYLL_BASEURL}"
fi

# Initialize environment
export RUBYOPT=W0
export RUBY_VERSION=2.7.0
export RAILS_VERSION=5.0.1
export BUNDLER_VER=${BUNDLER_VER}
export BUNDLE_GEMFILE=/maps/Gemfile
export BUNDLE_SILENCE_ROOT_WARNING=1
#export TA_LIBRARY_PATH=${PREFIX}/lib
export NOKOGIRI_USE_SYSTEM_LIBRARIES=1
#export TA_INCLUDE_PATH=${PREFIX}/include
export PAGES_REPO_NWO=$GITHUB_REPOSITORY
export VENDOR_BUNDLE=${WORKING_DIR}/vendor/bundle
export SSL_CERT_FILE=$(realpath .github/hook-scripts/cacert.pem)

# identity
echo -e "\n$hr\nWHOAMI\n$hr"
whoami
pwd
id

# os version
echo -e "\n$hr\nOS VERSION\n$hr"
cat /etc/os-release
uname -r

# file system
echo -e "\n$hr\nFILE SYSTEM\n$hr"
df -h

# rootdir
echo -e "$hr\nROOT DIR\n$hr"
cd / && pwd && ls -al

# packages
echo -e "$hr\nVENV DIR\n$hr"
cd /maps && pwd && ls -al

# current
echo -e "$hr\nWORK DIR\n$hr"
cd ${WORKING_DIR} && pwd && ls -al

#echo -e "$hr\nPRIOR INSTALLATION\n$hr"
#chown -R root:root ${HOME} && dpkg -l
 
# cloning default repository
# https://stackoverflow.com/a/74439875/4058484
git config --global user.name "${ACTOR}"
git config --global user.email "${ACTOR}@users.noreply.github.com"
git config --global credential.helper store &>/dev/null
echo "https://{ACTOR}:${TOKEN}@github.com" > /root/.git-credentials
git clone --quiet --recurse-submodules -j8 ${REPOSITORY} /maps/feed/default

export NPM_CACHE_DIR=${VENDOR_BUNDLE}/npm
apt-get install -qq npm &>/dev/null && apt-get install -qq yarn &>/dev/null
npm install --prefix /maps --cache ${NPM_CACHE_DIR} &>/dev/null

export PATH=${HOME}/.local/bin:$PATH
export PIP_CACHE_DIR=${VENDOR_BUNDLE}/pip

#wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz &>/dev/null
cd ${PREFIX} #tar -xzf ta-lib-0.4.0-src.tar.gz &>/dev/null && cd ta-lib/
./configure --prefix=/usr &>/dev/null && make &>/dev/null && make install &>/dev/null

cd ${WORKING_DIR}
# https://pypi.org/project/pipx/
python -m pip install --upgrade pip setuptools six wheel &>/dev/null
python -m pip install pytest-cov -r /maps/requirements.txt &>/dev/null
python -m pip install jax[cuda11_cudnn82] \
  -f https://storage.googleapis.com/jax-releases/jax_releases.html &>/dev/null

export GEM_PATH=${VENDOR_BUNDLE}/gem
export GEM_HOME=${GEM_PATH}/ruby/${RUBY_VERSION}
export PATH=$PATH:${GEM_HOME}/bin

# https://stackoverflow.com/a/30369485/4058484
apt-get install -qq ruby ruby-dev ruby-bundler build-essential &>/dev/null
gem install rails --version "$RAILS_VERSION" --quiet --silent &>/dev/null

# installed packages
#echo -e "\n$hr\nUPON INSTALLATION\n$hr"
#dpkg -l

# Setting default ruby version
echo -e "$hr\nTENSORFLOW VERSION\n$hr"
pip show tensorflow-gpu && pip -V

# https://stackoverflow.com/a/60945404/4058484
ruby -v && bundler version && python -V
node -v && npm -v

# Restore modification time (mtime) of git files
echo -e "$hr\nEPOCH TEST\n$hr"
${SCRIPT_DIR}/restore.sh
${SCRIPT_DIR}/prime_list.sh
${SCRIPT_DIR}/init_environment.sh

# Clean up bundler cache
CLEANUP_BUNDLER_CACHE_DONE=false
bundle config path ${GEM_PATH}
bundle config cache_all true

cleanup_bundler_cache() {
  ${SCRIPT_DIR}/cleanup_bundler.sh
  rm -rf ${GEM_HOME} && mkdir -p ${GEM_HOME}
  gem install bundler -v "${BUNDLER_VER}" &>/dev/null
  echo -e "\nCLEANUP BUNDLE\n$hr" && bundle install
  CLEANUP_BUNDLER_CACHE_DONE=true
}

# If the vendor/bundle folder is cached in a differnt OS (e.g. Ubuntu),
# it would cause `jekyll build` failed, we should clean up the cache firstly.
OS_NAME_FILE=${GEM_PATH}/os-name
os_name=$(cat /etc/os-release | grep '^NAME=')
os_name=${os_name:6:-1}

if [[ "$os_name" != "$(cat $OS_NAME_FILE 2>/dev/null)" ]]; then
  cleanup_bundler_cache
  echo -e $os_name > $OS_NAME_FILE
fi

# Check and execute pre_build_commands commands
cd ${JEKYLL_SRC}

if [[ ${PRE_BUILD_COMMANDS} ]]; then
  eval "${PRE_BUILD_COMMANDS}"
fi

build_jekyll() {
  echo -e "\n$hr\nJEKYLL BUILD\n$hr" && pwd
  # https://gist.github.com/DrOctogon/bfb6e392aa5654c63d12
  JEKYLL_GITHUB_TOKEN=${TOKEN} bundle exec jekyll build --trace --profile \
    ${JEKYLL_BASEURL} -c ${JEKYLL_CFG} -d ${WORKING_DIR}/build

  # vendor/bundle
  echo -e "\n$hr\nVENDOR BUNDLE\n$hr" && chown -R root:root ${HOME}
  cd ${HOME} && mv -f .gem gem && mv -f gem/* ${VENDOR_BUNDLE}/gem/
  echo ${VENDOR_BUNDLE} && ls -al ${VENDOR_BUNDLE} && echo -e "\n"
  echo ${NPM_CACHE_DIR} && ls -al ${NPM_CACHE_DIR} && echo -e "\n"
  echo ${PIP_CACHE_DIR} && ls -al ${PIP_CACHE_DIR} && echo -e "\n"
  echo ${GEM_PATH} && ls -al ${GEM_PATH} && echo -e "\n"
  echo ${GEM_HOME} && ls -al ${GEM_HOME} && echo -e "\n"
  chmod -R a+rwx,o-w ${PIP_CACHE_DIR}
  echo -e "Source cleaning..\n"
  rm -rf gem && ls -al
}

build_jekyll || {
  $CLEANUP_BUNDLER_CACHE_DONE && exit -1
  echo -e "\nRebuild all gems and try to build again\n"
  cleanup_bundler_cache
  build_jekyll
}


cd ${WORKING_DIR}
echo -e "$hr\nDEPLOYMENT\n$hr"
# https://unix.stackexchange.com/a/83895/158462
git submodule foreach -q ${SCRIPT_DIR}/github_pages.sh


apt-get clean && rm -rf /var/lib/apt/lists/* ${RUNNER_TEMP}/* /var${RUNNER_TEMP}/*
exit $?
