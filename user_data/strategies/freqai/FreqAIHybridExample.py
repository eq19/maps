from __future__ import annotations

from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import pandas as pd
import numpy as np

try:
    from ta.momentum import RSIIndicator
    from ta.trend import EMAIndicator, ADXIndicator
    from ta.volatility import AverageTrueRange
except Exception:  # pragma: no cover - optional dependency
    RSIIndicator = EMAIndicator = ADXIndicator = AverageTrueRange = None  # type: ignore


class FreqAIHybridExample(IStrategy):
    """
    Strategy that consumes FreqAI predictions.

    FreqAI injects columns like '&-prediction' (regression) and 'do_predict'.
    Ensure your config uses model_classname: "HybridTimeseriesFreqAIModel_tinhn".
    """

    timeframe = "1h"
    minimal_roi = {"0": 0.02}
    stoploss = -0.10
    # Allow short positions
    can_short: bool = True

    # Basic trailing stop configuration (can be tuned)
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.005  # 0.5%
    trailing_stop_positive_offset = 0.01  # activate after 1%
    # Allow enough history for indicators and label shifts
    startup_candle_count: int = 240

    @property
    def protections(self):
        # Mirror protections now required to be in-strategy (config key deprecated)
        return [
            {"method": "CooldownPeriod", "stop_duration_candles": 12},
            {
                "method": "MaxDrawdown",
                "lookback_period_candles": 720,
                "stop_duration_candles": 144,
                "max_allowed_drawdown": 0.20,
            },
        ]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Trigger FreqAI pipeline (training/prediction and column injection)
        df = self.freqai.start(dataframe, metadata, self)

        # Add ATR(14) and EMA(200) for volatility-aware thresholds and trend filter
        try:
            if AverageTrueRange is not None:
                atr_ind = AverageTrueRange(high=df["high"], low=df["low"], close=df["close"], window=14)
                df["atr"] = atr_ind.average_true_range()
            else:
                # Fallback ATR: simple rolling mean of True Range
                prev_close = df["close"].shift(1)
                tr = pd.concat([
                    (df["high"] - df["low"]).abs(),
                    (df["high"] - prev_close).abs(),
                    (df["low"] - prev_close).abs(),
                ], axis=1).max(axis=1)
                df["atr"] = tr.rolling(window=14, min_periods=1).mean()
        except Exception:
            # Ensure column exists even if computation fails
            df["atr"] = pd.Series(np.nan, index=df.index)

        try:
            if EMAIndicator is not None:
                df["ema200"] = EMAIndicator(close=df["close"], window=200).ema_indicator()
            else:
                df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()
        except Exception:
            df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

        # Derived helpers
        df["atr_pct"] = (df["atr"] / df["close"]).replace([np.inf, -np.inf], np.nan)
        if "&-prediction" in df.columns:
            df["pred_ret"] = (df["&-prediction"] - df["close"]) / df["close"]
        return df

    # --------- FreqAI required hooks ---------
    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        """Define target '&-prediction' as close shifted -label_period (reduces NaNs)."""
        label_period = int(self.freqai_info.get("feature_parameters", {}).get("label_period_candles", 24))
        df = dataframe.copy()
        df["&-prediction"] = df["close"].shift(-label_period)
        return df

    def feature_engineering_expand_all(self, dataframe: DataFrame, period: int, metadata: dict, **kwargs) -> DataFrame:
        """Create period-dependent features (expanded by FreqAI across periods/timeframes).

        Be robust to short slices (e.g., UI chart queries) by skipping indicators
        that require a minimum window length.
        """
        df = dataframe.copy()
        if RSIIndicator is not None:
            try:
                df["%-rsi"] = RSIIndicator(close=df["close"], window=period).rsi()
            except Exception:
                df["%-rsi"] = pd.Series(np.nan, index=df.index)
            try:
                df["%-ema"] = EMAIndicator(close=df["close"], window=period).ema_indicator()
            except Exception:
                df["%-ema"] = df["close"].ewm(span=max(1, period), adjust=False).mean()
            # ADX requires at least `period` candles; guard to avoid negative dimensions
            if len(df) >= max(2, period):
                try:
                    df["%-adx"] = ADXIndicator(
                        high=df["high"], low=df["low"], close=df["close"], window=period
                    ).adx()
                except Exception:
                    df["%-adx"] = pd.Series(np.nan, index=df.index)
            else:
                df["%-adx"] = pd.Series(np.nan, index=df.index)
        else:
            # Fallback: EMA + RSI (Wilder) via pandas
            df["%-ema"] = df["close"].ewm(span=max(1, period), adjust=False).mean()
            delta = df["close"].diff()
            up = delta.clip(lower=0)
            down = -delta.clip(upper=0)
            roll_up = up.ewm(alpha=1/14, adjust=False).mean()
            roll_down = down.ewm(alpha=1/14, adjust=False).mean()
            rs = roll_up / roll_down.replace(0, pd.NA)
            df["%-rsi"] = 100 - (100 / (1 + rs))
            df["%-adx"] = pd.Series(np.nan, index=df.index)
        return df

    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        df = dataframe.copy()
        df["%-pct_change"] = df["close"].pct_change()
        df["%-volume"] = df["volume"]
        return df

    def feature_engineering_standard(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        df = dataframe.copy()
        if "date" in df.columns:
            df["%-day_of_week"] = df["date"].dt.dayofweek / 6.0
            df["%-hour_of_day"] = df["date"].dt.hour / 23.0
        return df

    # --------- Entry/Exit using new API ---------
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        df = dataframe.copy()
        df["enter_long"] = 0
        df["enter_short"] = 0
        pred_col = "&-prediction" if "&-prediction" in df.columns else ("&-pred_up_prob" if "&-pred_up_prob" in df.columns else None)
        if pred_col is not None:
            if pred_col == "&-prediction" and all(c in df.columns for c in ["pred_ret", "atr_pct", "ema200"]):
                fee_buffer = 0.0015  # ~0.15% total fees; tune per exchange
                long_cond = (df["pred_ret"] > (fee_buffer + 0.5 * df["atr_pct"])) & (df["close"] > df["ema200"])
                short_cond = (df["pred_ret"] < -(fee_buffer + 0.5 * df["atr_pct"])) & (df["close"] < df["ema200"])
            elif pred_col == "&-prediction":
                long_cond = df[pred_col] > df["close"] * 1.001
                short_cond = df[pred_col] < df["close"] * 0.999
            else:
                long_cond = df[pred_col] > 0.55
                short_cond = df[pred_col] < 0.45
            if "do_predict" in df.columns:
                long_cond = long_cond & (df["do_predict"] == 1)
                short_cond = short_cond & (df["do_predict"] == 1)
            df.loc[long_cond.fillna(False), "enter_long"] = 1
            df.loc[short_cond.fillna(False), "enter_short"] = 1
        return df

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        df = dataframe.copy()
        df["exit_long"] = 0
        df["exit_short"] = 0
        pred_col = "&-prediction" if "&-prediction" in df.columns else ("&-pred_up_prob" if "&-pred_up_prob" in df.columns else None)
        if pred_col is not None:
            if pred_col == "&-prediction" and all(c in df.columns for c in ["pred_ret", "atr_pct"]):
                fee_buffer = 0.0015
                long_cond = (df["pred_ret"] < -(fee_buffer + 0.5 * df["atr_pct"]))
                short_cond = (df["pred_ret"] > (fee_buffer + 0.5 * df["atr_pct"]))
            elif pred_col == "&-prediction":
                long_cond = df[pred_col] < df["close"] * 0.999
                short_cond = df[pred_col] > df["close"] * 1.001
            else:
                long_cond = df[pred_col] < 0.45
                short_cond = df[pred_col] > 0.55
            if "do_predict" in df.columns:
                long_cond = long_cond & (df["do_predict"] == 1)
                short_cond = short_cond & (df["do_predict"] == 1)
            df.loc[long_cond.fillna(False), "exit_long"] = 1
            df.loc[short_cond.fillna(False), "exit_short"] = 1
        return df
