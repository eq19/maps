# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from functools import reduce
from typing import Any, Callable, Dict, List

import talib.abstract as ta
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class RSI_BB_MACD_OPT(IHyperOpt):
    """
    Default hyperopt provided by the Freqtrade bot.
    You can override it with your own Hyperopt
    """
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add several indicators needed for buy and sell strategies defined below.
        """

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe)
        dataframe['sell_rsi'] = ta.RSI(dataframe)

        # Bollinger bands
        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']

        # MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']

        return dataframe

    @staticmethod
    def buy_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the buy strategy parameters to be used by Hyperopt.
        """
        def populate_buy_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Buy strategy Hyperopt will build and use.
            """
            conditions = []

            # GUARDS AND TRENDS
            if 'rsi-enabled' in params and params['rsi-enabled']:
                conditions.append(dataframe['rsi'] > params['rsi-value'])

            # TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'bb_lower2':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband2'])
                if params['trigger'] == 'bb_lower3':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband3'])
                if params['trigger'] == 'macd_cross_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']))

            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'buy'] = 1

            return dataframe

        return populate_buy_trend

    @staticmethod
    def indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching buy strategy parameters.
        """
        return [
            Integer(5, 50, name='rsi-value'),
            Categorical([True, False], name='rsi-enabled'),
            Categorical(['bb_lower2', 'bb_lower3', 'macd_cross_signal'], name='trigger')
        ]

    @staticmethod
    def sell_strategy_generator(params: Dict[str, Any]) -> Callable:
        """
        Define the sell strategy parameters to be used by Hyperopt.
        """
        def populate_sell_trend(dataframe: DataFrame, metadata: dict) -> DataFrame:
            """
            Sell strategy Hyperopt will build and use.
            """
            conditions = []

            # GUARDS AND TRENDS
            if 'sell-rsi-enabled' in params and params['sell-rsi-enabled']:
                conditions.append(dataframe['rsi'] > params['sell-rsi-value'])

            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sell-bb_lower2':
                    conditions.append(dataframe['close'] > dataframe['bb_lowerband2'])
                if params['sell-trigger'] == 'sell-bb_middle2':
                    conditions.append(dataframe['close'] > dataframe['bb_middleband2'])
                if params['sell-trigger'] == 'sell-bb_upper2':
                    conditions.append(dataframe['close'] > dataframe['bb_upperband2'])
                if params['trigger'] == 'sell-macd_cross_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['macdsignal'], dataframe['macd']))



            if conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, conditions),
                    'sell'] = 1

            return dataframe

        return populate_sell_trend

    @staticmethod
    def sell_indicator_space() -> List[Dimension]:
        """
        Define your Hyperopt space for searching sell strategy parameters.
        """
        return [
            Integer(30, 100, name='sell-rsi-value'),
            Categorical([True, False], name='sell-rsi-enabled'),
            Categorical(['sell-bb_lower2',
                         'sell-bb_middle2',
                         'sell-bb_upper2',
                         'sell-macd_cross_signal'], name='sell-trigger')
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include buy space.
        """
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['bb_lowerband2']) &
                (dataframe['rsi'] > 30) &
                qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal'])
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include sell space.
        """
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['bb_middleband2']) &
                (dataframe['rsi'] > 70) &
                qtpylib.crossed_above(dataframe['macdsignal'], dataframe['macd'])
            ),
            'sell'] = 1

        return dataframe
