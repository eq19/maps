# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

from functools import reduce
from typing import Any, Callable, Dict, List

import talib.abstract as ta
from pandas import DataFrame
from skopt.space import Categorical, Dimension, Integer

import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.optimize.hyperopt_interface import IHyperOpt


class RSI_STOCHRSI_MACD_EMA_OPT(IHyperOpt):
    """
    Default hyperopt provided by the Freqtrade bot.
    You can override it with your own Hyperopt
    """
    @staticmethod
    def populate_indicators(dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add several indicators needed for buy and sell strategies defined below.
        """
        # 1. MACD
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # 2. RSI
        dataframe['rsi'] = ta.RSI(dataframe)

        # 3. Stoch RSI
        stoch_rsi = ta.STOCHRSI(dataframe)
        dataframe['fastd_rsi'] = stoch_rsi['fastd']
        #dataframe['fastk_rsi'] = stoch_rsi['fastk']

        # 4. EMA - Exponential Moving Average
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)


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

            # 1. GUARDS AND TRENDS
            if 'rsi-enabled' in params and params['rsi-enabled']:
                conditions.append(dataframe['rsi'] < params['rsi-value'])
            if 'fastd-rsi-enabled' in params and params['fastd-rsi-enabled']:
                conditions.append(dataframe['fastd-rsi'] < params['fastd-rsi-value'])

            # 2. TRIGGERS
            if 'trigger' in params:
                if params['trigger'] == 'macd_cross_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['macd'], dataframe['macdsignal']))
                if params['trigger'] == 'ema':
                    conditions.append(dataframe['close'] < dataframe['ema10'])

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
            Integer(15, 45, name='fastd-rsi-value'),
            Integer(20, 50, name='rsi-value'),
            Categorical([True, False], name='fastd-enabled'),
            Categorical([True, False], name='rsi-enabled'),
            Categorical(['macd_cross_signal', 'ema'], name='trigger')
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
            if 'sell-fastd-rsi-enabled' in params and params['sell-fastd-rsi-enabled']:
                conditions.append(dataframe['fastd-rsi'] > params['sell-fastd-rsi-value'])
            if 'sell-rsi-enabled' in params and params['sell-rsi-enabled']:
                conditions.append(dataframe['rsi'] > params['sell-rsi-value'])

            # TRIGGERS
            if 'sell-trigger' in params:
                if params['sell-trigger'] == 'sell-macd_cross_signal':
                    conditions.append(qtpylib.crossed_above(dataframe['macdsignal'], dataframe['macd']))
                if params['trigger'] == 'ema':
                    conditions.append(dataframe['close'] > dataframe['ema10'])

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
            Integer(40, 100, name='sell-fastd-rsi-value'),
            Integer(50, 100, name='sell-rsi-value'),
            Categorical([True, False], name='sell-fastd-enabled'),
            Categorical([True, False], name='sell-rsi-enabled'),
            Categorical(['sell-macd_cross_signal','ema'], name='sell-trigger')
        ]

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators. Should be a copy of same method from strategy.
        Must align to populate_indicators in this file.
        Only used when --spaces does not include buy space.
        """
        dataframe.loc[
            (
                (dataframe['macd'] > dataframe['macdsignal']) &
                (dataframe['close'] < dataframe['ema10']) &
                (dataframe['rsi'] > 30) &
                (dataframe['fastd_rsi'] > 20)
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
                (dataframe['macd'] < dataframe['macdsignal']) &
                (dataframe['close'] > dataframe['ema10']) &
                (dataframe['rsi'] > 70) &
                (dataframe['fastd_rsi'] > 80)
            ),
            'sell'] = 1

        return dataframe
