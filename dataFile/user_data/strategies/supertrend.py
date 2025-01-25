# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class supertrend(IStrategy):
    stoploss = -100.0
    timeframe = "1d"
    minimal_roi = {"0": 100.0}

# --- Plotting ---

    # Use this section if you want to plot the indicators on a chart after backtesting
    plot_config = {
        'main_plot': {
            # Create sma line
            'supertrend': {'color': 'green'},
        },
#        'subplots': {
#            "MACD": {
#                'macd': {'color': 'blue', 'fill_to': 'macdsignal'},
#                'macdsignal': {'color': 'orange'},
#                'macdhist': {'color': 'green', 'type': 'bar', 'plotly': {'opacity': 0.4}}
#            },
#        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Supertrend
        shighl = 50
        smult = 5.0
        dataframe["supertrend"] = pta.supertrend(
            high=dataframe["high"],
            low=dataframe["low"],
            close=dataframe["close"],
            length=shighl,
            multiplier=smult,
        )[f"SUPERT_{shighl}_{smult}"]

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            ((dataframe["close"] > dataframe["supertrend"])),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            ((dataframe["close"] < dataframe["supertrend"])),
            "sell",
        ] = 1
        return dataframe
