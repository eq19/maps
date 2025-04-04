# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas_ta as pta
import numpy as np  # noqa
import pandas as pd  # noqa

# These libs are for hyperopt
from functools import reduce
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)
# --------------------------------


class ADXMomentumHopt(IStrategy):
    """

    author@: Gert Wohlgemuth

    converted from:

        https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/AdxMomentum.cs

    """

    minimal_roi = {"0": 0.01}
    stoploss = -0.25
    timeframe = '1h'
    startup_candle_count: int = 20

    # Hyperopt spaces
    adx_buy_hline = IntParameter(15, 35, default=25, space="buy")
    adx_period = IntParameter(7, 21, default=14, space="buy")
    plus_di_period = IntParameter(20,30 , default=25, space="buy")
    minus_di_period = IntParameter(20, 30, default=25, space="buy")
    mom_period = IntParameter(7, 21, default=14, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for val in self.adx_period.range:
            dataframe[f'adx_{val}'] = ta.ADX(dataframe, timeperiod=val)
        for val in self.mom_period.range:
            dataframe[f'mom_{val}'] = ta.MOM(dataframe, timeperiod=val)
        for val in self.plus_di_period.range:
            dataframe[f'plus_di_{val}'] = ta.PLUS_DI(dataframe, timeperiod=val)
        for val in self.minus_di_period.range:
            dataframe[f'minus_di_{val}'] = ta.MINUS_DI(dataframe, timeperiod=val)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            (
                    (dataframe[f'adx_{self.adx_period.value}'] > self.adx_buy_hline.value) &
                    (dataframe[f'mom_{self.mom_period.value}'] > 0) &
                    (dataframe[f'plus_di_{self.plus_di_period.value}'] > self.adx_buy_hline.value) &
                    (dataframe[f'plus_di_{self.plus_di_period.value}'] > dataframe[f'minus_di_{self.minus_di_period.value}'])

            ),
        )
        if conditions:
            dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            (
                    (dataframe[f'adx_{self.adx_period.value}'] > self.adx_buy_hline.value) &
                    (dataframe[f'mom_{self.mom_period.value}'] < 0) &
                    (dataframe[f'minus_di_{self.minus_di_period.value}'] > self.adx_buy_hline.value) &
                    (dataframe[f'plus_di_{self.plus_di_period.value}'] < dataframe[f'minus_di_{self.minus_di_period.value}'])

            ),
        )
        if conditions:
            dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1
        return dataframe
