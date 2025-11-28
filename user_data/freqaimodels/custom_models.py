"""
Custom Models for FreqAI
========================

This module contains custom models designed for specific trading strategies:
- SmartMoney Regressor: Based on smart money concepts
- Volatility Regressor: Focused on volatility prediction
- MultiTimeframe Regressor: Combines multiple timeframes
- Trend Regressor: Trend-based prediction
- Momentum Regressor: Momentum-based prediction

These models are designed for specific trading strategies and market conditions.
"""

import logging
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, List, Tuple
from scipy import stats
from scipy.signal import savgol_filter
import warnings

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

# Import with error handling - using absolute imports
try:
    from tree_models import EnhancedCatboostRegressor, EnhancedLightGBMRegressor
except ImportError:
    EnhancedCatboostRegressor = EnhancedLightGBMRegressor = None

try:
    from neural_models import PyTorchLSTMRegressor
except ImportError:
    PyTorchLSTMRegressor = None

try:
    from traditional_models import RandomForestRegressor, RidgeRegressor
except ImportError:
    RandomForestRegressor = RidgeRegressor = None

logger = logging.getLogger(__name__)


class SmartMoneyRegressor(BaseFreqAIModel):
    """
    Smart Money Regressor for FreqAI
    
    This model is designed to identify and predict smart money movements
    based on volume, price action, and institutional patterns.
    
    Features:
    - Volume analysis
    - Price action patterns
    - Institutional flow detection
    - Market microstructure analysis
    """
    
    model_type = "custom"
    default_parameters = {
        "volume_threshold": 0.8,
        "price_threshold": 0.7,
        "lookback_period": 20,
        "smoothing_factor": 0.1,
        "base_model": "catboost"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_model = None
        self._initialize_base_model()
    
    def _initialize_base_model(self):
        """Initialize the base model based on parameter"""
        # Get parameters from config or use defaults
        config = getattr(self, 'config', {})
        freqai_config = config.get('freqai', {})
        model_hyperparams = freqai_config.get('model_hyperparameters', {})
        base_model_param = model_hyperparams.get('base_model', {}).get('default', 'catboost')
        
        model_type = base_model_param
        
        if model_type == "catboost":
            self.base_model = EnhancedCatboostRegressor(config=self.config)
            self.base_model.parameters = {"iterations": 100}
        elif model_type == "lightgbm":
            self.base_model = EnhancedLightGBMRegressor(config=self.config)
            self.base_model.parameters = {"n_estimators": 100}
        elif model_type == "random_forest":
            self.base_model = RandomForestRegressor(config=self.config)
            self.base_model.parameters = {"n_estimators": 100}
        else:
            self.base_model = EnhancedCatboostRegressor(config=self.config)
            self.base_model.parameters = {"iterations": 100}
    
    def _extract_smart_money_features(self, X: np.ndarray) -> np.ndarray:
        """Extract smart money specific features"""
        features = []
        
        for i in range(X.shape[0]):
            # Volume analysis
            volume_features = self._analyze_volume(X[i])
            
            # Price action analysis
            price_features = self._analyze_price_action(X[i])
            
            # Institutional patterns
            institutional_features = self._detect_institutional_patterns(X[i])
            
            # Combine features
            combined = np.concatenate([
                volume_features,
                price_features,
                institutional_features
            ])
            
            features.append(combined)
        
        return np.array(features)
    
    def _analyze_volume(self, data: np.ndarray) -> np.ndarray:
        """Analyze volume patterns for smart money detection"""
        # Simple volume analysis (assuming volume is in the data)
        volume_idx = min(4, len(data) - 1)  # Assume volume is at index 4
        
        if len(data) > volume_idx:
            volume = data[volume_idx]
            
            # Volume moving average
            volume_ma = np.mean(data[max(0, volume_idx-5):volume_idx])
            
            # Volume ratio
            volume_ratio = volume / (volume_ma + 1e-8)
            
            # Volume trend
            volume_trend = (volume - volume_ma) / (volume_ma + 1e-8)
            
            return np.array([volume_ratio, volume_trend])
        else:
            return np.array([1.0, 0.0])
    
    def _analyze_price_action(self, data: np.ndarray) -> np.ndarray:
        """Analyze price action patterns"""
        if len(data) < 3:
            return np.array([0.0, 0.0, 0.0])
        
        # Price change
        price_change = (data[0] - data[1]) / (data[1] + 1e-8)
        
        # Price momentum
        price_momentum = (data[0] - data[2]) / (data[2] + 1e-8)
        
        # Price volatility
        price_volatility = np.std(data[:3])
        
        return np.array([price_change, price_momentum, price_volatility])
    
    def _detect_institutional_patterns(self, data: np.ndarray) -> np.ndarray:
        """Detect institutional trading patterns"""
        if len(data) < 5:
            return np.array([0.0, 0.0])
        
        # Large order detection (simplified)
        large_order_indicator = 1.0 if np.std(data) > 0.1 else 0.0
        
        # Pattern consistency
        pattern_consistency = 1.0 - np.std(data[:5])
        
        return np.array([large_order_indicator, pattern_consistency])
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'SmartMoneyRegressor':
        """Train the smart money model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Extract smart money features
        X_smart = self._extract_smart_money_features(X)
        
        # Train base model
        self.base_model.fit(X_smart, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"smart_money_feature_{i}" for i in range(X_smart.shape[1])]
        
        logger.info(f"Smart Money model trained with {X.shape[0]} samples")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make smart money predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_smart = self._extract_smart_money_features(X)
        
        return self.base_model.predict(X_smart)


class VolatilityRegressor(BaseFreqAIModel):
    """
    Volatility Regressor for FreqAI
    
    This model specializes in predicting volatility patterns
    and market volatility regimes.
    
    Features:
    - Volatility clustering detection
    - GARCH-like modeling
    - Regime switching
    - Volatility forecasting
    """
    
    model_type = "custom"
    default_parameters = {
        "volatility_window": 20,
        "regime_threshold": 0.5,
        "smoothing_factor": 0.1,
        "base_model": "lstm"
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_model = None
        self.volatility_history = []
        self._initialize_base_model()
    
    def _initialize_base_model(self):
        """Initialize the base model"""
        # Get parameters from config or use defaults
        config = getattr(self, 'config', {})
        freqai_config = config.get('freqai', {})
        model_hyperparams = freqai_config.get('model_hyperparameters', {})
        base_model_param = model_hyperparams.get('base_model', {}).get('default', 'lstm')
        
        model_type = base_model_param
        
        if model_type == "lstm":
            self.base_model = PyTorchLSTMRegressor(config=self.config)
            self.base_model.parameters = {"hidden_dim": 64, "epochs": 50}
        elif model_type == "catboost":
            self.base_model = EnhancedCatboostRegressor(config=self.config)
            self.base_model.parameters = {"iterations": 100}
        else:
            self.base_model = RandomForestRegressor(config=self.config)
            self.base_model.parameters = {"n_estimators": 100}
    
    def _calculate_volatility_features(self, X: np.ndarray) -> np.ndarray:
        """Calculate volatility-specific features"""
        features = []
        
        for i in range(X.shape[0]):
            # Rolling volatility (2 features)
            volatility = self._calculate_rolling_volatility(X[i])
            
            # Volatility clustering (2 features)
            clustering = self._detect_volatility_clustering(X[i])
            
            # Regime indicators (2 features)
            regime = self._detect_volatility_regime(X[i])
            
            # Volatility momentum (1 feature)
            momentum = self._calculate_volatility_momentum(X[i])
            
            # Ensure all arrays have consistent shapes and pad if necessary
            volatility = np.array(volatility).flatten()
            clustering = np.array(clustering).flatten()
            regime = np.array(regime).flatten()
            momentum = np.array(momentum).flatten()
            
            # Ensure all arrays have the same length by padding to the maximum length
            max_len = max(len(volatility), len(clustering), len(regime), len(momentum))
            if max_len == 0:
                # If all arrays are empty, create a default feature
                combined = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            else:
                # Pad arrays to ensure consistent lengths
                volatility = np.pad(volatility, (0, max_len - len(volatility)), mode='constant')
                clustering = np.pad(clustering, (0, max_len - len(clustering)), mode='constant')
                regime = np.pad(regime, (0, max_len - len(regime)), mode='constant')
                momentum = np.pad(momentum, (0, max_len - len(momentum)), mode='constant')
                
                combined = np.concatenate([volatility, clustering, regime, momentum])
            features.append(combined)
        
        return np.array(features)
    
    def _calculate_rolling_volatility(self, data: np.ndarray) -> np.ndarray:
        """Calculate rolling volatility measures"""
        if len(data) < 5:
            return np.array([0.0, 0.0])
        
        # Simple volatility
        returns = np.diff(data) / (data[:-1] + 1e-8)
        volatility = np.std(returns)
        
        # Realized volatility
        realized_vol = np.sqrt(np.sum(returns**2))
        
        return np.array([volatility, realized_vol])
    
    def _detect_volatility_clustering(self, data: np.ndarray) -> np.ndarray:
        """Detect volatility clustering patterns"""
        if len(data) < 10:
            return np.array([0.0, 0.0])
        
        # Autocorrelation of volatility
        returns = np.diff(data) / (data[:-1] + 1e-8)
        volatility = np.abs(returns)
        
        if len(volatility) > 1:
            autocorr = np.corrcoef(volatility[:-1], volatility[1:])[0, 1]
        else:
            autocorr = 0.0
        
        # Volatility persistence
        persistence = np.mean(volatility[-5:]) / (np.mean(volatility) + 1e-8)
        
        return np.array([autocorr, persistence])
    
    def _detect_volatility_regime(self, data: np.ndarray) -> np.ndarray:
        """Detect volatility regime"""
        if len(data) < 5:
            return np.array([0.0, 0.0])
        
        # High volatility regime
        volatility = np.std(np.diff(data) / (data[:-1] + 1e-8))
        high_vol_regime = 1.0 if volatility > self.parameters.get("regime_threshold", 0.5) else 0.0
        
        # Regime stability
        regime_stability = 1.0 - volatility
        
        return np.array([high_vol_regime, regime_stability])
    
    def _calculate_volatility_momentum(self, data: np.ndarray) -> np.ndarray:
        """Calculate volatility momentum"""
        if len(data) < 10:
            return np.array([0.0])
        
        # Volatility momentum - fix broadcasting issue
        recent_data = data[-5:]
        past_data = data[-10:-5]
        
        if len(recent_data) >= 2:
            recent_vol = np.std(np.diff(recent_data))
        else:
            recent_vol = 0.0
            
        if len(past_data) >= 2:
            past_vol = np.std(np.diff(past_data))
        else:
            past_vol = 0.0
        
        momentum = (recent_vol - past_vol) / (past_vol + 1e-8)
        
        return np.array([momentum])
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'VolatilityRegressor':
        """Train the volatility model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Calculate volatility features
        X_vol = self._calculate_volatility_features(X)
        
        # Train base model
        self.base_model.fit(X_vol, y, **kwargs)
        
        self.is_trained = True
        self.feature_names = [f"volatility_feature_{i}" for i in range(X_vol.shape[1])]
        
        logger.info(f"Volatility model trained with {X.shape[0]} samples")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make volatility predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        X_vol = self._calculate_volatility_features(X)
        
        return self.base_model.predict(X_vol)


class MultiTimeframeRegressor(BaseFreqAIModel):
    """
    Multi-Timeframe Regressor for FreqAI

    Combines multiple timeframes to make robust predictions.

    Features:
    - Multi-timeframe analysis
    - Timeframe alignment
    - Cross-timeframe patterns
    - Hierarchical modeling
    """

    model_type = "custom"

    # Default parameters if user does not supply any via freqai.json
    default_parameters = {
        "timeframes": ["15m", "1h"],
        "alignment_method": "interpolation",
        "weight_method": "performance",
        "base_model": "ensemble",
    }

    def __init__(self, **kwargs):
        """
        Ensures BaseFreqAIModel initializes config, parameters,
        freqai_config, and internal structures.
        """
        super().__init__(**kwargs)

        # Guarantee parameters exist
        if not hasattr(self, "parameters") or self.parameters is None:
            self.parameters = {}

        # Merge defaults with provided parameters
        for k, v in self.default_parameters.items():
            self.parameters.setdefault(k, v)

        self.timeframes = self.parameters.get("timeframes", ["15m", "1h"])
        self.timeframe_models = {}
        self.timeframe_weights = {}

        self._initialize_timeframe_models()

    def _initialize_timeframe_models(self):
        """Initialize per-timeframe ML models."""
        tf_count = len(self.timeframes)
        default_weight = 1.0 / tf_count if tf_count > 0 else 1.0

        for tf in self.timeframes:
            # Create a model for each timeframe
            model = EnhancedCatboostRegressor(config=self.config)

            # Safe model parameters assignment
            model.parameters = model.parameters if hasattr(model, "parameters") else {}
            model.parameters.setdefault("iterations", 100)

            self.timeframe_models[tf] = model
            self.timeframe_weights[tf] = default_weight

    def _align_timeframes(self, X: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Aligns feature sets from different timeframes.
        Currently a pass-through.
        """
        aligned = {}
        for tf in self.timeframes:
            aligned[tf] = X  # TODO: insert real alignment logic later
        return aligned

    def _extract_timeframe_features(self, X: np.ndarray, timeframe: str) -> np.ndarray:
        """
        Extract timeframe-specific features.
        """
        if timeframe == "15m":
            return self._extract_short_term_features(X)
        elif timeframe == "1h":
            return self._extract_medium_term_features(X)
        elif timeframe == "1d":
            return self._extract_long_term_features(X)
        return X  # fallback if unknown timeframe
    
    def _extract_short_term_features(self, X: np.ndarray) -> np.ndarray:
        """Extract short-term features"""
        features = []
        
        for i in range(X.shape[0]):
            # Momentum indicators
            momentum = self._calculate_momentum(X[i], window=5)
            
            # Volatility indicators
            volatility = self._calculate_volatility(X[i], window=5)
            
            # Trend indicators
            trend = self._calculate_trend(X[i], window=5)
            
            combined = np.concatenate([momentum, volatility, trend])
            features.append(combined)
        
        return np.array(features)
    
    def _extract_medium_term_features(self, X: np.ndarray) -> np.ndarray:
        """Extract medium-term features"""
        features = []
        
        for i in range(X.shape[0]):
            # Medium-term momentum
            momentum = self._calculate_momentum(X[i], window=20)
            
            # Medium-term volatility
            volatility = self._calculate_volatility(X[i], window=20)
            
            # Support/resistance levels
            levels = self._calculate_support_resistance(X[i])
            
            combined = np.concatenate([momentum, volatility, levels])
            features.append(combined)
        
        return np.array(features)
    
    def _extract_long_term_features(self, X: np.ndarray) -> np.ndarray:
        """Extract long-term features"""
        features = []
        
        for i in range(X.shape[0]):
            # Long-term trend
            trend = self._calculate_trend(X[i], window=50)
            
            # Long-term volatility
            volatility = self._calculate_volatility(X[i], window=50)
            
            # Market regime
            regime = self._calculate_market_regime(X[i])
            
            combined = np.concatenate([trend, volatility, regime])
            features.append(combined)
        
        return np.array(features)
    
    def _calculate_momentum(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculate momentum indicators"""
        if len(data) < window:
            return np.array([0.0, 0.0])
        
        # Price momentum
        momentum = (data[-1] - data[-window]) / (data[-window] + 1e-8)
        
        # Rate of change
        roc = (data[-1] - data[-window]) / (data[-window] + 1e-8)
        
        return np.array([momentum, roc])
    
    def _calculate_volatility(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculate volatility indicators"""
        if len(data) < window:
            return np.array([0.0])
        
        returns = np.diff(data[-window:]) / (data[-window:-1] + 1e-8)
        volatility = np.std(returns)
        
        return np.array([volatility])
    
    def _calculate_trend(self, data: np.ndarray, window: int) -> np.ndarray:
        """Calculate trend indicators"""
        if len(data) < window:
            return np.array([0.0])
        
        # Linear trend
        x = np.arange(window)
        slope, _, _, _, _ = stats.linregress(x, data[-window:])
        
        return np.array([slope])
    
    def _calculate_support_resistance(self, data: np.ndarray) -> np.ndarray:
        """Calculate support and resistance levels"""
        if len(data) < 10:
            return np.array([0.0, 0.0])
        
        # Simple support/resistance
        resistance = np.max(data[-10:])
        support = np.min(data[-10:])
        
        return np.array([support, resistance])
    
    def _calculate_market_regime(self, data: np.ndarray) -> np.ndarray:
        """Calculate market regime indicators"""
        if len(data) < 20:
            return np.array([0.0])
        
        # Bull/bear regime
        trend = np.mean(np.diff(data[-20:]))
        regime = 1.0 if trend > 0 else 0.0
        
        return np.array([regime])
    
    def fit(self, X: np.ndarray, y: np.ndarray, **kwargs) -> 'MultiTimeframeRegressor':
        """Train the multi-timeframe model"""
        self.validate_data(X, y)
        X = self.preprocess_features(X)
        
        # Align timeframes
        aligned_data = self._align_timeframes(X)
        
        # Train models for each timeframe
        for timeframe, model in self.timeframe_models.items():
            X_tf = self._extract_timeframe_features(aligned_data[timeframe], timeframe)
            
            # Check if we have enough data and non-constant features
            if X_tf.shape[0] > 10 and X_tf.shape[1] > 0:
                # Add some noise to prevent constant features
                noise = np.random.normal(0, 1e-6, X_tf.shape)
                X_tf = X_tf + noise
                
                try:
                    model.fit(X_tf, y, **kwargs)
                except Exception as e:
                    logger.warning(f"Failed to train {timeframe} model: {e}")
                    # Use a simple fallback model
                    from sklearn.linear_model import LinearRegression
                    fallback_model = LinearRegression()
                    fallback_model.fit(X_tf, y)
                    self.timeframe_models[timeframe] = fallback_model
            else:
                logger.warning(f"Insufficient data for {timeframe} model: {X_tf.shape}")
                # Use a simple fallback model
                from sklearn.linear_model import LinearRegression
                fallback_model = LinearRegression()
                fallback_model.fit(X_tf, y)
                self.timeframe_models[timeframe] = fallback_model
        
        self.is_trained = True
        self.feature_names = [f"multitf_feature_{i}" for i in range(X.shape[1])]
        
        logger.info(f"Multi-Timeframe model trained with {X.shape[0]} samples")
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make multi-timeframe predictions"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        X = self.preprocess_features(X)
        aligned_data = self._align_timeframes(X)
        
        # Get predictions from each timeframe
        predictions = {}
        for timeframe, model in self.timeframe_models.items():
            X_tf = self._extract_timeframe_features(aligned_data[timeframe], timeframe)
            predictions[timeframe] = model.predict(X_tf)
        
        # Combine predictions with weights
        final_prediction = np.zeros_like(list(predictions.values())[0])
        for timeframe, pred in predictions.items():
            weight = self.timeframe_weights[timeframe]
            final_prediction += pred * weight
        
        return final_prediction


class CustomModelUtils:
    """Utility class for custom models"""
    
    @staticmethod
    def get_model_recommendations(strategy_type: str, market_conditions: Dict[str, Any]) -> List[str]:
        """Get model recommendations based on strategy and market conditions"""
        recommendations = []
        
        if strategy_type == "smart_money":
            recommendations.append("Use SmartMoneyRegressor for institutional flow detection")
        
        if market_conditions.get("high_volatility", False):
            recommendations.append("Use VolatilityRegressor for volatility regime detection")
        
        if market_conditions.get("multiple_timeframes", False):
            recommendations.append("Use MultiTimeframeRegressor for comprehensive analysis")
        
        return recommendations
    
    @staticmethod
    def analyze_model_specialization(model) -> Dict[str, Any]:
        """Analyze model specialization and strengths"""
        specialization = {
            "model_type": model.model_type,
            "specialization": model.__class__.__name__,
            "strengths": [],
            "limitations": []
        }
        
        if isinstance(model, SmartMoneyRegressor):
            specialization["strengths"] = ["Volume analysis", "Institutional patterns", "Market microstructure"]
            specialization["limitations"] = ["Requires high-quality data", "Complex feature engineering"]
        
        elif isinstance(model, VolatilityRegressor):
            specialization["strengths"] = ["Volatility forecasting", "Regime detection", "Risk management"]
            specialization["limitations"] = ["Sensitive to market changes", "Requires historical data"]
        
        elif isinstance(model, MultiTimeframeRegressor):
            specialization["strengths"] = ["Multi-timeframe analysis", "Robust predictions", "Comprehensive view"]
            specialization["limitations"] = ["Computational complexity", "Data synchronization"]
        
        return specialization 
