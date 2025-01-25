# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from functools import reduce
from typing import Any, Callable, Dict, List

import talib.abstract as ta
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class ADX_OPT(IHyperOpt):
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

        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=25)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=25)
        dataframe['sar'] = ta.SAR(dataframe)
        dataframe['mom'] = ta.MOM(dataframe, timeperiod=14)

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
                if params['trigger'] == 'adx':
                    conditions.append(dataframe['adx'] > 25)
                if params['trigger'] == 'mom':
                    conditions.append(dataframe['mom'] < 0)
                if params['trigger'] == 'minus_di':
                    conditions.append(dataframe['minus_di'] > 25)
                if params['trigger'] == 'plus_minus_DI':
                    conditions.append(dataframe['plus_di'] < dataframe['minus_di'])



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
            Categorical(['adx', 'mom', 'minus_di','plus_minus_DI'], name='trigger')
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
            if 'trigger' in params:
                if params['trigger'] == 'adx':
                    conditions.append(dataframe['adx'] > 25)
                if params['trigger'] == 'mom':
                    conditions.append(dataframe['mom'] > 0)
                if params['trigger'] == 'minus_di':
                    conditions.append(dataframe['minus_di'] > 25)
                if params['trigger'] == 'plus_minus_DI':
                    conditions.append(dataframe['plus_di'] > dataframe['minus_di'])


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
            Categorical(['adx', 'mom', 'minus_di','plus_minus_DI'], name='sell-trigger')
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include buy space.
        """
        dataframe.loc[
            (
                    (dataframe['adx'] > 25) &
                    (dataframe['mom'] < 0) &
                    (dataframe['minus_di'] > 25) &
                    (dataframe['plus_di'] < dataframe['minus_di']) &
                    (dataframe['rsi'] > 30)

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
                   (dataframe['adx'] > 25) &
                   (dataframe['mom'] > 0) &
                   (dataframe['minus_di'] > 25) &
                   (dataframe['plus_di'] > dataframe['minus_di']) &
                   (dataframe['rsi'] > 70)

           ),
           'sell'] = 1

        return dataframe
