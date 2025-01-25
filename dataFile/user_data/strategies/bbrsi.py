import talib.abstract as ta
import pandas
from pandas import DataFrame
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy

__author__       = "Robert Roman"
__credits__      = ["Bloom Trading, Mohsen Hassan - thanks for teaching me Freqtrade!"]
__copyright__    = "Free For Use"
__license__      = "MIT"
__version__      = "1.0"
__maintainer__   = "Robert Roman"
__email__        = "robertroman7@gmail.com"
__BTC_donation__ = "3FgFaG15yntZYSUzfEpxr5mDt1RArvcQrK"

# Optimized With Sortino Ratio and 2 years data

class bbrsi(IStrategy):

    ticker_interval = '15m'

    # ROI table:
    minimal_roi = {
        "0": 0.24991,
        "120": 0.15395,
        "201": 0.05842,
        "555": 0
    }

    # Stoploss:
    stoploss = -0.13159

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01011
    trailing_stop_positive_offset = 0.05334
    trailing_only_offset_is_reached = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        
        # MFI
        dataframe['mfi'] = ta.MFI(dataframe)

        # Bollinger Bands 1,2,3 and 4
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
        dataframe['bb_lowerband1'] = bollinger1['lower']
        dataframe['bb_middleband1'] = bollinger1['mid']
        dataframe['bb_upperband1'] = bollinger1['upper']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']

        bollinger4 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=4)
        dataframe['bb_lowerband4'] = bollinger4['lower']
        dataframe['bb_middleband4'] = bollinger4['mid']
        dataframe['bb_upperband4'] = bollinger4['upper']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # (dataframe['rsi'] < 52) &
                # (dataframe['mfi'] < 54) &
                (dataframe["close"] < dataframe['bb_lowerband1'])
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] > 56) &
                # (dataframe['mfi'] > 65) &
                (dataframe["close"] > dataframe['bb_upperband3'])
            ),
            'sell'] = 1

        return dataframe
