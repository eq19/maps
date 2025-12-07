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
from freqtrade.persistence import Trade, Order
from freqtrade.configuration import Configuration
from freqtrade.exceptions import OperationalException

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
from utils.indodax_patch import *


# Define indicator sets (could also come from the JSON if needed)
buy_indicators = ["BB", "ATR", "TTM", "VWAP", "MACD", "DEMA", "FIBBO", "STOCHRSI"]
sell_indicators = ["ATR", "TTM", "MACD", "FIBBO", "STOCHRSI"]
logger = logging.getLogger(__name__)

# ✅ 1. Recursively find the first occurrence of the 'span' key
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
        return CategoricalParameter(
            categories=config['choices'],
            default=default,
            space=space,
            optimize=optimize
        )
    else:
        raise ValueError(f"Unknown parameter type: {param_type}")

# ✅ 3. Generate permutations and insert them into the span config before using them
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

# 👇 Now define the strategy below
class Fibbo(IStrategy):
    """
    Fibonacci Strategy with Indodax exchange workarounds.
    
    Includes special handling for:
    - Order creation delays (30s wait)
    - Cancel order side requirements
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Optimal timeframe for the strategy.
    timeframe = "15m"
    informative_timeframe = "1h"

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
            "&-s_close": {"&-s_close": {"color": "green"}},
            "do_predict": {
                "do_predict": {"color": "brown"},
            },
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
        if self.config.get('runmode') == 'hyperopt':
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

    def bot_start(self, **kwargs) -> None:
        """Called once after the bot has started and dependencies are available."""

        if not self.config.get("dry_run", False):
            patch_indodax_create_order()
            patch_indodax_cancel_order()
            patch_indodax_fetch_order()
            logger.info("✅ Indodax patches applied (live mode).")
        else:
            logger.info(f"ℹ️ Indodax patches skipped (dry_run mode).")

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

    # Optional: Custom stoploss based on FreqAI confidence
    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Dynamic stoploss based on FreqAI confidence.
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        # If FreqAI confidence is high, use tighter stoploss
        if 'DI_values' in last_candle:
            confidence = last_candle['DI_values']
            
            # Adjust stoploss based on confidence
            if confidence > 0.8:
                # High confidence: tighter stoploss
                return -0.05
            elif confidence > 0.6:
                # Medium confidence: normal stoploss
                return self.stoploss
            else:
                # Low confidence: wider stoploss
                return -0.15
        
        return self.stoploss

    # Optional: Leverage adjustment based on FreqAI
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                side: str, **kwargs) -> float:
        """
        Adjust leverage based on FreqAI confidence.
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if 'DI_values' in last_candle:
            confidence = last_candle['DI_values']
            
            # Reduce leverage for low confidence predictions
            if confidence < 0.5:
                leverage_factor = 0.5
            elif confidence < 0.7:
                leverage_factor = 0.75
            else:
                leverage_factor = 1.0
            
            adjusted_leverage = min(max_leverage, proposed_leverage * leverage_factor)
            
            if adjusted_leverage != proposed_leverage:
                logger.info(f"FreqAI adjusted leverage: {confidence:.2%} confidence, "
                          f"leverage {proposed_leverage:.1f} → {adjusted_leverage:.1f}")
            
            return adjusted_leverage
        
        return proposed_leverage

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

        # IMPORTANT: FreqAI will automatically add prediction columns AFTER this function
        # Columns like 'do_predict', 'DI_values' will be available in populate_entry_trend

        logger.debug(f"Finished populating indicators. Total columns: {len(dataframe.columns)}")
        return merged_dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Combine your Fibbo strategy with FreqAI predictions.
        FreqAI columns are now available in the dataframe.
        """
        logger.debug(f"Generating entry signals for {metadata['pair']}")
        
        entry_conditions = []
        
        # === Your existing Fibbo conditions ===
        RSI = (dataframe['rsi'] < self.buy_rsi.value)
        VWAP = (dataframe['close'] > dataframe['vwap'])
        ATR = (dataframe['atr'] > dataframe['atr'].shift(1))
        BB = (dataframe['close'] <= dataframe['bb_lowerband'])
        MACD = (dataframe['macd'] > dataframe['macdsignal'])
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
        entry_conditions.append(RSI)
        
        if "BB" in self.buy_additional_indicator.value:
            entry_conditions.append(BB)
        if "ATR" in self.buy_additional_indicator.value:
            entry_conditions.append(ATR)
        if "VWAP" in self.buy_additional_indicator.value:
            entry_conditions.append(VWAP)
        if "MACD" in self.buy_additional_indicator.value:
            entry_conditions.append(MACD)
        if "DEMA" in self.buy_additional_indicator.value:
            entry_conditions.append(DEMA)
        if "FIBBO" in self.buy_additional_indicator.value:
            entry_conditions.append(FIBBO)
        if "STOCHRSI" in self.buy_additional_indicator.value:
            entry_conditions.append(STOCHRSI)
        
        # TTM Squeeze
        if "TTM" in self.buy_additional_indicator.value:
            squeeze_on = dataframe['squeeze_on']
            momentum_positive = dataframe['momentum_hist'] > 0
            entry_conditions.append(squeeze_on & momentum_positive)
        
        # === FreqAI Integration ===
        # Check if FreqAI predictions are available
        # According to FreqAI example, columns like 'do_predict' and 'DI_values' are added automatically
        
        if 'do_predict' in dataframe.columns:
            logger.debug("FreqAI predictions available")
            
            # Method 1: Standard FreqAI signal (1 = buy, -1 = sell)
            freqai_buy_signal = (dataframe['do_predict'] == 1)
            
            # Method 2: If confidence column exists
            if 'DI_values' in dataframe.columns:
                freqai_confident = (dataframe['DI_values'] > float(self.freqaithreshold.value))
                freqai_signal = freqai_buy_signal & freqai_confident
            else:
                freqai_signal = freqai_buy_signal
            
            # Combine FreqAI with your strategy
            if entry_conditions:
                # Option A: FreqAI must agree with ALL your conditions (conservative)
                fibbo_conditions = reduce(lambda x, y: x & y, entry_conditions)
                combined_signal = fibbo_conditions & freqai_signal
                
                # Option B: FreqAI can trigger with fewer conditions (aggressive)
                # combined_signal = freqai_signal & RSI  # Only require RSI + FreqAI
                
                dataframe.loc[combined_signal, 'enter_long'] = 1
                
                # Tag entries that were FreqAI confirmed
                dataframe.loc[freqai_signal & (dataframe['enter_long'] == 1), 'freqai_confirmed'] = 1
            else:
                # If no Fibbo conditions, use FreqAI alone
                dataframe.loc[freqai_signal, 'enter_long'] = 1
            
        else:
            # Fallback to original Fibbo strategy if no FreqAI
            logger.debug("No FreqAI predictions, using original Fibbo strategy")
            if entry_conditions:
                dataframe.loc[
                    reduce(lambda x, y: x & y, entry_conditions),
                    'enter_long'
                ] = 1
        
        logger.debug(f"Generated {dataframe['enter_long'].sum()} entry signals")
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit logic combining Fibbo strategy with FreqAI sell signals.
        """
        logger.debug(f"Generating exit signals for {metadata['pair']}")
        
        exit_conditions = []
        
        # === Your existing Fibbo exit conditions ===
        RSI = (dataframe['rsi'] >= self.sell_rsi.value)
        ATR = (dataframe['atr'] < dataframe['atr'].shift(1))
        MACD = (dataframe['macd'] < dataframe['macdsignal'])
        FIBBO = (dataframe['close'] >= dataframe['fib_236'])
        STOCHRSI = (
            (dataframe['fastk_rsi'] < dataframe['fastd_rsi']) &
            (dataframe['fastk_rsi'] > self.sell_stoch_osc.value)
        )
        
        # Always include RSI
        exit_conditions.append(RSI)
        
        if "ATR" in self.sell_additional_indicator.value:
            exit_conditions.append(ATR)
        if "MACD" in self.sell_additional_indicator.value:
            exit_conditions.append(MACD)
        if "FIBBO" in self.sell_additional_indicator.value:
            exit_conditions.append(FIBBO)
        if "STOCHRSI" in self.sell_additional_indicator.value:
            exit_conditions.append(STOCHRSI)

        # TTM Squeeze exit
        if "TTM" in self.sell_additional_indicator.value:
            squeeze_off = dataframe['squeeze_off']
            momentum_negative = dataframe['momentum_hist'] < 0
            exit_conditions.append(squeeze_off & momentum_negative)
        
        # === FreqAI Exit Signals ===
        if 'do_predict' in dataframe.columns:
            # FreqAI sell signal (standard is -1)
            freqai_sell_signal = (dataframe['do_predict'] == -1)
            
            # Add confidence filter if available
            if 'DI_values' in dataframe.columns:
                freqai_sell_confident = freqai_sell_signal & (dataframe['DI_values'] > float(self.freqaithreshold.value))
                exit_conditions.append(freqai_sell_confident)
            else:
                exit_conditions.append(freqai_sell_signal)
        
        # Combine exit conditions with OR logic
        # Exit if ANY condition is met
        if exit_conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, exit_conditions),
                'exit_long'
            ] = 1
        
        logger.debug(f"Generated {dataframe['exit_long'].sum()} exit signals")
        return dataframe

# Inject hyperopt parameters AFTER class definition
for key, value in strategy_attrs.items():
    setattr(Fibbo, key, value)
