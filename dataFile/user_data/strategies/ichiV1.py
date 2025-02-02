# --- Do not remove these libs ---
from sqlalchemy import true
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame, Series
import copy
import logging
import pathlib
import rapidjson
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd  # noqa
pd.options.mode.chained_assignment = None  # default='warn'
import technical.indicators as ftt
from freqtrade.exchange import timeframe_to_prev_date
from functools import reduce
from datetime import datetime, timedelta, timezone
import numpy as np
from technical.util import resample_to_interval, resampled_merge
from freqtrade.strategy import informative
from freqtrade.strategy import stoploss_from_open
from freqtrade.strategy import (BooleanParameter,timeframe_to_minutes, merge_informative_pair,
                                DecimalParameter, IntParameter, CategoricalParameter)
from freqtrade.persistence import Trade
from typing import Dict
import numpy # noqa
import math
import pandas_ta as pta
from typing import List
from skopt.space import Dimension, Integer
import time
from warnings import simplefilter

from technical.indicators import dema

logger = logging.getLogger(__name__)


class ichiV1(IStrategy):
#class Strategy005(IStrategy):
    """
    Strategy 005
    author@: Gerald Lonlas
    github@: https://github.com/freqtrade/freqtrade-strategies

    How to use it?
    > python3 ./freqtrade/main.py -s Strategy005
    """
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy
    timeframe = '1m'
    startup_candle_count = 168

    # Optimal stoploss designed for the strategy
    # This attribute will be overridden if the config file contains "stoploss"
    stoploss = -0.10

    # Custom stoploss
    use_custom_stoploss = True

    # trailing stoploss
    trailing_stop = False
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02

    # run "populate_indicators"
    process_only_new_candles = False

    # Experimental settings
    use_exit_signal = True
    exit_profit_only = False
    process_only_new_candles = True
    ignore_roi_if_entry_signal = False

    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'forcebuy': "market",
        'forcesell': 'market',
        'stoploss': 'market',
        'emergencysell': 'market',
        'stoploss_on_exchange': False,

        'stoploss_on_exchange_interval': 60,
        'stoploss_on_exchange_limit_ratio': 0.99
    }

    # Buy hyperspace params:
    buy_params = {
        "buy_rsi": 26,
        "buy_fastd": 1,
        "buy_volumeAVG": 150,
        "buy_fishRsiNorma": 5
    }

    buy_rsi = IntParameter(low=1, high=100, default=30, space='buy', optimize=True)
    buy_fastd = IntParameter(low=1, high=100, default=30, space='buy', optimize=True)
    buy_volumeAVG = IntParameter(low=50, high=300, default=70, space='buy', optimize=True)
    buy_fishRsiNorma = IntParameter(low=1, high=100, default=30, space='buy', optimize=True)

    # Sell hyperspace params:
    sell_params = {        
        "pHSL": -0.163,
        "pPF_1": 0.013,
        "pPF_2": 0.093,
        "pSL_1": 0.016,
        "pSL_2": 0.024,
        "sell_rsi": 74,
        "sell_minusDI": 4,
        "sell_fishRsiNorma": 30,
        "sell_trigger": "rsi-macd-minusdi"
    }

    sell_rsi = IntParameter(low=1, high=100, default=70, space='sell', optimize=True)
    sell_minusDI = IntParameter(low=1, high=100, default=50, space='sell', optimize=True)
    sell_fishRsiNorma = IntParameter(low=1, high=100, default=50, space='sell', optimize=True)
    sell_trigger = CategoricalParameter(["rsi-macd-minusdi", "sar-fisherRsi"], default=30, space='sell', optimize=True)

    # Hard stoploss profit
    pHSL = DecimalParameter(-0.200, -0.040, default=-0.08, decimals=3, space='sell', load=True)

    # profit threshold 1, trigger point, SL_1 is used
    pPF_1 = DecimalParameter(0.008, 0.020, default=0.016, decimals=3, space='sell', load=True)
    pSL_1 = DecimalParameter(0.008, 0.020, default=0.011, decimals=3, space='sell', load=True)

    # Profit threshold 2, SL_2 is used
    pPF_2 = DecimalParameter(0.040, 0.100, default=0.080, decimals=3, space='sell', load=True)
    pSL_2 = DecimalParameter(0.020, 0.070, default=0.040, decimals=3, space='sell', load=True)

    ## Custom Trailing stoploss ( credit to Perkmeister for this custom stoploss to help the strategy ride a green candle )
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:

        # Hard stoploss profit
        HSL = self.pHSL.value
        PF_1 = self.pPF_1.value
        SL_1 = self.pSL_1.value
        PF_2 = self.pPF_2.value
        SL_2 = self.pSL_2.value

        # For profits between PF_1 and PF_2 the stoploss (sl_profit) used is linearly interpolated
        # between the values of SL_1 and SL_2. For all profits above PL_2 the sl_profit value
        # rises linearly with current profit, for profits below PF_1 the hard stoploss profit is used.

        if (current_profit > PF_2):
            sl_profit = SL_2 + (current_profit - PF_2)
        elif (current_profit > PF_1):
            sl_profit = SL_1 + ((current_profit - PF_1) * (SL_2 - SL_1) / (PF_2 - PF_1))
        else:
            sl_profit = HSL

        # Only for hyperopt invalid return
        if (sl_profit >= current_profit):
            return -0.99

        return stoploss_from_open(sl_profit, current_profit)

    # Protection hyperspace params:
    protection_params = {
        "protection_cooldown_period": 2,
        "protection_maxdrawdown_lookback_period_candles": 35,
        "protection_maxdrawdown_max_allowed_drawdown": 0.097,
        "protection_maxdrawdown_stop_duration_candles": 1,
        "protection_maxdrawdown_trade_limit": 6,
        "protection_stoplossguard_lookback_period_candles": 16,
        "protection_stoplossguard_stop_duration_candles": 29,
        "protection_stoplossguard_trade_limit": 3,
    }

    protection_cooldown_period = IntParameter(low=1, high=48, default=1, space="protection", optimize=True)

    protection_maxdrawdown_lookback_period_candles = IntParameter(low=1, high=48, default=1, space="protection", optimize=True)
    protection_maxdrawdown_trade_limit = IntParameter(low=1, high=8, default=4, space="protection", optimize=True)
    protection_maxdrawdown_stop_duration_candles = IntParameter(low=1, high=48, default=1, space="protection", optimize=True)
    protection_maxdrawdown_max_allowed_drawdown = DecimalParameter(low=0.01, high=0.20, default=0.1, space="protection", optimize=True)

    protection_stoplossguard_lookback_period_candles = IntParameter(low=1, high=48, default=1, space="protection", optimize=True)
    protection_stoplossguard_trade_limit = IntParameter(low=1, high=8, default=4, space="protection", optimize=True)
    protection_stoplossguard_stop_duration_candles = IntParameter(low=1, high=48, default=1, space="protection", optimize=True)

    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": self.protection_cooldown_period.value
            },
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": self.protection_maxdrawdown_lookback_period_candles.value,
                "trade_limit": self.protection_maxdrawdown_trade_limit.value,
                "stop_duration_candles": self.protection_maxdrawdown_stop_duration_candles.value,
                "max_allowed_drawdown": self.protection_maxdrawdown_max_allowed_drawdown.value
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": self.protection_stoplossguard_lookback_period_candles.value,
                "trade_limit": self.protection_stoplossguard_trade_limit.value,
                "stop_duration_candles": self.protection_stoplossguard_stop_duration_candles.value,
                "only_per_pair": False
            }
        ]

    ############################################################################

    # ROI table:
    minimal_roi = {
        "0": 0.05,
        "15": 0.04,
        "51": 0.03,
        "81": 0.02,
        "112": 0.01,
        "154": 0.0001,
        "400": -10
    }

    class HyperOpt:
        @staticmethod
        def generate_roi_table(params: dict):
            """
            Generate the ROI table that will be used by Hyperopt
            This implementation generates the default legacy Freqtrade ROI tables.
            Change it if you need different number of steps in the generated
            ROI tables or other structure of the ROI tables.
            Please keep it aligned with parameters in the 'roi' optimization
            hyperspace defined by the roi_space method.
            """
            roi_table = {}
            roi_table[0] = 0.05
            roi_table[params['roi_t6']] = 0.04
            roi_table[params['roi_t5']] = 0.03
            roi_table[params['roi_t4']] = 0.02
            roi_table[params['roi_t3']] = 0.01
            roi_table[params['roi_t2']] = 0.0001
            roi_table[params['roi_t1']] = -10

            return roi_table

        @staticmethod
        def roi_space() -> List[Dimension]:
            """
            Values to search for each ROI steps
            Override it if you need some different ranges for the parameters in the
            'roi' optimization hyperspace.
            Please keep it aligned with the implementation of the
            generate_roi_table method.
            """
            return [
                Integer(240, 720, name='roi_t1'),
                Integer(120, 240, name='roi_t2'),
                Integer(90, 120, name='roi_t3'),
                Integer(60, 90, name='roi_t4'),
                Integer(30, 60, name='roi_t5'),
                Integer(1, 30, name='roi_t6'),
            ]

    ############################################################################

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        # Minus Directional Indicator / Movement
        dataframe['minus_di'] = ta.MINUS_DI(dataframe)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        # Inverse Fisher transform on RSI, values [-1.0, 1.0] (https://goo.gl/2JGGoy)
        rsi = 0.1 * (dataframe['rsi'] - 50)
        dataframe['fisher_rsi'] = (numpy.exp(2 * rsi) - 1) / (numpy.exp(2 * rsi) + 1)
        # Inverse Fisher transform on RSI normalized, value [0.0, 100.0] (https://goo.gl/2JGGoy)
        dataframe['fisher_rsi_norma'] = 50 * (dataframe['fisher_rsi'] + 1)

        # Stoch fast
        stoch_fast = ta.STOCHF(dataframe)
        dataframe['fastd'] = stoch_fast['fastd']
        dataframe['fastk'] = stoch_fast['fastk']

        # Overlap Studies
        # ------------------------------------

        # SAR Parabol
        dataframe['sar'] = ta.SAR(dataframe)

        # SMA - Simple Moving Average
        dataframe['sma'] = ta.SMA(dataframe, timeperiod=40)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """
        dataframe.loc[
            # Prod
            (
                (dataframe['close'] > 0.00000200) &
                (dataframe['volume'] > dataframe['volume'].rolling(self.buy_volumeAVG.value).mean() * 4) &
                (dataframe['close'] < dataframe['sma']) &
                (dataframe['fastd'] > dataframe['fastk']) &
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['fastd'] > self.buy_fastd.value) &
                (dataframe['fisher_rsi_norma'] < self.buy_fishRsiNorma.value)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame
        :return: DataFrame with buy column
        """

        conditions = []
        if self.sell_trigger.value == 'rsi-macd-minusdi':
            conditions.append(qtpylib.crossed_above(dataframe['rsi'], self.sell_rsi.value))
            conditions.append(dataframe['macd'] < 0)
            conditions.append(dataframe['minus_di'] > self.sell_minusDI.value)
        if self.sell_trigger.value == 'sar-fisherRsi':
            conditions.append(dataframe['sar'] > dataframe['close'])
            conditions.append(dataframe['fisher_rsi'] > self.sell_fishRsiNorma.value)

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), 'exit_long'] = 1

        return dataframe

    # Risk Management
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str,
                 side: str, **kwargs) -> float:
        return 1.0  # Conservative leverage

    # Plot Enhancements
    plot_config = {
        "main_plot": {
            "ema_14": {
                "color": "#888b48",
                "type": "line"
            },
            "buy_sell": {
                "sell_tag": {"color": "red"},
                "buy_tag": {"color": "blue"},
            },
        },
        "subplots": {
            "rsi4": {
                "rsi_4": {
                    "color": "#888b48",
                    "type": "line"
                }
            },
            "rsi14": {
                "rsi_14": {
                    "color": "#888b48",
                    "type": "line"
                }
            },
            "cti": {
                "cti": {
                    "color": "#573892",
                    "type": "line"
                }
            },
            "ewo": {
                "EWO": {
                    "color": "#573892",
                    "type": "line"
                }
            },
            "pct_change": {
                "pct_change": {
                    "color": "#26782f",
                    "type": "line"
                }
            }
        }
    }
