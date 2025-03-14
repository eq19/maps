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

class vulcanhopt(IStrategy):
    stoploss = -0.25
    timeframe = "30m"
    minimal_roi = {"0":  100}

    # Hyperopt spaces
    SMA = IntParameter(13, 56, default=21, space="buy")
    rsi_buy_hline = IntParameter(30, 70, default=50, space="buy")
    stoch_sell_hline = IntParameter(65, 85, default=75, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Instapsignalen
        dataframe["RSI"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["RSI_SMA"] = dataframe["RSI"].rolling(window=50).mean()

        for val in self.SMA.range:
            dataframe[f'SMA_{val}'] = ta.SMA(dataframe, timeperiod=val)
            # dataframe["SMA"] = ta.SMA(dataframe, timeperiod=23)
            dataframe["growing_SMA"] = (
                (dataframe[f'SMA_{val}'] > dataframe[f'SMA_{val}'].shift(1))
                & (dataframe[f'SMA_{val}'].shift(1) > dataframe[f'SMA_{val}'].shift(2))
                & (dataframe[f'SMA_{val}'].shift(2) > dataframe[f'SMA_{val}'].shift(3))
            )

        stoch = ta.STOCH(
            dataframe,
            fastk_period=14,
            slowk_period=4,
            slowk_matype=0,
            slowd_period=6,
            slowd_matype=0,
        )
        dataframe["slowd"] = stoch["slowd"]
        dataframe["slowk"] = stoch["slowk"]

        # Uitstapsignalen
        dataframe["last_lowest"] = dataframe["low"].rolling(100).min().shift(1)
        dataframe["lower_low"] = dataframe["close"] < dataframe["last_lowest"]

        # Print stuff
        # print(dataframe[['date','close','low','last_lowest','lower_low']].loc[dataframe['lower_low'] == True].tail(55))
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
                (dataframe["close"] > dataframe[f'SMA_{self.SMA.value}'])
                & (dataframe["growing_SMA"])
                & (dataframe["RSI"] > dataframe["RSI_SMA"])
                & (dataframe["RSI"] > self.rsi_buy_hline.value)
            ),

        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions),'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            ((dataframe["slowd"] > self.stoch_sell_hline.value) & (dataframe["slowk"] > self.stoch_sell_hline.value)) 
            & (qtpylib.crossed_below(dataframe["slowk"], dataframe["slowd"]))
            | (dataframe["lower_low"] == True)
            ),
        
        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions),'sell'] = 1

        return dataframe

