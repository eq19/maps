# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from scipy.spatial.distance import cosine
import numpy as np

class new_strat_1616(IStrategy):
    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.6
    }

    stoploss = -0.9

    timeframe = '4h'
    
    # Trailing stoploss
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.28

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=7)
        # 763% op 4h
        dataframe['marketMA'] = ta.SMA(dataframe, timeperiod=200)
        dataframe['fastMA'] = ta.SMA(dataframe, timeperiod=21)
        dataframe['slowMA'] = ta.SMA(dataframe, timeperiod=50)
        dataframe['entryMA'] = ta.SMA(dataframe, timeperiod=3)
        # Calculate slope of slowMA
        # See: https://www.wikihow.com/Find-the-Slope-of-a-Line
        dataframe['sy1'] = dataframe['slowMA'].shift(+1)
        dataframe['sy2'] = dataframe['slowMA'].shift(+11)
        sx1 = 1
        sx2 = 11
        dataframe['sy'] = dataframe['sy1'] - dataframe['sy2']
        dataframe['sx'] = sx2 - sx1
        dataframe['slow_slope'] = dataframe['sy']/dataframe['sx']
        dataframe['fy1'] = dataframe['fastMA'].shift(+1)
        dataframe['fy2'] = dataframe['fastMA'].shift(+11)
        fx1 = 1
        fx2 = 11
        dataframe['fy'] = dataframe['fy1'] - dataframe['fy2']
        dataframe['fx'] = fx2 - fx1
        dataframe['fast_slope'] = dataframe['fy']/dataframe['fx']
        # print(dataframe[['date','close', 'slow_slope','fast_slope']].tail(50))

        # ==== Trailing custom stoploss indicator ====
        dataframe['last_lowest'] = dataframe['low'].rolling(10).min().shift(1)

        return dataframe

    plot_config = {
        "main_plot": {
            # Configuration for main plot indicators.
            "fastMA": {"color": "red"},
            "slowMA": {"color": "blue"},
        },
        "subplots": {
            # Additional subplots
            "rsi": {"rsi": {"color": "blue"}},
            "fast_slope": {"fast_slope": {"color": "red"}, "slow_slope": {"color": "blue"}},
        },
    }


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Stap alleen in met een stijgende fast slope
                (dataframe['fast_slope'] > 0) &
                # Stap alleen in met een stijgende slow slope
                (dataframe['slow_slope'] > 0) &
                # Stap alleen wanneer de close price hoger is dan 3daags gemiddelde van 10 periodes geleden
                # (dataframe['close'] > dataframe['close'].shift(+11)) &
                (dataframe['close'] > dataframe['entryMA'].shift(+11)) &
                # Stap alleen in bij een rsi die groter is dan 55 ivm momentum
                (dataframe['rsi'] > 55) &
                # Stap alleen in als fast ma bocen slow ma is
                (dataframe['fastMA'] > dataframe['slowMA'])
                # (qtpylib.crossed_above(dataframe['fastMA'], dataframe['slowMA']))
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['fastMA'] < dataframe['slowMA'])
                & (dataframe['close'] < dataframe['last_lowest'])
                # (dataframe['close'] < dataframe['fastMA'])
            ),
            'sell'] = 1
        return dataframe

