# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame
from typing import Optional

from freqtrade.strategy import (
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IStrategy,
    IntParameter,
    merge_informative_pair,
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
import logging
from datetime import datetime
from pathlib import Path
from itertools import permutations

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

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


def load_hyperopt_span(path: Path) -> dict:
    default = {"enter": {}, "exit": {}}
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
        span = find_span(data)
        if not isinstance(span, dict):
            logger.warning("Hyperopt span not found or invalid in %s", path)
            return default
        return span
    except FileNotFoundError:
        logger.info("Hyperopt params file not found: %s - using defaults", path)
        return default
    except json.JSONDecodeError:
        logger.error("Invalid JSON in params file: %s - using defaults", path)
        return default
    except Exception as e:
        logger.error("Error loading hyperopt params: %s - using defaults", str(e))
        return default


def get_param_config(span: dict, space: str, name: str):
    section = span.get(space)
    if section is None:
        raise KeyError(f"Missing section '{space}' in strategy span")
    config = section.get(name)
    if config is None:
        raise KeyError(f"Missing parameter '{name}' in '{space}'")
    param_type = config.get("type")
    optimize = config.get("optimize", False)
    default = config.get("default")

    if param_type == "IntParameter":
        return IntParameter(
            low=config["low"],
            high=config["high"],
            default=default,
            space=space,
            optimize=optimize,
        )
    elif param_type == "DecimalParameter":
        return DecimalParameter(
            low=config["low"],
            high=config["high"],
            default=default,
            decimals=config.get("decimals", 3),
            space=space,
            optimize=optimize,
        )
    elif param_type == "BooleanParameter":
        return BooleanParameter(
            default=default,
            space=space,
            optimize=optimize,
        )
    elif param_type == "CategoricalParameter":
        return CategoricalParameter(
            categories=config.get("choices", []),
            default=default,
            space=space,
            optimize=optimize,
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
    for i in range(1, len(profiles) + 1):
        for perm in permutations(profiles, i):
            if len(perm) <= max_indicators:
                profile_permutations.add(", ".join(sorted(perm)))
    return profile_permutations


param_file = Path(__file__).parent / "hyperopt_params.json"
logger.info("Attempting to load hyperopt params file: %s", param_file)
span = load_hyperopt_span(param_file)

try:
    if "enter" in span:
        if "enter_long_indicator" in span["enter"]:
            span["enter"]["enter_long_indicator"]["choices"] = sorted(
                indicator_permutations(enter_indicators, max_indicators=4, include_none=True)
            )
        if "enter_short_indicator" in span["enter"]:
            span["enter"]["enter_short_indicator"]["choices"] = sorted(
                indicator_permutations(enter_indicators, max_indicators=4, include_none=True)
            )
    if "exit" in span:
        if "exit_long_indicator" in span["exit"]:
            span["exit"]["exit_long_indicator"]["choices"] = sorted(
                indicator_permutations(exit_indicators, max_indicators=4, include_none=True)
            )
        if "exit_short_indicator" in span["exit"]:
            span["exit"]["exit_short_indicator"]["choices"] = sorted(
                indicator_permutations(exit_indicators, max_indicators=4, include_none=True)
            )
except Exception as e:
    logger.warning("Error while filling indicator permutations: %s", e)

strategy_attrs = {}
for section, keys in span.items():
    if not isinstance(keys, dict):
        continue
    for key in keys:
        try:
            strategy_attrs[key] = get_param_config(span, section, key)
        except Exception as e:
            logger.debug("Skipping hyperopt param %s/%s: %s", section, key, e)


class Fibbo(IStrategy):
    """
    Fibonacci Strategy with Indodax exchange workarounds.

    - Safe import-time hyperopt loading
    - Reduced repeated DataFrame work
    - Caches informative data by pair/timeframe/last timestamp
    - Uses numpy boolean reductions in condition assembly
    """

    INTERFACE_VERSION = 3
    can_short: bool = False

    timeframe = "1m"
    informative_timeframe = "15m"

    stoploss = -0.1
    minimal_roi = {
        "0": 0.10,
        "60": 0.05,
        "180": 0.02,
        "360": 0,
    }

    macd_profiles = {
        "1m": {"fast": 6, "slow": 13, "signal": 4},
        "15m": {"fast": 8, "slow": 17, "signal": 9},
        "1h": {"fast": 12, "slow": 26, "signal": 9},
    }

    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    trailing_stop = True
    use_exit_signal = True
    exit_profit_only = True
    use_custom_stoploss = True
    ignore_roi_if_entry_signal = False
    position_adjustment_enable = False
    model_name = os.environ.get("FREQAI_MODEL", "PyTorchMLPRegressor")

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

        # Cache heavy indicator blocks and FreqAI outputs by pair/timeframe/last_ts
        self._indicator_cache = {}
        self._freqai_cache = {}
        self._last_populate_indicators_time = 0.0

        try:
            self.update_roi()
        except Exception as e:
            logger.debug("update_roi failed during init: %s", e)

        if hasattr(self, "max_open_trades"):
            try:
                if self.max_open_trades.value != -1:
                    self.config["max_open_trades"] = self.max_open_trades.value
            except Exception:
                pass

        self.di_rolling_window = getattr(self, "di_rolling_window", 200)
        freqai_config = self.config.get("freqai", {})
        self.freqai_enabled = freqai_config.get("enabled", False)

        if not self.freqai_enabled:
            self.freqai = None

    def bot_start(self, **kwargs) -> None:
        patch_dataprovider()

        if not self.config.get("dry_run", False):
            patch_ccxt_pair_only()
            patch_indodax_fetch_order()
            patch_indodax_cancel_order()
            patch_indodax_create_order()
            logger.info("✅ Indodax exchange patches applied (live mode)")
        else:
            logger.info("ℹ️ Indodax exchange patches skipped (dry_run mode).")

    def update_roi(self):
        if hasattr(self, "roi_p1") and hasattr(self, "roi_t1"):
            try:
                self.minimal_roi = {
                    "0": float(self.roi_p1.value),
                    str(int(self.roi_t1.value)): float(self.roi_p2.value),
                    str(int(self.roi_t2.value)): float(self.roi_p3.value),
                    str(int(self.roi_t3.value)): 0,
                }
                logger.info(f"ROI updated from hyperopt parameters: {self.minimal_roi}")
            except (AttributeError, ValueError, TypeError) as e:
                logger.warning(f"Failed to update ROI from hyperopt params: {e}. Using default ROI.")
        else:
            logger.debug("ROI hyperopt parameters not available. Using default ROI.")

    @property
    def protections(self):
        prot = []
        if hasattr(self, "config"):
            config: Configuration = self.config
            if config.get("runmode") == "hyperopt":
                spaces = config.get("spaces", [])
                if "all" in spaces or "protection" in spaces:
                    return prot

        prot.append(
            {
                "method": "CooldownPeriod",
                "stop_duration_candles": int(self.cooldown_lookback.value),
            }
        )

        if self.use_stop_protection.value:
            prot.append(
                {
                    "method": "StoplossGuard",
                    "lookback_period_candles": self.lookback_period_candles.value,
                    "stop_duration_candles": self.stop_duration_candles.value,
                    "trade_limit": self.trade_limit.value,
                    "only_per_pair": False,
                }
            )

        if self.use_max_drawdown_protection.value:
            prot.append(
                {
                    "method": "MaxDrawdown",
                    "lookback_period_candles": self.lookback_period_candles.value,
                    "stop_duration_candles": self.stop_duration_candles.value,
                    "trade_limit": self.max_drawdown_trade_limit.value,
                    "max_allowed_drawdown": 0.2,
                    "only_per_pair": False,
                }
            )

        if self.use_low_profit.value:
            prot.append(
                {
                    "method": "LowProfitPairs",
                    "lookback_period_candles": self.lookback_period_candles.value,
                    "stop_duration": self.stop_duration_candles.value,
                    "trade_limit": self.low_profit_trade_limit.value,
                    "required_profit": 0.02,
                    "only_per_pair": False,
                }
            )

        return prot

    def custom_params(self, pair: str, param: str):
        return self.custom_pair_params.get(pair, {}).get(param, getattr(self, param).value)

    def custom_stoploss(self, pair: str, trade: "Trade", current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        if "DI_values" in last_candle:
            confidence = last_candle["DI_values"]

            if confidence > self.freqai_sl_high_thresh.value:
                return self.freqai_sl_high_val.value
            elif confidence > self.freqai_sl_low_thresh.value:
                return self.stoploss
            else:
                return self.freqai_sl_low_val.value

        return self.stoploss

    def custom_exit(self, pair: str, trade: Trade, current_time: datetime,
                   current_rate: float, current_profit: float, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        # Handle high market regime volatility anomalies (take profit early)
        if last_candle.get("%-market_regime", 0) == 3 and current_profit > 0.02:
            return "high_volatility_exit"

        if last_candle.get("DI_values", 0) > 2.0 and current_profit > 0.01:
            return "low_confidence_exit"

        return None

    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str],
                 side: str, **kwargs) -> float:
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        if "DI_values" in last_candle:
            confidence = last_candle["DI_values"]
            if confidence < 0.5:
                leverage_factor = 0.5
            elif confidence < 0.7:
                leverage_factor = 0.75
            else:
                leverage_factor = 1.0

            adjusted_leverage = min(max_leverage, proposed_leverage * leverage_factor)
            if adjusted_leverage != proposed_leverage:
                logger.info(
                    f"FreqAI adjusted leverage: {confidence:.2%} confidence, "
                    f"leverage {proposed_leverage:.1f} → {adjusted_leverage:.1f}"
                )
            return adjusted_leverage

        return proposed_leverage

    def _selected_indicators(self):
        selected = set()
        for param in (
            getattr(self, "enter_long_indicator", None),
            getattr(self, "enter_short_indicator", None),
            getattr(self, "exit_long_indicator", None),
            getattr(self, "exit_short_indicator", None),
        ):
            if param is None:
                continue
            value = getattr(param, "value", "")
            if isinstance(value, str):
                selected.update([v.strip() for v in value.replace(" ", "").split(",") if v.strip()])
        return selected

    def ttm_squeeze(self, dataframe: DataFrame, bollinger_period: int = 20, keltner_period: int = 20, momentum_period: int = 12) -> DataFrame:
        tp = qtpylib.typical_price(dataframe)
        boll = qtpylib.bollinger_bands(tp, window=bollinger_period, stds=2)
        kelt = qtpylib.keltner_channel(dataframe, window=keltner_period)

        close_np = dataframe["close"].to_numpy()
        shifted_close = dataframe["close"].shift(momentum_period).to_numpy()
        momentum_hist = close_np - shifted_close

        squeeze_on = (
            (boll["lower"].to_numpy() > kelt["lower"].to_numpy())
            & (boll["upper"].to_numpy() < kelt["upper"].to_numpy())
        )
        squeeze_off = (
            (boll["lower"].to_numpy() < kelt["lower"].to_numpy())
            & (boll["upper"].to_numpy() > kelt["upper"].to_numpy())
        )

        dataframe["squeeze_on"] = squeeze_on
        dataframe["squeeze_off"] = squeeze_off
        dataframe["momentum_hist"] = momentum_hist
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
                dataframe["&-s_range"] = (
                    dataframe["close"].shift(-label_period).rolling(label_period).max()
                    - dataframe["close"].shift(-label_period).rolling(label_period).min()
                )
            else:
                dataframe["&-s_close"] = (dataframe["close"].shift(-label_period).rolling(label_period).mean() / dataframe["close"] - 1)

        return dataframe

    def confirm_trade_entry(
        self, pair: str, order_type: str, amount: float, rate: float, time_in_force: str, **kwargs
    ) -> bool:
        return True

    def informative_pairs(self):
        whitelist_pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.informative_timeframe) for pair in whitelist_pairs]

        if self.freqai_enabled:
            feature_parameters = self.config["freqai"]["feature_parameters"]
            for tf in feature_parameters.get("include_timeframes", []):
                for pair in feature_parameters.get("include_corr_pairlist", []):
                    if pair not in whitelist_pairs:
                        informative_pairs.append((pair, tf))

        logger.info(
            "INFORMATIVE PAIRS DIAGNOSTIC: "
            "base_timeframe=%s, informative_timeframe=%s, "
            "whitelist_count=%d, requested_count=%d",
            self.timeframe,
            self.informative_timeframe,
            len(whitelist_pairs),
            len(informative_pairs),
        )
        return list(dict.fromkeys(informative_pairs))

    def combine_conditions(self, dataframe: DataFrame, conditions: list, mode: str) -> pd.Series:
        if not conditions:
            return pd.Series(False, index=dataframe.index)

        cond_arrays = []
        for cond in conditions:
            if isinstance(cond, pd.Series):
                arr = cond.fillna(False).astype(bool).to_numpy()
            else:
                arr = np.asarray(cond)
                if arr.dtype == object:
                    arr = pd.Series(cond, index=dataframe.index).fillna(False).astype(bool).to_numpy()
                else:
                    arr = arr.astype(bool)
            cond_arrays.append(arr)

        n = len(cond_arrays)
        if mode == "all":
            out = np.logical_and.reduce(cond_arrays)
        elif mode == "any":
            out = np.logical_or.reduce(cond_arrays)
        else:
            votes = np.sum(np.vstack(cond_arrays), axis=0)
            if mode == "half":
                out = votes >= (n * 0.5)
            elif mode == "majority":
                out = votes >= (n * 0.66)
            else:
                out = np.logical_and.reduce(cond_arrays)

        return pd.Series(out, index=dataframe.index)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        pair = metadata["pair"]
        start_time = time.perf_counter()

        selected = self._selected_indicators()
        use_rsi = "RSI" in selected
        use_vwap = "VWAP" in selected
        use_bb = "BB" in selected
        use_macd = "MACD" in selected
        use_dema = "DEMA" in selected
        use_stochrsi = "STOCHRSI" in selected
        use_ttm = "TTM" in selected

        # FreqAI
        if self.freqai is not None and self.freqai_enabled:
            key = (pair, self.timeframe, dataframe["date"].iat[-1] if "date" in dataframe.columns else len(dataframe))
            cache = self._freqai_cache.get(key)
            if cache is None:
                try:
                    cache = self.freqai.start(dataframe.copy(), metadata, self)
                    self._freqai_cache[key] = cache
                except Exception as e:
                    logger.debug("FreqAI error for %s: %s", pair, e)
                    cache = dataframe
            dataframe = cache

            if "DI_values" in dataframe.columns:
                if len(dataframe) >= self.di_rolling_window:
                    dataframe["di_percentile"] = dataframe["DI_values"].rolling(self.di_rolling_window).rank(pct=True)
                else:
                    dataframe["di_percentile"] = 0.5

        # Core indicators that are always used by the strategy unless explicitly impossible
        if use_rsi or True:
            rsi_period = int(self.buy_rsi_period.value) if hasattr(self, "buy_rsi_period") and self.buy_rsi_period.value else 14
            dataframe["rsi"] = ta.RSI(dataframe["close"], timeperiod=max(2, rsi_period))

        if use_vwap or True:
            vwap_window = int(self.shared_vwap_window.value) if hasattr(self, "shared_vwap_window") else 20
            dataframe["vwap"] = qtpylib.rolling_vwap(dataframe, window=vwap_window)

        if use_ttm or True:
            dataframe = self.ttm_squeeze(dataframe)
            dataframe["volume_mean"] = dataframe["volume"].rolling(self.shared_ttm_window.value).mean()

        if use_bb or True:
            bb_period = int(self.buy_bb_period.value) if hasattr(self, "buy_bb_period") and self.buy_bb_period.value else 20
            bollinger = ta.BBANDS(dataframe, timeperiod=max(2, bb_period), nbdevup=2.0, nbdevdn=2.0, matype=0)
            dataframe["bb_upperband"] = bollinger["upperband"]
            dataframe["bb_middleband"] = bollinger["middleband"]
            dataframe["bb_lowerband"] = bollinger["lowerband"]

        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        dataframe["atr_pct"] = dataframe["atr"] / dataframe["close"]

        if use_stochrsi or True:
            rsi_min = dataframe["rsi"].rolling(self.shared_stoch_period.value).min()
            rsi_max = dataframe["rsi"].rolling(self.shared_stoch_period.value).max()
            stoch_rsi = (dataframe["rsi"] - rsi_min) / ((rsi_max - rsi_min).replace(0, 1e-10))
            dataframe["fastk_rsi_buy"] = (stoch_rsi * 100).rolling(self.buy_smoothK.value).mean()
            dataframe["fastd_rsi_buy"] = dataframe["fastk_rsi_buy"].rolling(self.buy_smoothD.value).mean()
            dataframe["fastk_rsi_sell"] = (stoch_rsi * 100).rolling(self.sell_smoothK.value).mean()
            dataframe["fastd_rsi_sell"] = dataframe["fastk_rsi_sell"].rolling(self.sell_smoothD.value).mean()

        if use_macd or True:
            macd = ta.MACD(dataframe, fastperiod=6, slowperiod=13, signalperiod=4)
            dataframe["macd"] = macd["macd"]
            dataframe["macdhist"] = macd["macdhist"]
            dataframe["macdsignal"] = macd["macdsignal"]

        buy_slow_ema_val = int(self.buy_slow_ema.value)
        buy_fast_dema_val = int(self.buy_fast_dema.value)
        sell_slow_ema_val = int(self.sell_slow_ema.value)
        sell_fast_dema_val = int(self.sell_fast_dema.value)

        if use_dema or True:
            dataframe[f"ema{buy_slow_ema_val}"] = ta.EMA(dataframe, timeperiod=buy_slow_ema_val)
            dataframe[f"dema{buy_fast_dema_val}"] = ta.DEMA(dataframe, timeperiod=buy_fast_dema_val)

            if buy_slow_ema_val != sell_slow_ema_val:
                dataframe[f"ema{sell_slow_ema_val}"] = ta.EMA(dataframe, timeperiod=sell_slow_ema_val)
            if buy_fast_dema_val != sell_fast_dema_val:
                dataframe[f"dema{sell_fast_dema_val}"] = ta.DEMA(dataframe, timeperiod=sell_fast_dema_val)

        swing_lookback = self.buy_swing_period.value
        dataframe["swing_high"] = dataframe["high"].shift(1).rolling(swing_lookback).max()
        dataframe["swing_low"] = dataframe["low"].shift(1).rolling(swing_lookback).min()
        swing_range = dataframe["swing_high"] - dataframe["swing_low"]

        buy_fib_val = float(self.buy_fib_level.value)
        buy_fib_str = str(self.buy_fib_level.value).replace(".", "")
        sell_fib_val = float(self.sell_fib_level.value)
        sell_fib_str = str(self.sell_fib_level.value).replace(".", "")

        dataframe[f"fib_long_{buy_fib_str}"] = dataframe["swing_high"] - swing_range * buy_fib_val
        dataframe[f"fib_short_{buy_fib_str}"] = dataframe["swing_low"] + swing_range * buy_fib_val

        if buy_fib_str != sell_fib_str:
            dataframe[f"fib_long_{sell_fib_str}"] = dataframe["swing_high"] - swing_range * sell_fib_val
            dataframe[f"fib_short_{sell_fib_str}"] = dataframe["swing_low"] + swing_range * sell_fib_val

        informative = None
        try:
            informative = self.dp.get_pair_dataframe(pair=pair, timeframe=self.informative_timeframe)
        except Exception:
            informative = None

        if informative is None or informative.empty or len(informative) < 50 or "close" not in informative.columns:
            logger.warning(f"Missing/insufficient informative data for {pair} ({self.informative_timeframe})")
            self._last_populate_indicators_time = time.perf_counter() - start_time
            return dataframe

        cache_key = (
            pair,
            self.informative_timeframe,
            informative["date"].iat[-1] if "date" in informative.columns else len(informative),
        )
        cached = self._indicator_cache.get(cache_key)
        if cached is None:
            informative_buf = informative.copy()
            informative_buf[f"ema{buy_slow_ema_val}"] = ta.EMA(informative_buf, timeperiod=buy_slow_ema_val)
            informative_buf[f"dema{buy_fast_dema_val}"] = ta.DEMA(informative_buf, timeperiod=buy_fast_dema_val)

            if buy_slow_ema_val != sell_slow_ema_val:
                informative_buf[f"ema{sell_slow_ema_val}"] = ta.EMA(informative_buf, timeperiod=sell_slow_ema_val)
            if buy_fast_dema_val != sell_fast_dema_val:
                informative_buf[f"dema{sell_fast_dema_val}"] = ta.DEMA(informative_buf, timeperiod=sell_fast_dema_val)

            self._indicator_cache[cache_key] = informative_buf
            cached = informative_buf

        dataframe = merge_informative_pair(
            dataframe, cached, self.timeframe, self.informative_timeframe, ffill=True
        )

        elapsed = time.perf_counter() - start_time
        self._last_populate_indicators_time = elapsed
        if elapsed > 2.0:
            logger.warning("populate_indicators for %s took %.2fs", pair, elapsed)

        # Simple cache trim
        if len(self._indicator_cache) > 128:
            self._indicator_cache.pop(next(iter(self._indicator_cache)))

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.debug(f"Generating entry signals for {metadata['pair']}")

        dataframe["enter_tag"] = ""

        entry_long_conditions = []
        entry_short_conditions = []

        RSI_LONG_ENTRY = dataframe["rsi"] < self.buy_rsi.value
        RSI_SHORT_ENTRY = dataframe["rsi"] > self.buy_rsi.value

        VWAP_LONG_ENTRY = dataframe["close"] > dataframe["vwap"]
        VWAP_SHORT_ENTRY = dataframe["close"] < dataframe["vwap"]

        BB_LONG_ENTRY = dataframe["close"] <= dataframe["bb_lowerband"]
        BB_SHORT_ENTRY = dataframe["close"] >= dataframe["bb_upperband"]

        MACD_LONG_ENTRY = dataframe["macd"] > dataframe["macdsignal"]
        MACD_SHORT_ENTRY = dataframe["macd"] < dataframe["macdsignal"]

        STOCHRSI_LONG_ENTRY = (
            (dataframe["fastk_rsi_buy"] > dataframe["fastd_rsi_buy"])
            & (dataframe["fastk_rsi_buy"] < self.buy_stoch_osc.value)
        )
        STOCHRSI_SHORT_ENTRY = (
            (dataframe["fastk_rsi_sell"] < dataframe["fastd_rsi_sell"])
            & (dataframe["fastk_rsi_sell"] > self.sell_stoch_osc.value)
        )

        buy_slow_ema_val = int(self.buy_slow_ema.value)
        buy_fast_dema_val = int(self.buy_fast_dema.value)

        ema_long_col = f"ema{buy_slow_ema_val}_{self.informative_timeframe}"
        dema_long_col = f"dema{buy_fast_dema_val}_{self.informative_timeframe}"

        if ema_long_col in dataframe.columns and dema_long_col in dataframe.columns:
            DEMA_LONG_ENTRY = (
                (dataframe["close"] > dataframe[ema_long_col])
                & (dataframe[dema_long_col] > dataframe[ema_long_col])
            )
            DEMA_SHORT_ENTRY = (
                (dataframe["close"] < dataframe[ema_long_col])
                & (dataframe[dema_long_col] < dataframe[ema_long_col])
            )
        else:
            DEMA_LONG_ENTRY = pd.Series(False, index=dataframe.index)
            DEMA_SHORT_ENTRY = pd.Series(False, index=dataframe.index)

        fib_long_col = f'fib_long_{str(self.buy_fib_level.value).replace(".", "")}'
        fib_short_col = f'fib_short_{str(self.buy_fib_level.value).replace(".", "")}'

        if fib_long_col in dataframe.columns and fib_short_col in dataframe.columns:
            FIBBO_LONG_ENTRY = (
                (dataframe["close"] >= (dataframe[fib_long_col] * (1 - dataframe["atr_pct"])))
                & (dataframe["close"] <= (dataframe[fib_long_col] * (1 + dataframe["atr_pct"])))
            )
            FIBBO_SHORT_ENTRY = (
                (dataframe["close"] >= (dataframe[fib_short_col] * (1 - dataframe["atr_pct"])))
                & (dataframe["close"] <= (dataframe[fib_short_col] * (1 + dataframe["atr_pct"])))
            )
        else:
            FIBBO_LONG_ENTRY = pd.Series(False, index=dataframe.index)
            FIBBO_SHORT_ENTRY = pd.Series(False, index=dataframe.index)

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

        if "TTM" in self.enter_long_indicator.value and "squeeze_on" in dataframe.columns:
            entry_long_conditions.append(dataframe["squeeze_on"] & (dataframe["momentum_hist"] > 0))
        if "TTM" in self.enter_short_indicator.value and "squeeze_on" in dataframe.columns:
            entry_short_conditions.append(dataframe["squeeze_on"] & (dataframe["momentum_hist"] < 0))

        use_freqai = False
        if "do_predict" in dataframe.columns:
            if dataframe["do_predict"].isin([1, -1]).any():
                use_freqai = True
                if "di_percentile" in dataframe.columns:
                    entry_long_conditions.append((dataframe["do_predict"] == 1) & (dataframe["di_percentile"] > float(self.freqai_buy.value)))
                    entry_short_conditions.append((dataframe["do_predict"] == -1) & (dataframe["di_percentile"] < float(self.freqai_sell.value)))
                else:
                    entry_long_conditions.append(dataframe["do_predict"] == 1)
                    entry_short_conditions.append(dataframe["do_predict"] == -1)

        if entry_long_conditions:
            signal_long = self.combine_conditions(dataframe, entry_long_conditions, self.enter_trade_mode.value)
            dataframe.loc[signal_long, "enter_long"] = 1

            dataframe.loc[signal_long & DEMA_LONG_ENTRY, "enter_tag"] = "Fib_Extension_Trend"
            dataframe.loc[signal_long & FIBBO_LONG_ENTRY & ~DEMA_LONG_ENTRY, "enter_tag"] = "Fib_Retracement"
            if use_freqai:
                dataframe.loc[signal_long & (dataframe["enter_tag"] == ""), "enter_tag"] = "FreqAI_Impulse"

        if entry_short_conditions and self.can_short:
            signal_short = self.combine_conditions(dataframe, entry_short_conditions, self.enter_trade_mode.value)
            dataframe.loc[signal_short, "enter_short"] = 1

            dataframe.loc[signal_short & DEMA_SHORT_ENTRY & (dataframe["enter_tag"] == ""), "enter_tag"] = "Fib_Short_Extension"
            dataframe.loc[signal_short & FIBBO_SHORT_ENTRY & ~DEMA_SHORT_ENTRY & (dataframe["enter_tag"] == ""), "enter_tag"] = "Fib_Short_Retracement"

        dataframe.loc[(dataframe["enter_long"] == 1) & (dataframe["enter_tag"] == ""), "enter_tag"] = "Standard_Mix"
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_tag"] = ""

        exit_long_conditions = []
        exit_short_conditions = []

        RSI_LONG_EXIT = dataframe["rsi"] > self.sell_rsi.value
        RSI_SHORT_EXIT = dataframe["rsi"] < self.sell_rsi.value

        VWAP_LONG_EXIT = dataframe["close"] < dataframe["vwap"]
        VWAP_SHORT_EXIT = dataframe["close"] > dataframe["vwap"]

        BB_LONG_EXIT = dataframe["close"] >= dataframe["bb_upperband"]
        BB_SHORT_EXIT = dataframe["close"] <= dataframe["bb_lowerband"]

        MACD_LONG_EXIT = dataframe["macd"] < dataframe["macdsignal"]
        MACD_SHORT_EXIT = dataframe["macd"] > dataframe["macdsignal"]

        STOCHRSI_LONG_EXIT = (
            (dataframe["fastk_rsi_sell"] < dataframe["fastd_rsi_sell"])
            & (dataframe["fastk_rsi_sell"] > self.sell_stoch_osc.value)
        )
        STOCHRSI_SHORT_EXIT = (
            (dataframe["fastk_rsi_buy"] > dataframe["fastd_rsi_buy"])
            & (dataframe["fastk_rsi_buy"] < self.buy_stoch_osc.value)
        )

        sell_slow_ema_val = int(self.sell_slow_ema.value)
        sell_fast_dema_val = int(self.sell_fast_dema.value)

        ema_long_col = f"ema{sell_slow_ema_val}_{self.informative_timeframe}"
        dema_long_col = f"dema{sell_fast_dema_val}_{self.informative_timeframe}"

        if ema_long_col in dataframe.columns and dema_long_col in dataframe.columns:
            DEMA_LONG_EXIT = (
                (dataframe["close"] < dataframe[ema_long_col])
                & (dataframe[dema_long_col] < dataframe[ema_long_col])
            )
            DEMA_SHORT_EXIT = (
                (dataframe["close"] > dataframe[ema_long_col])
                & (dataframe[dema_long_col] > dataframe[ema_long_col])
            )
        else:
            DEMA_LONG_EXIT = pd.Series(False, index=dataframe.index)
            DEMA_SHORT_EXIT = pd.Series(False, index=dataframe.index)

        fib_long_col = f'fib_long_{str(self.sell_fib_level.value).replace(".", "")}'
        fib_short_col = f'fib_short_{str(self.sell_fib_level.value).replace(".", "")}'

        if fib_long_col in dataframe.columns and fib_short_col in dataframe.columns:
            FIBBO_LONG_EXIT = (
                (dataframe["close"] >= (dataframe[fib_long_col] * (1 - dataframe["atr_pct"])))
                & (dataframe["close"] <= (dataframe[fib_long_col] * (1 + dataframe["atr_pct"])))
            )
            FIBBO_SHORT_EXIT = (
                (dataframe["close"] >= (dataframe[fib_short_col] * (1 - dataframe["atr_pct"])))
                & (dataframe["close"] <= (dataframe[fib_short_col] * (1 + dataframe["atr_pct"])))
            )
        else:
            FIBBO_LONG_EXIT = pd.Series(False, index=dataframe.index)
            FIBBO_SHORT_EXIT = pd.Series(False, index=dataframe.index)

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

        if "TTM" in self.exit_long_indicator.value and "squeeze_on" in dataframe.columns:
            exit_long_conditions.append(dataframe["squeeze_on"] & (dataframe["momentum_hist"] < 0))
        if "TTM" in self.exit_short_indicator.value and "squeeze_on" in dataframe.columns:
            exit_short_conditions.append(dataframe["squeeze_on"] & (dataframe["momentum_hist"] > 0))

        use_freqai = False
        if "do_predict" in dataframe.columns:
            if dataframe["do_predict"].isin([1, -1]).any():
                use_freqai = True
                if "di_percentile" in dataframe.columns:
                    exit_long_conditions.append((dataframe["do_predict"] == -1) & (dataframe["di_percentile"] < float(self.freqai_sell.value)))
                    exit_short_conditions.append((dataframe["do_predict"] == 1) & (dataframe["di_percentile"] > float(self.freqai_buy.value)))
                else:
                    exit_long_conditions.append(dataframe["do_predict"] == -1)
                    exit_short_conditions.append(dataframe["do_predict"] == 1)

        if exit_long_conditions:
            signal_long = self.combine_conditions(dataframe, exit_long_conditions, self.exit_trade_mode.value)
            dataframe.loc[signal_long, "exit_long"] = 1

            dataframe.loc[signal_long & FIBBO_LONG_EXIT, "exit_tag"] = "Exit_Fib_Extension"
            dataframe.loc[signal_long & DEMA_LONG_EXIT & ~FIBBO_LONG_EXIT, "exit_tag"] = "Exit_Trend_Break"
            if use_freqai:
                dataframe.loc[signal_long & (dataframe["exit_tag"] == ""), "exit_tag"] = "Exit_FreqAI_Signal"

        if exit_short_conditions and self.can_short:
            signal_short = self.combine_conditions(dataframe, exit_short_conditions, self.exit_trade_mode.value)
            dataframe.loc[signal_short, "exit_short"] = 1

            dataframe.loc[signal_short & FIBBO_SHORT_EXIT & (dataframe["exit_tag"] == ""), "exit_tag"] = "Exit_Short_Fib_Cover"
            dataframe.loc[signal_short & DEMA_SHORT_EXIT & ~FIBBO_SHORT_EXIT & (dataframe["exit_tag"] == ""), "exit_tag"] = "Exit_Short_Trend_Break"

        dataframe.loc[(dataframe["exit_long"] == 1) & (dataframe["exit_tag"] == ""), "exit_tag"] = "Exit_Standard_Mix"
        return dataframe


for key, value in strategy_attrs.items():
    try:
        setattr(Fibbo, key, value)
    except Exception:
        logger.debug("Failed to attach hyperopt param to Fibbo: %s", key)
