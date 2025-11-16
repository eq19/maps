import json
import logging
import math
import os
import sys
import time
from datetime import datetime, timedelta
from functools import reduce
from typing import Literal, Optional, Union

import numpy
import pandas
import talib.abstract as ta
from freqtrade.exchange import timeframe_to_minutes
from freqtrade.persistence import Trade
from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame
from technical import qtpylib

import indicator
import plot


# log = logging.getLogger(__name__)
# log.setLevel(logging.DEBUG)
log = logging.getLogger(__name__)
log_level: Literal[0, 1, 2] = 2

if log_level == 2:
    log.setLevel(logging.DEBUG)
elif log_level == 1:
    log.setLevel(logging.INFO)
elif log_level == 0:
    log.setLevel(logging.ERROR)

# See https://stackoverflow.com/questions/46807204/python-logging-duplicated
# See https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
if not log.handlers:
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s() %(message)s'))
    log.addHandler(sh)

log.propagate = False

def json_dumps(object_: dict) -> str:
    return json.dumps(object_, indent=4, default=list, sort_keys=True)

class StrategyNN(IStrategy):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self.indent = 4
        self.window_line = 50
        self.threshold_entry = 0.025
        self.threshold_exit_profit = 0.015
        self.threshold_exit_loss = 0.01
        self.threshold_line = 0.01
        self.time_position_maximum = timedelta(minutes=timeframe_to_minutes(config['timeframe']) * self.window_line)

    def bot_start(self, **kwargs) -> None:
        log.info('')

    def bot_loop_start(self, **kwargs) -> None:
        log.info('')

    # Disable ROI
    minimal_roi: dict = {  # dict[str, int]
        '0': 10000  # 10000 * 100%
    }

    # Disable stoploss
    stoploss: float = -1.00  # -100%

    plot_config = {
        'main_plot': {},
        'subplots': {},
    }

    startup_candle_count: int = 2000

    def populate_any_indicators(self, pair: str, dataframe: DataFrame, timeframe: str, informative: DataFrame = None,
                                set_generalized_indicators: bool = False) -> DataFrame:
        if informative is None:
            informative = self.dp.get_pair_dataframe(pair, timeframe)

        # informative[f'%{pair}-open'] = informative['open']
        # informative[f'%{pair}-high'] = informative['high']
        # informative[f'%{pair}-low'] = informative['low']
        # informative[f'%{pair}-close'] = informative['close']
        # informative[f'%{pair}-volume'] = informative['volume']
        informative[f'%{pair}-heikin_ashi-close'] = (
            (informative['open'] + informative['high'] + informative['low'] + informative['close']) / 4
        )
        # informative[f'%{pair}-moving_average_simple-200'] = (
        #     indicator.moving_average_simple(informative[f'%{pair}-heikin_ashi-close'].to_numpy(), window=200)
        # )

        # informative[f'{pair}-heikin_ashi-close'] = (
            # (informative['open'] + informative['high'] + informative['low'] + informative['close']) / 4
        # )

        for t in self.freqai_info['feature_parameters']['indicator_periods_candles']:
            t = int(t)
            # informative[f'%{pair}-MFI-{t}'] = ta.MFI(informative, timeperiod=t) / 100
            # informative[f'%{pair}-ADX-{t}'] = ta.ADX(informative, timeperiod=t) / 100

            # bollinger = qtpylib.bollinger_bands(
                # qtpylib.typical_price(informative), window=t, stds=2.2
            # )
            # informative[f'{pair}-bb_lowerband-{t}'] = bollinger['lower']
            # informative[f'{pair}-bb_middleband-{t}'] = bollinger['mid']
            # informative[f'{pair}-bb_upperband-{t}'] = bollinger['upper']
            # informative[f'%{pair}-bb_width-{t}'] = (
                # informative[f'{pair}-bb_upperband-{t}']
                # - informative[f'{pair}-bb_lowerband-{t}']
            # ) / informative[f'{pair}-bb_middleband-{t}']
            # informative[f'%{pair}-close-bb_lower-{t}'] = (
                # informative['close'] / informative[f'{pair}-bb_lowerband-{t}']
            # )

            # informative[f'%{pair}-ROC-{t}'] = ta.ROC(informative, timeperiod=t)
            # informative[f'%{pair}-relative_volume-{t}'] = (
                # informative['volume'] / informative['volume'].rolling(t).mean()
            # )

            # informative[f'%{pair}-RSI-{t}'] = ta.RSI(informative[f'{pair}-heikin_ashi-close'], timeperiod=t) / 100
            # informative[f'%{pair}-RCI-{t}'] = rci(informative[f'{pair}-heikin_ashi-close'].to_numpy(), timeperiod=t) / 100

            # informative[f'{pair}-RSI-{t}'] = ta.RSI(informative[f'{pair}-heikin_ashi-close'], timeperiod=t) / 100
            # informative[f'%{pair}-EMA(RSI)-{t}'] = ta.EMA(informative[f'{pair}-RSI-{t}'], timeperiod=t)
            # informative[f'%{pair}-WMA(RSI)-{t}'] = ta.WMA(informative[f'{pair}-RSI-{t}'], timeperiod=t)
            # informative[f'%{pair}-HMA(RSI)-{t}'] = qtpylib.hma(informative[f'{pair}-RSI-{t}'], window=t)
            # informative[f'%{pair}-Regression_1(RSI)-{t}'] = (
                # indicator.regression_1(informative[f'{pair}-RSI-{t}'].to_numpy(), window=t)
            # )
            # informative[f'%{pair}-moving_average_simple(RSI)-{t}'] = (
                # indicator.moving_average_simple(informative[f'{pair}-RSI-{t}'].to_numpy(), window=t)
            # )

            # informative[f'{pair}-Group1-moving_average_simple-{t}'] = (
                # indicator.moving_average_simple(informative[f'{pair}-heikin_ashi-close'].to_numpy(), window=t)
            # )
            # informative[f'{pair}-Group1-Regression_1-{t}'] = (
                # indicator.regression_1(informative[f'{pair}-heikin_ashi-close'].to_numpy(), window=t)
            # )
            # informative[f'{pair}-Group1-EMA-{t}'] = ta.EMA(informative[f'{pair}-heikin_ashi-close'], timeperiod=t)
            # informative[f'{pair}-Group1-WMA-{t}'] = ta.WMA(informative[f'{pair}-heikin_ashi-close'], timeperiod=t)
            # informative[f'{pair}-Group1-HMA-{t}'] = qtpylib.hma(informative[f'{pair}-heikin_ashi-close'], window=t)

            # bollinger = qtpylib.bollinger_bands(informative[f'{pair}-heikin_ashi-close'], window=t, stds=2.2)
            # informative[f'{pair}-Group1-BB_lower-{t}'] = bollinger['lower']
            # informative[f'{pair}-Group1-BB_upper-{t}'] = bollinger['upper']

        indicators = [col for col in informative if col.startswith('%')]
        for n in range(self.freqai_info['feature_parameters']['include_shifted_candles'] + 1):
            if n == 0:
                continue
            informative_shift = informative[indicators].shift(n)
            informative_shift = informative_shift.add_suffix('_shift-' + str(n))
            informative = pandas.concat((informative, informative_shift), axis=1)

        dataframe = merge_informative_pair(dataframe, informative, self.config['timeframe'], timeframe, ffill=True)
        skip_columns = [
            (s + '_' + timeframe) for s in ['date', 'open', 'high', 'low', 'close', 'volume']
        ]
        dataframe = dataframe.drop(columns=skip_columns)

        column_group1 = [column for column in dataframe if column.startswith(f'{pair}-Group1-')]
        column = column_group1
        for i in range(len(column)):
            for j in range(i + 1, len(column)):
                # dataframe[f'%({column[i]} - {column[j]})'] = dataframe[column[i]] - dataframe[column[j]]
                dataframe[f'%({column[i]} / {column[j]})'] = dataframe[column[i]] / dataframe[column[j]]

        if set_generalized_indicators:
            log.debug(list(dataframe))

            # dataframe['%day_of_week'] = dataframe['date'].dt.dayofweek / 7
            # dataframe['%hour_of_day'] = dataframe['date'].dt.hour / 24
            # dataframe['%minute_of_hour'] = dataframe['date'].dt.minute / 60

            line_price = dataframe[f'%{pair}-heikin_ashi-close_{self.timeframe}'].to_numpy()
            dataframe['line_price'] = line_price

            # line = indicator.moving_average_simple(line_price, self.window_line)
            line = indicator.ema_window(line_price, self.window_line)
            # line = ta.WMA(line_price, self.window_line)
            dataframe['line'] = line
            dataframe['&prediction_line'] = indicator.shift(line, period=-self.window_line) / line

            # line = pandas.Series(line_price).rolling(100).max().to_numpy()
            # dataframe['line2'] = line
            # dataframe['&prediction_line2'] = indicator.shift(line, period=-100) / line

            # line = pandas.Series(line_price).rolling(100).min().to_numpy()
            # dataframe['line3'] = line
            # dataframe['&prediction_line3'] = indicator.shift(line, period=-100) / line

            # x = line_price
            # x = indicator.profit_long(x, 100)
            # x = indicator.sort_mean(x, 0, 100)
            # dataframe['line'] = x.numpy()
            # x = indicator.shift(x.numpy(), -100)
            # dataframe['&prediction_line'] = x

            dataframe['RSI'] = ta.RSI(dataframe[f'%{pair}-heikin_ashi-close_{self.timeframe}'], timeperiod=13)

        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.freqai.start(dataframe, metadata, self)
        log.debug(list(dataframe))

        dataframe.loc[
            (
                (dataframe['do_predict'] == 1)
                &
                (dataframe['&prediction_line'] > 1 + self.threshold_entry)
                # &
                # ((dataframe['line'] * dataframe['&prediction_line']) / dataframe['line_price'] > 1 + 0.02)
                &
                (dataframe['RSI'] < 30)
            )
            , ['enter_long', 'enter_tag']
        ] = (1, 'Long')

        dataframe.loc[
            (
                (dataframe['do_predict'] == 1)
                &
                (dataframe['&prediction_line'] < 1 - self.threshold_entry)
                # &
                # ((dataframe['line'] * dataframe['&prediction_line']) / dataframe['line_price'] < 1 - 0.02)
                &
                (dataframe['RSI'] > 70)
            )
            , ['enter_short', 'enter_tag']
        ] = (1, 'Short')

        if True:
            dataframe['prediction_line'] = dataframe['line'] * dataframe['&prediction_line']
            dataframe['line_shift'] = dataframe['line'].shift(-self.window_line)

            # dataframe['prediction_line2'] = dataframe['line2'] * dataframe['&prediction_line2']
            # dataframe['line_shift2'] = dataframe['line2'].shift(-self.window_line)

            # dataframe['prediction_line3'] = dataframe['line3'] * dataframe['&prediction_line3']
            # dataframe['line_shift3'] = dataframe['line3'].shift(-self.window_line)

            # dataframe['line_shift'] = dataframe['line'].shift(-self.window_line)

            addplot = [
                {
                    'column': 'line',
                    'kind': 'line',
                    'color': 'gray',
                },
                {
                    'column': 'line_shift',
                    'kind': 'line',
                    'color': 'red',
                },
                {
                    'column': 'prediction_line',
                    'kind': 'line',
                    'color': 'blue',
                },
                # {
                #     'column': 'line2',
                #     'kind': 'line',
                #     'color': 'gray',
                # },
                # {
                #     'column': 'line_shift2',
                #     'kind': 'line',
                #     'color': 'red',
                # },
                # {
                #     'column': 'prediction_line2',
                #     'kind': 'line',
                #     'color': 'blue',
                # },
                # {
                #     'column': 'line3',
                #     'kind': 'line',
                #     'color': 'gray',
                # },
                # {
                #     'column': 'line_shift3',
                #     'kind': 'line',
                #     'color': 'red',
                # },
                # {
                #     'column': 'prediction_line3',
                #     'kind': 'line',
                #     'color': 'blue',
                # },
            ]

            subplot = [
                # [
                #     {
                #         'column': 'line',
                #         'kind': 'line',
                #         'color': 'gray',
                #     },
                #     {
                #         'column': 'line_shift',
                #         'kind': 'line',
                #         'color': 'red',
                #     },
                #     {
                #         'column': '&prediction_line',
                #         'kind': 'line',
                #         'color': 'blue',
                #     },
                # ],
                # [
                #     {
                #         'column': 'enter_long',
                #         'kind': 'line',
                #     },
                #     {
                #         'column': 'enter_short',
                #         'kind': 'line',
                #     },
                # ],
            ]

            filename = f"{metadata['pair'].replace('/', '-')}.html"
            plot.plot(metadata['pair'], dataframe[dataframe['&prediction_line'] > 0], addplot=addplot, subplot=subplot, filename=filename)

        return dataframe

    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float, proposed_stake: float,
                            min_stake: Optional[float], max_stake: float, leverage: float, entry_tag: Optional[str], side: str,
                            **kwargs) -> float:

        if min_stake > max_stake:
            log.info(
                f'Entry signal has skipped: min_stake > max_stake: {min_stake:0.4f} > {max_stake:0.4f}'
            )
            return 0.

        initial_stake = self.stake_amount

        if initial_stake < min_stake:
            initial_stake = math.ceil(min_stake)

        if initial_stake > max_stake:
            log.info(
                f'Entry signal has skipped: initial_stake > max_stake: {initial_stake:0.4f} > {max_stake:0.4f}'
            )
            return 0.

        # dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        # candle_last = dataframe.iloc[-1].squeeze()

        log.info(
            f'current_time:{current_time}'
            f' pair:{pair}'
            f' (initial_stake/stake_amount):({initial_stake}/{self.stake_amount})'
            f' side:{side}'
            f' entry_tag:{entry_tag}'
            f' min_stake:{min_stake:0.4f}'
            f' max_stake:{max_stake:0.4f}'
            f' current_rate:{current_rate:0.4f}'
        )

        return initial_stake

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, current_profit: float,
                    **kwargs) -> Optional[Union[str, bool]]:

        # dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        # candle_last = dataframe.iloc[-1].squeeze()

        reason = None

        if (current_time - trade.open_date_utc) > self.time_position_maximum:
            reason = 'timeout'

        if current_profit > self.threshold_exit_profit:
            reason = 'profit'

        if current_profit < -self.threshold_exit_loss:
            reason = 'loss'

        if reason is None:
            return False

        color_ansi: dict = {  # dict[str, str]
            'black'  : '\x1b[0;30m',
            'blue'   : '\x1b[0;34m',
            'cyan'   : '\x1b[0;36m',
            'green'  : '\x1b[0;32m',
            'magenda': '\x1b[0;35m',
            'red'    : '\x1b[0;31m',
            'yellow' : '\x1b[0;33m',
            'reset'  : '\x1b[0m'   ,
        }

        color_begin = ''
        color_end = color_ansi['reset']

        if current_profit > 0:
            color_begin = color_ansi['green']
        elif current_profit < 0:
            color_begin = color_ansi['red']

        log.info(
            f'current_time:{current_time}'
            f' pair:{pair}'
            f' reason:{reason}'
            f' current_profit:{color_begin}{current_profit:.8f}{color_end}'
            f' open_rate:{trade.open_rate:0.4f}'
            f' current_rate:{current_rate:0.4f}'
            f' timedelta:{current_time - trade.open_date_utc}'
        )

        return reason

    # def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float, time_in_force: str,
    #                         current_time: datetime, entry_tag: Optional[str], side: str, **kwargs) -> bool:

    #     dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    #     candle_last = dataframe.iloc[-1].squeeze()

    #     if side == 'long':
    #         if rate > (candle_last['line'] * (1 + self.threshold_line)):
    #             log.info('')
    #             return False
    #     else:
    #         if rate < (candle_last['line'] * (1 - self.threshold_line)):
    #             log.info('')
    #             return False

    #     return True

    # def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float, rate: float, time_in_force: str,
    #                        exit_reason: str, current_time: datetime, **kwargs) -> bool:

    #     dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    #     candle_last = dataframe.iloc[-1].squeeze()

    #     if trade.trade_direction == 'long':
    #         if rate < (candle_last['line'] * (1 - self.threshold_line)):
    #             log.info('')
    #             return False
    #     else:
    #         if rate > (candle_last['line'] * (1 + self.threshold_line)):
    #             log.info('')
    #             return False

    #     return True

    def leverage(self, pair: str, current_time: datetime, current_rate: float, proposed_leverage: float, max_leverage: float,
                 entry_tag: Optional[str], side: str, **kwargs) -> float:
        return 1.

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
