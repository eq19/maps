# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from functools import reduce
from typing import Any, Callable, Dict, List

import talib.abstract as ta
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class BBRSI_OPT(IHyperOpt):
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
        bollinger1 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=1)
        dataframe['bb_lowerband1'] = bollinger1['lower']
        dataframe['bb_middleband1'] = bollinger1['mid']
        dataframe['bb_upperband1'] = bollinger1['upper']

        bollinger2 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband2'] = bollinger2['lower']
        dataframe['bb_middleband2'] = bollinger2['mid']
        dataframe['bb_upperband2'] = bollinger2['upper']

        bollinger3 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=3)
        dataframe['bb_lowerband3'] = bollinger3['lower']
        dataframe['bb_middleband3'] = bollinger3['mid']
        dataframe['bb_upperband3'] = bollinger3['upper']

        bollinger4 = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=4)
        dataframe['bb_lowerband4'] = bollinger4['lower']
        dataframe['bb_middleband4'] = bollinger4['mid']
        dataframe['bb_upperband4'] = bollinger4['upper']

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
                if params['trigger'] == 'bb_lower1':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband1'])
                if params['trigger'] == 'bb_lower2':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband2'])
                if params['trigger'] == 'bb_lower3':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband3'])
                if params['trigger'] == 'bb_lower4':
                    conditions.append(dataframe['close'] < dataframe['bb_lowerband4'])

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
            Categorical(['bb_lower1', 'bb_lower2', 'bb_lower3', 'bb_lower4'], name='trigger')
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
                if params['sell-trigger'] == 'sell-bb_lower1':
                    conditions.append(dataframe['close'] > dataframe['bb_lowerband1'])
                if params['sell-trigger'] == 'sell-bb_middle1':
                    conditions.append(dataframe['close'] > dataframe['bb_middleband1'])
                if params['sell-trigger'] == 'sell-bb_upper1':
                    conditions.append(dataframe['close'] > dataframe['bb_upperband1'])

                if params['sell-trigger'] == 'sell-bb_lower2':
                    conditions.append(dataframe['close'] > dataframe['bb_lowerband2'])
                if params['sell-trigger'] == 'sell-bb_middle2':
                    conditions.append(dataframe['close'] > dataframe['bb_middleband2'])
                if params['sell-trigger'] == 'sell-bb_upper2':
                    conditions.append(dataframe['close'] > dataframe['bb_upperband2'])

                if params['sell-trigger'] == 'sell-bb_lower3':
                    conditions.append(dataframe['close'] > dataframe['bb_lowerband3'])
                if params['sell-trigger'] == 'sell-bb_middle3':
                    conditions.append(dataframe['close'] > dataframe['bb_middleband3'])
                if params['sell-trigger'] == 'sell-bb_upper3':
                    conditions.append(dataframe['close'] > dataframe['bb_upperband3'])


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
            Categorical(['sell-bb_lower1',
                         'sell-bb_middle1',
                         'sell-bb_upper1',
                         'sell-bb_lower2',
                         'sell-bb_middle2',
                         'sell-bb_upper2',
                         'sell-bb_lower3',
                         'sell-bb_middle3',
                         'sell-bb_upper3'], name='sell-trigger')
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include buy space.
        """
        dataframe.loc[
            (
                (dataframe['rsi'] > 20) &
                (dataframe['close'] < dataframe['bb_lowerband2'])
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
               (dataframe['close'] > dataframe['bb_middleband2'])
           ),
           'sell'] = 1

        return dataframe
