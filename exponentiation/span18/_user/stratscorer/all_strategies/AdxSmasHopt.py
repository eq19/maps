# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# These libs are for hyperopt
from functools import reduce
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

# --------------------------------


class AdxSmasHopt(IStrategy):
    """

    author@: Gert Wohlgemuth
    Hyperopt file by: DutchCryptoDad

    converted from:

    https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/AdxSmas.cs

    """

    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.1
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.25

    # Optimal timeframe for the strategy
    timeframe = '1d'

    # Hyperopt spaces
    adx_line = IntParameter(15, 35, default=25, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['short'] = ta.SMA(dataframe, timeperiod=3)
        dataframe['long'] = ta.SMA(dataframe, timeperiod=6)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
                (dataframe['adx'] > self.adx_line.value) &
                (qtpylib.crossed_above(dataframe['short'], dataframe['long']))
            ),

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions),'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
                (dataframe['adx'] < self.adx_line.value) &
                (qtpylib.crossed_above(dataframe['long'], dataframe['short']))
            ),
        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions),'sell'] = 1
        return dataframe
