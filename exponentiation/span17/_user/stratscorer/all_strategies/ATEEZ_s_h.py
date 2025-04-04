# ==============================================================================================
# ATEEZ trading strategy for SPOT
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
# As published, explained and tested in my Youtube video
#
# Visit my site for more information: https://www.dutchalgotrading.com/
# Become my Patron: https://www.patreon.com/dutchalgotrading
#
# freqtrade backtesting -s ATEEZ_s -c user_data/spot_config.json --timeframe=1d
# freqtrade backtesting -s ATEEZ_s -p BTC/USDT -c user_data/spot_config.json --timeframe=1d
# freqtrade plot-dataframe -s ATEEZ_s -p BTC/USDT -c user_data/spot_config.json --timeframe=1d
# freqtrade hyperopt -c user_data/spot_config.json -s ATEEZ_s_h --epochs 50 --spaces buy --hyperopt-loss SharpeHyperOptLoss
# ==============================================================================================
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
from functools import reduce
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


class ATEEZ_s_h(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Proposed timeframe for the strategy. Can be altered to your own preferred timeframe.
    timeframe = "1d"

    # Can this strategy go short?
    can_short: bool = False
    
    # Minimal ROI designed for the strategy.
    # Set to 100%
    minimal_roi = {"0": 1.0}

    # Optimal stoploss designed for the strategy.
    # Set to 10%
    stoploss = -0.15

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
            # Main plot indicators (Moving averages, ...)
            'main_plot': {
                'ema21': {'color': 'red'},
                'ema100': {'color': 'blue'},
            },
            'subplots': {
                # Subplots - each dict defines one additional plot
                "TSI": {
                    'tsi': {'color': 'blue'},
                    'tsi_signal': {'color': 'orange'},
                },
                "APO": {
                    'apo': {'color': 'purple'},
                },
                "ZSCORE": {
                    'zscore': {'color': 'orange'},
                }

            }
        }

    # Optimization spaces
    quick_ema = IntParameter(13, 56, default=21, space="buy")
    slow_ema = IntParameter(13, 56, default=100, space="buy")
    zscore_val= IntParameter(20, 51, default=50, space="buy")


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Below are the ATEEZ indicators for the strategy used.
        # Absolute Price Oscillator
        # True Strength Index
        # Ema 21
        # Ema 100
        # Z-score

        for val in self.quick_ema.range:
            dataframe[f'quick_ema_{val}'] = pta.ema(close = dataframe['close'], length = val) 
        for val in self.slow_ema.range:
            dataframe[f'slow_ema_{val}'] = pta.ema(close = dataframe['close'], length = val) 

        for val in self.zscore_val.range:
            dataframe[f'zscore_{val}'] = pta.zscore(close = dataframe['close'], length = val) 


        dataframe['apo']=pta.apo(close=dataframe['close'], mamode='ema')

        fa = 13
        sl = 25
        si = 13

        dataframe['tsi'] = pta.tsi(close = dataframe['close'], fast = fa, slow = sl, signal = si)[f'TSI_{fa}_{sl}_{si}']
        dataframe['tsi_signal'] = pta.tsi(close = dataframe['close'], fast = fa, slow = sl, signal = si)[f'TSIs_{fa}_{sl}_{si}']

        # first check if dataprovider is available
        if self.dp:
            if self.dp.runmode.value in ("live", "dry_run"):
                ob = self.dp.orderbook(metadata["pair"], 1)
                dataframe["best_bid"] = ob["bids"][0][0]
                dataframe["best_ask"] = ob["asks"][0][0]

        # print(self)
        # print(metadata)
        # print(dataframe)
        # print(dataframe[['date', 'close', 'apo', 'tsi','tsi_signal', 'ema21', 'ema100', 'zscore','signal','advice_changed']][dataframe['advice_changed']==True].tail(15))
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Long trades here:
        conditions = []
        conditions.append(
            (dataframe['apo'] > 0) 
            & ( dataframe['close'] > dataframe[f'quick_ema_{self.quick_ema.value}']) 
            & (dataframe['close'] > dataframe[f'slow_ema_{self.slow_ema.value}']) 
            & (dataframe[f'quick_ema_{self.quick_ema.value}'] > dataframe[f'slow_ema_{self.slow_ema.value}']) 
            & (dataframe['tsi'] > dataframe['tsi_signal']) 
            & (dataframe['tsi'] > 0) 
            & (dataframe[f'zscore_{self.zscore_val.value}']  > 0.0)
            & (dataframe["volume"] > 0)  # Guard
        )
        if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'enter_long'] = 1

        # # For short trades, use the section below
        # dataframe.loc[
        #     (
        #     # If sell short signal is True, then enter a short trade
        #     (dataframe["signal"] == 'short')
        #     # & (dataframe["advice_changed"] == True)
        #     & (dataframe["volume"] > 0)  # Guard            
        #     ),
        #     ["enter_short", "enter_tag"],
        # ] = (1, "short_signal")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Exit long here:
        conditions = []
        conditions.append(
            (dataframe['tsi'] < dataframe['tsi_signal'])
            & (dataframe["volume"] > 0)  # Guard
        )
        if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'exit_long'] = 1
           

        # # For short trades, use the section below
        # dataframe.loc[
        #     (
        #     # The exit signal for shorts trades is pretty straightforward.
        #     # Sell when the close price is below the kijun sen
        #     (dataframe["short_exit"] == True)
        #     & (dataframe["volume"] > 0)  # Guard
        #     ),
        #     ["exit_short", "exit_tag"],
        # ] = (1, "exit_short_signal")

        return dataframe
