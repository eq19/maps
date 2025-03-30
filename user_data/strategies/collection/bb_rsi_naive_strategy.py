# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy import (
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IStrategy,
    IntParameter,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class BBRSINaiveStrategy(IStrategy):
    """
    This is a strategy template to get you started.
    More information in https://www.freqtrade.io/en/latest/strategy-customization/

    You can:
        :return: a Dataframe with all mandatory indicators for the strategies
    - Rename the class name (Do not forget to update class_name)
    - Add any methods you want to build your strategy
    - Add any lib you need to build your strategy

    You must keep:
    - the lib in the section "Do not remove these libs"
    - the methods: populate_indicators, populate_buy_trend, populate_sell_trend
    You should keep:
    - timeframe, minimal_roi, stoploss, trailing_*
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {"0": 0.236, "87": 0.052, "163": 0.018, "466": 0}

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.257

    # Trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.041
    trailing_stop_positive_offset = 0.044
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy.
    timeframe = "5m"

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping.
    order_types = {
        "buy": "limit",
        "sell": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force.
    order_time_in_force = {"buy": "gtc", "sell": "gtc"}

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        "main_plot": {
            "tema": {},
            "sar": {"color": "white"},
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
        },
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # RSI
        dataframe["rsi"] = ta.RSI(dataframe)

        # MACD
        macd = ta.MACD(dataframe)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=50, stds=1
        )
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]
        dataframe["bb_percent"] = (dataframe["close"] - dataframe["bb_lowerband"]) / (
            dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        )
        dataframe["bb_width"] = (
            dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        ) / dataframe["bb_middleband"]

        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, window=30)

        # Parabolic SAR
        dataframe["sar"] = ta.SAR(dataframe)

        # TEMA - Triple Exponential Moving Average
        dataframe["tema"] = ta.TEMA(dataframe, timeperiod=9)

        # Retrieve best bid and best ask from the orderbook
        # ------------------------------------
        """
        # first check if dataprovider is available
        if self.dp:
            if self.dp.runmode.value in ('live', 'dry_run'):
                ob = self.dp.orderbook(metadata['pair'], 1)
                dataframe['best_bid'] = ob['bids'][0][0]
                dataframe['best_ask'] = ob['asks'][0][0]
        """

        return dataframe

    # def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    #     """
    #     Based on TA indicators, populates the buy signal for the given dataframe
    #     :param dataframe: DataFrame populated with indicators
    #     :param metadata: Additional information, like the currently traded pair
    #     :return: DataFrame with buy column
    #     """
    #     dataframe.loc[
    #         (
    #             (qtpylib.crossed_above(dataframe["rsi"], 55))
    #             # (dataframe["rsi"] > 25)
    #             & (
    #                 qtpylib.crossed_above(dataframe["macd"], (dataframe["macdsignal"]))
    #                 | qtpylib.crossed_above(
    #                     dataframe["close"], dataframe["bb_upperband"]
    #                 )
    #             )
    #             # & (dataframe["close"] > dataframe["bb_upperband"])
    #             # & (dataframe["close"] > dataframe["bb_middleband"])
    #             # & (dataframe["volume"] > 0)
    #         ),
    #         "buy",
    #     ] = 1

    #     return dataframe

    # def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    #     """
    #     Based on TA indicators, populates the sell signal for the given dataframe
    #     :param dataframe: DataFrame populated with indicators
    #     :param metadata: Additional information, like the currently traded pair
    #     :return: DataFrame with buy column
    #     """
    #     dataframe.loc[
    #         (
    #             (qtpylib.crossed_below(dataframe["rsi"], 70))
    #             # (dataframe["rsi"] > 70)
    #             # & (dataframe["macdhist"] < 0)
    #             # | qtpylib.crossed_below(dataframe["macd"], dataframe["macdsignal"])
    #             | qtpylib.crossed_below(dataframe["close"], dataframe["bb_upperband"])
    #             # & (dataframe["volume"] > 0)  # Make sure Volume is not 0
    #         ),
    #         "sell",
    #     ] = 1
    #     return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], 30))
                & (  # Signal: RSI crosses above 30
                    dataframe["tema"] <= dataframe["bb_middleband"]
                )
                & (  # Guard: tema below BB middle
                    dataframe["tema"] > dataframe["tema"].shift(1)
                )
                & (  # Guard: tema is raising
                    dataframe["volume"] > 0
                )  # Make sure Volume is not 0
            ),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                (qtpylib.crossed_above(dataframe["rsi"], 70))
                & (  # Signal: RSI crosses above 70
                    dataframe["tema"] > dataframe["bb_middleband"]
                )
                & (  # Guard: tema above BB middle
                    dataframe["tema"] < dataframe["tema"].shift(1)
                )
                & (  # Guard: tema is falling
                    dataframe["volume"] > 0
                )  # Make sure Volume is not 0
            ),
            "sell",
        ] = 1
        return dataframe
