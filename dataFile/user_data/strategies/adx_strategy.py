from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

__author__       = "Robert Roman"
__copyright__    = "Free For Use"
__license__      = "MIT"
__version__      = "1.0"
__maintainer__   = "Robert Roman"
__email__        = "robertroman7@gmail.com"
__BTC_donation__ = "3FgFaG15yntZYSUzfEpxr5mDt1RArvcQrK"

# Optimized With Sortino Ratio and 2 years data

class adx_strategy(IStrategy):
    ticker_interval = '15m'

    # ROI table:
    minimal_roi = {
        "0": 0.26552,
        "30": 0.10255,
        "210": 0.03545,
        "540": 0
    }

    # Stoploss:
    stoploss = -0.1255

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
      
        # ADX
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['adx'] > 16) &
                    (dataframe['minus_di'] > 4) &
                    # (dataframe['plus_di'] > 33) &
                    (qtpylib.crossed_above(dataframe['minus_di'], dataframe['plus_di']))

            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['adx'] > 43) &
                    # (dataframe['minus_di'] > 22) &
                    (dataframe['plus_di'] > 24) &
                    (qtpylib.crossed_above(dataframe['plus_di'], dataframe['minus_di']))

            ),
            'sell'] = 1
        return dataframe
