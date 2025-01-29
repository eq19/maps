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
    timeframe = '15m'
    can_short: bool = False

    # Optimized ROI
    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "120": 0.03,
        "240": 0
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
    ewo_low = DecimalParameter(-20.0, -6.0, default=-10.0, space='buy')
    ewo_high = DecimalParameter(4.0, 12.0, default=8.0, space='buy')
    hull_period = IntParameter(10, 30, default=18, space='sell')
    volume_filter = DecimalParameter(0.8, 1.5, default=1.2, space='buy')

    
    def calculate_ichimoku(self, dataframe):
        if dataframe.empty:
            logger.error("Empty dataframe!")
            return dataframe
            
        try:
            tenkan = 9
            kijun = 26
            senkou = 52
            
            # CORRECTED LINES BELOW
            dataframe['tenkan'] = (
                dataframe['high'].rolling(tenkan).max() + 
                dataframe['low'].rolling(tenkan).min()
            ) / 2
            
            dataframe['kijun'] = (
                dataframe['high'].rolling(kijun).max() + 
                dataframe['low'].rolling(kijun).min()
            ) / 2
            
            dataframe['senkou_a'] = (
                (dataframe['tenkan'] + dataframe['kijun']) / 2
            ).shift(kijun)
            
            # FIXED LINE 101: Removed ".2" before shift
            dataframe['senkou_b'] = (
                (
                    dataframe['high'].rolling(senkou).max() + 
                    dataframe['low'].rolling(senkou).min()
                ) / 2  # Properly closed division
            ).shift(kijun)  # Shift applied to entire result
            
        except KeyError as e:
            logger.error(f"Column error: {e}")
            logger.error(f"Columns: {dataframe.columns.tolist()}")
            raise
        
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        cols_repr = [repr(col) for col in dataframe.columns]
        logger.debug(f"Columns: {cols_repr}")
        
        required = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required if col not in dataframe.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
            
        dataframe = dataframe.astype({
            'open': 'float64',
            'high': 'float64', 
            'low': 'float64',
            'close': 'float64',
            'volume': 'float64'
        })
        
        dataframe = self.calculate_ichimoku(dataframe)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                (dataframe['tenkan'] > dataframe['kijun'])
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['senkou_a']) |
                (dataframe['close'] < dataframe['senkou_b']) |
                (dataframe['tenkan'] < dataframe['kijun'])
            ),
            'exit_long'] = 1
        return dataframe
