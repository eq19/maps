# ==============================================================================================
# long_short_baseline
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
# Date    : 2023-04
# Remarks :
#    As published, explained and tested in my Youtube video:
#
# Visit my site for more information:
# Become my Patron: https://www.patreon.com/dutchalgotrading
#    -
#    -
# ==============================================================================================
# --- Used commands for later reference ---
# source .env/bin/activate
# freqtrade --version
# freqtrade new-config
# freqtrade new-strategy --strategy <strategyname>
# freqtrade test-pairlist -c user_data/futures_config.json
# freqtrade download-data -c user_data/futures_config.json --timerange 20170606- -t 1d 4h 1h 30m 15m 5m 1m
# freqtrade backtesting -c user_data/futures_config.json -s <strategyname> --timerange=20190101-20210530 --timeframe=1d
# freqtrade backtesting-analysis
#
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


class long_short_baseline(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Proposed timeframe for the strategy. Can be altered to your own preferred timeframe.
    timeframe = "1d"

    # Can this strategy go short?
    can_short: bool = True

    # Minimal ROI designed for the strategy.
    # Set to 100% since the exit signal determines the trade exit.
    minimal_roi = {"0": 1.0}

    # Optimal stoploss designed for the strategy.
    # Set to 100% since the exit signal dermines the trade exit.
    stoploss = -1.0

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
            "main_plot": {
                "tema": {},
                "sar": {"color": "white"},
            },
            "subplots": {
                # Subplots - each dict defines one additional plot
                "MACD": {
                    "macd": {"color": "blue"},
                    "macdsignal": {"color": "orange"},
                },
                "RSI": {
                    "rsi": {"color": "red"},
                },
            },
        }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["EMA_QUICK"] = ta.SMA(dataframe, timeperiod=7)
        dataframe["EMA_SLOW"] = ta.SMA(dataframe, timeperiod=21)

        print(dataframe)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["close"] > dataframe["EMA_QUICK"])
                & (dataframe["EMA_QUICK"] > dataframe["EMA_SLOW"])
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "Strong_long_signal")

        # For short trades, use the section below
        dataframe.loc[
            (
                (dataframe["close"] < dataframe["EMA_QUICK"])
                & (dataframe["EMA_QUICK"] < dataframe["EMA_SLOW"])
            ),
            ["enter_short", "enter_tag"],
        ] = (1, "Strong_short_signal")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            ((dataframe["close"] < dataframe["EMA_QUICK"]) & (dataframe["volume"] > 0)),  # Guard
            ["exit_long", "exit_tag"],
        ] = (1, "Close_below_kijun")

        # For short trades, use the section below
        dataframe.loc[
            ((dataframe["close"] > dataframe["EMA_QUICK"]) & (dataframe["volume"] > 0)),  # Guard
            ["exit_short", "exit_tag"],
        ] = (1, "Close_above_kijun")

        return dataframe
