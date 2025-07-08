# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from typing import Optional, Union

from freqtrade.strategy import (
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IStrategy,
    IntParameter,
    merge_informative_pair
)
from freqtrade.persistence import Trade

# --------------------------------
# Add your lib to import here
import random
from itertools import product, chain
from datetime import datetime
from functools import reduce
import talib.abstract as ta
import pandas_ta as pd_ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from itertools import permutations

random.seed(18)
# random.seed(datetime.now().timestamp())

def indicator_permutations(profiles, max_indicators=1, include_none=True):
    profile_permutations = set()
    if include_none:
        profile_permutations.add("NONE")

    if max_indicators == 1:
        profile_permutations.update(profiles)
        return profile_permutations

    for i in range(1, len(profiles)+1):
        for perm in permutations(profiles, i):
            if len(perm) <= max_indicators:
                profile_permutations.add(", ".join(sorted(list(perm))))
    return profile_permutations


class AwesomeCombinationStrategy(IStrategy):

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Optimal timeframe for the strategy.
    timeframe = "15m"
    # informative_timeframe = '15m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperoptable parameters
    macd_profiles = {
        "5m": {
            "fast": 6,
            "slow": 13,
            "signal": 4
        },
        "15m": {
            "fast": 8,
            "slow": 17,
            "signal": 9
        },
        "1h": {
            "fast": 12,
            "slow": 26,
            "signal": 9
        },
    }

    buy_profiles    = ["MACD", "BB", "STOCH_OSC", "EMA", "TTM"]
    sell_profiles   = ["MACD", "STOCH_OSC", "TTM"]
    
    buy_additional_indicators   = indicator_permutations(buy_profiles, max_indicators=2)
    sell_additional_indicators  = indicator_permutations(sell_profiles, max_indicators=2)

    buy_rsi                     = IntParameter(10, 45, default=25, optimize=True)
    # buy_stoch_osc               = IntParameter(0, 30, default=10, optimize=True)
    buy_additional_indicator    = CategoricalParameter(buy_additional_indicators, default="NONE", optimize=True)
    

    sell_rsi                    = IntParameter(70, 100, default=89, optimize=True)
    # sell_stoch_osc              = IntParameter(70, 100, default=77, optimize=True)
    sell_additional_indicator   = CategoricalParameter(sell_additional_indicators, default="NONE", optimize=True)

    # fast_emas = ["3", "5", "9", "10", "21", "50"]
    # slow_emas = ["50", "100", "200"]
    # buy_fast_ema = CategoricalParameter(fast_emas, default="10", optimize=True)
    # buy_slow_ema = CategoricalParameter(slow_emas, default="50", optimize=True)

    # Define the parameter spaces
    cooldown_lookback           = IntParameter(2, 48, default=30, space="protection", optimize=True)
    low_profit_trade_limit      = IntParameter(2, 10, default=9, space="protection", optimize=True)
    max_drawdown_trade_limit    = IntParameter(2, 10, default=3, space="protection", optimize=True)
    stop_duration               = IntParameter(12, 200, default=43, space="protection", optimize=True)
    trade_limit                 = IntParameter(2, 10, default=5, space="protection", optimize=True)
    use_low_profit              = BooleanParameter(default=False, space="protection", optimize=True)
    use_max_drawdown_protection = BooleanParameter(default=False, space="protection", optimize=True)
    use_stop_protection         = BooleanParameter(default=True, space="protection", optimize=True)

    @property
    def protections(self):
        prot = []

        # Cooldown period to prevent over-trading
        prot.append({
            "method": "CooldownPeriod",
            "stop_duration_candles": self.cooldown_lookback.value
        })

        # Stoploss guard to limit losses
        if self.use_stop_protection.value:
            prot.append({
                "method": "StoplossGuard",
                "lookback_period_candles": 48,  # 24 hours * 4 quarters per hour (15min candles)
                "trade_limit": self.trade_limit.value,
                "stop_duration_candles": self.stop_duration.value,
                "only_per_pair": False
            })

        # Max drawdown guard to prevent trading after excessive losses
        if self.use_max_drawdown_protection.value:
            prot.append({
                "method": "MaxDrawdown",
                "lookback_period_candles": 48,  # 24 hours * 4 quarters per hour (15min candles)
                "trade_limit": self.max_drawdown_trade_limit.value,
                "max_allowed_drawdown": 0.2,  # 20% drawdown
                "stop_duration_candles": self.stop_duration.value,
                "only_per_pair": False
            })

        if self.use_low_profit.value:
            # Low profit pairs protection
            prot.append({
                "method": "LowProfitPairs",
                "lookback_period_candles": 48,
                "trade_limit": self.low_profit_trade_limit.value,
                "stop_duration": self.stop_duration.value,
                "required_profit": 0.02,
                "only_per_pair": False,
            })

        return prot

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "0": 0.298,
        "115": 0.144,
        "280": 0.055,
        "507": 0
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.327

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.037
    trailing_only_offset_is_reached = False


    # ATR Stoploss Multiplier
    atr_stoploss_multiplier = IntParameter(1, 3, default=1.5, space='stoploss', optimize=True)

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Optional order type mapping.
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force.
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    plot_config = {
        "main_plot": {
            "tema": {},
            "sar": {"color": "white"},
        },
        "subplots": {
            "MACD": {
                "macd": {"color": "blue"},
                "macdsignal": {"color": "orange"},
            },
            "RSI": {
                "rsi": {"color": "red"},
            },
        },
    }



    def custom_params(self, pair: str, param: str):
        return self.custom_pair_params.get(pair, {}).get(param, getattr(self, param).value)

    def ttm_squeeze(self, dataframe: DataFrame, bollinger_period: int = 20, keltner_period: int = 20, momentum_period: int = 12) -> DataFrame:
        # Calculate Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=bollinger_period, stds=2)

        # Calculate Keltner Channels
        keltner = qtpylib.keltner_channel(dataframe, window=keltner_period)

        # Calculate Momentum Histogram
        momentum_hist = dataframe['close'] - dataframe['close'].shift(momentum_period)

        # Determine squeeze conditions
        squeeze_on = (bollinger['lower'] > keltner["lower"]) & (bollinger['upper'] < keltner["upper"])
        squeeze_off = (bollinger['lower'] < keltner["lower"]) & (bollinger['upper'] > keltner["upper"])

        dataframe['squeeze_on'] = squeeze_on
        dataframe['squeeze_off'] = squeeze_off
        dataframe['momentum_hist'] = momentum_hist

        return dataframe
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Stochastic RSI
        stoch_rsi = ta.STOCHRSI(dataframe)
        dataframe['fastd_rsi'] = stoch_rsi['fastd']
        dataframe['fastk_rsi'] = stoch_rsi['fastk']

        # Calculate ATR with a 14-period setting and rolling mean of the True Range
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # Get the 14 day rsi
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # EMA - Exponential Moving Average
        dataframe['ema3']   = ta.EMA(dataframe, timeperiod=3)
        dataframe['ema5']   = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema9']   = ta.EMA(dataframe, timeperiod=9)
        dataframe['ema10']  = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema21']  = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema50']  = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # MACD
        macd = ta.MACD(dataframe, slow=self.macd_profiles[self.timeframe]["slow"], fast=self.macd_profiles[self.timeframe]["fast"], signal=self.macd_profiles[self.timeframe]["signal"])
        dataframe["macd"]       = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"]   = macd["macdhist"]

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband']   = bollinger['lower']
        dataframe['bb_middleband']  = bollinger['mid']
        dataframe['bb_upperband']   = bollinger['upper']
        
        # VWAP
        # dataframe['vwap'] = qtpylib.vwap(dataframe)
        dataframe['vwap'] = (((dataframe['high'] + dataframe['low'] + dataframe['close']) / 3) * dataframe['volume']).cumsum() / dataframe['volume'].cumsum()

        # TTM Squeeze
        dataframe = self.ttm_squeeze(dataframe)

        return dataframe


    use_custom_stoploss = True
    def custom_stoploss(self, pair: str, trade: Trade, current_time: 'datetime', current_rate: float, current_profit: float, **kwargs) -> float:
        # Calculate ATR-based stoploss
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        atr_stoploss = last_candle['atr'] * self.atr_stoploss_multiplier.value
        
        # Set stoploss based on ATR
        stoploss_price = trade.open_rate - atr_stoploss
        if current_rate < stoploss_price:
            return -1  # stop out
        return 1  # continue

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
       # Define the buy conditions
        long_conditions = []
        
        ### Momentum Indicators ###
        RSI         = (dataframe['rsi'] < self.buy_rsi.value)
        MACD        = (dataframe["macd"] < dataframe["macdsignal"])
        VWAP        = (dataframe['close'] > dataframe['vwap'])
        STOCK_OSC   = (dataframe['fastk_rsi'] > dataframe['fastd_rsi']) #& (dataframe['fastk_rsi'] < self.buy_stoch_osc.value)
        BB          = (dataframe["close"] <= dataframe["bb_lowerband"]) #& (dataframe["close"].shift(1) < dataframe["close"])
        EMA         = (dataframe["ema10"] > dataframe["ema50"])
        # EMA         = (dataframe[f"ema{self.buy_fast_ema.value}"] > dataframe[f"ema{self.buy_slow_ema.value}"])
        
        long_conditions.append(RSI)
        long_conditions.append(VWAP)

        if "MACD" in self.buy_additional_indicator.value:
            long_conditions.append(MACD)
        if "STOCK_OSC" in self.buy_additional_indicator.value:
            long_conditions.append(STOCK_OSC)
        if "BB" in self.buy_additional_indicator.value:
            long_conditions.append(BB)
        if "EMA" in self.buy_additional_indicator.value:
            long_conditions.append(EMA)
        

        # TTM Squeeze entry condition
        squeeze_on = dataframe['squeeze_on']
        momentum_positive = dataframe['momentum_hist'] > 0
        if "TTM" in self.buy_additional_indicator.value:
            long_conditions.append(squeeze_on & momentum_positive)

        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, long_conditions),
                'enter_long'] = 1

        return dataframe


    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Define the sell conditions
        long_conditions = []

        ### Momentum Indicators ###
        RSI = (dataframe['rsi'] >= self.sell_rsi.value)
        MACD = (dataframe["macd"] >= dataframe["macdsignal"])
        STOCK_OSC = (dataframe['fastk_rsi'] <= dataframe['fastd_rsi']) #& (dataframe['fastk_rsi'] >= self.sell_stoch_osc.value)

        long_conditions.append(RSI)

        if "MACD" in self.sell_additional_indicator.value:
            long_conditions.append(MACD)
        if "STOCK_OSC" in self.sell_additional_indicator.value:
            long_conditions.append(STOCK_OSC)

        # TTM Squeeze exit condition
        squeeze_off = dataframe['squeeze_off']
        momentum_negative = dataframe['momentum_hist'] < 0
        if "TTM" in self.sell_additional_indicator.value:
            long_conditions.append(squeeze_off & momentum_negative)
            
        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, long_conditions),
                'exit_long'] = 1
            
        return dataframe
