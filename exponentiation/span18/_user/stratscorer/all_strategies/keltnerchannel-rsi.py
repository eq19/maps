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

class keltnerhopt(IStrategy):
    timeframe = "1d"
    # Both stoploss and roi are set to 100 to prevent them to give a sell signal.
    stoploss = -1
    minimal_roi = {"0": 100}

    # Hyperopt spaces
    window_range = IntParameter(13, 56, default=20, space="buy")
    atrs_range = IntParameter(1, 8, default=1, space="buy")
    rsi_buy_hline = IntParameter(30, 70, default=55, space="buy")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Keltner Channel
        for windows in self.window_range.range:
            for atrss in self.atrs_range.range:
                dataframe[f"kc_upperband_{windows}_{atrss}"] = qtpylib.keltner_channel(dataframe, window=windows, atrs=atrss)["upper"]
                dataframe[f"kc_middleband_{windows}_{atrss}"] = qtpylib.keltner_channel(dataframe, window=windows, atrs=atrss)["mid"]

        # Rsi
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)


        # Print stuff for debugging dataframe
        # print(metadata)
        # print(dataframe.tail(20)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
           (qtpylib.crossed_above(dataframe['close'], dataframe[f"kc_upperband_{self.window_range.value}_{self.atrs_range.value}"]))
           & (dataframe['rsi'] > self.rsi_buy_hline.value )
           )

        if conditions:
            dataframe.loc[   
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            (qtpylib.crossed_below(dataframe['close'], dataframe[f"kc_middleband_{self.window_range.value}_{self.atrs_range.value}"]))
           )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
