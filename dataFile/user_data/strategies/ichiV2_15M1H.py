from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter
from pandas import DataFrame, Series
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np
from datetime import datetime

class ConsolidatedIchimoku15M(IStrategy):
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
        # Ichimoku Cloud with Dynamic Span Alignment
        dataframe = self.calculate_ichimoku(dataframe)

        # Momentum Indicators
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema35'] = ta.EMA(dataframe, timeperiod=35)
        dataframe['ewo'] = (dataframe['ema5'] - dataframe['ema35']) / dataframe['ema35'] * 100

        # Adaptive Hull MA
        hull_window = self.hull_period.value
        dataframe['hull_wma'] = ta.WMA(2 * ta.WMA(dataframe['close'], int(hull_window/2)) - 
                                     ta.WMA(dataframe['close'], hull_window), 
                                     int(np.sqrt(hull_window)))

        # Volume Validation
        dataframe['volume_mean24'] = dataframe['volume'].rolling(24).mean()
        dataframe['volume_ratio'] = dataframe['volume'] / dataframe['volume_mean24']

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Core Trend Alignment
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                
                # Momentum Signals
                (qtpylib.crossed_above(dataframe['tenkan'], dataframe['kijun'])) &
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['ewo'] > self.ewo_high.value) &
                
                # Volume Confirmation
                (dataframe['volume_ratio'] > self.volume_filter.value)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Trend Reversal Detection
                (qtpylib.crossed_below(dataframe['close'], dataframe['hull_wma'])) |
                
                # Profit Protection
                (dataframe['rsi'] > self.sell_rsi.value) |
                (dataframe['close'] < dataframe['senkou_a'])
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
