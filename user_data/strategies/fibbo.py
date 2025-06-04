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
import json
import random
import logging
from itertools import product, chain
from datetime import datetime
from functools import reduce
from pathlib import Path
import talib.abstract as ta
import pandas_ta as pd_ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
from itertools import permutations


logger = logging.getLogger(__name__)

# ✅ 1. Load span config from JSON
with open('user_data/config_examples/config_params.example.json') as f:
    span = json.load(f)

# ✅ 2. Helper function to construct parameters
def get_param_config(span: dict, space: str, name: str):
    config = span[space][name]
    param_type = config["type"]
    optimize = config.get("optimize", False)
    default = config["default"]

    if param_type == "IntParameter":
        return IntParameter(
            low=config["low"],
            high=config["high"],
            default=default,
            space=space,
            optimize=optimize
        )
    elif param_type == "DecimalParameter":
        return DecimalParameter(
            low=config['low'],
            high=config['high'],
            default=default,
            decimals=config.get('decimals', 3),
            space=space,
            optimize=optimize
        )
    elif param_type == "BooleanParameter":
        return BooleanParameter(
            default=default,
            space=space,
            optimize=optimize
        )
    elif param_type == "CategoricalParameter":
        choices = config["choices"]
        if isinstance(choices, str):
            # Replace placeholder names like "slow_emas" with actual list
            # You must define these somewhere
            if choices == "slow_emas":
                choices = [21, 34, 55]
            elif choices == "fast_demas":
                choices = [8, 13, 21]
        return CategoricalParameter(
            choices=choices,
            default=default,
            space=space,
            optimize=optimize
        )
    else:
        raise ValueError(f"Unknown parameter type: {param_type}")

def indicator_permutations(profiles, max_indicators=1, include_none=False):
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


class fibbo(IStrategy):
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Optimal timeframe for the strategy.
    timeframe = "1m"
    informative_timeframe = "15m"

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Class variable to hold parameters
    _param_config = None
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

    # Hyperoptable parameters
    stoploss = -0.1
    minimal_roi = {
        "0": 0.298,
        "115": 0.144,
        "280": 0.055,
        "507": 0
    }

    macd_profiles = {
        "1m": {
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

    # See the config
    trailing_stop = True
    use_exit_signal = True
    exit_profit_only = False
    use_custom_stoploss = True
    process_only_new_candles = True
    ignore_roi_if_entry_signal = False

    # Optional
    fast_demas                      = [5, 8, 13, 21]
    slow_emas                       = [34, 55, 89, 144]
    order_time_in_force             = {"entry": "GTC", "exit": "GTC"}
    sell_indicators                 = ["MACD", "TTM", "FIBBO", "STOCHRSI"]
    buy_indicators                  = ["BB", "MACD", "TTM", "FIBBO", "STOCHRSI"]

    # Indicator permutations
    buy_additional_indicators       = indicator_permutations(buy_indicators, max_indicators=2)
    sell_additional_indicators      = indicator_permutations(sell_indicators, max_indicators=2)
    buy_additional_indicator        = CategoricalParameter(buy_additional_indicators, default="NONE", optimize=True)
    sell_additional_indicator       = CategoricalParameter(sell_additional_indicators, default="NONE", optimize=True)
    
    # Hyperoptable buy parameters
    period = get_param_config(span, "buy", "period")
    smoothD = get_param_config(span, "buy", "smoothD")
    SmoothK = get_param_config(span, "buy", "SmoothK")
    buy_rsi = get_param_config(span, "buy", "buy_rsi")
    buy_stoch_osc = get_param_config(span, "buy", "buy_stoch_osc")
    buy_swing_period = get_param_config(span, "buy", "buy_swing_period")
    buy_slow_ema                    = CategoricalParameter(slow_emas, default=34, space="buy", optimize=False)
    buy_fast_dema                   = CategoricalParameter(fast_demas, default=13, space="buy", optimize=False)
    buy_fib_level                   = CategoricalParameter(["0.236", "0.382", "0.618", "0.786"], default="0.618", space='buy', optimize=False)

    # Hyperoptable sell parameters
    sell_rsi = get_param_config(span, "sell", "sell_rsi")
    sell_stoch_osc = get_param_config(span, "sell", "sell_stoch_osc")
    sell_rsi_threshold = get_param_config(span, "sell", "sell_rsi_threshold")
    sell_fib_level                  = CategoricalParameter(["0.236", "0.382", "0.618", "0.786"], default="0.786", space='sell', optimize=False)

    # Protection
    cooldown_lookback = get_param_config(span, "protection", "cooldown_lookback")
    low_profit_trade_limit = get_param_config(span, "protection", "low_profit_trade_limit")
    max_drawdown_trade_limit = get_param_config(span, "protection", "max_drawdown_trade_limit")
    stop_duration = get_param_config(span, "protection", "stop_duration")
    trade_limit = get_param_config(span, "protection", "trade_limit")
    use_low_profit = get_param_config(span, "protection", "use_low_profit")
    use_max_drawdown_protection = get_param_config(span, "protection", "use_max_drawdown_protection")
    use_stop_protection = get_param_config(span, "protection", "use_stop_protection")

    # Hyperoptable ROI parameters - keep these as class variables
    roi_t1 = get_param_config(span, "roi", "roi_t1")
    roi_t2 = get_param_config(span, "roi", "roi_t2")
    roi_t3 = get_param_config(span, "roi", "roi_t3")
    roi_p1 = get_param_config(span, "roi", "roi_p1")
    roi_p2 = get_param_config(span, "roi", "roi_p2")
    roi_p3 = get_param_config(span, "roi", "roi_p3")

    # Stoploss (Singular Optimation)
    atr_stoploss_multiplier         = DecimalParameter(1, 3, default=1.5, space='stoploss', optimize=True)

    # Trailing stop
    trailing_stop_positive          = DecimalParameter(0.01, 0.50, default=0.236, decimals=3, space='trailing', optimize=True)
    trailing_stop_positive_offset   = DecimalParameter(0.50, 1.00, default=0.786, decimals=3, space='trailing', optimize=True)
    trailing_only_offset_is_reached = BooleanParameter(default=True, space='trailing', optimize=True)

    # Trades (Singular Optimation)
    max_open_trades_param           = IntParameter(1, 10, default=2, space='trade', optimize=True)


    def __init__(self, config: dict) -> None:
        # Initialize parent class first
        super().__init__(config)
    
        # Load parameters (if using lazy-loading)
        if hasattr(self, 'load_params'):
            self.load_params()
    
        # Update ROI dynamically (if needed)
        if hasattr(self, 'update_roi'):
            self.update_roi()
    
        # Apply max_open_trades optimization
        if hasattr(self, 'max_open_trades') and self.max_open_trades.value != -1:
            self.config['max_open_trades'] = self.max_open_trades_param.value

    @classmethod
    def load_params(cls):
        """Lazy-load parameters when first needed"""
        if cls._param_config is None:
            param_file = Path(__file__).parent/'hyperopt_params.json'
            try:
                with open(param_file) as file:
                    cls._param_config = json.load(file)
                    logger.info(f"Load params file: {param_file}")
            except FileNotFoundError:
                logger.warning(f"Params file not found: {param_file}")
                cls._param_config = {}
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in params file: {param_file}")
                cls._param_config = {}
            except Exception as e:
                logger.error(f"Error loading params: {str(e)}")
                cls._param_config = {}
    
    def update_roi(self):
        """Update ROI based on current parameter values"""
        self.minimal_roi = {
            "0": float(self.roi_p1.value),
            str(int(self.roi_t1.value)): float(self.roi_p2.value),
            str(int(self.roi_t2.value)): float(self.roi_p3.value),
            str(int(self.roi_t3.value)): 0
        }

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

    # ATR Stoploss Multiplier
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

    def informative_pairs(self):
        # Get all trading pairs from the whitelist
        pairs = self.dp.current_whitelist()
    
        # Assign the desired timeframe for each pair
        informative_pairs = [(pair, '15m') for pair in pairs]

        # Add any additional fixed pairs
        informative_pairs += [("USDT/IDR", "1m"), ("USDT/IDR", "15m")]

        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI 
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # VWAP
        # dataframe['vwap'] = qtpylib.vwap(dataframe)
        dataframe['vwap'] = (((dataframe['high'] + dataframe['low'] + dataframe['close']) / 3) * dataframe['volume']).cumsum() / dataframe['volume'].cumsum()

        # TTM Squeeze
        dataframe = self.ttm_squeeze(dataframe)
        dataframe['volume_mean'] = dataframe['volume'].rolling(20).mean()

        # ATR (Volatility)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=int(self.period.value))

        # STOCHRSI (Missaligned Issue)
        #stoch_rsi = ta.STOCHRSI(dataframe)
        #dataframe['fastd_rsi'] = stoch_rsi['fastd']
        #dataframe['fastk_rsi'] = stoch_rsi['fastk']
        stoch_rsi = (dataframe['rsi'] - dataframe['rsi'].rolling(self.period.value).min()) / (dataframe['rsi'].rolling(self.period.value).max() - dataframe['rsi'].rolling(self.period.value).min())
        dataframe['fastk_rsi'] = (stoch_rsi * 100).rolling(self.SmoothK.value).mean()
        dataframe['fastd_rsi'] = dataframe['fastk_rsi'].rolling(self.smoothD.value).mean()

        # MACD (See Hyperopt Table)
        macd = ta.MACD(dataframe, fastperiod=6, slowperiod=13, signalperiod=4)
        dataframe['macd'] = macd['macd']
        dataframe['macdhist'] = macd['macdhist']
        dataframe['macdsignal'] = macd['macdsignal']

        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        dataframe['bb_upperband'] = bollinger['upperband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_lowerband'] = bollinger['lowerband']

        # EMA & DEMA
        for period in self.slow_emas:
            dataframe[f'ema{period}'] = ta.EMA(dataframe, timeperiod=period)
        for period in self.fast_demas:
            dataframe[f'dema{period}'] = ta.DEMA(dataframe, timeperiod=period)

        # Swing high/low for Fibonacci levels
        dataframe['swing_high'] = dataframe['high'].rolling(self.buy_swing_period.value).max()
        dataframe['swing_low'] = dataframe['low'].rolling(self.buy_swing_period.value).min()
        swing_range = dataframe['swing_high'] - dataframe['swing_low']

        dataframe['fib_236'] = dataframe['swing_high'] - swing_range * 0.236
        dataframe['fib_382'] = dataframe['swing_high'] - swing_range * 0.382
        dataframe['fib_618'] = dataframe['swing_high'] - swing_range * 0.618
        dataframe['fib_786'] = dataframe['swing_high'] - swing_range * 0.786

        # ---- Fetch and merge informative timeframe (15m) ----
        logger.debug("Informative pairs data: %s", self.informative_pairs)
        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

        if informative is None or 'close' not in informative.columns:
            logger.error("Missing 'close' column in informative DataFrame for pair: %s", metadata['pair'])
            return dataframe  # Return original dataframe to prevent crashing
    
        # Now it's safe to use 'close'
        informative['rsi'] = ta.RSI(informative, timeperiod=14)
        informative['atr'] = ta.ATR(informative, timeperiod=14)

        macd_inf = ta.MACD(informative, fastperiod=12, slowperiod=26, signalperiod=9)
        informative['macd'] = macd_inf['macd']
        informative['macdhist'] = macd_inf['macdhist']
        informative['macdsignal'] = macd_inf['macdsignal']

        for period in self.slow_emas:
            informative[f'ema{period}'] = ta.EMA(informative, timeperiod=period)
        for period in self.fast_demas:
            informative[f'dema{period}'] = ta.DEMA(informative, timeperiod=period)

        # Merge informative pair data into main dataframe
        merged_dataframe = merge_informative_pair(dataframe, informative, self.timeframe, self.informative_timeframe, ffill=True)

        # Check for length mismatch
        if len(merged_dataframe) != len(dataframe):
            logger.warning(
                f"Dataframe length mismatch after merging informative pair: {metadata['pair']} "
                f"(before: {len(dataframe)}, after: {len(merged_dataframe)})"
            )

        return merged_dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Define the buy conditions
        long_conditions = []

        ### Momentum Indicators ###
        RSI          = (dataframe['rsi'] < self.buy_rsi.value)
        ATR          = (dataframe['atr'] > dataframe['atr'].shift(1))
        VWAP         = (dataframe['close'] > dataframe['vwap'])
        MACD         = (dataframe["macd"] < dataframe["macdsignal"])
        DEMA         = (dataframe[f"dema{self.buy_fast_dema.value}"] > dataframe[f"ema{self.buy_slow_ema.value}_15m"])
        FIBBO        = (dataframe['close'].shift(1) < dataframe['fib_618']) & (dataframe['close'] > dataframe['fib_618'])
        BB           = (dataframe["close"] <= dataframe["bb_lowerband"]) #& (dataframe["close"].shift(1) < dataframe["close"])
        STOCHRSI     = (dataframe['fastk_rsi'] > dataframe['fastd_rsi']) & (dataframe['fastk_rsi'] < self.buy_stoch_osc.value)

        long_conditions.append(RSI)

        if "BB" in self.buy_additional_indicator.value:
            long_conditions.append(BB)
        if "ATR" in self.buy_additional_indicator.value:
            long_conditions.append(ATR)
        if "DEMA" in self.buy_additional_indicator.value:
            long_conditions.append(DEMA)
        if "VWAP" in self.buy_additional_indicator.value:
            long_conditions.append(VWAP)
        if "MACD" in self.buy_additional_indicator.value:
            long_conditions.append(MACD)
        if "FIBBO" in self.buy_additional_indicator.value:
            long_conditions.append(FIBBO)
        if "STOCHRSI" in self.buy_additional_indicator.value:
            long_conditions.append(STOCHRSI)
  
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
        RSI          = (dataframe['rsi'] >= self.sell_rsi.value)
        ATR          = (dataframe['atr'] < dataframe['atr']).shift(1)
        MACD         = (dataframe["macd"] >= dataframe["macdsignal"])
        STOCHRSI     = (dataframe['fastk_rsi'] < dataframe['fastd_rsi']) & (dataframe['fastk_rsi'] > self.sell_stoch_osc.value)

        long_conditions.append(RSI)

        if "ATR" in self.sell_additional_indicator.value:
            long_conditions.append(ATR)
        if "MACD" in self.sell_additional_indicator.value:
            long_conditions.append(MACD)
        if "STOCHRSI" in self.sell_additional_indicator.value:
            long_conditions.append(STOCHRSI)

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
