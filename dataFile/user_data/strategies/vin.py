from freqtrade.strategy import IStrategy, informative
from freqtrade.exchange import timeframe_to_prev_date
from freqtrade.persistence import Trade
import logging
import numpy as np
from pandas import DataFrame
from functools import reduce
from datetime import datetime
import locale
locale.setlocale(category=locale.LC_ALL, locale='')
log = logging.getLogger(__name__)

class ViN(IStrategy):
    INTERFACE_VERSION = 2

    def version(self) -> str:
        return 'v1.2.4'

    min_day_listed: int = 5
    custom_buy_info = {}
    max_concurrent_buy_signals_check = True

    minimal_roi = {"0": 100}
    stoploss = -1
    stoploss_on_exchange = False
    trailing_stop = False
    use_custom_stoploss = False
    timeframe = '5m'
    process_only_new_candles = True
    use_sell_signal = True
    sell_profit_only = False
    startup_candle_count: int = 144

    @property
    def protections(self):
        return [
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": 36
            }
        ]

    def populate_indicators_buy(self, df: DataFrame, metadata: dict) -> DataFrame:
        return df

    def populate_indicators_sell(self, df: DataFrame, metadata: dict) -> DataFrame:
        return df

    @informative('1h')
    def populate_indicators_1h(self, df: DataFrame, metadata: dict) -> DataFrame:
        i = self.min_day_listed * 24
        df['candle_count'] = df['volume'].rolling(window=i, min_periods=i).count()
        return df

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        green = (df['close'] - df['open']).ge(0)
        bodysize = (df['close'] / df['open']).where(green, df['open'] / df['close'])
        hi_adj = df['close'].where(green, df['open']) + (df['high'] - df['close']).where(green, (df['high'] - df['open'])) / bodysize.pow(0.25)
        lo_adj = df['open'].where(green, df['close']) - (df['open'] - df['low']).where(green, (df['close'] - df['low'])) / bodysize.pow(0.25)
        df['hlc3_adj'] = (hi_adj + lo_adj + df['close']) / 3
        df['lc2_adj'] = (lo_adj + df['close']) / 2
        df['hc2_adj'] = (hi_adj + df['close']) / 2
        df['ho2_adj'] = (hi_adj + df['open']) / 2
        df_closechange = df['close'] - df['close'].shift(1)
        s = (1, 2, 3)
        for i in s:
            df['updown'] = np.where(df_closechange.rolling(window=i, min_periods=i).sum().gt(0), 1, np.where(df_closechange.rolling(window=i, min_periods=i).sum().lt(0), -1, 0))
            df[f"streak_{i}"] = df['updown'].groupby((df['updown'].ne(df['updown'].shift(1))).cumsum()).cumsum()
        df['streak_s_min'] = df[[f"streak_{i}" for i in s]].min(axis=1)
        df['streak_s_min_change'] = df['close'] / df['close'].to_numpy()[df.index.to_numpy() - df['streak_s_min'].abs().to_numpy()]
        df['streak_s_max'] = df[[f"streak_{i}" for i in s]].max(axis=1)
        df.drop(columns=[f"streak_{i}" for i in s], inplace=True)
        df_closechange = df['close'] - df['close'].shift(1)
        i = 12
        df['updown'] = np.where(df_closechange.rolling(window=i, min_periods=i).sum().gt(0), 1, np.where(df_closechange.rolling(window=i, min_periods=i).sum().lt(0), -1, 0))
        df['streak_h'] = df['updown'].groupby((df['updown'].ne(df['updown'].shift(1))).cumsum()).cumsum()
# maybe streak_h_min_change for dumps?
        df.drop(columns=['updown'], inplace=True)
        df = self.populate_indicators_buy(df, metadata)
        df = self.populate_indicators_sell(df, metadata)
        return df

    def fill_custom_buy_info(self, df:DataFrame, metadata: dict):
        df_buy: DataFrame = df.loc[df['buy'], ['date', 'buy_tag']]
        for index, row in df_buy.iterrows():
            buy_date = row['date']
            if buy_date not in self.custom_buy_info:
                self.custom_buy_info[buy_date] = {}
                self.custom_buy_info[buy_date]['buy_signals'] = 1
            else:
                self.custom_buy_info[buy_date]['buy_signals'] += 1
            self.custom_buy_info[buy_date][metadata['pair']] = row['buy_tag']
        return None

    def populate_buy_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'buy'] = False
        return df

    def populate_sell_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'sell'] = False
        return df

    def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float, current_profit: float, **kwargs):
        return None

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, **kwargs) -> bool:
        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        buy_candle_date = df['date'].iloc[-1]
        d = buy_candle_date.strftime('%Y-%m-%d %H:%M')
        try:
            buy_info = self.custom_buy_info[buy_candle_date]
            buy_tag = buy_info[pair]
            buy_signal_count = buy_info['buy_signals']
            if self.max_concurrent_buy_signals_check:
                pairs = len(self.dp.current_whitelist())
                max_concurrent_buy_signals = max(int(pairs * 0.08), 2)
                if buy_signal_count > max_concurrent_buy_signals:
                    log.info(f"{d} confirm_trade_entry: Cancel buy for pair {pair} with buy tag {buy_tag}. There are {buy_signal_count} concurrent buy signals (max = {max_concurrent_buy_signals}).")
                    return False
            log.info(f"{d} confirm_trade_entry: Buy for pair {pair} with buy tag {buy_tag} and {buy_signal_count} concurrent buy signals.")
        except:
            log.warning(f"{d} confirm_trade_entry: No buy info for pair {pair}.")
            return False
        return True

    def confirm_trade_exit(self, pair: str, trade: "Trade", order_type: str, amount: float,
                           rate: float, time_in_force: str, sell_reason: str, **kwargs) -> bool:
        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        buy_candle_date = df['date'].iloc[-1]
        d = buy_candle_date.strftime('%Y-%m-%d %H:%M')
        if sell_reason[:4] != 'hc2c':
            try:
                buy_info = self.custom_buy_info[buy_candle_date]
                buy_signal_count = buy_info['buy_signals']
                if self.max_concurrent_buy_signals_check:
                    pairs = len(self.dp.current_whitelist())
                    max_concurrent_buy_signals = max(int(pairs * 0.04), 1)
                    if buy_signal_count > max_concurrent_buy_signals:
                        log.info(f"{d} confirm_trade_exit: Cancel sell {sell_reason} for pair {pair}. There are {buy_signal_count} concurrent buy signals (max = {max_concurrent_buy_signals}).")
                        return False
            except:
                return True
        return True

class ViNBuyPct(ViN):
    pct_lb = range(21, 29)
    def populate_indicators_buy(self, df: DataFrame, metadata: dict) -> DataFrame:
        for i in self.pct_lb:
            df[f"pctchange_{i}"] = df['close'].pct_change(periods=i)
            pctchange_mean = df[f"pctchange_{i}"].rolling(window=i, min_periods=i).mean()
            pctchange_std = df[f"pctchange_{i}"].rolling(window=i, min_periods=i).std()
            df[f"bb_pctchange_{i}_up"] = pctchange_mean + 2 * pctchange_std
            df[f"bb_pctchange_{i}_lo"] = pctchange_mean - 2 * pctchange_std
            df[f"volume_mean_{i}"] = df['volume'].rolling(window=i, min_periods=i).mean()
        return df

    def populate_buy_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'buy_tag'] = ''
        for i in self.pct_lb:
            buy_conditions = [
                df['candle_count_1h'].ge(self.min_day_listed * 24),
                df['volume'].ge(df[f"volume_mean_{i}"].shift(1)),
                df['streak_s_min'].le(-1),
                df['streak_s_max'].between(-5, 0),
                df['streak_h'].ge(-20),
                df['streak_s_min'].ge(df['streak_h']),
                df['streak_s_min_change'].le(0.97),
                (df[f"pctchange_{i}"] / df[f"bb_pctchange_{i}_lo"]).between(1.01, 1.39),
                (df[f"bb_pctchange_{i}_up"] - df[f"bb_pctchange_{i}_lo"]).ge(0.02),
                (df['lc2_adj'] / df['close']).between(0.945, 0.995)
            ]
            buy = reduce(lambda x, y: x & y, buy_conditions)
            df.loc[buy, 'buy_tag'] += f"{i} "
        df.loc[:, 'buy'] = df['buy_tag'].ne('')
        df.loc[df['buy'], 'buy_tag'] = 'pct ' + df['buy_tag'].str.strip()
        self.fill_custom_buy_info(df, metadata)
        return df

class ViNBuyLc2(ViN):
    lc2_lb = range(15, 21)
    def populate_indicators_buy(self, df: DataFrame, metadata: dict) -> DataFrame:
        for i in self.lc2_lb:
            df[f"lc2_low_{i}"] = df['lc2_adj'].rolling(window=i, min_periods=i).min()
            df[f"volume_mean_{i}"] = df['volume'].rolling(window=i, min_periods=i).mean()
        return df

    def populate_buy_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'buy_tag'] = ''
        for i in self.lc2_lb:
            buy_conditions = [
                df['candle_count_1h'].ge(self.min_day_listed * 24),
                df['volume'].gt(df[f"volume_mean_{i}"].shift(1)),
                (df['lc2_adj'] / df[f"lc2_low_{i}"].shift(1)).le(0.97),
                (df['lc2_adj'] / df['close']).between(0.945, 0.995)
            ]
            buy = reduce(lambda x, y: x & y, buy_conditions)
            df.loc[buy, 'buy_tag'] += f"{i} "
        df.loc[:, 'buy'] = df['buy_tag'].eq('15 16 17 18 19 20 ')
        df.loc[df['buy'], 'buy_tag'] = 'lc2 ' + df['buy_tag'].str.strip()
        # print(df.loc[df['buy'], ['date', 'lc2_adj', 'lc2_low_20', 'close']])
        self.fill_custom_buy_info(df, metadata)
        return df

class ViNBuyHlc3(ViN):
    hlc3_lb = range(16, 30)
    def populate_indicators_buy(self, df: DataFrame, metadata: dict) -> DataFrame:
        for i in self.hlc3_lb:
            df[f"hl3_volatility_{i}"] = df['hlc3_adj'].rolling(window=i, min_periods=i).max() / df['hlc3_adj'].rolling(window=i, min_periods=i).min()
            df[f"volume_mean_{i}"] = df['volume'].rolling(window=i, min_periods=i).mean()
        return df

    def populate_buy_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[:, 'buy_tag'] = ''
        for i in self.hlc3_lb:
            buy_conditions = [
                df['candle_count_1h'].ge(self.min_day_listed * 24),
                df[f"hl3_volatility_{i}"].shift(2).le(1.02),
                (df['volume'].shift(1) / df[f"volume_mean_{i}"].shift(2)).gt(1.01),
                (df['volume'] / df['volume'].shift(1)).gt(1.01),
                (df['hlc3_adj'].shift(1) / df['hlc3_adj'].shift(2)).gt(1.015),
                (df['hlc3_adj'] / df['hlc3_adj'].shift(1)).gt(1.01)
                # (df['hc2_adj'] / df['close']).le(1.01)
            ]
            buy = reduce(lambda x, y: x & y, buy_conditions)
            df.loc[buy, 'buy_tag'] += f"{i} "
        df.loc[:, 'buy'] = ~df['buy_tag'].isin(['', '14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 '])
        df.loc[df['buy'], 'buy_tag'] = 'hlc3 ' + df['buy_tag'].str.strip()
        self.fill_custom_buy_info(df, metadata)
        return df

class ViNSellRiseFall(ViN):
    def custom_sell(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):
        df: DataFrame = self.dp.get_analyzed_dataframe(pair, self.timeframe)[0]
        trade_open_date = timeframe_to_prev_date(self.timeframe, trade.open_date_utc)
        df_trade = df.loc[df['date'].ge(trade_open_date)]
        trade_len = len(df_trade)
        candle_1 = df_trade.iloc[-1]
        trade_recent_buys = df_trade['buy'].tail(min(trade_len, 6)).sum()
        if trade_len <= 2 or trade_recent_buys >= 1 or candle_1['streak_s_min'] >= -1 or candle_1['streak_s_max'] >= 1:
            return None
        candle_2 = df_trade.iloc[-2]
        hlc3_min = df_trade['hlc3_adj'].tail(trade_len).min()
        hlc3_max = df_trade['hlc3_adj'].tail(trade_len).max()
        candle_min = df_trade.loc[df_trade['hlc3_adj'] <= 1.001 * hlc3_min].iloc[-1]
        candle_max = df_trade.loc[df_trade['hlc3_adj'] >= 0.999 * hlc3_max].iloc[-1]
        rise = candle_max['hlc3_adj'] / candle_min['hlc3_adj'] if candle_max['date'] > candle_min['date'] else 1
        fall = candle_max['hlc3_adj'] / candle_1['hlc3_adj']
        cp = (candle_1['close'] - trade.open_rate) / trade.open_rate
        t = 'profit' if cp >= 0.005 else 'loss'
        d = candle_1['date'].strftime('%Y-%m-%d %H:%M')
        u: str = trade.buy_tag[:3]
        if fall > max(1.16 - trade_len / 3200, pow(rise, 0.5)):
            log.info(f"{d} custom_sell: fall sell for pair {pair} with {t} {cp:.2f} and trade len {trade_len}.")
            return f"fall {u}"
        if candle_1['hc2_adj'] / candle_1['close'] >= 1.016 and candle_1['volume'] / candle_2['volume'] <= 0.80:
            log.info(f"{d} custom_sell: hc2c sell for pair {pair} with {t} {cp:.2f} and trade len {trade_len}.")
            return f"hc2c {u}"
        if candle_1['ho2_adj'] / candle_1['open'] >= 1.008 and candle_1['volume'] / candle_2['volume'] <= 0.90:
            log.info(f"{d} custom_sell: hc2o sell for pair {pair} with {t} {cp:.2f} and trade len {trade_len}.")
            return f"hc2o {u}"
        j = int(54 * pow(rise, 2))
        if trade_len > j:
            hlc3_min = df_trade['hlc3_adj'].tail(j).min()
            hlc3_max = df_trade['hlc3_adj'].tail(j).max()
            if hlc3_max / hlc3_min < min(1.05, trade_len / j) and candle_1['streak_s_max'] < 1 and candle_1['streak_s_min'] < 0:
                log.info(f"{d} custom_sell: sideways sell for pair {pair} with {t} {cp:.2f} and trade len {trade_len}.")
                return f"side {u}"
        return None

class ViNPctRiseFall(ViNBuyPct, ViNSellRiseFall):
    pass

class ViNLc2RiseFall(ViNBuyLc2, ViNSellRiseFall):
    pass

class ViNHlc3RiseFall(ViNBuyHlc3, ViNSellRiseFall):
    pass
