# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
# --------------------------------
class BbandRsi(IStrategy):
    """
    author@: Gert Wohlgemuth
    converted from:
    https://github.com/sthewissen/Mynt/blob/master/src/Mynt.Core/Strategies/BbandRsi.cs
    """
    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {"0": 0.1}
    # Optimal stoploss designed for the strategy
    stoploss = -0.25
    # Optimal timeframe for the strategy
    timeframe = '1h'

    # Hyperopt spaces
    rsi_buy_hline = IntParameter(20, 40, default=30, space="buy")
    rsi_sell_hline = IntParameter(60, 80, default=70, space="sell")
    bb_stds = IntParameter(1, 4, default=2, space="buy")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger bands
        for std in self.bb_stds.range:
            dataframe[f'bb_lowerband_{std}'] = (qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=std))['lower']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            (
                    (dataframe['rsi'] < self.rsi_buy_hline.value ) &
                    (dataframe['close'] < dataframe[f'bb_lowerband_{self.std.value}'])

            ),
        )

        if conditions:
            dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        conditions.append(
            (
                    (dataframe['rsi'] > self.rsi_sell_hline.value ) &
            ),
        )

        if conditions:
            dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

