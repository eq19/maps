# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from freqtrade.persistence import Trade
from freqtrade.state import RunMode
from freqtrade.exchange import timeframe_to_prev_date
from datetime import datetime, timedelta
# from freqtrade.strategy import stoploss_from_open

class new_strat_bb_macd_rsi_5_4_2033(IStrategy):
    stoploss = -0.2
    timeframe = "30m"
    minimal_roi = {
        "240": 0.1,
        "360": 0.05,
        "0": 0.5,  
            }

    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": True,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }

    # Trailing stoploss
    # trailing_stop = True
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.04

    # make use of the custom stoploss function
    use_custom_stoploss = True
    # use_custom_stoploss = False
    
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime, current_rate: float, current_profit: float, **kwargs) -> float:
        # dataframe.shape
        # timeframe=trade.timeframe
        # strategy=trade.strategy
        # sl = trade.stop_loss
        # stake = trade.stake_amount
        # sl_pct = trade.stop_loss_pct
        # sl_upd = trade.stoploss_last_update
        # sl_init = trade.initial_stop_loss
        # opendate = trade.open_date
        # openvalue = trade.open_trade_value
        # openrate = trade.open_rate # prijs van aanschaf
        # print(self)
        # print(pair)
        # print(trade)
        # print(current_time)
        # print(current_rate) # huidige prijs
        # print(current_profit)
        # print('===========')
        # print(sl, sl_pct, sl_upd, opendate, openrate)
        # print(timeframe, strategy, sl_init, sl, sl_pct, sl_upd, stake, opendate, openvalue)
        # result = 1
        # if self.custom_info and pair in self.custom_info and trade:
        #     # using current_time directly (like below) will only work in backtesting.
        #     # so check "runmode" to make sure that it's only used in backtesting/hyperopt
        #     if self.dp and self.dp.runmode.value in ('backtest', 'hyperopt'):
        #         relative_sl = self.custom_info[pair].loc[current_time]['atr']
        #     # in live / dry-run, it'll be really the current time
        #     else:
        #       # but we can just use the last entry from an already analyzed dataframe instead
        #       dataframe, last_updated = self.dp.get_analyzed_dataframe(pair=pair, timeframe=self.timeframe)
        #       # WARNING
        #       # only use .iat[-1] in live mode, not in backtesting/hyperopt
        #       # otherwise you will look into the future
        #       # see: https://www.freqtrade.io/en/latest/strategy-customization/#common-mistakes-when-developing-strategies
        #       relative_sl = dataframe['atr'].iat[-1]

        #     if (relative_sl is not None):
        #         # new stoploss relative to current_rate
        #         new_stoploss = (current_rate-relative_sl)/current_rate
        #         # turn into relative negative offset required by `custom_stoploss` return implementation
        #         result = new_stoploss - 1
        #     return result
        return -0.005

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["rsi_sma"] = dataframe["rsi"].rolling(window=14).mean()

        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, nbdevup=2.0, nbdevdn=2.0, timeperiod=50)
        dataframe["bb_lowerband"] = bollinger["lowerband"]
        dataframe["bb_middleband"] = bollinger["middleband"]
        dataframe["bb_upperband"] = bollinger["upperband"]
        
        # Bollinger % percent
        dataframe["bb_percent"] = (
            (dataframe["close"] - dataframe["bb_lowerband"]) /
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"])
        )
        
        # Bollinger width
        dataframe["bb_width"] = (
            (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe["bb_middleband"]
        )

        # MACD
        # https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
        macd = ta.MACD(
            dataframe,
            fastperiod=8,
            fastmatype=0,
            slowperiod=24,
            slowmatype=0,
            signalperiod=9,
            signalmatype=0,
        )
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        # === ENTRY CONDITIONS ===
        # Check for oversold conditions:
        # RSI oversold crosses above treshold is the first signal to look out for
        dataframe["rsi_oversold"]=qtpylib.crossed_above(dataframe['rsi'], 30)
        # Before or during oversold conditions price should be lower than lower bollinger band and move into the band
        # (BB percent should cross above 0 percent)
        dataframe["bb_percent_cross"] = qtpylib.crossed_above(dataframe['bb_percent'], 0)
        dataframe["signal_0"] = (dataframe["rsi_oversold"] & dataframe["bb_percent_cross"]) | (dataframe["rsi_oversold"].shift(+1) & dataframe["bb_percent_cross"]) | (dataframe["rsi_oversold"].shift(+2) & dataframe["bb_percent_cross"]) | (dataframe["rsi_oversold"].shift(+3) & dataframe["bb_percent_cross"]) | (dataframe["rsi_oversold"].shift(+4) & dataframe["bb_percent_cross"]) | (dataframe["rsi_oversold"].shift(+5) & dataframe["bb_percent_cross"])

        # Gaining bullish momentum:
        # RSI should cross rsi_sma above after oversold conditions
        dataframe["rsi_sma_cross"] = qtpylib.crossed_above(dataframe['rsi'], dataframe['rsi_sma'])
        # Entry signal 1 is valid when a rsi sma cross occurs after a the RSI and BB% oversold conditions
        dataframe["signal_1"] = (dataframe["signal_0"] & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+1) & dataframe["rsi_sma_cross"])| (dataframe["signal_0"].shift(+2) & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+3) & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+4) & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+5) & dataframe["rsi_sma_cross"]) #| (dataframe["signal_0"].shift(+6) & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+7) & dataframe["rsi_sma_cross"]) | (dataframe["signal_0"].shift(+8) & dataframe["rsi_sma_cross"])
        # After signal 1 a MACD cross should happen below 0 line which indicates that a bullish move can happen
        dataframe["macd_cross"] = (dataframe["macd"] < 0) & (dataframe["macdsignal"] < 0) & (dataframe["macdhist"] > 0)
        # Entry signal 2 is valid when macd cross happens shortly after signal 1
        # Entry 1 and Entry 2 do not have to occur at the same time for a valid signal
        # but signal 1 has to happen within x periods before macd cross
        dataframe["signal_2"] = (dataframe["signal_1"] & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+1) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+2) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+3) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+4) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+5) & dataframe["macd_cross"])#| (dataframe["signal_1"].shift(+6) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+7) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+8) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+9) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+10) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+11) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+12) & dataframe["macd_cross"]) | (dataframe["signal_1"].shift(+13) & dataframe["macd_cross"])

        # Crossing tresholds:
        # When price closes above bollinger middle band the expectation is that enough momentum has been gained
        # to keep moving in the bullish direction so technically, this is the real entry condition.
        dataframe["sma_cross"]=dataframe["close"] > dataframe["bb_middleband"]
        dataframe["entry"] = (dataframe["signal_2"] & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+1) & dataframe["sma_cross"])| (dataframe["signal_2"].shift(+2) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+3) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+4) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+5) & dataframe["sma_cross"]) #| (dataframe["signal_2"].shift(+6) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+7) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+8) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+9) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+10) & dataframe["sma_cross"]) #| (dataframe["signal_2"].shift(+11) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+12) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+13) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+14) & dataframe["sma_cross"]) | (dataframe["signal_2"].shift(+15) & dataframe["sma_cross"])
        
        # # Stuff for later?
        # dataframe['last_high'] = dataframe['high'].rolling(20).max().shift(1)
        
        # === EXIT CONDITIONS ===
        dataframe["exit"]=(qtpylib.crossed_above(dataframe['bb_middleband'], dataframe['close'])) & (dataframe["macd"] < 0)
 
        # ==== Trailing custom stoploss indicator ====
        # dataframe['last_lowest'] = dataframe['low'].rolling(10).min()

        # dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        # # if self.dp.runmode.value in ('backtest', 'hyperopt'):
        # #   # add indicator mapped to correct DatetimeIndex to custom_info
        # #   self.custom_info[metadata['pair']] = dataframe[['date', 'atr']].copy().set_index('date')

        # # print(dataframe[['date','close','low','last_lowest','close','last_highest']].tail(40 ))

        # === PRINT STUFF ===
        # print(dataframe[['date','close','signal_0','signal_1','signal_2','macd_cross','entry']].loc[dataframe['entry'] == True].tail(55))
        # print(dataframe[['date','close','entry_2','entry_3','exit_1']].loc[dataframe['exit_1'] == True].tail(55))
        # print(dataframe[['date','close','entry_0','entry_1','entry_2','entry_3']].loc[dataframe['entry_1'] == True].tail(55))
        # print(dataframe[['date','close','bb_percent','bb_percent_cross','rsi','rsi_sma','rsi_sma_cross','entry_1','macd_cross','entry_2']].loc[dataframe['entry_2'] == True].tail(55))
        # print(dataframe.tail(55))
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["signal_2"] == True),
            # (),
            "buy",
        ] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            # (dataframe['exit'] == True),
            # (qtpylib.crossed_above(dataframe['bb_middleband'], dataframe['close'])),
            # (qtpylib.crossed_above(dataframe['bb_percent'], 1)),
            (()), 
            "sell",
        ] = 1
        return dataframe


# Step 2:
# For these beliefs some potential considerations for the best trading signals are below. Note that the number values have been selected arbitrarily so you will need to test various values to find those you are happiest with:

#     Setup:
#     Instrument made a new 100 day high in the last 5 days;  OR
#     50 day moving average is above the 200 day moving average; OR
#     Price is 10 ATR higher than it was 2 months ago…
#     Entry:
#     Positive directional movement indicator crosses above negative directional movement indicator; OR
#     Short term moving average crosses above the medium term moving average; OR
#     Price crosses above the parabolic SAR indicator…
#     Exit:
#     100 day low channel breakout; OR
#     Chandelier exit; OR
#     Price crosses below the 200 day moving average …
#     Initial stops:
#     Lowest low of the last 10 days; OR
#     Yesterday’s close minus three times the average true range; OR
#     Yesterday’s close minus 1 standard deviation of daily price movements…
