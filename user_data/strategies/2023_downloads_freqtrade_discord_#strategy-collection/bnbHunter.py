# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
from functools import reduce


# --------------------------------


class bnbHunter(IStrategy):
    # 1047/2616:     73 trades. 68/1/4 Wins/Draws/Losses. Avg profit   4.84%. Median profit   4.39%. Total profit  12.53646531 BNB ( 353.32Σ%). Avg duration 1259.2 min. Objective: -21.19613

    # Buy hyperspace params:
    buy_params = {
        'buy-adx-value': 11, 'buy-mom-value': -23, 'buy-pd-value': 37
    }

    # Sell hyperspace params:
    sell_params = {
        'sell-adx-value': 100, 'sell-min-value': 49, 'sell-mom-value': 9
    }

    # ROI table:
    minimal_roi = {
        "0": 0.736,
        "699": 0.13555,
        "1645": 0.08157,
        "5453": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.0157
    trailing_stop_positive_offset = 0.019
    trailing_only_offset_is_reached = False
    # Optimal stoploss designed for the strategy
    stoploss = -0.13366
    # 72/100:    179 trades. 161/0/18 Wins/Draws/Losses. Avg profit   6.04%. Median profit   5.01%. Total profit  19.99723428 BNB ( 1080.54Σ%). Avg duration  71.1 min. Objective: -88.60722

    # ROI table:
    minimal_roi = {
        "0": 0.22695,
        "1380": 0.14814,
        "2414": 0.07239,
        "4403": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01066
    trailing_stop_positive_offset = 0.01234
    trailing_only_offset_is_reached = False
    # 1/40:    173 trades. 163/1/9 Wins/Draws/Losses. Avg profit   6.20%. Median profit   5.43%. Total profit  29.53105479 BNB ( 1072.77Σ%). Avg duration 405.1 min. Objective: -75.72540

    # Stoploss:
    stoploss = -0.33438
    # 82/100:    173 trades. 163/1/9 Wins/Draws/Losses. Avg profit   6.59%. Median profit   5.48%. Total profit  29.04429388 BNB ( 1139.68Σ%). Avg duration 405.1 min. Objective: -75.54600

    # ROI table:
    minimal_roi = {
        "0": 0.30112,
        "1891": 0.24999,
        "3933": 0.04942,
        "9139": 0
    }

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01025
    trailing_stop_positive_offset = 0.01237
    trailing_only_offset_is_reached = True
    # Optimal timeframe for the strategy
    timeframe = '4h'

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)
        #print(f"\"{metadata['pair']}\"")
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        # if self.buy_params.get('buy-adx-enabled'):
        conditions.append(dataframe['adx'] > self.buy_params['buy-adx-value'])
        # if self.buy_params.get('buy-mom-enabled'):
        conditions.append(dataframe['mom'] > self.buy_params['buy-mom-value'])
        # if self.buy_params.get('buy-pd-enabled'):
        conditions.append(dataframe['plus_di'] > self.buy_params['buy-pd-value'])
        # if self.buy_params.get('buy-com-enabled'):
        conditions.append(dataframe['plus_di'] > dataframe['minus_di'])
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        # if self.sell_params.get('sell-adx-enabled'):
        conditions.append(dataframe['adx'] > self.sell_params['sell-adx-value'])
        # if self.sell_params.get('sell-mom-enabled'):
        conditions.append(dataframe['mom'] < self.sell_params['sell-mom-value'])
        # if self.sell_params.get('sell-min-enabled'):
        conditions.append(dataframe['minus_di'] > self.sell_params['sell-min-value'])
        # if self.sell_params.get('sell-com-enabled'):
        conditions.append(dataframe['plus_di'] < dataframe['minus_di'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1
        return dataframe
