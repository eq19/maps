import logging
from functools import reduce

import pandas as pd
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.strategy import IStrategy, merge_informative_pair


logger = logging.getLogger(__name__)


class StrategyRL(IStrategy):

    minimal_roi: dict = {
        '0': 10000  # 10000 * 100%
    }

    # Disable stoploss
    stoploss: float = -1.00  # -100%

    plot_config = {
        'main_plot': {},
        'subplots': {
            'prediction': {'prediction': {'color': 'blue'}},
            'do_predict': {
                'do_predict': {'color': 'brown'},
            },
        },
    }

    startup_candle_count: int = 40

    def populate_any_indicators(self, pair: str, dataframe: DataFrame, timeframe: str, informative: DataFrame = None,
                                set_generalized_indicators: bool = False) -> DataFrame:

        if informative is None:
            informative = self.dp.get_pair_dataframe(pair, timeframe)

        # for t in self.freqai_info['feature_parameters']['indicator_periods_candles']:
            # t = int(t)
            # informative[f'%{pair}-rsi-period_{t}'] = ta.RSI(informative, timeperiod=t)
            # informative[f'%{pair}-mfi-period_{t}'] = ta.MFI(informative, timeperiod=t)
            # informative[f'%{pair}-adx-period_{t}'] = ta.ADX(informative, window=t)

        # informative[f'%{pair}-close'] = informative['close']
        # informative[f'%{pair}-open'] = informative['open']
        # informative[f'%{pair}-high'] = informative['high']
        # informative[f'%{pair}-low'] = informative['low']
        # informative[f'%{pair}-volume'] = informative['volume']

        informative[f"%-{pair}raw_close"] = informative["close"]
        informative[f"%-{pair}raw_open"] = informative["open"]
        informative[f"%-{pair}raw_high"] = informative["high"]
        informative[f"%-{pair}raw_low"] = informative["low"]

        # indicators = [col for col in informative if col.startswith('%')]
        # for n in range(self.freqai_info['feature_parameters']['include_shifted_candles'] + 1):
            # if n == 0:
                # continue
            # informative_shift = informative[indicators].shift(n)
            # informative_shift = informative_shift.add_suffix('_shift-' + str(n))
            # informative = pd.concat((informative, informative_shift), axis=1)

        dataframe = merge_informative_pair(dataframe, informative, self.config['timeframe'], timeframe, ffill=True)
        skip_columns = [
            (s + '_' + timeframe) for s in ['date', 'open', 'high', 'low', 'close', 'volume']
        ]
        dataframe = dataframe.drop(columns=skip_columns)

        if set_generalized_indicators:
            dataframe['&-action'] = 0

        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.freqai.start(dataframe, metadata, self)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        enter_long_conditions = [dataframe['do_predict'] == 1, dataframe['&-action'] == 1]

        if enter_long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, enter_long_conditions), ['enter_long', 'enter_tag']
            ] = (1, 'long')

        enter_short_conditions = [dataframe['do_predict'] == 1, dataframe['&-action'] == 3]

        if enter_short_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, enter_short_conditions), ['enter_short', 'enter_tag']
            ] = (1, 'short')

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        exit_long_conditions = [dataframe['do_predict'] == 1, dataframe['&-action'] == 2]
        if exit_long_conditions:
            dataframe.loc[reduce(lambda x, y: x & y, exit_long_conditions), 'exit_long'] = 1

        exit_short_conditions = [dataframe['do_predict'] == 1, dataframe['&-action'] == 4]
        if exit_short_conditions:
            dataframe.loc[reduce(lambda x, y: x & y, exit_short_conditions), 'exit_short'] = 1

        return dataframe

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time,
        entry_tag,
        side: str,
        **kwargs,
    ) -> bool:

        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = df.iloc[-1].squeeze()

        if side == 'long':
            if rate > (last_candle['close'] * (1 + 0.0025)):
                return False
        else:
            if rate < (last_candle['close'] * (1 - 0.0025)):
                return False

        return True
