import freqtrade.vendor.qtpylib.indicators as qtpylib
from numpy import ceil
from pandas.core.series import Series
from freqtrade import data
from freqtrade.exchange import timeframe_to_minutes
from freqtrade.strategy import IStrategy
from pandas.core.frame import DataFrame
from mcDuck.custom_indicators import merge_dataframes, stoch_rsi_smooth, klinger_oscilator
from functools import reduce

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from StrategyKlingerStochWBtc import StrategyKlingerStochWBtc

"""
Optimized for use with BTC
"""
class StrategyKlingerStochWBtc2(StrategyKlingerStochWBtc):
    INTERFACE_VERSION = 2

    # Optimal ticker interval for the strategy.
    timeframe = '5m'
    timeframe_main = '4h'
    timeframe_support = '1d'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = False
    sell_profit_only = False
    ignore_roi_if_buy_signal = False
    ignore_buying_expired_candle_after = 30
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 55

    # ROI table:
    minimal_roi = {
        "0": 0.489,
        "961": 0.318,
        "2479": 0.105,
        "4379": 0
    }

    # Stoploss:
    stoploss = -0.04

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.06
    trailing_only_offset_is_reached = False

   