# ==============================================================================================
# KDA strategy for Spot
#
# Made by:
# ______         _         _      _____                      _         ______            _
# |  _  \       | |       | |    /  __ \                    | |        |  _  \          | |
# | | | | _   _ | |_  ___ | |__  | /  \/ _ __  _   _  _ __  | |_  ___  | | | | __ _   __| |
# | | | || | | || __|/ __|| '_ \ | |    | '__|| | | || '_ \ | __|/ _ \ | | | |/ _` | / _` |
# | |/ / | |_| || |_| (__ | | | || \__/\| |   | |_| || |_) || |_| (_) || |/ /| (_| || (_| |
# |___/   \__,_| \__|\___||_| |_| \____/|_|    \__, || .__/  \__|\___/ |___/  \__,_| \__,_|
#                                               __/ || |
#                                              |___/ |_|
# Version : 1.0
# Date    : 2023-05
# Remarks :
# As published, explained and tested in my Youtube video and blog site.
# Visit my site for more information: https://www.dutchalgotrading.com/
# Become my Patron: https://www.patreon.com/dutchalgotrading
# ==============================================================================================
# --- Used commands for later reference ---
# source .env/bin/activate
# freqtrade --version
# freqtrade new-config
# freqtrade new-strategy --strategy <strategyname>
# freqtrade test-pairlist -c user_data/spot_config.json
# freqtrade download-data -c user_data/spot_config.json --timerange 20170606- -t 1d 4h 1h 30m 15m 5m 1m
# freqtrade backtesting -c user_data/spot_config.json -s kda_s --timerange=20190101-20210530 --timeframe=1d
# freqtrade backtesting -c user_data/spot_config.json -s kda_s --timerange=-20230101 --timeframe=1d
# freqtrade backtesting-analysis
# freqtrade hyperopt -c user_data/spot_config.json -s kda_s --epochs 50 --spaces sell --random-state 8105 --min-trades 10 --hyperopt-loss SharpeHyperOptLoss
# freqtrade plot-dataframe -p BTC/USDT --strategy kda_s -c user_data/spot_config.json
#
# freqtrade backtesting -c user_data/spot_config.json -s kda_s --timerange=-20230101 --timeframe=1d -p CRV/USDT --export=signals
# freqtrade backtesting-analysis -c user_data/spot_config.json --analysis-groups 0 1 2 3 4 5 --enter-reason-list signal_long --indicator-list buyprice takeprofit stoploss close atr
# freqtrade plot-dataframe -p CRV/USDT --strategy kda_s -c user_data/spot_config.json
# ==============================================================================================

# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    IStrategy,
    merge_informative_pair,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib


class kda_s(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Proposed timeframe for the strategy. Can be altered to your own preferred timeframe.
    timeframe = "1d"

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    minimal_roi = {"0": 100.0}

    # Optimal stoploss designed for the strategy.
    # Either the stoploss according to the strategy get's hit or 25% loss should be taken.
    stoploss = -1

    # Trailing stoploss
    trailing_stop = False

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Number of candles the strategy requires before producing valid signals
    # Set to the default of 30.
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force.
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    @property
    def plot_config(self):
        return {
            'main_plot': {
                'takeprofit': {"color": "green"},
                'stoploss': {'color': 'red'},
                'buyprice': {'color': 'grey'}
            },
            'subplots': {
                # Subplots - each dict defines one additional plot
                "KTS": {
                    'kst': {'color': 'blue'},
                    'ksts': {'color': 'orange'},
                },
                "DPO": {
                    'dpo': {'color': 'purple'},
                },
                "ATR": {
                    'atr': {'color': 'grey'},
                }

            }
        }

    # Optimization spaces - Using categorical parameters to limit the amount of possible outcomes and optimization time
    # Uncomment this if you want to hyperopt
    atr_sl_mult_space = CategoricalParameter([1, 1.5, 2, 2.5, 3, 3.5, 4], default=2, space="sell")
    r_r_space = CategoricalParameter([1, 1.5, 2, 2.5, 3, 3.5, 4], default=2, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Creating the Know Sure Thing', 'Deterrent Price Oscillator' and 'Average True Range'.
        dataframe['kst'] = pta.kst(close=dataframe['close'])['KST_10_15_20_30_10_10_10_15']
        dataframe['ksts'] = pta.kst(close=dataframe['close'])['KSTs_9']
        dataframe['dpo'] = pta.dpo(close=dataframe['close'], lookahead=False)
        dataframe['atr'] = pta.atr(close=dataframe['close'],
                                   high=dataframe['high'], low=dataframe['low'])

        # These are the variables where I can determine how low the stop loss should be or
        # how far the risk reward ratio should be. These should be tweaked for optimal performance
        # Uncomment this if you want to manually determine the atr and r:r settings
        # atr_sl_mult = 2.5
        # r_r = 2

        # Determine the optimal stoploss and risk:reward settings
        # Uncomment this if you want to hyperopt
        for val in self.atr_sl_mult_space.range:
            atr_sl_mult = val
        for val in self.r_r_space.range:
            r_r = val

        # Functions for additional columns and calculations

        def buy_sell(data):
            '''
            This function looks at the conditions for each cell in a row and detects long or short if all the specific conditions are met.
            If not, then the Neutral signal is given.
            '''
            signal = []

            for i in range(len(dataframe)):
                if ((dataframe['kst'][i] > dataframe['ksts'][i]) & (dataframe['dpo'][i] > 0)):
                    signal.append('long')
                elif ((dataframe['kst'][i] < dataframe['ksts'][i]) & (dataframe['dpo'][i] < 0)):
                    signal.append('short')
                else:
                    signal.append('Neutral')

            return signal

        # Add the long or short signals to the dataframe column signal
        dataframe['signal'] = buy_sell(dataframe)
        dataframe['advice_changed'] = dataframe['signal'].shift(+1) != dataframe['signal']

        def tp_sl(data):
            # Make some empty lists to store information later
            stoploss = []
            takeprofit = []
            buyprice = []

            # Preconfigured values that are used as 'memory' of the last candle value in this function
            previous_signal = None
            previous_stoploss = np.nan
            previous_takeprofit = np.nan
            previous_buyprice = np.nan

            for i, row in data.iterrows():
                current_signal = row['signal']

                # Here is where the values are calculated, based on the status of the signals
                if current_signal != previous_signal:
                    if current_signal == 'long':
                        stoploss.append(row['close'] - (row['atr'] * atr_sl_mult))
                        takeprofit.append(row['close'] + ((row['atr'] * atr_sl_mult) * r_r))
                        buyprice.append(row['close'])
                    elif current_signal == 'short':
                        stoploss.append(row['close'] + (row['atr'] * atr_sl_mult))
                        takeprofit.append(row['close'] - ((row['atr'] * atr_sl_mult) * r_r))
                        buyprice.append(row['close'])
                    else:
                        stoploss.append(np.nan)
                        takeprofit.append(np.nan)
                        buyprice.append(np.nan)

                    previous_stoploss = stoploss[-1]
                    previous_takeprofit = takeprofit[-1]
                    previous_buyprice = buyprice[-1]
                else:
                    stoploss.append(previous_stoploss)
                    takeprofit.append(previous_takeprofit)
                    buyprice.append(previous_buyprice)

                previous_signal = current_signal

            # Finally add the outcome of the statements above to the dataframe
            data['stoploss'] = stoploss
            data['takeprofit'] = takeprofit
            data['buyprice'] = buyprice

            return data

        # Run the function that creates tp, sl and buy
        tp_sl(dataframe)

        # first check if dataprovider is available
        if self.dp:
            if self.dp.runmode.value in ("live", "dry_run"):
                ob = self.dp.orderbook(metadata["pair"], 1)
                dataframe["best_bid"] = ob["bids"][0][0]
                dataframe["best_ask"] = ob["asks"][0][0]

        # Uncomment this for analyzing dataframe generation and output
        # print(self)
        # print(metadata)
        # print(dataframe.tail(55))
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # If buy long signal is True, then enter a long trade
                (dataframe["signal"] == 'long')
                & (dataframe["advice_changed"] == True)
                & (dataframe["volume"] > 0)  # Guard
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "signal_long")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # There can be two conditions under which the long trade can be exited
                # close is either above takeprofit or below stoploss.
                (dataframe["close"] > dataframe["takeprofit"])
                # & (dataframe["signal"] == 'long')
                & (dataframe["volume"] > 0)  # Guard
            ),
            ["exit_long", "exit_tag"],
        ] = (1, "takeprofit_long_exit")

        dataframe.loc[
            (
                # There can be two conditions under which the long trade can be exited
                # close is either above takeprofit or below stoploss.
                (dataframe["close"] < dataframe["stoploss"])
                # & (dataframe["signal"] == 'long')
                & (dataframe["volume"] > 0)  # Guard
            ),
            ["exit_long", "exit_tag"],
        ] = (1, "stoploss_long_exit")

        # # Just an additional idea that I left behind
        # dataframe.loc[
        #     (
        #         # There is one final exit signal that indicates that the momentum is over
        #         # and the chance of getting profits is negligable. That is when the KST get's below its KST signal line
        #         (dataframe["kst"] < dataframe["ksts"])
        #         # & (dataframe["signal"] == 'long')
        #         & (dataframe["volume"] > 0)  # Guard
        #     ),
        #     ["exit_long", "exit_tag"],
        # ] = (1, "momentum_long_passed_exit")

        return dataframe
