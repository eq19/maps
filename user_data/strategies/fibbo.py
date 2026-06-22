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
import os
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
from utils import (
    patch_dataprovider,
    patch_ccxt_pair_only,
    patch_indodax_fetch_order, 
    patch_indodax_cancel_order,
    patch_indodax_create_order,
)

# Define indicator sets (could also come from the JSON if needed)
enter_indicators = ["BB", "RSI", "TTM", "VWAP", "MACD", "DEMA", "STOCHRSI"]
exit_indicators = ["BB", "RSI", "TTM", "VWAP", "MACD", "DEMA", "STOCHRSI"]

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
span["enter"]["enter_long_indicator"]["choices"] = sorted(
    indicator_permutations(enter_indicators, max_indicators=4, include_none=True)
)
span["enter"]["enter_short_indicator"]["choices"] = sorted(
    indicator_permutations(enter_indicators, max_indicators=4, include_none=True)
)
span["exit"]["exit_long_indicator"]["choices"] = sorted(
    indicator_permutations(exit_indicators, max_indicators=4, include_none=True)
)
span["exit"]["exit_short_indicator"]["choices"] = sorted(
    indicator_permutations(exit_indicators, max_indicators=4, include_none=True)
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
    
    IMPROVED:
    - Flexible entry conditions (AND vs OR logic vs N-out-of-M)
    - Can now trade more frequently with softer entry requirements
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
        "0": 0.10,      # 10% profit target immediately
        "60": 0.05,     # 5% profit target after 60 candles (~15 hours at 15m)
        "180": 0.02,    # 2% profit target after 180 candles (~45 hours)
        "360": 0        # Exit at any profit after 360 candles (~6 days)
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
    ignore_roi_if_entry_signal = False
    position_adjustment_enable = False
    #max_entry_position_adjustment = 2
    model_name = os.environ.get('FREQAI_MODEL', 'CatboostClassifier')
    
    # Plot config
    plot_config = {
        "main_plot": {
            "tema": {},
            "sar": {"color": "white"},
        },
        "subplots": {
            "&-s_close": {
                "&-s_close": {"color": "green"}
            },
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
            # ✅ FIX: Use realistic ROI targets instead of unrealistic 100%
            self.minimal_roi = {
                "0": 0.08,      # 8% profit target
                "30": 0.04,     # 4% profit target after 30 candles
                "60": 0         # Exit at any profit after 60 candles
            }
            logger.info("⚠️ Hyperopt mode: Using conservative ROI to avoid over-optimization")

        # Update ROI from hyperopt parameters (if ROI space is being optimized)
        self.update_roi()

        # Optional: apply hyperopt value of max_open_trades to config
        if hasattr(self, 'max_open_trades') and self.max_open_trades.value != -1:
            self.config['max_open_trades'] = self.max_open_trades.value

        # Make rolling window configurable
        self.di_rolling_window = getattr(self, 'di_rolling_window', 200)

        # Read from config
        freqai_config = self.config.get('freqai', {})
        self.freqai_enabled = freqai_config.get('enabled', False)
    
        # Also ensure 'freqai' attribute exists check for safety
        if not self.freqai_enabled:
            self.freqai = None

    def bot_start(self, **kwargs) -> None:

        if not self.config.get("dry_run", False):

            patch_ccxt_pair_only()          # 🔥 REQUIRED
            patch_indodax_fetch_order()     # 🔥 REQUIRED
            patch_indodax_cancel_order()    # 🔥 REQUIRED
            patch_indodax_create_order()    # ⚠️ optional but recommended
            patch_dataprovider()            # 🔥 optional but recommended

            logger.info("✅ Indodax fully patched (stable mode)")
        else:
            logger.info(f"ℹ️ CCXT patches skipped (dry_run mode).")

    def update_roi(self):
        """
        Update ROI based on hyperopt parameters.
        This method converts roi_t* and roi_p* parameters into the final minimal_roi dict,
        keeping the results clean and free of intermediate parameters.
        """
        if hasattr(self, 'roi_p1') and hasattr(self, 'roi_t1'):
            try:
                self.minimal_roi = {
                    "0": float(self.roi_p1.value),
                    str(int(self.roi_t1.value)): float(self.roi_p2.value),
                    str(int(self.roi_t2.value)): float(self.roi_p3.value),
                    str(int(self.roi_t3.value)): 0
                }
                logger.info(f"ROI updated from hyperopt parameters: {self.minimal_roi}")
            except (AttributeError, ValueError, TypeError) as e:
                logger.warning(f"Failed to update ROI from hyperopt params: {e}. Using default ROI.")
        else:
            logger.debug("ROI hyperopt parameters not available. Using default ROI.")

    @property
    def protections(self):
        prot = []

        if hasattr(self, 'config'):
            config: Configuration = self.config
            if config.get('runmode') == 'hyperopt':
                spaces = config.get('spaces', [])
                if 'all' in spaces or 'protection' in spaces:
                    return prot

        prot.append({
            "method": "CooldownPeriod",
            "stop_duration_candles": self.cooldown_lookback.value
        })

        if self.use_stop_protection.value:
            prot.append({
                "method": "StoplossGuard",
                "lookback_period_candles": self.lookback_period_candles.value,
                "stop_duration_candles": self.stop_duration_candles.value,
                "trade_limit": self.trade_limit.value,
                "only_per_pair": False
            })

        if self.use_max_drawdown_protection.value:
            prot.append({
                "method": "MaxDrawdown",
                "lookback_period_candles": self.lookback_period_candles.value,
                "stop_duration_candles": self.stop_duration_candles.value,
                "trade_limit": self.max_drawdown_trade_limit.value,
                "max_allowed_drawdown": 0.2,
                "only_per_pair": False
            })

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

    def custom_params(self, pair: str, param: str):
        return self.custom_pair_params.get(pair, {}).get(param, getattr(self, param).value)

    def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if 'DI_values' in last_candle:
            confidence = last_candle['DI_values']
            if confidence > 0.8:
                return -0.05
            elif confidence > 0.6:
                return self.stoploss
            else:
                return -0.15
        
        return self.stoploss

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, 
                   current_rate: float, current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if last_candle.get('%-market_regime', 0) == 3 and current_profit > 0.01:
            return 'high_volatility_exit'
        
        if last_candle.get('DI_values', 0) > 2.0:
            return 'low_confidence_exit'
        
        return None

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                side: str, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        if 'DI_values' in last_candle:
            confidence = last_candle['DI_values']
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

    def ttm_squeeze(self, dataframe: DataFrame, bollinger_period: int = 20, keltner_period: int = 20, momentum_period: int = 12) -> DataFrame:
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=bollinger_period, stds=2)
        keltner = qtpylib.keltner_channel(dataframe, window=keltner_period)
        momentum_hist = dataframe['close'] - dataframe['close'].shift(momentum_period)

        squeeze_on = (bollinger['lower'] > keltner["lower"]) & (bollinger['upper'] < keltner["upper"])
        squeeze_off = (bollinger['lower'] < keltner["lower"]) & (bollinger['upper'] > keltner["upper"])

        dataframe['squeeze_on'] = squeeze_on
        dataframe['squeeze_off'] = squeeze_off
        dataframe['momentum_hist'] = momentum_hist

        return dataframe

    def feature_engineering_expand_all(
        self, dataframe: DataFrame, period: int, metadata: dict, **kwargs
    ) -> DataFrame:
        dataframe["%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe["%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe["%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe["%-ema-period"] = ta.EMA(dataframe, timeperiod=period)

        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=period, stds=2.2
        )
        dataframe["bb_lowerband-period"] = bollinger["lower"]
        dataframe["bb_middleband-period"] = bollinger["mid"]
        dataframe["bb_upperband-period"] = bollinger["upper"]

        dataframe["%-bb_width-period"] = (
            dataframe["bb_upperband-period"] - dataframe["bb_lowerband-period"]
        ) / dataframe["bb_middleband-period"]
        dataframe["%-close-bb_lower-period"] = dataframe["close"] / dataframe["bb_lowerband-period"]
        dataframe["%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
        dataframe["%-relative_volume-period"] = (
            dataframe["volume"] / dataframe["volume"].rolling(period).mean()
        )
        return dataframe

    def feature_engineering_expand_basic(
        self, dataframe: DataFrame, metadata: dict, **kwargs
    ) -> DataFrame:
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        return dataframe

    def feature_engineering_standard(
        self, dataframe: DataFrame, metadata: dict, **kwargs
    ) -> DataFrame:
        dataframe["%-day_of_week"] = dataframe["date"].dt.dayofweek
        dataframe["%-hour_of_day"] = dataframe["date"].dt.hour
        return dataframe

    def set_freqai_targets(
        self, dataframe: DataFrame, metadata: dict, **kwargs
    ) -> DataFrame:
        model_name = self.model_name.lower()
        is_classifier = "classifier" in model_name
        is_multi_target = "multitarget" in model_name
        label_period = self.freqai_info["feature_parameters"]["label_period_candles"]

        if is_classifier:
            if is_multi_target:
                self.freqai.class_names = [0, 1, 2, 3]
                dataframe["&s-up_or_down"] = (dataframe["close"].shift(-label_period) > dataframe["close"]).astype(int)
                dataframe["&s-volatility"] = (
                    (dataframe["close"].rolling(label_period).std() > dataframe["close"].rolling(label_period).std().median()).astype(int) + 2
                )
            else:
                self.freqai.class_names = [0, 1]
                dataframe["&s-up_or_down"] = (dataframe["close"].shift(-label_period) > dataframe["close"]).astype(int)
        else:
            if is_multi_target:
                dataframe["&-s_close"] = (dataframe["close"].shift(-label_period).rolling(label_period).mean() / dataframe["close"] - 1)
                dataframe["&-s_range"] = (dataframe["close"].shift(-label_period).rolling(label_period).max() - dataframe["close"].shift(-label_period).rolling(label_period).min())
            else:
                dataframe["&-s_close"] = (dataframe["close"].shift(-label_period).rolling(label_period).mean() / dataframe["close"] - 1)

        return dataframe

    def confirm_trade_entry(
        self, pair: str, order_type: str, amount: float, rate: float, time_in_force: str, **kwargs
    ) -> bool:
        return True

    def informative_pairs(self):
        whitelist_pairs = self.dp.current_whitelist()
        corr_pairs = self.config["freqai"]["feature_parameters"]["include_corr_pairlist"]
        informative_pairs = []
        
        for tf in self.config["freqai"]["feature_parameters"]["include_timeframes"]:
            for pair in whitelist_pairs:
                informative_pairs.append((pair, self.informative_timeframe))
            for pair in corr_pairs:
                if pair in whitelist_pairs:
                    continue
                informative_pairs.append((pair, tf))
        
        return informative_pairs

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        pair = metadata["pair"]

        if self.freqai is not None and self.freqai_enabled:
            try:
                dataframe = self.freqai.start(dataframe, metadata, self)
                if 'DI_values' in dataframe.columns:
                    if len(dataframe) >= self.di_rolling_window:
                        dataframe['di_percentile'] = (dataframe['DI_values'].rolling(self.di_rolling_window).rank(pct=True))
                        logger.debug(f"FreqAI DI_percentile calculated for {pair}")
                    else:
                        dataframe['di_percentile'] = 0.5
                        logger.debug(f"FreqAI: Insufficient data for {pair}, using neutral confidence")
            except KeyError:
                logger.debug(f"FreqAI model not ready for {pair} - skipping AI signals")
            except Exception as e:
                logger.warning(f"FreqAI error for {pair}: {e}")

        rsi_period = int(self.buy_rsi_period.value) if self.buy_rsi_period.value else 14
        dataframe['rsi'] = ta.RSI(dataframe['close'], timeperiod=max(2, rsi_period))

        vwap_window = int(self.shared_vwap_window.value) if hasattr(self, 'shared_vwap_window') else 20
        dataframe['vwap'] = qtpylib.rolling_vwap(dataframe, window=vwap_window)

        dataframe = self.ttm_squeeze(dataframe)
        dataframe['volume_mean'] = dataframe['volume'].rolling(self.shared_ttm_window.value).mean()
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['atr_pct'] = dataframe['atr'] / dataframe['close']

        rsi_min = dataframe['rsi'].rolling(self.shared_stoch_period.value).min()
        rsi_max = dataframe['rsi'].rolling(self.shared_stoch_period.value).max()
        stoch_rsi = (dataframe['rsi'] - rsi_min) / ((rsi_max - rsi_min).replace(0, 1e-10))

        dataframe['fastk_rsi_buy'] = (stoch_rsi * 100).rolling(self.buy_smoothK.value).mean()
        dataframe['fastd_rsi_buy'] = dataframe['fastk_rsi_buy'].rolling(self.buy_smoothD.value).mean()
        dataframe['fastk_rsi_sell'] = (stoch_rsi * 100).rolling(self.sell_smoothK.value).mean()
        dataframe['fastd_rsi_sell'] = dataframe['fastk_rsi_sell'].rolling(self.sell_smoothD.value).mean()

        macd = ta.MACD(dataframe, fastperiod=6, slowperiod=13, signalperiod=4)
        dataframe['macd'] = macd['macd']
        dataframe['macdhist'] = macd['macdhist']
        dataframe['macdsignal'] = macd['macdsignal']

        bb_period = int(self.buy_bb_period.value) if self.buy_bb_period.value else 20
        bollinger = ta.BBANDS(dataframe, timeperiod=max(2, bb_period), nbdevup=2.0, nbdevdn=2.0, matype=0)
        dataframe['bb_upperband'] = bollinger['upperband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_lowerband'] = bollinger['lowerband']

        for period in span["buy"]["buy_slow_ema"]["choices"]:
            p_int = int(period)
            dataframe[f'ema{p_int}'] = ta.EMA(dataframe, timeperiod=p_int)
        for period in span["buy"]["buy_fast_dema"]["choices"]:
            p_int = int(period)
            dataframe[f'dema{p_int}'] = ta.DEMA(dataframe, timeperiod=p_int)

        swing_lookback = self.buy_swing_period.value
        dataframe['swing_high'] = dataframe['high'].shift(1).rolling(swing_lookback).max()
        dataframe['swing_low'] = dataframe['low'].shift(1).rolling(swing_lookback).min()
        swing_range = dataframe['swing_high'] - dataframe['swing_low']

        dataframe['fib_long_0236'] = dataframe['swing_high'] - swing_range * 0.236
        dataframe['fib_long_0382'] = dataframe['swing_high'] - swing_range * 0.382
        dataframe['fib_long_0618'] = dataframe['swing_high'] - swing_range * 0.618
        dataframe['fib_long_0786'] = dataframe['swing_high'] - swing_range * 0.786

        dataframe['fib_short_0236'] = dataframe['swing_low'] + swing_range * 0.236
        dataframe['fib_short_0382'] = dataframe['swing_low'] + swing_range * 0.382
        dataframe['fib_short_0618'] = dataframe['swing_low'] + swing_range * 0.618
        dataframe['fib_short_0786'] = dataframe['swing_low'] + swing_range * 0.786

        informative = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=self.informative_timeframe)

        if (
            informative is None
            or informative.empty
            or len(informative) < 50
            or 'close' not in informative.columns
        ):
            logger.warning(f"Missing/insufficient informative data for {metadata['pair']} ({self.informative_timeframe})")
            return dataframe
    
        informative['atr'] = ta.ATR(informative, timeperiod=14)
        informative['rsi'] = ta.RSI(informative['close'], timeperiod=max(2, rsi_period))

        macd_inf = ta.MACD(informative, fastperiod=12, slowperiod=26, signalperiod=9)
        informative['macd'] = macd_inf['macd']
        informative['macdhist'] = macd_inf['macdhist']
        informative['macdsignal'] = macd_inf['macdsignal']

        for period in span["buy"]["buy_slow_ema"]["choices"]:
            p_int = int(period)
            informative[f'ema{p_int}'] = ta.EMA(informative, timeperiod=p_int)
        for period in span["buy"]["buy_fast_dema"]["choices"]:
            p_int = int(period)
            informative[f'dema{p_int}'] = ta.DEMA(informative, timeperiod=p_int)

        dataframe = merge_informative_pair(
            dataframe, informative, self.timeframe, self.informative_timeframe, ffill=True
        )

        return dataframe

    def combine_conditions(self, dataframe: DataFrame, conditions: list, mode: str) -> pd.Series:
        if not conditions:
            return pd.Series(False, index=dataframe.index)
        if mode == 'all':
            return reduce(lambda x, y: x & y, conditions)
        elif mode == 'any':
            return reduce(lambda x, y: x | y, conditions)
        elif mode == 'half':
            return sum(conditions) >= (len(conditions) * 0.5)
        elif mode == 'majority':
            return sum(conditions) >= (len(conditions) * 0.66)
        return reduce(lambda x, y: x & y, conditions)

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.debug(f"Generating entry signals for {metadata['pair']}")
        
        # Initialize the enter_tag column with empty strings
        dataframe['enter_tag'] = ''
        
        entry_long_conditions = []
        entry_short_conditions = []
        
        # === Base Indicators ===
        RSI_LONG_ENTRY = dataframe['rsi'] < self.buy_rsi.value
        RSI_SHORT_ENTRY = dataframe['rsi'] > self.buy_rsi.value

        VWAP_LONG_ENTRY = dataframe['close'] > dataframe['vwap']
        VWAP_SHORT_ENTRY = dataframe['close'] < dataframe['vwap']

        BB_LONG_ENTRY = dataframe['close'] <= dataframe['bb_lowerband']
        BB_SHORT_ENTRY = dataframe['close'] >= dataframe['bb_upperband']

        MACD_LONG_ENTRY = dataframe['macd'] > dataframe['macdsignal']
        MACD_SHORT_ENTRY = dataframe['macd'] < dataframe['macdsignal']

        STOCHRSI_LONG_ENTRY = (
            (dataframe['fastk_rsi_buy'] > dataframe['fastd_rsi_buy']) &
            (dataframe['fastk_rsi_buy'] < self.buy_stoch_osc.value)
        )
        STOCHRSI_SHORT_ENTRY = (
            (dataframe['fastk_rsi_sell'] < dataframe['fastd_rsi_sell']) &
            (dataframe['fastk_rsi_sell'] > self.sell_stoch_osc.value)
        )

        # ✅ FIX: Safe-checking column existence before assessing DEMA entry logic to prevent KeyError
        buy_slow_ema_val = int(self.buy_slow_ema.value)
        buy_fast_dema_val = int(self.buy_fast_dema.value)

        ema_long_col = f"ema{buy_slow_ema_val}_{self.informative_timeframe}"
        dema_long_col = f"dema{buy_fast_dema_val}_{self.informative_timeframe}"

        if ema_long_col in dataframe.columns and dema_long_col in dataframe.columns:
            DEMA_LONG_ENTRY = (
                (dataframe['close'] > dataframe[ema_long_col]) &
                (dataframe[dema_long_col] > dataframe[ema_long_col])
            )
            DEMA_SHORT_ENTRY = (
                (dataframe['close'] < dataframe[ema_long_col]) &
                (dataframe[dema_long_col] < dataframe[ema_long_col])
            )
        else:
            # Fallback arrays filled with False if columns haven't been populated yet
            DEMA_LONG_ENTRY = pd.Series(False, index=dataframe.index)
            DEMA_SHORT_ENTRY = pd.Series(False, index=dataframe.index)

        fib_long_col = f'fib_long_{str(self.buy_fib_level.value).replace(".", "")}'
        fib_short_col = f'fib_short_{str(self.buy_fib_level.value).replace(".", "")}'

        if fib_long_col in dataframe.columns and fib_short_col in dataframe.columns:
            FIBBO_LONG_ENTRY = (
                (dataframe['close'] >= (dataframe[fib_long_col] * (1 - dataframe['atr_pct']))) &
                (dataframe['close'] <= (dataframe[fib_long_col] * (1 + dataframe['atr_pct'])))
            )
            FIBBO_SHORT_ENTRY = (
                (dataframe['close'] >= (dataframe[fib_short_col] * (1 - dataframe['atr_pct']))) &
                (dataframe['close'] <= (dataframe[fib_short_col] * (1 + dataframe['atr_pct'])))
            )
        else:
            FIBBO_LONG_ENTRY = pd.Series(False, index=dataframe.index)
            FIBBO_SHORT_ENTRY = pd.Series(False, index=dataframe.index)

        # Always include FIBBO
        entry_long_conditions.append(FIBBO_LONG_ENTRY)
        entry_short_conditions.append(FIBBO_SHORT_ENTRY)
        
        if "BB" in self.enter_long_indicator.value:
            entry_long_conditions.append(BB_LONG_ENTRY)
        if "BB" in self.enter_short_indicator.value:
            entry_short_conditions.append(BB_SHORT_ENTRY)
        if "RSI" in self.enter_long_indicator.value:
            entry_long_conditions.append(RSI_LONG_ENTRY)
        if "RSI" in self.enter_short_indicator.value:
            entry_short_conditions.append(RSI_SHORT_ENTRY)
        if "VWAP" in self.enter_long_indicator.value:
            entry_long_conditions.append(VWAP_LONG_ENTRY)
        if "VWAP" in self.enter_short_indicator.value:
            entry_short_conditions.append(VWAP_SHORT_ENTRY)
        if "MACD" in self.enter_long_indicator.value:
            entry_long_conditions.append(MACD_LONG_ENTRY)
        if "MACD" in self.enter_short_indicator.value:
            entry_short_conditions.append(MACD_SHORT_ENTRY)
        if "DEMA" in self.enter_long_indicator.value:
            entry_long_conditions.append(DEMA_LONG_ENTRY)
        if "DEMA" in self.enter_short_indicator.value:
            entry_short_conditions.append(DEMA_SHORT_ENTRY)
        if "STOCHRSI" in self.enter_long_indicator.value:
            entry_long_conditions.append(STOCHRSI_LONG_ENTRY)
        if "STOCHRSI" in self.enter_short_indicator.value:
            entry_short_conditions.append(STOCHRSI_SHORT_ENTRY)

        if "TTM" in self.enter_long_indicator.value and 'squeeze_on' in dataframe.columns:
            entry_long_conditions.append(dataframe['squeeze_on'] & (dataframe['momentum_hist'] > 0))
        if "TTM" in self.enter_short_indicator.value and 'squeeze_on' in dataframe.columns:
            entry_short_conditions.append(dataframe['squeeze_on'] & (dataframe['momentum_hist'] < 0))

        use_freqai = False
        if 'do_predict' in dataframe.columns:
            if dataframe['do_predict'].isin([1, -1]).any():
                use_freqai = True
                if 'di_percentile' in dataframe.columns:
                    entry_long_conditions.append((dataframe['do_predict'] == 1) & (dataframe['di_percentile'] > float(self.buy_freqai.value)))
                    entry_short_conditions.append((dataframe['do_predict'] == -1) & (dataframe['di_percentile'] < float(self.sell_freqai.value)))
                else:
                    entry_long_conditions.append(dataframe['do_predict'] == 1)
                    entry_short_conditions.append(dataframe['do_predict'] == -1)

        if entry_long_conditions:
            signal = self.combine_conditions(entry_long_conditions, self.enter_trade_mode.value)
            dataframe.loc[signal, 'enter_long'] = 1
            
            dataframe.loc[signal & DEMA_LONG_ENTRY, 'enter_tag'] = 'Fib_Extension_Trend'
            dataframe.loc[signal & FIBBO_LONG_ENTRY & ~DEMA_LONG_ENTRY, 'enter_tag'] = 'Fib_Retracement'
            if use_freqai:
                dataframe.loc[signal & (dataframe['enter_tag'] == ''), 'enter_tag'] = 'FreqAI_Impulse'
            
        if entry_short_conditions:
            signal = self.combine_conditions(entry_short_conditions, self.enter_trade_mode.value)
            dataframe.loc[signal, 'enter_short'] = 1
            
            dataframe.loc[signal & DEMA_SHORT_ENTRY, 'enter_tag'] = 'Fib_Short_Extension'
            dataframe.loc[signal & FIBBO_SHORT_ENTRY & ~DEMA_SHORT_ENTRY, 'enter_tag'] = 'Fib_Short_Retracement'

        dataframe.loc[(dataframe['enter_long'] == 1) & (dataframe['enter_tag'] == ''), 'enter_tag'] = 'Standard_Mix'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Initialize the exit_tag column with empty strings
        dataframe['exit_tag'] = ''

        exit_long_conditions = []
        exit_short_conditions = []
        
        # === Base Indicators ===
        RSI_LONG_EXIT = dataframe['rsi'] > self.sell_rsi.value
        RSI_SHORT_EXIT = dataframe['rsi'] < self.sell_rsi.value

        VWAP_LONG_EXIT = dataframe['close'] < dataframe['vwap']
        VWAP_SHORT_EXIT = dataframe['close'] > dataframe['vwap']

        BB_LONG_EXIT = dataframe['close'] >= dataframe['bb_upperband']
        BB_SHORT_EXIT = dataframe['close'] <= dataframe['bb_lowerband']

        MACD_LONG_EXIT = dataframe['macd'] < dataframe['macdsignal']
        MACD_SHORT_EXIT = dataframe['macd'] > dataframe['macdsignal']

        # LONG EXIT (Closing a Buy): Exit when Stochastic RSI crosses DOWN in an overbought zone
        STOCHRSI_LONG_EXIT = (
            (dataframe['fastk_rsi_sell'] < dataframe['fastd_rsi_sell']) &
            (dataframe['fastk_rsi_sell'] > self.sell_stoch_osc.value)
        )

        # SHORT EXIT (Covering a Short): Exit when Stochastic RSI crosses UP in an oversold zone
        STOCHRSI_SHORT_EXIT = (
            (dataframe['fastk_rsi_buy'] > dataframe['fastd_rsi_buy']) &
            (dataframe['fastk_rsi_buy'] < self.buy_stoch_osc.value)
        )

        # ✅ FIX: Safe-checking column existence before assessing DEMA exit logic to prevent KeyError
        sell_slow_ema_val = int(self.sell_slow_ema.value)
        sell_fast_dema_val = int(self.sell_fast_dema.value)

        ema_long_col = f"ema{sell_slow_ema_val}_{self.informative_timeframe}"
        dema_long_col = f"dema{sell_fast_dema_val}_{self.informative_timeframe}"

        if ema_long_col in dataframe.columns and dema_long_col in dataframe.columns:
            DEMA_LONG_EXIT = (
                (dataframe['close'] < dataframe[ema_long_col]) &
                (dataframe[dema_long_col] < dataframe[ema_long_col])
            )
            DEMA_SHORT_EXIT = (
                (dataframe['close'] > dataframe[ema_long_col]) &
                (dataframe[dema_long_col] > dataframe[ema_long_col])
            )
        else:
            DEMA_LONG_EXIT = pd.Series(False, index=dataframe.index)
            DEMA_SHORT_EXIT = pd.Series(False, index=dataframe.index)

        fib_long_col = f'fib_long_{str(self.sell_fib_level.value).replace(".", "")}'
        fib_short_col = f'fib_short_{str(self.sell_fib_level.value).replace(".", "")}'

        if fib_long_col in dataframe.columns and fib_short_col in dataframe.columns:
            # LONG EXIT: Close is inside the cushion band around the long target level
            FIBBO_LONG_EXIT = (
                (dataframe['close'] >= (dataframe[fib_long_col] * (1 - dataframe['atr_pct']))) &
                (dataframe['close'] <= (dataframe[fib_long_col] * (1 + dataframe['atr_pct'])))
            )
            # SHORT EXIT: Close is inside the cushion band around the short target level
            FIBBO_SHORT_EXIT = (
                (dataframe['close'] >= (dataframe[fib_short_col] * (1 - dataframe['atr_pct']))) &
                (dataframe['close'] <= (dataframe[fib_short_col] * (1 + dataframe['atr_pct'])))
            )
        else:
            FIBBO_LONG_EXIT = pd.Series(False, index=dataframe.index)
            FIBBO_SHORT_EXIT = pd.Series(False, index=dataframe.index)

        # Always include FIBBO
        exit_long_conditions.append(FIBBO_LONG_EXIT)
        exit_short_conditions.append(FIBBO_SHORT_EXIT)
        
        if "BB" in self.exit_long_indicator.value:
            exit_long_conditions.append(BB_LONG_EXIT)
        if "BB" in self.exit_short_indicator.value:
            exit_short_conditions.append(BB_SHORT_EXIT)
        if "RSI" in self.exit_long_indicator.value:
            exit_long_conditions.append(RSI_LONG_EXIT)
        if "RSI" in self.exit_short_indicator.value:
            exit_short_conditions.append(RSI_SHORT_EXIT)
        if "VWAP" in self.exit_long_indicator.value:
            exit_long_conditions.append(VWAP_LONG_EXIT)
        if "VWAP" in self.exit_short_indicator.value:
            exit_short_conditions.append(VWAP_SHORT_EXIT)
        if "MACD" in self.exit_long_indicator.value:
            exit_long_conditions.append(MACD_LONG_EXIT)
        if "MACD" in self.exit_short_indicator.value:
            exit_short_conditions.append(MACD_SHORT_EXIT)
        if "DEMA" in self.exit_long_indicator.value:
            exit_long_conditions.append(DEMA_LONG_EXIT)
        if "DEMA" in self.exit_short_indicator.value:
            exit_short_conditions.append(DEMA_SHORT_EXIT)
        if "STOCHRSI" in self.exit_long_indicator.value:
            exit_long_conditions.append(STOCHRSI_LONG_EXIT)
        if "STOCHRSI" in self.exit_short_indicator.value:
            exit_short_conditions.append(STOCHRSI_SHORT_EXIT)

        if "TTM" in self.exit_long_indicator.value and 'squeeze_on' in dataframe.columns:
            exit_long_conditions.append(dataframe['squeeze_on'] & (dataframe['momentum_hist'] < 0))
        if "TTM" in self.exit_short_indicator.value and 'squeeze_on' in dataframe.columns:
            exit_short_conditions.append(dataframe['squeeze_on'] & (dataframe['momentum_hist'] > 0))

        use_freqai = False
        if 'do_predict' in dataframe.columns:
            if dataframe['do_predict'].isin([1, -1]).any():
                use_freqai = True
                if 'di_percentile' in dataframe.columns:
                    exit_long_conditions.append((dataframe['do_predict'] == -1) & (dataframe['di_percentile'] < float(self.sell_freqai.value)))
                    exit_short_conditions.append((dataframe['do_predict'] == 1) & (dataframe['di_percentile'] > float(self.buy_freqai.value)))
                else:
                    exit_long_conditions.append(dataframe['do_predict'] == -1)
                    exit_short_conditions.append(dataframe['do_predict'] == 1)

        if exit_long_conditions:
            signal = self.combine_conditions(exit_long_conditions, self.exit_trade_mode.value)
            dataframe.loc[signal, 'exit_long'] = 1
            
            dataframe.loc[signal & FIBBO_LONG_EXIT, 'exit_tag'] = 'Exit_Fib_Extension'
            dataframe.loc[signal & DEMA_LONG_EXIT & ~FIBBO_LONG_EXIT, 'exit_tag'] = 'Exit_Trend_Break'
            if use_freqai:
                dataframe.loc[signal & (dataframe['exit_tag'] == ''), 'exit_tag'] = 'Exit_FreqAI_Signal'
            
        if exit_short_conditions:
            signal = self.combine_conditions(exit_short_conditions, self.exit_trade_mode.value)
            dataframe.loc[signal, 'exit_short'] = 1
            
            dataframe.loc[signal & FIBBO_SHORT_EXIT, 'exit_tag'] = 'Exit_Short_Fib_Cover'
            dataframe.loc[signal & DEMA_SHORT_EXIT & ~FIBBO_SHORT_EXIT, 'exit_tag'] = 'Exit_Short_Trend_Break'

        dataframe.loc[(dataframe['exit_long'] == 1) & (dataframe['exit_tag'] == ''), 'exit_tag'] = 'Exit_Standard_Mix'
        return dataframe

# Inject hyperopt parameters AFTER class definition
for key, value in strategy_attrs.items():
    setattr(Fibbo, key, value)
