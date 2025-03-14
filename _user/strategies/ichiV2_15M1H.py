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

class ichiV2_15M1H(IStrategy):
    INTERFACE_VERSION = 3
    can_short: bool = False
    informative_timeframe = '1h'

    # Optimized ROI
    minimal_roi = {
        "0": 0.05,
        "30": 0.03,
        "60": 0.01,
        "120": 0
    }

    # Enhanced Risk Parameters
    stoploss = -0.15
    trailing_stop = True
    trailing_stop_positive = 0.015
    trailing_stop_positive_offset = 0.025
    trailing_only_offset_is_reached = True

    # Hyperoptable Parameters
    buy_rsi = IntParameter(25, 45, default=35, space='buy')
    sell_rsi = IntParameter(65, 85, default=75, space='sell')
    ewo_low = DecimalParameter(-20.0, -5.0, default=-10.0, space='buy')
    ewo_high = DecimalParameter(2.0, 10.0, default=5.0, space='buy')
    hull_period = IntParameter(8, 20, default=12, space='sell')
    volume_filter = DecimalParameter(0.8, 1.5, default=1.2, space='buy')

    def informative_pairs(self):
        # get access to all pairs available in whitelist.
        pairs = self.dp.current_whitelist()
        # Assign tf to each pair so they can be downloaded and cached for strategy.
        informative_pairs = [(pair, '1d') for pair in pairs]
        # Optionally Add additional "static" pairs
        informative_pairs += [("USDT/IDR", "15m"),
                              ("USDT/IDR", "1h"),
                            ]
        return informative_pairs

    def calculate_ichimoku(self, dataframe):
        if dataframe.empty:
            logger.error("Empty dataframe!")
            return dataframe
            
        try:
            ichimoku = ftt.ichimoku(dataframe, conversion_line_period=20, base_line_periods=60, laggin_span=120, displacement=30)
            dataframe['chikou_span'] = ichimoku['chikou_span']
            dataframe['tenkan_sen'] = ichimoku['tenkan_sen']
            dataframe['kijun_sen'] = ichimoku['kijun_sen']
            dataframe['senkou_a'] = ichimoku['senkou_span_a']
            dataframe['senkou_b'] = ichimoku['senkou_span_b']
            dataframe['leading_senkou_span_a'] = ichimoku['leading_senkou_span_a']
            dataframe['leading_senkou_span_b'] = ichimoku['leading_senkou_span_b']
            dataframe['cloud_green'] = ichimoku['cloud_green']
            dataframe['cloud_red'] = ichimoku['cloud_red']
            
        except KeyError as e:
            logger.error(f"Column error: {e}")
            logger.error(f"Columns: {dataframe.columns.tolist()}")
            raise      
        return dataframe

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        if not self.dp:
            # Don't do anything if DataProvider is not available.
            return dataframe

        # 1. Process 15m timeframe first
        dataframe = self.calculate_ichimoku(dataframe)
        
        # 2. Get and process 1h timeframe
        informative = self.dp.get_pair_dataframe(
            pair=metadata['pair'],
            timeframe=self.informative_timeframe
        )
        informative = self.calculate_ichimoku(informative)
        informative['ema_200'] = ta.EMA(informative['close'], timeperiod=200)
        informative['rsi'] = ta.RSI(informative['close'], timeperiod=14)
        
        # 3. Merge timeframes with proper suffix handling
        # Use the helper function merge_informative_pair to safely merge the pair
        # Automatically renames the columns and merges a shorter timeframe dataframe and a longer timeframe informative pair
        # use ffill to have the 1d value available in every row throughout the day.
        # Without this, comparisons between columns of the original and the informative pair would only work once per day.
        # Full documentation see https://www.freqtrade.io/en/stable/strategy-customization/#complete-dataprovider-sample
        dataframe = merge_informative_pair(
            dataframe,
            informative,
            self.timeframe,
            self.informative_timeframe,
            ffill=True
        )
        
        # 4. Add remaining indicators
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema_short'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema_long'] = ta.EMA(dataframe, timeperiod=35)
        dataframe['ewo'] = (dataframe['ema_short'] - dataframe['ema_long']) / dataframe['ema_long'] * 100
        
        dataframe['hull'] = ta.WMA(
            2 * ta.WMA(dataframe['close'], int(self.hull_period.value/2)) - 
            ta.WMA(dataframe['close'], self.hull_period.value), 
            int(np.sqrt(self.hull_period.value))
        )
        
        dataframe['volume_sma_24'] = dataframe['volume'].rolling(24).mean()     
        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (
                (dataframe['close_1h'] > dataframe['ema_200_1h']) &
                (dataframe['close_1h'] > dataframe['senkou_a_1h']) &
                (dataframe['close_1h'] > dataframe['senkou_b_1h']) &
                (dataframe['rsi_1h'] > 50) &
                
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                (qtpylib.crossed_above(dataframe['tenkan_sen'], dataframe['kijun_sen'])) &
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['ewo'] > self.ewo_high.value) &
                (dataframe['volume'] > dataframe['volume_sma_24'])
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (
                (qtpylib.crossed_below(dataframe['close'], dataframe['hull'])) |
                (dataframe['close_1h'] < dataframe['ema_200_1h']) |
                (dataframe['close'] < dataframe['senkou_a']) |
                (dataframe['rsi'] > self.sell_rsi.value)
            ),
            'exit_long'] = 1
        return dataframe

    # Risk Management Enhancements
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str,
                 side: str, **kwargs) -> float:
        return 1.0  # Conservative leverage

    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 7
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 12,
            }
        ]
