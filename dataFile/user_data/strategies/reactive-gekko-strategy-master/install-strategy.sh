#!/bin/bash

echo '----------------------------------------'
echo 'Core files: '

echo "> reative-strategy"
ln -s ./strategy-files/reative-strategy.js ./strategies/reative-strategy.js
ln -s ./strategy-files/reative-strategy.toml ./config/strategies/reative-strategy.toml

echo 'Extras: '

for f in stochastic
do
  echo "> $f"
  stratfile="$f.js"
	configfile="$f.toml"

  sin="./strategy-files/extra-strategies/${stratfile}"
  sout="./strategies/${stratfile}"
  ln -s $sin $sout

  cin="./strategy-files/extra-strategies/${configfile}"
  cout="./config/strategies/${configfile}"
  ln -s $cin $cout
done

echo '----------------------------------------'
echo 'Installation complete'
