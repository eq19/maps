# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import numpy as np

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

rsi_lower = 50


class x_strat_dryrun_org(IStrategy):
    stoploss = -0.01
    timeframe = "4h"

    # Trailing stoploss
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.002
    trailing_stop_positive_offset = 0.003

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": True,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }

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
            "dema": {"color": "red"},
            "sma": {"color": "blue"},
        },
        "subplots": {
            # Additional subplot RSI
            "rsi": {"rsi": {"color": "blue"}, "rsi_sma": {"color": "red"}},
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["sma"] = ta.SMA(dataframe, timeperiod=21)
        dataframe["dema"] = ta.DEMA(dataframe, timeperiod=9)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=21)
        dataframe["rsi_sma"] = dataframe["rsi"].rolling(window=14).mean()

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

        # SMA check
        dataframe["ma_pos"] = np.where(dataframe["dema"] > dataframe["sma"], 1, 0)
        # RSI check
        dataframe["rsi_pos"] = np.where(dataframe["rsi"] > dataframe["rsi_sma"], 1, 0)
        # Posities tellen
        dataframe["pos_cnt"] = dataframe["ma_pos"] + dataframe["rsi_pos"]
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            ((dataframe["pos_cnt"] == 2)),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            ((dataframe["dema"] < dataframe["sma"])),
            "sell",
        ] = 1
        return dataframe
