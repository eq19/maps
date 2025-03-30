import freqtrade.vendor.qtpylib.indicators as qtpylib
from numpy import ceil
from freqtrade.exchange import timeframe_to_minutes
from freqtrade.strategy import IStrategy
from pandas.core.frame import DataFrame
from mcDuck.custom_indicators import klinger_oscilator, merge_dataframes

"""
Buys when the 1D Klinger and de 4H Klinger crosses
"""
class StrategyKlinger1D4hSupport(IStrategy):
    INTERFACE_VERSION = 2

    # Optimal ticker interval for the strategy.
    timeframe = '5m'
    timeframe_main = '4h'
    timeframe_support = '1d'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False
    ignore_buying_expired_candle_after = 360
    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 55

    # ROI table:
    """
    minimal_roi = {
        "0": 0.704,
        "1886": 0.219,
        "4355": 0.094,
        "7353": 0
    }

    # Stoploss:
    stoploss = -0.07
    """
    # ROI table:
    """
    minimal_roi = {
        '0': 0.05,
        '480': 0.025,
        '960': 0.012,
        '1440': 0
    }
    """
    
    minimal_roi = {
        "0": 100
    }

    # Stoploss:
    #stoploss = -0.045
    stoploss = -100
    # Trailing stop:
    trailing_stop = False
    trailing_stop_positive = 0.24
    trailing_stop_positive_offset = 0.315
    trailing_only_offset_is_reached = False

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.timeframe_main) for pair in pairs] + \
                            [(pair, self.timeframe_support) for pair in pairs]
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        if self.config['runmode'].value in ('backtest', 'hyperopt'):
            assert (timeframe_to_minutes(self.timeframe) <=
                    5), "Backtest this strategy in 5m or 1m timeframe."

        if not self.dp:
            return dataframe

        dataframe_main = self.dp.get_pair_dataframe(
                pair=metadata['pair'], 
                timeframe=self.timeframe_main
        )   
        dataframe_support = self.dp.get_pair_dataframe(
                pair=metadata['pair'], 
                timeframe=self.timeframe_support
        )         
        [dataframe_main["main_kvo"], dataframe_main["main_ks"]] = \
            klinger_oscilator(dataframe_main)
        [dataframe_support["support_kvo"], dataframe_support["support_ks"]] = \
            klinger_oscilator(dataframe_support)
        
        dataframe = merge_dataframes(
            source=dataframe_main,
            sourceTimeframe=self.timeframe_main,
            destination=dataframe,
            destinationTimeFrame=self.timeframe
        )
        dataframe = merge_dataframes(
            source=dataframe_support,
            sourceTimeframe=self.timeframe_support,
            destination=dataframe,
            destinationTimeFrame=self.timeframe
        )     

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        minimum_coin_price = 0.0000015
        last_day = dataframe.shift(self.shift_value(self.timeframe_main))
        last_candle_support_1 = dataframe.shift(self.shift_value(self.timeframe_support))
        last_candle_support_2 = dataframe.shift(self.shift_value(self.timeframe_support) * 2 )
        last_candle_support_3 = dataframe.shift(self.shift_value(self.timeframe_support) * 3 )
        dataframe.loc[(
            (
                qtpylib.crossed_above(dataframe["support_kvo"], dataframe["support_ks"]) | 
                qtpylib.crossed_above(last_candle_support_1["support_kvo"], last_candle_support_1["support_ks"]) | 
                qtpylib.crossed_above(last_candle_support_2["support_kvo"], last_candle_support_2["support_ks"]) | 
                qtpylib.crossed_above(last_candle_support_3["support_kvo"], last_candle_support_3["support_ks"]) 
            ) &
            ((last_day['main_kvo'] < last_day['main_ks']) &
            (dataframe['main_kvo'] > dataframe['main_ks'])) &
            (dataframe["volume"] > 0) &
            (dataframe["close"] > minimum_coin_price)
        ), "buy"] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        last_day = dataframe.shift(self.shift_value(self.timeframe_main))
        last_candle_support_1 = dataframe.shift(self.shift_value(self.timeframe_support))
        last_candle_support_2 = dataframe.shift(self.shift_value(self.timeframe_support) * 2 )
        last_candle_support_3 = dataframe.shift(self.shift_value(self.timeframe_support) * 3 )        
        dataframe.loc[(
            (
                qtpylib.crossed_below(dataframe["support_kvo"], dataframe["support_ks"]) | 
                qtpylib.crossed_below(last_candle_support_1["support_kvo"], last_candle_support_1["support_ks"]) | 
                qtpylib.crossed_below(last_candle_support_2["support_kvo"], last_candle_support_2["support_ks"]) | 
                qtpylib.crossed_below(last_candle_support_3["support_kvo"], last_candle_support_3["support_ks"]) 
            ) &
            ((last_day['main_kvo'] > last_day['main_ks']) &
            (dataframe['main_kvo'] < dataframe['main_ks'])) &            
            (dataframe["volume"] > 0)
        ), "sell"] = 1
        return dataframe

    def shift_value(self, timeframe: str) -> int:
        return int(ceil(timeframe_to_minutes(timeframe) / timeframe_to_minutes(self.timeframe)))