
from pandas.core.frame import DataFrame
from freqtrade.strategy import IStrategy, merge_informative_pair
from freqtrade.exchange import timeframe_to_minutes
import freqtrade.vendor.qtpylib.indicators as qtpylib
from mcDuck.custom_indicators import klinger_oscilator, populate_incomplete_candle


class StrategyKlinger(IStrategy):
    INTERFACE_VERSION = 2

    # Optimal ticker interval for the strategy.
    timeframe = '5m'
    informative_timeframe = '4h'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = True
    ignore_roi_if_buy_signal = False
    ignore_buying_expired_candle_after = 360
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 55


    minimal_roi = {
        "0": 100
    }

    # Stoploss:
    stoploss = -100
    # Optional order type mapping.
    
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]
        return informative_pairs
        
    def do_indicators(self, dataframe: DataFrame, metadata: dict)  -> DataFrame:
        [dataframe["kvo"], dataframe["ks"]] = klinger_oscilator(dataframe)
        return dataframe  

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        
        if self.config['runmode'].value in ('backtest', 'hyperopt'):
            assert (timeframe_to_minutes(self.timeframe) <= 5), "Backtest this strategy in 5m or 1m timeframe."

        if self.timeframe == self.informative_timeframe:
            ticker = self.dp.ticker(metadata["pair"])
            populated_dataframe = self.do_indicators(populate_incomplete_candle(dataframe,ticker), metadata)
            [dataframe["kvo"],dataframe["ks"]] = [populated_dataframe["kvo"],populated_dataframe["ks"]]  
            return dataframe

        if not self.dp:
            return dataframe
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

        informative = self.do_indicators(informative.copy(), metadata)

        dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe, ffill=True)
        skip_columns = [(s + "_" + self.informative_timeframe) for s in ['date', 'open', 'high', 'low', 'close', 'volume']]
        dataframe.rename(columns=lambda s: s.replace("_{}".format(self.informative_timeframe), "") if (not s in skip_columns) else s, inplace=True)

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        dataframe.loc[(
            (qtpylib.crossed_above(dataframe["kvo"],dataframe["ks"]))  & 
            (dataframe["volume"] > 0) &
            (dataframe["close"] > minimum_coin_price)
        ),"buy"] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[(
            (qtpylib.crossed_below(dataframe["kvo"],dataframe["ks"])) & 
            (dataframe["volume"] > 0)
        ),"sell"] = 1        
        return dataframe

