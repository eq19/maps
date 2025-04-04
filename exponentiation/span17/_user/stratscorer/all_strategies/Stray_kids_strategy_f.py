# ==============================================================================================
# Stray kids strategy for Futures
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
# As published, explained and tested in my Youtube video:
#
# Visit my site for more information: https://www.dutchalgotrading.com/
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
# freqtrade backtesting -c user_data/futures_config.json -s skz_f --timerange=20190101-20210530 --timeframe=1d
# freqtrade backtesting -c user_data/futures_config.json -s skz_f --timerange=-20230101 --timeframe=1d
# freqtrade backtesting-analysis
# freqtrade plot-dataframe -p BTC/USDT:USDT --strategy skz_f -c user_data/futures_config.json
# freqtrade plot-dataframe -p AXS/USDT:USDT --strategy skz_f -c user_data/futures_config.json
# freqtrade plot-dataframe -p SOL/USDT:USDT --strategy skz_f -c user_data/futures_config.json
# freqtrade hyperopt -c user_data/futures_config.json -s skz_f --timeframe=1d --spaces roi stoploss --epochs 500 --random-state 8105 --min-trades 10 --hyperopt-loss SharpeHyperOptLoss
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


class skz_f(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Proposed timeframe for the strategy. Can be altered to your own preferred timeframe.
    timeframe = "1d"

    # Can this strategy go short?
    can_short: bool = True

    # Minimal ROI designed for the strategy.
    # Set to 10000% since the exit signal determines the trade exit.
    # Some crypto even got ROI triggered at 100% so had to set it to this value.
    minimal_roi = {"0": 100.0}

    # Optimal stoploss designed for the strategy.
    # Set to 100% since the exit signal dermines the trade exit.
    stoploss = -0.25

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
            "main_plot": {
                'kijun': {"color": "red"},
                # 'st': {"color": "blue"}
            },
            'subplots': {
                # Create subplot MACD
                "zscore": {
                    'zscore': {'color': 'green', 'type': 'bar', 'plotly': {'opacity': 0.4}}
                    },
                },
        }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Z score indicator
        dataframe['zscore'] = pta.zscore(close=dataframe['close'], length=14)

        # Supertrend indicator
        st_length = 10
        st_mult = 5.0
        dataframe['st'] = pta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'],
                                         length=st_length, multiplier=st_mult)[f'SUPERTd_{st_length}_{st_mult}']

        # CREATE ICHIMOKU INDICATOR
        # Specify the lenghts for each indicator (20, 60, 120, 60 is for crypto trading)

        TS = 9
        KS = 26
        SS = 52
        CS = 26
        OS = 0

        # Only create the kijun sen here
        dataframe["kijun"] = pta.ichimoku(
            high=dataframe["high"],
            low=dataframe["low"],
            close=dataframe["close"],
            tenkan=TS,
            kijun=KS,
            senkou=SS,
            offset=OS,
        )[0][f"IKS_{KS}"]

        # The actual signals can be configured here as dataframe columns
        # Or either as signals in the entry function below.
        dataframe['long'] = (dataframe['st'] == 1) & (dataframe['close'] >
                                                      dataframe['kijun']) & (dataframe['zscore'] > 0)
        dataframe['short'] = (dataframe['st'] == -1) & (dataframe['close'] <
                                                        dataframe['kijun']) & (dataframe['zscore'] < 0)

        # first check if dataprovider is available
        if self.dp:
            if self.dp.runmode.value in ("live", "dry_run"):
                ob = self.dp.orderbook(metadata["pair"], 1)
                dataframe["best_bid"] = ob["bids"][0][0]
                dataframe["best_ask"] = ob["asks"][0][0]

        # print(self)
        print(metadata)
        # print(dataframe[dataframe['long'] == True])
        # print(dataframe[dataframe['short'] == True])
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Uncomment this line if you use the dataframe signal column above
                # (dataframe["long"] == True) & (dataframe["volume"] > 0)  # Guard
                (dataframe['st'] == 1)
                & (dataframe['zscore'] > 0)
                & (qtpylib.crossed_above(dataframe['close'], dataframe['kijun']))
                # & (dataframe['close'] > dataframe['kijun'])
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "Long _signal")

        # For short trades, use the section below
        dataframe.loc[
            (
                # Uncomment this line if you use the dataframe signal column above
                # (dataframe["short"] == True) & (dataframe["volume"] > 0)  # Guard
                (dataframe['st'] == -1)
                & (dataframe['zscore'] < 0)
                & (qtpylib.crossed_below(dataframe['close'], dataframe['kijun']))
                # & (dataframe['close'] < dataframe['kijun'])

            ),
            ["enter_short", "enter_tag"],
        ] = (1, "Short_signal")

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # The exit signal for long trades is pretty straightforward.
                # Sell when the close price is below the kijun sen
                # (dataframe["close"] < dataframe["kijun"]) & (dataframe["volume"] > 0)  # Guard
                (qtpylib.crossed_below(dataframe['close'], dataframe['kijun'])) & (
                    dataframe["volume"] > 0)  # Guard
            ),
            ["exit_long", "exit_tag"],
        ] = (1, "Long_exit")

        # For short trades, use the section below
        dataframe.loc[
            (
                # The exit signal for shorts trades is pretty straightforward.
                # Sell when the close price is above the kijun sen
                # (dataframe["close"] > dataframe["kijun"]) & (dataframe["volume"] > 0)  # Guard
                (qtpylib.crossed_above(dataframe['close'], dataframe['kijun'])) & (
                    dataframe["volume"] > 0)  # Guard
            ),
            ["exit_short", "exit_tag"],
        ] = (1, "Short_exit")

        return dataframe
