# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class ema_strat_15m_prod(IStrategy):
    stoploss = -0.2
    timeframe = "15m"

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
        "60": 0.6,
        "120": 0.05,
        "600": 0.035,
        "630": 0.012,
        "0": 0.09,
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["EMA_QUICK"] = ta.SMA(dataframe, timeperiod=7)
        dataframe["EMA_SLOW"] = ta.SMA(dataframe, timeperiod=21)
        # print(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe["close"] > dataframe["EMA_QUICK"])
                & (dataframe["EMA_QUICK"] > dataframe["EMA_SLOW"])
            ),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(), "sell",] = 1
        return dataframe
