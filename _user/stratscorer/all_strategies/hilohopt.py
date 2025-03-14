# --- Do not remove these libs ---
import talib.abstract as ta
import pandas_ta as pta
import numpy as np  # noqa
import pandas as pd  # noqa
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
from functools import reduce
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

class HiLoHopt(IStrategy):
    timeframe = "1d"
    stoploss = -1.0
    minimal_roi = {"0": 100.0}

# --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            # Create sma line
            'hilo': {'color': 'blue'},
        },
        'subplots': {
            # Create rsi subplot
            "MACD": {
                'macd': {'color': 'blue', 'fill_to': 'macdsignal'},
                'macdsignal': {'color': 'orange'},
                'macdhist': {'color': 'green', 'type': 'bar', 'plotly': {'opacity': 0.4}}
            },
        },
    }

# --- Define spaces for the indicators ---

    hilo_range = IntParameter(3, 60, default=21, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Gann HiLo
        for val in self.hilo_range.range:
            dataframe[f"hilo_{val}"] = pta.hilo(
                high=dataframe["high"],
                low=dataframe["low"],
                close=dataframe["close"],
                high_length=val,
                low_length=val,
                mamode=None,
                offset=None,
            )[f"HILO_{val}_{val}"]

        # MACD
        macd = ta.MACD(
            dataframe,
            fastperiod=12,
            fastmatype=0,
            slowperiod=26,
            slowmatype=0,
            signalperiod=9,
            signalmatype=0,
        )
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        # print(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       conditions = []
       conditions.append(
           (dataframe['close'] > dataframe[f'hilo_{self.hilo_range.value}'])
           & (dataframe['macd'] > dataframe['macdsignal'])
           )

       if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'buy'] = 1

       return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       conditions = []
       conditions.append(
           (dataframe['macd'] < dataframe['macdsignal'])
           )

       if conditions:
           dataframe.loc[
               reduce(lambda x, y: x & y, conditions),
               'sell'] = 1

       return dataframe
