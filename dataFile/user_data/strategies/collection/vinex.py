from freqtrade.strategy import IStrategy
import logging
import numpy as np
from pandas import DataFrame
import locale
locale.setlocale(category=locale.LC_ALL, locale='')
log = logging.getLogger(__name__)

class ViNex(IStrategy):
    INTERFACE_VERSION = 2

    df_csv = './user_data/df.csv'

    minimal_roi = {"0": 100}
    stoploss = -1
    stoploss_on_exchange = False
    trailing_stop = False
    use_custom_stoploss = False
    timeframe = '5m'
    process_only_new_candles = True
    use_sell_signal = True
    sell_profit_only = False
    startup_candle_count: int = 300

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df['green'] = (df['close'] - df['open']).ge(0)
        df['bodysize'] = (df['close'] / df['open']).where(df['green'], df['open'] / df['close'])
        df['hi_adj'] = df['close'].where(df['green'], df['open']) + (df['high'] - df['close']).where(df['green'], (df['high'] - df['open'])) / df['bodysize'].pow(0.25)
        df['lo_adj'] = df['open'].where(df['green'], df['close']) - (df['open'] - df['low']).where(df['green'], (df['close'] - df['low'])) / df['bodysize'].pow(0.25)
        df['hlc3_adj'] = (df['hi_adj'] + df['lo_adj'] + df['close']) / 3
        df['lc2_adj'] = (df['lo_adj'] + df['close']) / 2
        df['hc2_adj'] = (df['hi_adj'] + df['close']) / 2
        df_closechange = df['close'] - df['close'].shift(1)
        s = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 19, 24, 36, 60, 120, 288)
        for i in s:
            df['updown'] = np.where(df_closechange.rolling(window=i, min_periods=i).sum().gt(0), 1, np.where(df_closechange.rolling(window=i, min_periods=i).sum().lt(0), -1, 0))
            df[f"streak_{i}"] = df['updown'].groupby((df['updown'].ne(df['updown'].shift(1))).cumsum()).cumsum()
            df[f"streak_{i}_change"] = df['close'] / df['close'].to_numpy()[df.index.to_numpy() - df[f"streak_{i}"].abs().to_numpy()]
        df['streak_s_min'] = df[[f"streak_{i}" for i in s]].min(axis=1)
        df['streak_s_max'] = df[[f"streak_{i}" for i in s]].max(axis=1)
        df['pair'] = metadata['pair']
        with open(self.df_csv, 'a') as f:
            df.to_csv(f, sep='\t', header=f.tell()==0, index=False)
        return df

    def populate_buy_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'buy'] = False
        return df

    def populate_sell_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'sell'] = False
        return df

    def bot_loop_start(self, **kwargs) -> None:
        if self.config['runmode'].value not in ('live', 'dry_run'):
            if self.write_to_csv:
                with open(self.df_csv, 'w') as f:
                    pass
        return None
