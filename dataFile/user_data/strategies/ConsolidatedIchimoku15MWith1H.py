from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.strategy import DecimalParameter, IntParameter
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd
from typing import Dict, List
from datetime import datetime, timedelta, timezone
import numpy as np

class ConsolidatedIchimoku15MWith1H(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    informative_timeframe = '1h'
    
    # ROI table:
    minimal_roi = {
        "0": 0.05,
        "30": 0.03,
        "60": 0.01,
        "120": 0
    }

    stoploss = -0.10
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Add Ichimoku parameters
    ichimoku_tenkan = 9
    ichimoku_kijun = 26
    ichimoku_senkou = 52

    # Hyperopt parameters
    buy_rsi = IntParameter(30, 50, default=40, space='buy')
    sell_rsi = IntParameter(60, 80, default=70, space='sell')
    ewo_low = DecimalParameter(-20.0, -8.0, default=-12.0, space='buy')
    ewo_high = DecimalParameter(3.0, 12.0, default=6.0, space='buy')
    hull_period = IntParameter(9, 24, default=14, space='sell')

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs

    def calculate_ichimoku(self, dataframe):
        # Manually calculate Ichimoku components
        dataframe['tenkan'] = dataframe['high'].rolling(window=self.ichimoku_tenkan).max().shift() + dataframe['low'].rolling(window=self.ichimoku_tenkan).min().shift()
        dataframe['tenkan'] /= 2
        
        dataframe['kijun'] = dataframe['high'].rolling(window=self.ichimoku_kijun).max().shift() + dataframe['low'].rolling(window=self.ichimoku_kijun).min().shift()
        dataframe['kijun'] /= 2
        
        dataframe['senkou_a'] = ((dataframe['tenkan'] + dataframe['kijun']) / 2).shift(self.ichimoku_kijun)
        dataframe['senkou_b'] = ((dataframe['high'].rolling(window=self.ichimoku_senkou).max() + 
                                 dataframe['low'].rolling(window=self.ichimoku_senkou).min()) / 2).shift(self.ichimoku_kijun)
        return dataframe
    
    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Calculate Ichimoku manually instead of using talib
        dataframe = self.calculate_ichimoku(dataframe)
        
        # For 1h timeframe
        informative = self.dp.get_pair_dataframe(
            pair=metadata['pair'], 
            timeframe=self.informative_timeframe
        )
        informative = self.calculate_ichimoku(informative)
        informative['ema_200_1h'] = ta.EMA(informative, timeperiod=200)
        informative['rsi_1h'] = ta.RSI(informative, timeperiod=14)
        
        dataframe = merge_informative_pair(
            dataframe, 
            informative, 
            self.timeframe, 
            self.informative_timeframe, 
            suffixes=('', '_1h')
        )
        
        # Rest of your indicators
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
                # 1H Trend Confirmation
                (dataframe['close_1h'] > dataframe['ema_200_1h']) &
                (dataframe['close_1h'] > dataframe['senkou_a_1h']) &
                (dataframe['close_1h'] > dataframe['senkou_b_1h']) &
                (dataframe['rsi_1h'] > 50) &
                
                # 15M Entry Signals
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                (qtpylib.crossed_above(dataframe['tenkan'], dataframe['kijun'])) &
                (dataframe['rsi'] > self.buy_rsi.value) &
                (dataframe['ewo'] > self.ewo_high.value) &
                (dataframe['volume'] > dataframe['volume_sma_24'])
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe.loc[
            (
                # 15M Exit Conditions
                (qtpylib.crossed_below(dataframe['close'], dataframe['hull'])) |
                (dataframe['rsi'] > self.sell_rsi.value) |
                (dataframe['close'] < dataframe['senkou_a']) |
                
                # 1H Trend Weakness
                (dataframe['close_1h'] < dataframe['ema_200_1h'])
            ),
            'exit_long'] = 1

        return dataframe

    # Risk management
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str,
                 side: str, **kwargs) -> float:
        return 1.0

    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 5
            },
            {
                "method": "StoplossGuard",
                "lookback_period_candles": 24,
                "trade_limit": 4,
                "stop_duration_candles": 2,
                "only_per_pair": True
            }
        ]
