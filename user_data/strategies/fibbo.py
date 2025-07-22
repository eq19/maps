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
from freqtrade.exchange import Exchange
from freqtrade.persistence import Trade
from freqtrade.configuration import Configuration
from freqtrade.exceptions import OperationalException

# --------------------------------
# Add your lib to import here
import time
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


# Define indicator sets (could also come from the JSON if needed)
buy_indicators = ["BB", "ATR", "TTM", "VWAP", "MACD", "DEMA", "FIBBO", "STOCHRSI"]
sell_indicators = ["ATR", "TTM", "MACD", "FIBBO", "STOCHRSI"]
logger = logging.getLogger(__name__)

# ✅ 1. Call every patches once at module level
def patch_indodax_create_order():
    """Monkey-patch Exchange.create_order() to delay return for Indodax and ensure fill."""
    if hasattr(Exchange.create_order, '_is_patched'):
        return  # Avoid multiple patching

    original_create_order = Exchange.create_order

    def patched_create_order(self, pair, order_type, side, amount, rate, **kwargs):
        order = original_create_order(self, pair, order_type, side, amount, rate, **kwargs)

        if self.exchange.id == "indodax":
            import time
            # 💤 Wait to allow Indodax to fully fill the order
            time.sleep(30)

            # 🛠 Optional: force-refresh order info if available
            try:
                refreshed_order = self.exchange.fetch_order(order['id'], symbol=pair)
                order.update(refreshed_order)
            except Exception as e:
                logger.warning(f"Failed to refresh order status for {order['id']}: {e}")

        return order

    Exchange.create_order = patched_create_order
    Exchange.create_order._is_patched = True

def patch_indodax_cancel_order():
    """Monkey-patch Exchange.cancel_order() to handle Indodax's side requirement."""
    if hasattr(Exchange.cancel_order, '_is_patched'):
        return  # Avoid double-patching

    original_cancel_order = Exchange.cancel_order

    def patched_cancel_order(self, order_id: str, symbol: str, *args, **kwargs):
        if self.exchange.id == "indodax":
            trade = Trade.get_open_order_trades(order_id).first()
            if not trade or not trade.orders:
                raise OperationalException(f"Cannot cancel order {order_id} - missing trade or order history")

            side = trade.orders[-1].side
            params = kwargs.get('params', {})
            params['side'] = side
            kwargs['params'] = params

        return original_cancel_order(self, order_id, symbol, *args, **kwargs)

    Exchange.cancel_order = patched_cancel_order
    Exchange.cancel_order._is_patched = True

# Check if dry_run is False before patching
if not Configuration.get_config().get('dry_run', False):
    patch_indodax_create_order()
    patch_indodax_cancel_order()

# ✅ 2. Recursively find the first occurrence of the 'span' key
def find_span(obj):
    if isinstance(obj, dict):
        if "span" in obj:
            return obj["span"]
        for value in obj.values():
            result = find_span(value)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_span(item)
            if result is not None:
                return result
    return None

# Load JSON and extract 'span'
param_file = Path(__file__).parent/'hyperopt_params.json'
logger.info(f"Load params file: {param_file}")
try:
    with open(param_file) as file:
        span = find_span(json.load(file))
except FileNotFoundError:
    logger.warning(f"Params file not found: {param_file}")
except json.JSONDecodeError:
    logger.error(f"Invalid JSON in params file: {param_file}")
except Exception as e:
    logger.error(f"Error loading params: {str(e)}")

# ✅ 3. Helper function to construct parameters
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
        return CategoricalParameter(
            categories=config['choices'],
            default=default,
            space=space,
            optimize=optimize
        )
    else:
        raise ValueError(f"Unknown parameter type: {param_type}")

# ✅ 4. Generate permutations and insert them into the span config before using them
def indicator_permutations(profiles, max_indicators=1, include_none=False):
    profile_permutations = set()
    if include_none:
        profile_permutations.add("NONE")
    if max_indicators == 1:
        profile_permutations.update(profiles)
        return profile_permutations
    for i in range(1, len(profiles) + 1):
        for perm in permutations(profiles, i):
            if len(perm) <= max_indicators:
                profile_permutations.add(", ".join(sorted(perm)))
    return profile_permutations

# Insert computed categories into the JSON-loaded span
span["buy"]["buy_additional_indicator"]["choices"] = sorted(
    indicator_permutations(buy_indicators, max_indicators=2, include_none=True)
)
span["sell"]["sell_additional_indicator"]["choices"] = sorted(
    indicator_permutations(sell_indicators, max_indicators=2, include_none=True)
)

# Preload strategy attributes
strategy_attrs = {}
for section, keys in span.items():
    for key in keys:
        strategy_attrs[key] = get_param_config(span, section, key)

# 👇 Now define your strategy below
class fibbo(IStrategy):

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Optimal timeframe for the strategy.
    timeframe = "1m"
    informative_timeframe = "15m"

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

    order_time_in_force = {
        "entry": "GTC",
        "exit": "GTC"
    }

    # See the config
    trailing_stop = True
    use_exit_signal = True
    exit_profit_only = False
    use_custom_stoploss = True
    process_only_new_candles = True
    ignore_roi_if_entry_signal = False
    position_adjustment_enable = False
    #max_entry_position_adjustment = 2

    # Plot config
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


    def __init__(self, config: dict) -> None:
        super().__init__(config)

        # Override settings ONLY during hyperopt
        if config.get('runmode') == 'hyperopt':
            self.trailing_stop = True
            self.use_exit_signal = False
            self.use_custom_stoploss = False
            self.minimal_roi = {"0": 100}

        # Optional: update dynamic ROI logic
        if hasattr(self, 'update_roi'):
            self.update_roi()

        # Optional: apply hyperopt value of max_open_trades to config
        if hasattr(self, 'max_open_trades') and self.max_open_trades.value != -1:
            self.config['max_open_trades'] = self.max_open_trades.value

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

        # Disable protections during hyperopt if spaces contain 'all' or 'protection'
        if hasattr(self, 'config'):
            config: Configuration = self.config
            if config.get('runmode') == 'hyperopt':
                spaces = config.get('spaces', [])
                if 'all' in spaces or 'protection' in spaces:
                    return prot

        # Cooldown period to prevent over-trading
        prot.append({
            "method": "CooldownPeriod",
            "stop_duration_candles": self.cooldown_lookback.value
        })

        # Stoploss guard to limit losses
        if self.use_stop_protection.value:
            prot.append({
                "method": "StoplossGuard",
                "lookback_period_candles": self.lookback_period_candles.value,
                "stop_duration_candles": self.stop_duration_candles.value,
                "trade_limit": self.trade_limit.value,
                "only_per_pair": False
            })

        # Max drawdown guard
        if self.use_max_drawdown_protection.value:
            prot.append({
                "method": "MaxDrawdown",
                "lookback_period_candles": self.lookback_period_candles.value,
                "stop_duration_candles": self.stop_duration_candles.value,
                "trade_limit": self.max_drawdown_trade_limit.value,
                "max_allowed_drawdown": 0.2,
                "only_per_pair": False
            })

        # Low profit pairs guard
        if self.use_low_profit.value:
            prot.append({
                "method": "LowProfitPairs",
                "lookback_period_candles": self.lookback_period_candles.value,
                "stop_duration": self.stop_duration_candles.value,
                "trade_limit": self.low_profit_trade_limit.value,
                "required_profit": 0.02,
                "only_per_pair": False
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
    
        # Assign the desired timeframe for each pair using self.informative_timeframe
        informative_pairs = [(pair, self.informative_timeframe) for pair in pairs]

        # Add any additional fixed pairs using self.timeframe and self.informative_timeframe
        #informative_pairs += [("USDT/IDR", self.timeframe), ("USDT/IDR", self.informative_timeframe)]

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
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        # STOCHRSI (Missaligned Issue)
        #stoch_rsi = ta.STOCHRSI(dataframe)
        #dataframe['fastd_rsi'] = stoch_rsi['fastd']
        #dataframe['fastk_rsi'] = stoch_rsi['fastk']
        stoch_rsi = (dataframe['rsi'] - dataframe['rsi'].rolling(self.period.value).min()) / (dataframe['rsi'].rolling(self.period.value).max() - dataframe['rsi'].rolling(self.period.value).min())
        dataframe['fastk_rsi'] = (stoch_rsi * 100).rolling(self.smoothK.value).mean()
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
        for period in span["buy"]["buy_slow_ema"]["choices"]:
            dataframe[f'ema{period}'] = ta.EMA(dataframe, timeperiod=int(period))
        for period in span["buy"]["buy_fast_dema"]["choices"]:
            dataframe[f'dema{period}'] = ta.DEMA(dataframe, timeperiod=int(period))

        # Swing high/low for Fibonacci levels
        dataframe['swing_high'] = dataframe['high'].rolling(self.buy_swing_period.value).max()
        dataframe['swing_low'] = dataframe['low'].rolling(self.buy_swing_period.value).min()
        swing_range = dataframe['swing_high'] - dataframe['swing_low']

        dataframe['fib_236'] = dataframe['swing_high'] - swing_range * 0.236
        dataframe['fib_382'] = dataframe['swing_high'] - swing_range * 0.382
        dataframe['fib_618'] = dataframe['swing_high'] - swing_range * 0.618
        dataframe['fib_786'] = dataframe['swing_high'] - swing_range * 0.786

        # ---- Fetch and merge informative timeframe ----
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

        for period in span["buy"]["buy_slow_ema"]["choices"]:
            informative[f'ema{period}'] = ta.EMA(informative, timeperiod=int(period))
        for period in span["buy"]["buy_fast_dema"]["choices"]:
            informative[f'dema{period}'] = ta.DEMA(informative, timeperiod=int(period))

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
        long_conditions = []

        ### Momentum Indicators ###
        RSI = (dataframe['rsi'] < self.buy_rsi.value)
        VWAP = (dataframe['close'] > dataframe['vwap'])
        ATR = (dataframe['atr'] > dataframe['atr'].shift(1))
        BB = (dataframe['close'] <= dataframe['bb_lowerband'])
        MACD = (dataframe['macd'] > dataframe['macdsignal'])  # FIXED: Bullish crossover
        STOCHRSI = (
            (dataframe['fastk_rsi'] > dataframe['fastd_rsi']) &
            (dataframe['fastk_rsi'] < self.buy_stoch_osc.value)
        )
        DEMA = (
            dataframe[f"dema{self.buy_fast_dema.value}"] >
            dataframe[f"ema{self.buy_slow_ema.value}_{self.informative_timeframe}"]
        )
        FIBBO = (
            ((dataframe['close'].shift(1) < dataframe['fib_618']) & (dataframe['close'] > dataframe['fib_618'])) |
            ((dataframe['close'].shift(1) < dataframe['fib_786']) & (dataframe['close'] > dataframe['fib_786']))
        )

        # Always include RSI
        long_conditions.append(RSI)

        if "BB" in self.buy_additional_indicator.value:
            long_conditions.append(BB)
        if "ATR" in self.buy_additional_indicator.value:
            long_conditions.append(ATR)
        if "VWAP" in self.buy_additional_indicator.value:
            long_conditions.append(VWAP)
        if "MACD" in self.buy_additional_indicator.value:
            long_conditions.append(MACD)
        if "DEMA" in self.buy_additional_indicator.value:
            long_conditions.append(DEMA)
        if "FIBBO" in self.buy_additional_indicator.value:
            long_conditions.append(FIBBO)
        if "STOCHRSI" in self.buy_additional_indicator.value:
            long_conditions.append(STOCHRSI)

        # TTM Squeeze
        if "TTM" in self.buy_additional_indicator.value:
            squeeze_on = dataframe['squeeze_on']
            momentum_positive = dataframe['momentum_hist'] > 0
            long_conditions.append(squeeze_on & momentum_positive)

        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, long_conditions),
                'enter_long'
            ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        long_conditions = []

        ### Momentum Indicators ###
        RSI = (dataframe['rsi'] >= self.sell_rsi.value)
        ATR = (dataframe['atr'] < dataframe['atr'].shift(1))  # FIXED bug
        MACD = (dataframe['macd'] < dataframe['macdsignal'])  # FIXED: Bearish crossover
        FIBBO = (dataframe['close'] >= dataframe['fib_236'])  # Optional fib exit
        STOCHRSI = (
            (dataframe['fastk_rsi'] < dataframe['fastd_rsi']) &
            (dataframe['fastk_rsi'] > self.sell_stoch_osc.value)
        )

        # Always include RSI
        long_conditions.append(RSI)

        if "ATR" in self.sell_additional_indicator.value:
            long_conditions.append(ATR)
        if "MACD" in self.sell_additional_indicator.value:
            long_conditions.append(MACD)
        if "FIBBO" in self.sell_additional_indicator.value:
            long_conditions.append(FIBBO)
        if "STOCHRSI" in self.sell_additional_indicator.value:
            long_conditions.append(STOCHRSI)

        # TTM Squeeze
        if "TTM" in self.sell_additional_indicator.value:
            squeeze_off = dataframe['squeeze_off']
            momentum_negative = dataframe['momentum_hist'] < 0
            long_conditions.append(squeeze_off & momentum_negative)

        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, long_conditions),
                'exit_long'
            ] = 1

        return dataframe

# Inject hyperopt parameters AFTER class definition
for key, value in strategy_attrs.items():
    setattr(fibbo, key, value)
