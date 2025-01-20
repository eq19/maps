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

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

##### SETINGS #####
# It hyperopt just one set of params for all buy and sell strategies if true.
DUALFIT = False
COUNT = 10
GAP = 3
### END SETINGS ###

def max_pump_detect_price_15m(dataframe, period=14, pause = 288 ):
    df = dataframe.copy()
    df['size'] = df['high'] - df['low']
    cumulativeup = 0
    countup = 0
    cumulativedown = 0
    countdown = 0
    for i in range(period):

        cumulativeup = cumulativeup + df['volume'].shift(i) * df['size'].shift(i) * np.where(df['close'].shift(i) > df['open'].shift(i), 1, 0)
        cumulativedown = cumulativedown + df['volume'].shift(i) * df['size'].shift(i) * np.where(df['close'].shift(i) > df['open'].shift(i), 0, 1)
            
    flow_price = cumulativeup - cumulativedown
    flow_price_normalized = flow_price / (df['volume'].rolling(499).mean() * (df['high']-df['low']).rolling(499).mean())
    max_flow_price = flow_price_normalized.rolling(pause).max()
    
    return max_flow_price

def flow_price_15m(dataframe, period=14, pause = 288 ):
    df = dataframe.copy()
    df['size'] = df['high'] - df['low']
    cumulativeup = 0
    countup = 0
    cumulativedown = 0
    countdown = 0
    for i in range(period):

        cumulativeup = cumulativeup + df['volume'].shift(i) * df['size'].shift(i) * np.where(df['close'].shift(i) > df['open'].shift(i), 1, 0)
        cumulativedown = cumulativedown + df['volume'].shift(i) * df['size'].shift(i) * np.where(df['close'].shift(i) > df['open'].shift(i), 0, 1)
            
    flow_price = cumulativeup - cumulativedown
    flow_price_normalized = flow_price / (df['volume'].rolling(499).mean() * (df['high']-df['low']).rolling(499).mean())
    
    return flow_price_normalized

def to_minutes(**timdelta_kwargs):
    return int(timedelta(**timdelta_kwargs).total_seconds() / 60)

#########################################################
#######################  ichiV1_Mod #####################
"""
Here are some potential logical issues in the provided strategy file:

1. **Exception Handling in `adjust_trade_position`**:
   The method catches all exceptions but does not log the exception or 
   provide any feedback. It returns `None` in all cases, which may hide 
   underlying issues.

2. **Pump Protection and Slippage Parameters**:
   The pump protection and slippage parameters are set but may not be 
   optimized correctly for your trading environment. Ensure the values 
   for `pump_period`, `pump_limit`, `pump_recorver_price`, `pump_pause_duration`, 
   `max_slip`, `buy_btc_safe`, `buy_btc_safe_1d`, `antipump_threshold`, 
   and `antipump_threshold_2` are suitable for your strategy.

3. **Trailing Stop Parameters**: 
   The trailing stop parameters are defined but commented out.
   Ensure you are using them if needed.

4. **ROI Table and Stoploss Values**:
   The `minimal_roi` and `stoploss` values should be reviewed to ensure
   they align with your risk management and profit-taking strategy.

5. **Custom Stoploss Calculation**:
   The `custom_stoploss` method uses a complex calculation for `sl_profit`,
   which may not work as intended. Ensure the logic is correct and revisited.

6. **Confirm Trade Exit Conditions**:
   The `confirm_trade_exit` method has multiple checks that might
   result in unintended behavior. Review the conditions to ensure they 
   correctly implement your exit strategy.

7. **Use of Heikin Ashi Candles**:
   The comment `#dataframe['close'] = heikinashi['close']` might
   indicate an issue with using Heikin Ashi close prices. 
   Ensure you are using the correct close prices for your calculations.

Review and optimize these aspects of your strategy to improve performance.
"""
#########################################################
class ichiV1(IStrategy):

    DATESTAMP = 0
    SELLMA = 1

    # ROI table:
    minimal_roi = {
        "0": 0.05,
        "23": 0.04,
        "55": 0.03,
        "86": 0.02,
        "118": 0.01,
        "233": 0.0001,
        "528": -10
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

    # Optimal
    timeframe = '15m'
    startup_candle_count = 120
    ignore_roi_if_buy_signal = False
    process_only_new_candles = False

    # Stoploss:
    stoploss = -0.275
    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    #trailing_stop_positive = 0.002
    #trailing_stop_positive_offset = 0.025
    #trailing_only_offset_is_reached = True

    # Buy hyperspace params:
    buy_params = {
        "buy_trend_above_senkou_level": 1,
        "buy_trend_bullish_level": 6,
        "buy_fan_magnitude_shift_value": 3,
        "buy_min_fan_magnitude_gain": 1.002 # NOTE: Good value (Win% ~70%), alot of trades
        #"buy_min_fan_magnitude_gain": 1.008 # NOTE: Very save value (Win% ~90%), only the biggest moves 1.008,
    }

    buy_trend_above_senkou_level = IntParameter(1, 8, default=buy_params['buy_trend_above_senkou_level'], space="buy")
    buy_trend_bullish_level = IntParameter(1, 8, default=buy_params['buy_trend_bullish_level'], space="buy")
    buy_fan_magnitude_shift_value = IntParameter(1, 10, default=buy_params['buy_fan_magnitude_shift_value'], space="buy")
    buy_min_fan_magnitude_gain = DecimalParameter(1.001, 1.02, default=buy_params['buy_min_fan_magnitude_gain'], space="buy")

    # Sell hyperspace params:
    # NOTE: was 15m but kept bailing out in dryrun
    sell_params = {
        "pHSL": -0.08,
        "ProfitLoss1": 0.005,
        "ProfitLoss2": 0.021,
        "ProfitMargin1": 0.018,
        "ProfitMargin2": 0.051,
        "ExitTrendIndicator": "trend_close_2h"
    }

    # trailing stoploss hyperopt parameters
    pHSL = DecimalParameter(-0.15, -0.08, default=sell_params['pHSL'], decimals=3, space='sell', optimize=True)
    ProfitLoss1 = DecimalParameter(0.005, 0.012, default=sell_params['ProfitLoss1'], decimals=3, space='sell', optimize=True)
    ProfitLoss2 = DecimalParameter(0.010, 0.025, default=sell_params['ProfitLoss2'], decimals=3, space='sell', optimize=True)
    ProfitMargin1 = DecimalParameter(0.009, 0.019, default=sell_params['ProfitMargin1'], decimals=3, space='sell', optimize=True)
    ProfitMargin2 = DecimalParameter(0.033, 0.099, default=sell_params['ProfitMargin2'], decimals=3, space='sell', optimize=True)
    ExitTrendIndicator = CategoricalParameter(['trend_close_30m', 'trend_close_1h', 'trend_close_2h', 'trend_close_4h', 'trend_close_6h', 'trend_close_8h'], default=sell_params['ExitTrendIndicator']', space='sell')

    plot_config = {
        'main_plot': {
            # fill area between senkou_a and senkou_b
            'senkou_a': {
                'color': 'green', #optional
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud', #optional
                'fill_color': 'rgba(255,76,46,0.2)', #optional
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {},
            'trend_close_15m': {'color': '#FF5733'},
            'trend_close_30m': {'color': '#FF8333'},
            'trend_close_1h': {'color': '#FFB533'},
            'trend_close_2h': {'color': '#FFE633'},
            'trend_close_4h': {'color': '#E3FF33'},
            'trend_close_6h': {'color': '#C4FF33'},
            'trend_close_8h': {'color': '#61FF33'},
            'trend_close_1d': {'color': '#33FF7D'}
        },
        'subplots': {
            'fan_magnitude': {
                'fan_magnitude': {}
            },
            'fan_magnitude_gain': {
                'fan_magnitude_gain': {}
            }
        }
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['open'] = heikinashi['open']
        #dataframe['close'] = heikinashi['close']
        if 'close' not in dataframe.columns:
            dataframe['close'] = heikinashi['close']
        dataframe['high'] = heikinashi['high']
        dataframe['low'] = heikinashi['low']

        dataframe['trend_close_15m'] = dataframe['close']
        dataframe['trend_close_30m'] = ta.EMA(dataframe['close'], timeperiod=2)
        dataframe['trend_close_1h'] = ta.EMA(dataframe['close'], timeperiod=4)
        dataframe['trend_close_2h'] = ta.EMA(dataframe['close'], timeperiod=8)
        dataframe['trend_close_4h'] = ta.EMA(dataframe['close'], timeperiod=16)
        dataframe['trend_close_6h'] = ta.EMA(dataframe['close'], timeperiod=24)
        dataframe['trend_close_8h'] = ta.EMA(dataframe['close'], timeperiod=32)
        dataframe['trend_close_1d'] = ta.EMA(dataframe['close'], timeperiod=96)

        dataframe['trend_open_15m'] = dataframe['open']
        dataframe['trend_open_30m'] = ta.EMA(dataframe['open'], timeperiod=2)
        dataframe['trend_open_1h'] = ta.EMA(dataframe['open'], timeperiod=4)
        dataframe['trend_open_2h'] = ta.EMA(dataframe['open'], timeperiod=8)
        dataframe['trend_open_4h'] = ta.EMA(dataframe['open'], timeperiod=16)
        dataframe['trend_open_6h'] = ta.EMA(dataframe['open'], timeperiod=24)
        dataframe['trend_open_8h'] = ta.EMA(dataframe['open'], timeperiod=32)
        dataframe['trend_open_1d'] = ta.EMA(dataframe['open'], timeperiod=96)

        dataframe['fan_magnitude'] = (dataframe['trend_close_1h'] / dataframe['trend_close_8h'])
        dataframe['fan_magnitude_gain'] = dataframe['fan_magnitude'] / dataframe['fan_magnitude'].shift(1)

        displacement = 30
        ichimoku = ftt.ichimoku(dataframe, 
            conversion_line_period=20, 
            base_line_periods=60,
            laggin_span=120, 
            displacement=displacement
            )
        
        dataframe['chikou_span'] = ichimoku['chikou_span']
        dataframe['tenkan_sen'] = ichimoku['tenkan_sen']
        dataframe['kijun_sen'] = ichimoku['kijun_sen']
        dataframe['senkou_a'] = ichimoku['senkou_span_a']
        dataframe['senkou_b'] = ichimoku['senkou_span_b']
        dataframe['leading_senkou_span_a'] = ichimoku['leading_senkou_span_a']
        dataframe['leading_senkou_span_b'] = ichimoku['leading_senkou_span_b']
        dataframe['cloud_green'] = ichimoku['cloud_green']
        dataframe['cloud_red'] = ichimoku['cloud_red']

        dataframe['atr'] = ta.ATR(dataframe)

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Trending market
        if self.buy_params['buy_trend_above_senkou_level'] >= 1:
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 2:
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 3:
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 4:
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 5:
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 6:
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 7:
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 8:
            conditions.append(dataframe['trend_close_1d'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_1d'] > dataframe['senkou_b'])

        # Trends bullish
        if self.buy_params['buy_trend_bullish_level'] >= 1:
            conditions.append(dataframe['trend_close_15m'] > dataframe['trend_open_15m'])

        if self.buy_params['buy_trend_bullish_level'] >= 2:
            conditions.append(dataframe['trend_close_30m'] > dataframe['trend_open_30m'])

        if self.buy_params['buy_trend_bullish_level'] >= 3:
            conditions.append(dataframe['trend_close_1h'] > dataframe['trend_open_1h'])

        if self.buy_params['buy_trend_bullish_level'] >= 4:
            conditions.append(dataframe['trend_close_2h'] > dataframe['trend_open_2h'])

        if self.buy_params['buy_trend_bullish_level'] >= 5:
            conditions.append(dataframe['trend_close_4h'] > dataframe['trend_open_4h'])

        if self.buy_params['buy_trend_bullish_level'] >= 6:
            conditions.append(dataframe['trend_close_6h'] > dataframe['trend_open_6h'])

        if self.buy_params['buy_trend_bullish_level'] >= 7:
            conditions.append(dataframe['trend_close_8h'] > dataframe['trend_open_8h'])

        if self.buy_params['buy_trend_bullish_level'] >= 8:
            conditions.append(dataframe['trend_close_1d'] > dataframe['trend_open_1d'])

        # Trends magnitude
        conditions.append(dataframe['fan_magnitude_gain'] >= self.buy_params['buy_min_fan_magnitude_gain'])
        conditions.append(dataframe['fan_magnitude'] > 1)

        for x in range(self.buy_params['buy_fan_magnitude_shift_value']):
            conditions.append(dataframe['fan_magnitude'].shift(x+1) < dataframe['fan_magnitude'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe


    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        conditions.append(qtpylib.crossed_below(dataframe['trend_close_15m'], dataframe[self.sell_params['ExitTrendIndicator']]))

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
