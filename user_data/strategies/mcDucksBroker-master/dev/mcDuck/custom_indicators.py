from freqtrade import data
from numpy import array, where
from pandas.core.frame import DataFrame
from pandas import Timestamp
from freqtrade.strategy import merge_informative_pair
import talib as ta
from talib.abstract import SMA, STOCH, RSI, EMA, TYPPRICE

MAIN_DATAFRAME_COLUMNS = ['date', 'open', 'high', 'low', 'close', 'volume']
BULLISH = "bullish"
BEARISH = "bearish"

def klinger_oscilator(dataframe: DataFrame) -> array:
    previous_dataframe = dataframe.shift(1)
    previous_typical_price = TYPPRICE(previous_dataframe)
    typical_price = TYPPRICE(dataframe)
    signal_volume = where((typical_price - previous_typical_price) >= 0,
                          dataframe["volume"], dataframe["volume"] * -1)
    klinger_volume_indicator = EMA(signal_volume, timeperiod=34) - \
        EMA(signal_volume, timeperiod=55)
    signal = EMA(klinger_volume_indicator, 13)

    return [klinger_volume_indicator, signal]

def stoch_rsi_smooth(dataframe: DataFrame) -> DataFrame:
    rsi = RSI(dataframe["close"],14)
    stoch_k, stoch_d = STOCH(rsi,rsi,rsi,
                            fastk_period=14,slowk_period=3,
                            slowk_matype=ta.MA_Type.EMA,
                            slowd_period=3,
                            slowd_matype=ta.MA_Type.EMA)
    dataframe["stochk"] = SMA(stoch_k,3)
    dataframe["stochd"] = SMA(dataframe["stochk"],3)
    return dataframe

def simpleTrendReversal(dataframe: DataFrame) -> DataFrame:
    dataframe['type'] = where((dataframe['open'] > dataframe['close']),BULLISH, BEARISH)
    dataframe['size'] = abs(dataframe['open'] - dataframe['close'])    
    candle_1 = dataframe.shift(1)
    candle_2 = dataframe.shift(2)
    candle_3 = dataframe.shift(3)
    dataframe.loc[((candle_1['type'] == BEARISH) & \
       (candle_1['size'] < dataframe['size']) & \
       (candle_2['type'] == BEARISH) & \
       (candle_2['size'] < dataframe['size']) & \
       (candle_3['type'] == BEARISH) & \
       (candle_3['size'] < dataframe['size'])),'trend_reversal'] = True

    #for i in range(1,3):
    #    candle = dataframe.shift(i)
    #    if (candle['type'] != BEARISH) | \
    #       (candle['size'] > dataframe['size']):
    #        break
    #    if i == 3:
    #        dataframe['trend_reversal'] = True
    return dataframe


def populate_incomplete_candle(dataframe: DataFrame, ticker: dict) -> DataFrame:
    return dataframe.copy().iloc[1:].append({
        "date": Timestamp(ticker["timestamp"], unit='ms', tz='UTC', freq='240T'),
        "open": ticker["open"],
        "high": ticker["high"],
        "low": ticker["low"],
        "close": ticker["close"],
        "volume": ticker["baseVolume"]
    }, ignore_index=True)


"""
Merge two dataframes into one
"""
def merge_dataframes(source: DataFrame, 
                    sourceTimeframe: str, 
                    destination: DataFrame, 
                    destinationTimeFrame: str) -> DataFrame:
    destination = merge_informative_pair(destination, source, destinationTimeFrame, sourceTimeframe, ffill=True)
    skip_columns = [(s + "_" + sourceTimeframe) for s in MAIN_DATAFRAME_COLUMNS]
    destination.drop(inplace=True,columns=skip_columns)
    destination.rename(inplace=True,columns=lambda s: 
        s.replace("_{}".format(sourceTimeframe), "") if (not s in skip_columns) else s)
    return destination

