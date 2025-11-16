import copy
import json
import logging
import math
import os
import sys
import time
from datetime import datetime
from functools import reduce
from typing import Literal, Optional, Union

import numpy
import pandas as pd
import talib.abstract as ta
from freqtrade.persistence import Trade
from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame
from technical import qtpylib

import indicator

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

class StrategyZigzag(IStrategy):
    def __init__(self, config: dict) -> None:
        super().__init__(config=config)
        self.path_runtime = './runtime.json'
        self.indent = 4

    def runtime_write(self) -> None:
        with open(self.path_runtime, mode='w') as file:
            json.dump(self.runtime, file, indent=self.indent, sort_keys=True)

    def runtime_load(self) -> None:
        with open(self.path_runtime, mode='r') as file:
            self.runtime = json.load(file)

    def runtime_pair_initial(self) -> dict:
        threshold = 0.04

        return {
            'previous': {
                'threshold': None,
                'stoploss': None,
                'takeprofit': None,
                'direction': None,
                'profit': None,
            },
            'current': {
                'threshold': threshold,
                'stoploss': -threshold,
                'takeprofit': threshold,
                'direction': None,
                'profit': 0.,
            },
        }

    def runtime_pair_reset(self, pair: str) -> None:
        if pair not in self.runtime:
            raise Exception

        self.runtime[pair] = self.runtime_pair_initial()

    def runtime_update(self, list_pair: list) -> None:  # list[str]
        runtime_old = self.runtime
        self.runtime = {}

        for pair in runtime_old:
            if runtime_old[pair] != self.runtime_pair_initial():
                self.runtime[pair] = runtime_old[pair]

        for pair in list_pair:
            if pair not in self.runtime:
                self.runtime[pair] = self.runtime_pair_initial()

    def bot_start(self, **kwargs) -> None:
        time_begin = time.perf_counter()

        if not self.dp:
            raise Exception('DataProvider is required')

        if self.dp.runmode.value == 'hyperopt':
            raise Exception('Hyperopt is not supported')

        if self.dp.runmode.value in ['dry_run', 'live']:
            if os.path.isfile(self.path_runtime):
                self.runtime_load()
            else:
                self.runtime = {}

        elif self.dp.runmode.value == 'backtest':
            self.runtime = {}

        if self.dp.runmode.value != 'plot':
            list_pair = self.dp.current_whitelist()
            self.runtime_update(list_pair)
        # log.debug(f'runtime:\n{json_dumps(self.runtime)}')

        time_end = time.perf_counter()
        log.info(
            f'runmode:{self.dp.runmode.value}'
            f' timeframe:{self.timeframe}'
            f' {time_end - time_begin:0.4f} (second)'
        )

    def bot_loop_start(self, **kwargs) -> None:
        time_begin = time.perf_counter()

        if self.dp.runmode.value in ['dry_run', 'live']:
            self.runtime_write()

        time_end = time.perf_counter()
        log.info(
            f'runmode:{self.dp.runmode.value}'
            f' timeframe:{self.timeframe}'
            f' {time_end - time_begin:0.4f} (second)'
        )

    # Disable ROI
    # minimal_roi: dict[str, int] = {
    minimal_roi: dict = {
        '0': 10000  # 10000 * 100%
    }

    # Disable stoploss
    stoploss: float = -1.00  # -100%

    plot_config = {
        "main_plot": {},
        "subplots": {},
    }

    startup_candle_count: int = 20

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        a = numpy.arange(len(dataframe)) % 2
        dataframe.loc[a == 1, ['enter_long', 'enter_tag']] = (1, 'Long')
        dataframe.loc[a == 0, ['enter_short', 'enter_tag']] = (1, 'Short')

        return dataframe

    def custom_stake_amount(self, pair: str, current_time: datetime, current_rate: float, proposed_stake: float,
                            min_stake: Optional[float], max_stake: float, leverage: float, entry_tag: Optional[str], side: str,
                            **kwargs) -> float:

        previous_direction = self.runtime[pair]['previous']['direction']
        if previous_direction == side:
            return 0.

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

        threshold_step = 0.0025
        # threshold = abs(self.runtime[pair]['current']['stoploss']) + self.runtime[pair]['current']['takeprofit'] / 4
        # threshold = (self.runtime[pair]['current']['takeprofit'] - self.runtime[pair]['current']['stoploss']) / 4

        if self.runtime[pair]['previous']['profit'] is None:
            pass

        # elif self.runtime[pair]['previous']['profit'] < 0:
        elif self.runtime[pair]['previous']['profit'] < 0 and self.runtime[pair]['previous']['stoploss'] < -0.02:
            # self.runtime[pair]['current']['threshold'] += threshold_step
            # self.runtime[pair]['current']['threshold'] = threshold
            self.runtime[pair]['current']['stoploss'] = self.runtime[pair]['previous']['stoploss'] + threshold_step

        # elif self.runtime[pair]['previous']['profit'] > 0:
        elif self.runtime[pair]['previous']['profit'] < 0 and self.runtime[pair]['previous']['stoploss'] > -0.02:
            # self.runtime[pair]['current']['threshold'] -= threshold_step
            # self.runtime[pair]['current']['threshold'] = threshold
            self.runtime[pair]['current']['stoploss'] = self.runtime[pair]['previous']['stoploss'] - threshold_step

        # self.runtime[pair]['current']['threshold'] = max(0.01, self.runtime[pair]['current']['threshold'])
        # self.runtime[pair]['current']['stoploss'] = -self.runtime[pair]['current']['threshold']
        self.runtime[pair]['current']['threshold'] = 0.04
        self.runtime[pair]['current']['stoploss'] = min(-0.01, self.runtime[pair]['current']['stoploss'])

        self.runtime[pair]['current']['takeprofit'] = self.runtime[pair]['current']['threshold']
        self.runtime[pair]['current']['direction'] = side
        self.runtime[pair]['current']['profit'] = 0.

        log.debug(f'runtime[pair]:\n{json_dumps(self.runtime[pair])}')

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
        threshold = self.runtime[pair]['current']['threshold']

        # takeprofit_candidate = current_profit
        takeprofit_candidate = threshold + current_profit
        stoploss_candidate = -threshold + current_profit

        if takeprofit_candidate > self.runtime[pair]['current']['takeprofit']:
            self.runtime[pair]['current']['takeprofit'] = takeprofit_candidate

        if stoploss_candidate > self.runtime[pair]['current']['stoploss']:
            self.runtime[pair]['current']['stoploss'] = stoploss_candidate

        reason = None

        # if current_profit > threshold and current_profit < self.runtime[pair]['takeprofit'] / 4 * 3:
            # reason = f'takeprofit_{self.runtime[pair]["takeprofit"]:0.2f}'
        # if current_profit < 0 and current_profit < self.runtime[pair]['stoploss']:
            # reason = f'stoploss_{self.runtime[pair]["stoploss"]:0.2f}'

        if current_profit > self.runtime[pair]['current']['takeprofit']:
            reason = f'takeprofit_{self.runtime[pair]["current"]["takeprofit"]:0.2f}'

        if current_profit < self.runtime[pair]['current']['stoploss']:
            reason = f'stoploss_{self.runtime[pair]["current"]["stoploss"]:0.2f}'

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

        self.runtime[pair]['current']['profit'] = current_profit
        self.runtime[pair]['previous'] = copy.deepcopy(self.runtime[pair]['current'])
        log.debug(f'runtime:\n{json_dumps(self.runtime)}')

        log.info(
            f'{color_begin}'
            f'current_time:{current_time}'
            f' pair:{pair}'
            f' reason:{reason}'
            f' current_profit:{current_profit}'
            f' open_rate:{trade.open_rate:0.4f}'
            f' current_rate:{current_rate:0.4f}'
            f' timedelta:{current_time - trade.open_date_utc}'
            f'{color_end}'
        )

        return reason

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe
