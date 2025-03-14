# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


# --------------------------------
class bb_riding(IStrategy):
    minimal_roi = {
        "0": 0.3
    }

    stoploss = -0.235

    timeframe = '30m'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        boll = ta.BBANDS(dataframe, nbdevup=2.0, nbdevdn=2.0, timeperiod=20)
        dataframe['bb_lower'] = boll['lowerband']
        dataframe['bb_middle'] = boll['middleband']
        dataframe['bb_upper'] = boll['upperband']

        dataframe["bb_width"] = (
            (dataframe["bb_upper"] - dataframe["bb_lower"]) / dataframe["bb_middle"]
        )

        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        #print(metadata)
        #print(dataframe[["date","close","bb_upper","bb_middle","bb_lower","bb_width"]].tail(25))

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['close'] > dataframe['bb_upper']) 
                    & (dataframe['bb_width'] > 0.02) 
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                    (dataframe['macdsignal'] < 0)
            ),
            'sell'] = 1
        return dataframe
