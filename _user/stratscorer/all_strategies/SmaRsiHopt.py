# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
import numpy as np  # noqa
import pandas as pd  # noqa
from functools import reduce
from pandas import DataFrame
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

# --- Custom libs here ---
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# Class should have same name as file
class SmaRsiHopt(IStrategy):
    # This strategy does not use crossovers but just enters/exits trades
    # when 'is above' / 'is under' conditions are met.
    timeframe = "1d"
    stoploss = -1
    minimal_roi = {"0": 100.0}

# --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            # Create sma line
            'sma': {'color': 'blue'},
        },
        'subplots': {
            # Create rsi subplot
            "rsi": {
                'rsi': {'color': 'orange'},
                'rsi_buy_hline': {'color': 'grey','plotly': {'opacity': 0.4}},
                'rsi_sell_hline': {'color': 'grey','plotly': {'opacity': 0.4}}
            },
        },
    }


# --- Define spaces for the indicators ---

    # Buy space - UNCOMMENT THIS FOR HYPEROPTING
    sma = IntParameter(13, 56, default=21, space="buy")
    rsi_buy_hline = IntParameter(30, 70, default=50, space="buy")
    rsi_sell_hline = IntParameter(75, 95, default=85, space="sell")


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        for val in self.sma.range:
            dataframe[f'sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       conditions = []
       conditions.append(
           (dataframe['close'] > dataframe[f'sma_{self.sma.value}'])
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
           (dataframe['close'] < dataframe[f'sma_{self.sma.value}'])
           & (dataframe['rsi'] < self.rsi_sell_hline.value )
           )

       if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'sell'] = 1

       return dataframe
