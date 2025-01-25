# ==============================================================================================
# TaSearchLevelG15m
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
# Remarks :
# This strategy has been tipped by my patreon Reza Azadeh
# The original files are on the following location: https://github.com/ivanproskuryakov/ta-search
# I adjusted some of the code to make this file work on my system. The settings are based on the 
# original authors settings (config.json files).
# ALL CREDITS OF THIS STRATEGY GO TO THE ORIGINAL AUTHOR, IM AM JUST A PASSTHROUGH!!
#
# Visit my site for more information: https://www.dutchalgotrading.com/
# Become my Patron: https://www.patreon.com/dutchalgotrading
#
# --- Used commands for later reference ---
# source .env/bin/activate
# freqtrade --version
# freqtrade new-config
# freqtrade new-strategy --strategy <strategyname>
# freqtrade test-pairlist -c user_data/futures_config.json
# freqtrade download-data -c user_data/futures_config.json --timerange 20170606- -t 1d 4h 1h 30m 15m 5m 1m
# freqtrade backtesting -c user_data/futures_config.json -s TaSearchLevelG15m --timerange=20190101-20210530 --timeframe=1d --pairs BTC/USDT:USDT
# freqtrade backtesting-analysis
# ==============================================================================================
#
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---

import pandas as pd
import numpy as np
import talib.abstract as ta
import logging

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from scipy import signal
from statistics import mean

from freqtrade.persistence.trade_model import Trade
from freqtrade.strategy.interface import IStrategy

"minimal_roi": {
    "0": 0.05
},
"stoploss": -0.05,

"trailing_stop": true,
"trailing_stop_positive": 0.05,
"trailing_stop_positive_offset": 0.2,
"trailing_only_offset_is_reached": true,


class TaSearchLevelG15m(IStrategy):

    # DCD: Some of my own additions to make this strategy work on my setup for backtesting
    
    INTERFACE_VERSION = 3
    timeframe = "15m"
        # Minimal ROI designed for the strategy.
    # Set to 100% since the exit signal determines the trade exit.
    minimal_roi =  {
        "0": 0.15,
        "100": 0.1,
        "200": 0.05
        },

    # Optimal stoploss designed for the strategy.
    # Set to 100% since the exit signal dermines the trade exit.
    # stoploss = -0.05

    # Trailing stoploss
    # The author has set this to true, but since backtesting with stoploss is
    # not reliable I do not do this.
    trailing_stop = False
    # trailing_stop = true,
    # trailing_stop_positive =  0.05,
    # trailing_stop_positive_offset = 0.1,
    # trailing_only_offset_is_reached = true,


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


    can_short: bool = True

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        pd.set_option('display.max_rows', 100000)
        pd.set_option('display.precision', 10)
        pd.set_option('mode.chained_assignment', None)

        df['rsi_7'] = ta.RSI(df['close'], timeperiod=7).round(2)
        df['min_level'] = 0
        df['max_level'] = 0
        df['buy_short'] = 0
        df['buy_long'] = 0
        df['buy_short2'] = 0
        df['buy_long2'] = 0
        df['i_close'] = 0
        df['i_open'] = 0
        df['i_low'] = 0
        df['i_high'] = 0

        logging.getLogger('freqtrade').info(str(metadata))

        df = self.do_heikin_ashi(df)
        df = self.do_long(df)
        df = self.do_short(df)

        return df

    def do_long(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 200
        df['min_local'] = df.iloc[signal.argrelextrema(df.c.values, np.less_equal, order=n)[0]]['c']
        min = df['c'].max()

        times = df.query(f'min_local > 0')
        prices = []

        if len(times) > 0:
            for i in range(500, len(df)):
                if df['min_local'].loc[i] > 0:
                    close = df['c'].loc[i]

                    chunk = df[:i - 10]
                    chunk['min_local'] = chunk.iloc[signal.argrelextrema(chunk.c.values, np.less_equal, order=n)[0]]['c']

                    time_chunk = chunk.query(f'min_local > 0')

                    for x, row in time_chunk.iterrows():
                        close_chunk = time_chunk['c'].loc[x]
                        prices.append(close_chunk)

                    for p in prices:
                        diff = self.diff_percentage(p, close)

                        if 0 < diff < 0.3:
                            logging.getLogger('freqtrade').info(str([i, '+++', diff, p]))
                            df['min_level'].loc[i] = 1

                for x in range(i - 2, i):
                    # if candle green
                    # if df['min_level'].loc[x] > 0 and df['o'].loc[i] < df['c'].loc[i]:
                    if df['min_level'].loc[x] > 0:
                        close = df['c'].loc[i]

                        # if same value presented in past
                        # and if value < average for long

                        df_tail = df[i - 200: i].query(f'c < {close}')

                        if len(df_tail) > 0:
                            logging.getLogger('freqtrade').info(
                                str([i, '++++', min, diff, '---', prices, 'long ++++++'])
                            )
                            df['buy_long'].loc[i] = 1
                            df['i_low'].loc[i] = df['low'].loc[x]
                            df['i_high'].loc[i] = df['high'].loc[x]
                            df['i_open'].loc[i] = df['o'].loc[x]
                            df['i_close'].loc[i] = df['c'].loc[x]

                for x in range(i - 100, i):
                    if df['min_level'].loc[x] > 0:
                        diff = self.diff_percentage(df['c'].loc[x], df['c'].loc[i])
                        # print('long ------- ', diff)
                        # long
                        # past < now
                        # if df['c'].loc[x] < df['c'].loc[i] and 0 < diff < 1:
                        if 0 < diff < 1:
                            logging.getLogger('freqtrade').info(
                                str([i, '---- long2 ----'])
                            )
                            df['buy_long2'].loc[i] = 1
                            df['i_low'].loc[i] = df['low'].loc[x]
                            df['i_high'].loc[i] = df['high'].loc[x]
                            df['i_open'].loc[i] = df['o'].loc[x]
                            df['i_close'].loc[i] = df['c'].loc[x]

        return df

    def do_short(self, df: pd.DataFrame) -> pd.DataFrame:
        n = 200
        df['max_local'] = df.iloc[signal.argrelextrema(df.c.values, np.greater_equal, order=n)[0]]['c']
        max = df['c'].min()

        times = df.query(f'max_local > 0')
        prices = []

        if len(times) > 0:
            for i in range(500, len(df)):
                if df['max_local'].loc[i] > 0:
                    close = df['c'].loc[i]

                    chunk = df[:i - 10]
                    chunk['max_x'] = chunk.iloc[signal.argrelextrema(chunk.c.values, np.greater_equal, order=n)[0]]['c']

                    time_chunk = chunk.query(f'max_x > 0')

                    for x, row in time_chunk.iterrows():
                        close_chunk = time_chunk['c'].loc[x]
                        prices.append(close_chunk)

                    for p in prices:
                        diff = self.diff_percentage(p, close)

                        if 0 < diff < 0.3:
                            logging.getLogger('freqtrade').info(str([i, '---', diff, p]))
                            df['max_level'].loc[i] = 1

                for x in range(i - 2, i):
                    # if candle red
                    # if df['max_level'].loc[x] > 0 and df['o'].loc[i] > df['c'].loc[i]:
                    if df['max_level'].loc[x] > 0:
                        close = df['c'].loc[i]

                        # if same value presented in past
                        # and if value > average for short
                        df_tail = df[i - 200: i].query(f'c > {close}')

                        if len(df_tail) > 0:
                            logging.getLogger('freqtrade').info(
                                str([i, '---', max, diff, '---', prices, 'short -----'])
                            )
                            df['buy_short'].loc[i] = 1
                            df['i_low'].loc[i] = df['low'].loc[x]
                            df['i_high'].loc[i] = df['high'].loc[x]
                            df['i_open'].loc[i] = df['o'].loc[x]
                            df['i_close'].loc[i] = df['c'].loc[x]

                for x in range(i - 100, i):
                    if df['max_level'].loc[x] > 0:
                        diff = self.diff_percentage(df['c'].loc[x], df['c'].loc[i])
                        # past > now
                        # if df['c'].loc[x] > df['c'].loc[i] and 0 < diff < 1:
                        if 0 < diff < 1:
                            logging.getLogger('freqtrade').info(
                                str([i, '---- short2 ----'])
                            )
                            df['buy_short2'].loc[i] = 1
                            df['i_low'].loc[i] = df['low'].loc[x]
                            df['i_high'].loc[i] = df['high'].loc[x]
                            df['i_open'].loc[i] = df['o'].loc[x]
                            df['i_close'].loc[i] = df['c'].loc[x]


        return df

    def populate_entry_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[(df['buy_short'] > 0), 'enter_short'] = 1
        df.loc[(df['buy_short2'] > 0), 'enter_short'] = 1

        df.loc[(df['buy_long'] > 0), 'enter_long'] = 1
        df.loc[(df['buy_long2'] > 0), 'enter_long'] = 1

        return df

    def populate_exit_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        df.loc[
            (df['rsi_7'] < 10),
            'exit_short'
        ] = 1
        df.loc[
            (df['rsi_7'] > 90),
            'exit_long'
        ] = 1

        return df

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:

        return 10

    def diff_percentage(self, v2, v1) -> float:
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return np.abs(diff)

    def do_heikin_ashi(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        https://www.investopedia.com/trading/heikin-ashi-better-candlestick/
        """
        df['h'] = df.apply(lambda x: max(x['high'], x['open'], x['close']), axis=1)
        df['l'] = df.apply(lambda x: min(x['low'], x['open'], x['close']), axis=1)

        for i in range(1, len(df)):
            df.loc[i, 'c'] = 1 / 4 * (
                df['open'].iloc[i] +
                df['close'].iloc[i] +
                df['high'].iloc[i] +
                df['low'].iloc[i]
            )
            df.loc[i, 'o'] = 1 / 2 * (
                df['open'].iloc[i - 1] +
                df['close'].iloc[i - 1]
            )

        return df

    def confirm_trade_entry(self,
                            pair: str,
                            order_type: str,
                            amount: float,
                            rate: float,
                            time_in_force: str,
                            current_time: datetime,
                            entry_tag: Optional[str],
                            side: str,
                            **kwargs) -> bool:
        """
        https://www.freqtrade.io/en/stable/strategy-callbacks/#trade-entry-buy-order-confirmation
        """
        df, last_updated = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)

        print('------------------- confirm_trade_entry -------------', pair, rate)

        mean = (
            df['i_open'].iat[-1] +
            df['i_close'].iat[-1]
        ) / 2

        # # open = df['i_open'].iat[-1]
        # # close = df['i_close'].iat[-1]
        # min_ = min(
        #     # df['i_high'].iat[-1],
        #     # df['i_low'].iat[-1],
        #     df['i_open'].iat[-1],
        #     df['i_close'].iat[-1]
        # )
        # max_ = max(
        #     # df['i_high'].iat[-1],
        #     # df['i_low'].iat[-1],
        #     df['i_open'].iat[-1],
        #     df['i_close'].iat[-1]
        # )

        if mean == 0:
            return False

        if side == 'long':
            return rate < mean

        if side == 'short':
            return rate > mean

        return False

    # def custom_entry_price(self, pair: str, current_time: datetime, proposed_rate: float,
    #                        entry_tag: Optional[str], side: str, **kwargs) -> float:
    #
    #     # https://www.freqtrade.io/en/stable/strategy-callbacks/#custom-order-entry-and-exit-price-example
    #
    #     df, last_updated = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
    #     avg = (
    #         # df['i_high'].iat[-1] +
    #         # df['i_low'].iat[-1] +
    #         df['i_open'].iat[-1] +
    #         df['i_close'].iat[-1]
    #     ) / 2
    #
    #     min_ = min(
    #         df['i_high'].iat[-1],
    #         df['i_low'].iat[-1],
    #         df['i_open'].iat[-1],
    #         df['i_close'].iat[-1]
    #     )
    #     max_ = max(
    #         df['i_high'].iat[-1],
    #         df['i_low'].iat[-1],
    #         df['i_open'].iat[-1],
    #         df['i_close'].iat[-1]
    #     )
    #
    #     print(
    #         '------------------- confirm_trade_entry -------------',
    #         pair, proposed_rate, side, '---', min_, max_, avg
    #     )
    #
    #     if side == 'long':
    #         return min(proposed_rate, avg)
    #
    #     if side == 'short':
    #         return max(proposed_rate, avg)
    #
    #     return avg