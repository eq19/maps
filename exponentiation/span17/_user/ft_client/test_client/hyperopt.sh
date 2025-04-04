#!/bin/bash
# 1.1 Changed timerange values to include 2022 dataset, added futures config/spot config choice,
# changed loss function to Sortino (was Sharpe)
# 1.2 Added the backtest command after hyperopting the strategy. This way the strategy gets tested directly after optimizing.

# VARIABLE SECTION
LOGDIR=user_data/backtest_results
TIMESTAMP=`date "+%Y%m%d-%H%M%S"`
TIMERANGE='-20230101'
EXTENSION='txt'
DATADIR='binance'

read -p 'Input strategy name: ' STRATEGY
read -p 'Is this a spot or futures strategy (s/f): ' TYPE
read -p 'Input timeframe (1d/4h/1h/30m/15m/5m/1m): ' TIMEFRAME
read -p 'Do you want to use roi & stoploss (y/n)?: ' SPACECHOICE
read -p 'Do you want to use trailing stoploss (y/n)?: ' TRAILING

# Determine the config that belongs to the type of strategy
if [ $TYPE = 's' ]; then
    CONFIG=./user_data/spot_config.json
  	TPE='spot'
elif [ $TYPE = 'f' ]; then
    CONFIG=./user_data/futures_config.json
	TPE='futures'
else
   echo "You entered an unknown parameter."
   echo "Exiting!"
   set -u
fi

# Determine which loss function should be used
if [ $TIMEFRAME = '1d' ]; then
	LOSS="SortinoHyperOptLossDaily"
	#LOSS="SharpeHyperOptLossDaily"
else
	LOSS="SortinoHyperOptLoss"
	#LOSS="SharpeHyperOptLoss"
fi

# Determine the correct timerange for the chosen timeframe
if [ $TIMEFRAME = '1m' ]; then
	TIMERANGE="--timerange=20210901-20230101"
elif [ $TIMEFRAME = '5m' ]; then
	TIMERANGE="--timerange=20210601-20230101"
elif [ $TIMEFRAME = '15m' ]; then
	TIMERANGE="--timerange=20210101-20230101"
else 
    TIMERANGE="--timerange=-20230101"
fi

# Determine if default spaces should be used
if [ $SPACECHOICE = 'y' ]; then
	SPACES="roi stoploss "
elif [ $SPACECHOICE = 'n' ]; then
	SPACES=""
else
   echo "You entered an unknown parameter."
   echo "Exiting!"
   set -u
fi

if [ $TRAILING = 'y' ]; then
    TRAILING="trailing "
elif [ $TRAILING = 'n' ]; then
    TRAILING=""
else
   echo "You entered an unknown parameter."
   echo "Exiting!"
   set -u
fi

# Ask for other spaces if needed
read -p 'Input more spaces (buy sell): ' MORESPACES

echo
echo "Recap of all settings: " | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
echo -strategy: $STRATEGY | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
echo -timeframe: $TIMEFRAME | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
echo -lossfunction: $LOSS | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
#echo $SPACES
#echo $MORESPACES
echo -spaces: $SPACES $TRAILING $MORESPACES | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
echo -timerange: $TIMERANGE | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP
echo
echo Hyperopt log will be placed in  $LOGDIR | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP


#echo "freqtrade hyperopt -c user_data/backtest-config.json  --epochs 10 --timeframe $TIMEFRAME --spaces $SPACES $MORESPACES --hyperopt-loss $LOSS -s $STRATEGY $TIMERANGE"
start=$SECONDS

# Start hyperopt
freqtrade hyperopt -c $CONFIG --epochs 1000 --random-state 12345 --timeframe $TIMEFRAME --spaces $SPACES $TRAILING $MORESPACES --hyperopt-loss $LOSS -s $STRATEGY $TIMERANGE 2>&1 | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP

# After hyperopt start backtest with hyperopt optimization
freqtrade backtesting --config $CONFIG --export trades --export-filename 'user_data/backtest_results/'$STRATEGY'-'$TPE'-HYPEROPTSETTINGS' --timeframe $TIMEFRAME $TIMERANGE --strategy $STRATEGY --datadir user_data/data/$DATADIR 2>&1 | tee -a $LOGDIR/$STRATEGY-$TPE-$TIMESTAMP'-HYPEROPTSETTINGS'.$EXTENSION


end=$SECONDS
echo
echo "Duration of Hyperopt: $(((start-end)/60)) minutes." | tee -a $LOGDIR/$STRATEGY-hyperopt-$TIMESTAMP

#freqtrade hyperopt -c  user_data/backtest-config.json  --epochs 1000 --spaces stoploss roi --hyperopt-loss SharpeHyperOptLoss --timeframe 15m -s ReinforcedSmoothScalp --timerange=20210601-20230101 --random-state 12345

echo
echo "Use 'freqtrade hyperopt-list --best' to show best recent Hyperopt results."
echo "Use 'freqtrade hyperopt-list --profitable' to show most profitable recent Hyperopt results."
echo "Use 'btst $STRATEGY --timeframe $TIMEFRAME' to backtest strategy with hyperopt result"
