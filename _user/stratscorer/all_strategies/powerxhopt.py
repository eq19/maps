# Commands
# freqtrade hyperopt -c user_data/backtest-config.json -s powerxhopt --epochs 50 --spaces buy roi stoploss --hyperopt-loss SharpeHyperOptLossDaily
# freqtrade backtesting -c user_data/backtest-config.json -s powerxhopt

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

class powerxhopt(IStrategy):
    # Trading strategy based on Markus Heitkoetter's PowerX strategy
    # https://www.youtube.com/watch?v=6C_ac36iXMw
    stoploss = -1
    timeframe = "1d"
    minimal_roi = {"0": 100.}

    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": True,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        "main_plot": {
            "sma": {},
        },
        "subplots": {
            # Subplots - each dict defines one additional plot
            "MACD": {
                "macd": {"color": "blue"},
                "macdsignal": {"color": "orange"},
            },
            "RSI": {
                "rsi": {"color": "red"},
            },
            "STOCH": {
                "slowd": {"color": "red"},
            },
        },
    }

# --- Define spaces for the indicators ---
    rsi_hline = IntParameter(30, 70, default=50, space="buy")
    stoch_hline = IntParameter(30, 70, default=50, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # SMA
        dataframe["SMA"] = ta.SMA(dataframe, timeperiod=20)
        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=7)
        # SLOW STOCHASTIC
        # https://mrjbq7.github.io/ta-lib/doc_index.html
        stoch = ta.STOCH(
            dataframe,
            fastk_period=14,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
        )
        dataframe["slowd"] = stoch["slowd"]
        dataframe["slowk"] = stoch["slowk"]
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
        # print(metadata)
        # print(dataframe.tail(20))
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # pass
        conditions = []
        conditions.append(
            (dataframe['rsi'] > self.rsi_hline.value )
            & (dataframe['slowd'] > self.stoch_hline.value )
            & (dataframe["macdhist"] > 0)
            )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # The PowerX strategy works on R:R 2:1 take profit therefore exits based on indicators 
        # is actually not the official way to take profit
        # pass
        conditions = []
        conditions.append(
            # (dataframe['rsi'] < self.rsi_hline.value )
            # Playing with these exit indicators proved that using only the slowd
            # crossing had a higher profit than using the three indicators together
            # or separate but only when RSI > 34 and slowd > 68
            (dataframe['slowd'] < self.stoch_hline.value )
            # | (dataframe["macdhist"] < 0)
            )

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe
