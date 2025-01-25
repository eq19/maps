from freqtrade.strategy.interface import IStrategy
from pandas.core.frame import DataFrame
from functools import reduce
from mcDuck.custom_indicators import simpleTrendReversal


class StrategyTrendReversal(IStrategy):
    INTERFACE_VERSION = 2

    timeframe = '5m'
    timeframe_support = '5m'
    timeframe_main = '5m'

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = False
    sell_profit_only = False
    ignore_roi_if_buy_signal = False
    ignore_buying_expired_candle_after = 5
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 4

    # ROI table:
    minimal_roi = {
        "0": 0.179,
        "26": 0.093,
        "80": 0.035,
        "177": 0
    }

    # Stoploss:
    stoploss = -0.316

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = simpleTrendReversal(dataframe)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        conditions = []
        conditions.append(dataframe["volume"] > 0)
        conditions.append(dataframe["close"] > minimum_coin_price)
        conditions.append(dataframe["trend_reversal"] == True)
        if conditions:
            dataframe.loc[reduce(lambda x, y: x & y, conditions), "buy"] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return super().populate_sell_trend(dataframe, metadata)
