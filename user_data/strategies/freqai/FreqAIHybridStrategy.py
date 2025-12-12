# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union
from functools import reduce

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,
    DecimalParameter,
    IntParameter,
    CategoricalParameter
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import pandas_ta as pta
from technical import qtpylib
import logging
logger = logging.getLogger(__name__)
try:
    # Lightweight runtime hook to read governance decisions/policy
    from monitoring.governance_runtime import get_governance_state
except Exception:  # pragma: no cover - strategy must not break if optional module fails
    def get_governance_state(*args, **kwargs):
        class _S:
            status = "none"
            risk_multiplier = 1.0
            tighten_stop_factor = 1.0
            disable_shorts = False
            max_leverage = None
            min_stop_pct = None
            max_stop_pct = None
        return _S()


class FreqAIHybridStrategy(IStrategy):
    """
    Hybrid Futures Leverage Strategy with FreqAI
    - Market Regime Detection (Situation Awareness)
    - Dynamic Indicator Windows
    - Multi-Model Ensemble Support
    - RL Agent Ready
    - LONG/SHORT Trading for Futures with Leverage
    
    Author: Strategy Team
    Version: 1.0.0 MVP (Futures)
    """
    
    INTERFACE_VERSION = 3
    
    # Optimal timeframe for the strategy
    timeframe = '5m'
    
    # Can this strategy go short?
    can_short: bool = True
    
    # Startup candle count
    startup_candle_count: int = 200
    
    # ROI table - Dynamic based on predictions
    minimal_roi = {
        # Faster partial take-profits to bank gains sooner
        "0": 0.02,    # 2%
        "15": 0.01,   # 1% after 15m
        "45": 0.005,  # 0.5% after 45m
        "120": 0.0,   # breakeven after 2h
    }
    
    # Stoploss
    stoploss = -0.05
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    use_custom_stoploss = True
    
    # Hyperopt parameters
    buy_di_threshold = DecimalParameter(0.0, 1.0, default=1.0, space='buy', optimize=True)
    sell_di_threshold = DecimalParameter(0.0, 1.0, default=1.0, space='sell', optimize=True)
    # Entry gating params
    z_base_thr = DecimalParameter(0.0, 1.5, default=0.3, space='buy', optimize=True)
    z_hv_thr = DecimalParameter(0.5, 2.0, default=0.8, space='buy', optimize=True)
    vol_min = DecimalParameter(0.5, 1.5, default=0.7, space='buy', optimize=True)
    vol_max = DecimalParameter(1.5, 5.0, default=4.0, space='buy', optimize=True)
    # Toggle for entry audit logs
    entry_audit_logs: bool = False
    
    # Market regime thresholds
    trend_threshold = DecimalParameter(0.001, 0.01, default=0.005, space='buy', optimize=True)
    volatility_threshold = DecimalParameter(0.5, 2.0, default=1.0, space='buy', optimize=True)
    
    # Process only new candles
    process_only_new_candles = True
    
    # Plot config
    plot_config = {
        'main_plot': {
            'tema': {},
        },
        'subplots': {
            "Regime": {
                'regime': {'color': 'blue'},
            },
            "Predictions": {
                '&-prediction': {'color': 'green'},
                'do_predict': {'color': 'red'},
            }
        }
    }
    
    def informative_pairs(self):
        """
        Define additional informative pairs
        """
        whitelist_pairs = self.dp.current_whitelist()
        corr_pairs = self.config["freqai"]["feature_parameters"]["include_corr_pairlist"]
        informative_pairs = []
        
        for tf in self.config["freqai"]["feature_parameters"]["include_timeframes"]:
            for pair in whitelist_pairs:
                informative_pairs.append((pair, tf))
            for pair in corr_pairs:
                if pair in whitelist_pairs:
                    continue
                informative_pairs.append((pair, tf))
        
        return informative_pairs
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Main indicator population - FreqAI will be called here
        """
        # Call FreqAI
        dataframe = self.freqai.start(dataframe, metadata, self)
        
        # Add some basic indicators for strategy logic (not for FreqAI)
        dataframe['ema_50'] = ta.EMA(dataframe, timeperiod=50)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['atr_14'] = ta.ATR(dataframe, timeperiod=14)
        
        # Replace inf/nan with 0 for all columns
        dataframe = dataframe.replace([np.inf, -np.inf], np.nan)
        dataframe = dataframe.fillna(0)

        # Lightweight debug to understand why no trades are produced
        try:
            if metadata.get('pair') and metadata.get('timeframe') == self.timeframe:
                # Only log for the first pair to avoid excessive logs
                if metadata['pair'] == self.dp.current_whitelist()[0]:
                    cols = [c for c in dataframe.columns if c.startswith('&-') or c in ['do_predict', 'DI_values', 'enter_long', 'enter_short']]
                    do_pred_count = int((dataframe.get('do_predict', 0) == 1).sum()) if 'do_predict' in dataframe else 0
                    enter_l = int(dataframe.get('enter_long', 0).sum()) if 'enter_long' in dataframe else 0
                    enter_s = int(dataframe.get('enter_short', 0).sum()) if 'enter_short' in dataframe else 0
                    # Basic stats for targets if present
                    s_close_stats = None
                    if '&-s_close' in dataframe:
                        s_close_stats = (float(dataframe['&-s_close'].min()), float(dataframe['&-s_close'].max()))
                    s_close_mean_std_present = ('&-s_close_mean' in dataframe.columns, '&-s_close_std' in dataframe.columns)
                    logger.info("[FreqAIHybridStrategy DEBUG] pair=%s do_predict_count=%s enter_long_sum=%s enter_short_sum=%s cols_sample=%s", metadata['pair'], do_pred_count, enter_l, enter_s, cols[:6])
                    logger.info("[FreqAIHybridStrategy DEBUG] s_close_present=%s s_close_min_max=%s s_close_mean_std_present=%s", ('&-s_close' in dataframe), s_close_stats, s_close_mean_std_present)
        except Exception:
            # Never fail because of debug
            pass
        
        return dataframe
    
    # ============ FreqAI Feature Engineering ============
    
    def feature_engineering_expand_all(self, dataframe: DataFrame, period, **kwargs) -> DataFrame:
        """
        Features that will be auto-expanded based on:
        - indicator_periods_candles
        - include_timeframes  
        - include_shifted_candles
        - include_corr_pairlist
        
        This function is called once per period defined in config
        """
        # Price-based features
        dataframe[f"%-rsi-period"] = ta.RSI(dataframe, timeperiod=period)
        dataframe[f"%-mfi-period"] = ta.MFI(dataframe, timeperiod=period)
        dataframe[f"%-adx-period"] = ta.ADX(dataframe, timeperiod=period)
        dataframe[f"%-sma-period"] = ta.SMA(dataframe, timeperiod=period)
        dataframe[f"%-ema-period"] = ta.EMA(dataframe, timeperiod=period)
        
        # Momentum indicators
        dataframe[f"%-mom-period"] = ta.MOM(dataframe, timeperiod=period)
        dataframe[f"%-roc-period"] = ta.ROC(dataframe, timeperiod=period)
        
        # Volatility
        bollinger = ta.BBANDS(dataframe, timeperiod=period, nbdevup=2.0, nbdevdn=2.0)
        dataframe[f"%-bb_lowerband-period"] = bollinger['lowerband']
        dataframe[f"%-bb_middleband-period"] = bollinger['middleband']
        dataframe[f"%-bb_upperband-period"] = bollinger['upperband']
        # Handle division by zero
        dataframe[f"%-bb_width-period"] = np.where(
            bollinger['middleband'] != 0,
            (bollinger['upperband'] - bollinger['lowerband']) / bollinger['middleband'],
            0
        )
        
        # ATR for volatility
        dataframe[f"%-atr-period"] = ta.ATR(dataframe, timeperiod=period)
        
        # MACD
        macd = ta.MACD(dataframe, fastperiod=int(period/2), slowperiod=period, signalperiod=int(period/3))
        dataframe[f"%-macd-period"] = macd['macd']
        dataframe[f"%-macdsignal-period"] = macd['macdsignal']
        dataframe[f"%-macdhist-period"] = macd['macdhist']
        
        return dataframe
    
    def feature_engineering_expand_basic(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Features that will be expanded based on:
        - include_timeframes
        - include_shifted_candles  
        - include_corr_pairlist
        
        NOT expanded by indicator_periods_candles
        """
        # Price change features
        dataframe["%-pct-change"] = dataframe["close"].pct_change()
        dataframe["%-raw_volume"] = dataframe["volume"]
        dataframe["%-raw_price"] = dataframe["close"]
        
        # Price volatility (rolling std)
        dataframe["%-volatility"] = dataframe["close"].rolling(window=20).std()
        
        # Volume features
        dataframe["%-volume_mean_20"] = dataframe["volume"].rolling(window=20).mean()
        dataframe["%-volume_std_20"] = dataframe["volume"].rolling(window=20).std()
        
        return dataframe
    
    def feature_engineering_standard(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Features that are NOT auto-expanded
        Use this for custom features that should appear only once
        
        This is where we add Market Regime Detection (Situation Awareness)
        """
        # Time-based features
        dataframe["%-day_of_week"] = (dataframe["date"].dt.dayofweek + 1) / 7
        dataframe["%-hour_of_day"] = (dataframe["date"].dt.hour + 1) / 25
        
        # ========== MARKET REGIME DETECTION ==========
        
        # Trend detection (EMA crossover based)
        ema_short = ta.EMA(dataframe, timeperiod=20)
        ema_long = ta.EMA(dataframe, timeperiod=50)
        # Handle division by zero
        dataframe["%-trend_strength"] = np.where(
            ema_long != 0,
            (ema_short - ema_long) / ema_long,
            0
        )
        
        # Volatility regime (ATR normalized)
        atr_20 = ta.ATR(dataframe, timeperiod=20)
        # Handle division by zero
        dataframe["%-volatility_regime"] = np.where(
            dataframe["close"] != 0,
            atr_20 / dataframe["close"],
            0
        )
        
        # Volume regime
        volume_ma = dataframe["volume"].rolling(window=20).mean()
        # Handle division by zero
        dataframe["%-volume_regime"] = np.where(
            volume_ma != 0,
            dataframe["volume"] / volume_ma,
            1
        )
        
        # Market regime classification
        # 0 = Range, 1 = Trending Up, 2 = Trending Down, 3 = High Volatility
        dataframe["%-market_regime"] = 0  # Default: Range
        
        trend_up = dataframe["%-trend_strength"] > self.trend_threshold.value
        trend_down = dataframe["%-trend_strength"] < -self.trend_threshold.value
        high_vol = dataframe["%-volatility_regime"] > self.volatility_threshold.value * 0.02
        
        dataframe.loc[trend_up & ~high_vol, "%-market_regime"] = 1  # Trending Up
        dataframe.loc[trend_down & ~high_vol, "%-market_regime"] = 2  # Trending Down
        dataframe.loc[high_vol, "%-market_regime"] = 3  # High Volatility
        
        # Regime indicators for different time horizons
        dataframe["%-regime_short"] = dataframe["%-market_regime"].rolling(window=10).mean()
        dataframe["%-regime_medium"] = dataframe["%-market_regime"].rolling(window=50).mean()
        dataframe["%-regime_long"] = dataframe["%-market_regime"].rolling(window=200).mean()
        
        return dataframe
    
    def set_freqai_targets(self, dataframe: DataFrame, metadata, **kwargs) -> DataFrame:
        """
        Define prediction targets for the model
        
        We use multiple targets for ensemble predictions
        """
        # Target 1: Future price change (main target)
        future_close = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
        )
        # Handle division by zero
        dataframe["&-s_close"] = np.where(
            dataframe["close"] != 0,
            (future_close / dataframe["close"]) - 1,
            0
        )
        
        # Target 2: Future volatility (for risk management)
        future_volatility = (
            dataframe["close"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .std()
        )
        # Handle division by zero
        dataframe["&-s_volatility"] = np.where(
            dataframe["close"] != 0,
            future_volatility / dataframe["close"],
            0
        )
        
        # Target 3: Future volume surge (for confirmation)
        future_volume = (
            dataframe["volume"]
            .shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            .rolling(self.freqai_info["feature_parameters"]["label_period_candles"])
            .mean()
        )
        # Handle division by zero
        dataframe["&-s_volume"] = np.where(
            dataframe["volume"] != 0,
            (future_volume / dataframe["volume"]) - 1,
            0
        )
        
        # Clean up inf/nan in targets
        dataframe = dataframe.replace([np.inf, -np.inf], np.nan)
        dataframe["&-s_close"] = dataframe["&-s_close"].fillna(0)
        dataframe["&-s_volatility"] = dataframe["&-s_volatility"].fillna(0)
        dataframe["&-s_volume"] = dataframe["&-s_volume"].fillna(0)
        
        return dataframe
    
    # ============ Entry/Exit Logic ============
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Balanced entry signals using z-score of target vs rolling mean/std,
        with DI, regime, trend, and volume filters. Entries trigger on threshold crossings
        to reduce churn. Supports LONG and SHORT for futures.
        """
        # Use target as prediction proxy for z-score (robust across models)
        target = dataframe['&-s_close'] if '&-s_close' in dataframe.columns else 0
        mean = dataframe['&-s_close_mean'] if '&-s_close_mean' in dataframe.columns else 0
        std = dataframe['&-s_close_std'] if '&-s_close_std' in dataframe.columns else 1
        z = (target - mean) / (std + 1e-12)

        # Filters
        do_pred = (dataframe.get('do_predict', 0) == 1)
        di_ok = dataframe.get('DI_values', 1.0) < self.buy_di_threshold.value  # smaller is closer to training, more reliable
        vol_regime = dataframe.get('%-volume_regime', 1.0)
        # Require healthy but not extreme volume (hyperoptable bounds)
        vol_ok = (vol_regime > float(self.vol_min.value)) & (vol_regime < float(self.vol_max.value))
        regime = dataframe.get('%-market_regime', 0)
        # Trend strength gating (EMA-based strength computed in features)
        ts = dataframe.get('%-trend_strength', 0.0)
        ts_ok_long = ts > self.trend_threshold.value
        ts_ok_short = ts < -self.trend_threshold.value

        # Thresholds
        # Thresholds (hyperoptable)
        base_thr = float(self.z_base_thr.value)
        hv_thr = float(self.z_hv_thr.value)
        long_thr = np.where(regime == 3, hv_thr, base_thr)
        short_thr = np.where(regime == 3, hv_thr, base_thr)

        # Crossings to reduce flapping
        long_sig = qtpylib.crossed_above(z, long_thr)
        short_sig = qtpylib.crossed_below(z, -short_thr)

        gov = get_governance_state()
        # If governance status is halt -> block new entries
        allow_entries = (gov.status != 'halt')
        allow_shorts = (not gov.disable_shorts)

        long_cond = allow_entries & (do_pred & di_ok & vol_ok & ts_ok_long & long_sig)
        short_baseline = do_pred & di_ok & vol_ok & ts_ok_short & short_sig
        short_cond = allow_entries & allow_shorts & short_baseline

        dataframe.loc[long_cond, 'enter_long'] = 1
        dataframe.loc[short_cond, 'enter_short'] = 1
        
        # Optional entry audit logs (first whitelist pair only)
        try:
            if getattr(self, 'entry_audit_logs', False) and metadata.get('pair') and metadata.get('timeframe') == self.timeframe:
                if metadata['pair'] == self.dp.current_whitelist()[0]:
                    do_pred_count = int(do_pred.sum()) if hasattr(do_pred, 'sum') else int(do_pred)
                    di_ok_count = int((do_pred & di_ok).sum()) if hasattr(di_ok, 'sum') else 0
                    vol_ok_count = int((do_pred & vol_ok).sum()) if hasattr(vol_ok, 'sum') else 0
                    ts_long_count = int((do_pred & ts_ok_long).sum()) if hasattr(ts_ok_long, 'sum') else 0
                    ts_short_count = int((do_pred & ts_ok_short).sum()) if hasattr(ts_ok_short, 'sum') else 0
                    long_sig_count = int(long_sig.sum()) if hasattr(long_sig, 'sum') else 0
                    short_sig_count = int(short_sig.sum()) if hasattr(short_sig, 'sum') else 0
                    enter_l = int(dataframe.get('enter_long', 0).sum()) if 'enter_long' in dataframe else 0
                    enter_s = int(dataframe.get('enter_short', 0).sum()) if 'enter_short' in dataframe else 0
                    logger.info(
                        "[EntryAudit] pair=%s do_pred=%s di_ok=%s vol_ok=%s ts_long=%s ts_short=%s long_sig=%s short_sig=%s enter_long=%s enter_short=%s base_thr=%.3f hv_thr=%.3f vol_bounds=(%.2f,%.2f) di_thr=%.3f",
                        metadata['pair'], do_pred_count, di_ok_count, vol_ok_count, ts_long_count, ts_short_count,
                        long_sig_count, short_sig_count, enter_l, enter_s,
                        float(self.z_base_thr.value), float(self.z_hv_thr.value), float(self.vol_min.value), float(self.vol_max.value), float(self.buy_di_threshold.value)
                    )
        except Exception:
            pass

        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit on z-score flips and high-volatility regime deterioration.
        """
        target = dataframe['&-s_close'] if '&-s_close' in dataframe.columns else 0
        mean = dataframe['&-s_close_mean'] if '&-s_close_mean' in dataframe.columns else 0
        std = dataframe['&-s_close_std'] if '&-s_close_std' in dataframe.columns else 1
        z = (target - mean) / (std + 1e-12)

        do_pred = (dataframe.get('do_predict', 0) == 1)
        regime = dataframe.get('%-market_regime', 0)

        # Exits: when z crosses back through 0 in the adverse direction or when regime=3
        exit_long_cond = (do_pred & qtpylib.crossed_below(z, 0.0)) | (regime == 3)
        exit_short_cond = (do_pred & qtpylib.crossed_above(z, 0.0)) | (regime == 3)

        dataframe.loc[exit_long_cond, 'exit_long'] = 1
        dataframe.loc[exit_short_cond, 'exit_short'] = 1
        
        return dataframe
    
    # ============ Custom Methods ============
    
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: Optional[str], 
                 side: str, **kwargs) -> float:
        """
        Dynamic leverage based on market regime and model confidence
        - Conservative: 3x in normal markets
        - Moderate: 5x in trending markets
        - Safe: 2x in volatile markets
        """
        gov = get_governance_state()
        # Base leverage from regime
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) > 0:
            last_candle = dataframe.iloc[-1].squeeze()
            regime = last_candle.get('%-market_regime', 0)
            di_value = last_candle.get('DI_values', 1.0)
            
            # High volatility regime - use minimum leverage
            if regime == 3 or di_value > 1.5:
                base = 2.0
            # Trending regime with good confidence
            elif regime in [1, 2] and di_value < 0.5:
                base = 5.0
            # Normal regime
            else:
                base = 3.0
        else:
            base = 3.0
        # Apply governance risk multiplier and cap by policy/max_leverage
        lev = float(base) * float(getattr(gov, 'risk_multiplier', 1.0) or 1.0)
        # Enforce exchange/max caps
        cap_list = [x for x in [gov.max_leverage, max_leverage] if x is not None]
        if cap_list:
            lev = min(lev, *cap_list)
        # Never below 1.0 for futures leverage
        return max(1.0, float(lev))
    
    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, 
                   current_rate: float, current_profit: float, **kwargs):
        """
        Custom exit logic - can be used for advanced risk management
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()
        
        # Exit if entering high volatility regime with profit
        if last_candle.get('%-market_regime', 0) == 3 and current_profit > 0.01:
            return 'high_volatility_exit'
        
        # Exit if model confidence drops (high DI values)
        if last_candle.get('DI_values', 0) > 2.0:
            return 'low_confidence_exit'
        
        return None

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                        current_rate: float, current_profit: float, **kwargs) -> float:
        """
        ATR-based dynamic stoploss. Returns negative percentage (e.g., -0.025 for -2.5%).
        Uses atr_14 as volatility proxy and caps within [-5%, -1.5%].
        """
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if dataframe is None or len(dataframe) == 0:
            return self.stoploss

        last = dataframe.iloc[-1].squeeze()
        atr = float(last.get('atr_14', 0))
        price = float(last.get('close', 0))
        if price <= 0:
            return self.stoploss

        atrp = atr / price  # ATR percent of price
        # Scale: base 1.5x ATR
        dyn = 1.5 * atrp
        # Apply governance tightening factor
        gov = get_governance_state()
        tighten = float(getattr(gov, 'tighten_stop_factor', 1.0) or 1.0)
        dyn = dyn * tighten
        # Clamp within governance policy bounds if provided, else default 1.5%-5%
        min_stop = 0.015 if getattr(gov, 'min_stop_pct', None) is None else float(gov.min_stop_pct)
        max_stop = 0.05 if getattr(gov, 'max_stop_pct', None) is None else float(gov.max_stop_pct)
        dyn = max(min_stop, min(max_stop, dyn))
        return -float(dyn)
