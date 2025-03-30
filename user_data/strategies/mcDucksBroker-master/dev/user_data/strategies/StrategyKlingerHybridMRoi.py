from pandas.core.frame import DataFrame
from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.exchange import timeframe_to_minutes
import freqtrade.vendor.qtpylib.indicators as qtpylib
from mcDuck.custom_indicators import klinger_oscilator, populate_incomplete_candle

# Buy at 1d candles, sell at 4h candles
class StrategyKlingerHybridMRoi(IStrategy):
    INTERFACE_VERSION = 2

    # Optimal ticker interval for the strategy.
    timeframe = '5m'
    informative_timeframe_buy = '4h'
    informative_timeframe_sell = '1d'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = False
    ignore_buying_expired_candle_after = 60
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 55

    # ROI table:
    minimal_roi = {
        '0': 0.05,
        '480': 0.025,
        '960': 0.012,
        '1440': 0
    }
    # Stoploss:
    stoploss = -0.045

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.19
    trailing_stop_positive_offset = 0.235
    trailing_only_offset_is_reached = False

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe_buy) for pair in pairs] + \
                            [(pair, self.informative_timeframe_sell) for pair in pairs]
        return informative_pairs

    def do_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        [dataframe["kvo"], dataframe["ks"]] = klinger_oscilator(dataframe)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        if self.config['runmode'].value in ('backtest', 'hyperopt'):
            assert (timeframe_to_minutes(self.timeframe) <=
                    5), "Backtest this strategy in 5m or 1m timeframe."

        # Live / dry run
        if self.timeframe == self.informative_timeframe_sell:
            dataframe_sell = self.do_indicators(self.dp.get_pair_dataframe(
                pair=metadata['pair'], timeframe=self.informative_timeframe_sell), metadata)
            dataframe_buy = self.do_indicators(dataframe.copy(), metadata)
            [dataframe["skvo"], dataframe["sks"]] = [dataframe_sell["kvo"], dataframe_sell["ks"]]
            [dataframe["bkvo"], dataframe["bks"]] = [dataframe_buy["kvo"], dataframe_buy["ks"]]
            return dataframe

        if not self.dp:
            return dataframe

        informative_buy = self.do_indicators(self.dp.get_pair_dataframe(
            pair=metadata['pair'], timeframe=self.informative_timeframe_buy), metadata)
        [informative_buy["bkvo"], informative_buy["bks"]] = [
            informative_buy["kvo"], informative_buy["ks"]]
        informative_sell = self.do_indicators(self.dp.get_pair_dataframe(
            pair=metadata['pair'], timeframe=self.informative_timeframe_sell), metadata)
        [informative_sell["skvo"], informative_sell["sks"]] = [
            informative_sell["kvo"], informative_sell["ks"]]

        dataframe = merge_informative_pair(
            dataframe, informative_buy, self.timeframe, self.informative_timeframe_buy, ffill=True)
        dataframe = merge_informative_pair(
            dataframe, informative_sell, self.timeframe, self.informative_timeframe_sell, ffill=True)
        skip_columns = [(s + "_" + self.informative_timeframe_buy) for s in ['date', 'open', 'high', 'low', 'close', 'volume']] + \
                       [(s + "_" + self.informative_timeframe_sell)
                        for s in ['date', 'open', 'high', 'low', 'close', 'volume']]
        dataframe.rename(columns=lambda s: s.replace("_{}".format(
            self.informative_timeframe_buy), "") if (not s in skip_columns) else s, inplace=True)
        dataframe.rename(columns=lambda s: s.replace("_{}".format(
            self.informative_timeframe_sell), "") if (not s in skip_columns) else s, inplace=True)

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        dataframe.loc[(
            (qtpylib.crossed_above(dataframe["bkvo"], dataframe["bks"])) &
            (dataframe["volume"] > 0) &
            (dataframe["close"] > minimum_coin_price)
        ), "buy"] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(
            (qtpylib.crossed_below(dataframe["skvo"], dataframe["sks"])) &
            (dataframe["volume"] > 0)
        ), "sell"] = 1
        return dataframe
