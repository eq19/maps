# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import numpy as np

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

# These libs are for hyperopt, remove if not used.
from functools import reduce
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,IStrategy, IntParameter)

class DemaSmaCrossoverHopt(IStrategy):
    stoploss = -0.25
    timeframe = "1d"

    minimal_roi = {
        "240": 0.05,
        "480": 0.1,
        "720": 0.17,
        "960": 0.22,
        "0": 0.3,
    }

    plot_config = {
        "main_plot": {
            # Configuration for main plot indicators.
            # Specifies `ema10` to be red, and `ema50` to be a shade of gray
            "buy_dema": {"color": "red"},
            "buy_sma": {"color": "orange"},
            "sell_dema": {"color": "blue"},
            "sell_sma": {"color": "purple"},
            "lt_sma": {"color": "green"},
        },
        "subplots": {
            # Additional subplot RSI
            "rsi": {"rsi": {"color": "blue"}, "rsi_sma": {"color": "red"}},
        },
    }

# Hyperopt spaces where you search for the best parameter value
    lt_sma_space = IntParameter(40, 101, default=55, space="buy")
    buy_sma_space = IntParameter(14, 40, default=21, space="buy")
    buy_dema_space = IntParameter(6, 21, default=14, space="buy")
    sell_sma_space = IntParameter(14, 40, default=21, space="sell")
    sell_dema_space = IntParameter(6, 21, default=14, space="sell")


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # dataframe["lt_sma"] = ta.SMA(dataframe, timeperiod=55)
        for val in self.lt_sma_space.range:
            dataframe[f'lt_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        # dataframe["buy_sma"] = ta.SMA(dataframe, timeperiod=21)
        for val in self.buy_sma_space.range:
            dataframe[f'buy_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        # dataframe["buy_dema"] = ta.DEMA(dataframe, timeperiod=9)
        for val in self.buy_dema_space.range:
            dataframe[f'buy_dema_{val}'] = ta.DEMA(dataframe, timeperiod=val)

        # dataframe["sell_sma"] = ta.SMA(dataframe, timeperiod=21)
        for val in self.sell_sma_space.range:
            dataframe[f'sell_sma_{val}'] = ta.SMA(dataframe, timeperiod=val)

        # dataframe["sell_dema"] = ta.DEMA(dataframe, timeperiod=9)
        for val in self.sell_dema_space.range:
            dataframe[f'sell_dema_{val}'] = ta.DEMA(dataframe, timeperiod=val)

        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["rsi_sma"] = dataframe["rsi"].rolling(window=21).mean()

        # # BUY MA check
        # dataframe["buy_ma_pos"] = np.where(dataframe["buy_dema"] > dataframe["buy_sma"], 1, 0)
        # # SELL MA
        # dataframe["sell_ma_pos"] = np.where(dataframe["sell_dema"] < dataframe["sell_sma"], 1, 0)
        # # RSI check
        # dataframe["rsi_pos"] = np.where(dataframe["rsi"] > dataframe["rsi_sma"], 1, 0)
        # # Posities tellene
        # dataframe["pos_cnt"] = dataframe["buy_ma_pos"] + dataframe["rsi_pos"]
        # print(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["close"] > dataframe[f'lt_sma_{self.lt_sma_space.value}'])
                & (dataframe[f'buy_dema_{self.buy_dema_space.value}'] > dataframe[f'buy_sma_{self.buy_sma_space.value}'])
                & (dataframe["rsi"] > dataframe["rsi_sma"])
            ),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe[f'sell_dema_{self.sell_dema_space.value}'] < dataframe[f'sell_sma_{self.sell_sma_space.value}'])
            ),
            "sell",
        ] = 1
        return dataframe
