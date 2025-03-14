# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from functools import reduce
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

# --- Add your lib to import here ---
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
# import pandas-ta as pta

# --- Generic strategy settings ---

class smamacdcrossover(IStrategy):
    INTERFACE_VERSION = 2
    
    # Determine timeframe and # of candles before strategysignals becomes valid
    timeframe = '1d'

    # Determine roi take profit and stop loss points
    minimal_roi = {"0": 2}
    stoploss = -1
    trailing_stop = False
    use_sell_signal = True
    sell_profit_only = False
    sell_profit_offset = 0.0
    ignore_roi_if_buy_signal = False

# --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            # Create sma21 line and fill the area between sma21 and sma 50
            'sma': {'color': 'blue'},
        },
        'subplots': {
            # Create subplot MACD
            "MACD": {
                'macd': {'color': 'blue', 'fill_to': 'macdsignal'},
                'macdsignal': {'color': 'orange'},
                'macdhist': {'color': 'green', 'type': 'bar', 'plotly': {'opacity': 0.4}}
            },
        },
    }


# --- Define spaces for the indicators ---

    # UNCOMMENT THIS FOR HYPEROPTING
    sma = IntParameter(5, 221, default=21, space="buy")

# --- Used indicators of strategy code ----

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Populate this section with the indicators you want to use in your strategy
        
        # Simple moving average - COMMENT THIS FOR HYPEROPTING
#        dataframe['sma'] = ta.SMA(dataframe, timeperiod=21)

        # UNCOMMENT THIS FOR HYPEROPTING
        for val in self.sma.range:
            dataframe[f'sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        # MACD
        # https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
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

        return dataframe

# --- Buy settings ---

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # UNCOMMENT THIS FOR HYPEROPTING
        conditions = []
        conditions.append(((dataframe['macd'] > dataframe['macdsignal']) &
        (qtpylib.crossed_above(dataframe['close'],dataframe[f'sma_{self.sma.value}'])))
        | ((dataframe['close'] > dataframe[f'sma_{self.sma.value}']) &
        (qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal'])))
        )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        # Enter the conditions for buying - COMMENT THIS SECTION OUT FOR HYPEROPTING
#        dataframe.loc[
#            (
#                # Buy when close price crosses above sma21 when macd has already crossed macdsignal
#                ((dataframe['macd'] > dataframe['macdsignal']) &
#                (qtpylib.crossed_above(dataframe['close'], dataframe['sma'])))
#                # Or buy when macd crosses above macdsignal when close price has already crossed sma21
#                | ((dataframe['close'] > dataframe['sma']) &
#                (qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal'])))
#            ),
#            'buy'] = 1

        return dataframe

# --- Sell settings ---

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # UNCOMMENT THIS FOR HYPEROPTING
        conditions = []
        (conditions.append((qtpylib.crossed_below(dataframe['close'],dataframe[f'sma_{self.sma.value}']))
        | ((qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']))))
        )
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        # Enter the conditions for selling (besides ROI TP if available)
#        dataframe.loc[
#            (
#                # Sell when macd crosses down macdsignal
#                (qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal']))
#                # Or sell when close price crosses below sma21
#                | (qtpylib.crossed_below(dataframe['close'], dataframe['sma']))
#            ),
#        'sell'] = 1

        return dataframe
