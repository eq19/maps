from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

class SampleStrategy(IStrategy):
    # Define strategy parameters
    minimal_roi = {
        "0": 0.1  # 10% profit
    }
    stoploss = -0.2  # 20% stop loss
    timeframe = '1h'

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Add SMA indicators
        dataframe['sma_short'] = dataframe['close'].rolling(window=10).mean()
        dataframe['sma_long'] = dataframe['close'].rolling(window=50).mean()
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Buy when short SMA crosses above long SMA
        dataframe.loc[
            (dataframe['sma_short'] > dataframe['sma_long']),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Sell when short SMA crosses below long SMA
        dataframe.loc[
            (dataframe['sma_short'] < dataframe['sma_long']),
            'sell'] = 1
        return dataframe
