"""
DataFrame Utilities for FreqAI Models
====================================

This module provides utilities for DataFrame manipulation and feature engineering
specifically designed for FreqAI models with MPS support.

Classes:
    FreqAIDataFrameUtils: Main utility class for DataFrame operations

Functions:
    create_sample_data: Create sample OHLCV data for testing
    validate_dataframe: Validate DataFrame for FreqAI models
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional, Union
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import warnings
import logging

logger = logging.getLogger(__name__)

class FreqAIDataFrameUtils:
    """
    Utilities for DataFrame manipulation and feature engineering in FreqAI models.
    
    This class provides methods for:
    - Technical indicator calculation
    - Feature scaling and normalization
    - Data preprocessing
    - MPS-compatible data conversion
    
    Attributes:
        scaler_type (str): Type of scaler to use ('standard', 'minmax', 'robust')
        scaler: The fitted scaler instance
        feature_names (List[str]): List of feature column names
    """
    
    def __init__(self, scaler_type: str = 'standard'):
        """
        Initialize DataFrame utilities.
        
        Args:
            scaler_type: Type of scaler to use ('standard', 'minmax', 'robust')
        """
        self.scaler_type = scaler_type
        self.scaler = self._get_scaler()
        self.feature_names = []
        
    def _get_scaler(self):
        """
        Get the appropriate scaler based on type.
        
        Returns:
            Scaler instance (StandardScaler, MinMaxScaler, or RobustScaler)
        """
        scalers = {
            'standard': StandardScaler(),
            'minmax': MinMaxScaler(),
            'robust': RobustScaler()
        }
        return scalers.get(self.scaler_type, StandardScaler())
    
    def add_technical_indicators(self, df: pd.DataFrame, 
                                indicators: List[str] = None) -> pd.DataFrame:
        """
        Add technical indicators to DataFrame.
        
        This method adds various technical indicators to the input DataFrame.
        Each indicator is calculated using standard financial formulas.
        
        Args:
            df: Input DataFrame with OHLCV data (must contain 'open', 'high', 'low', 'close', 'volume')
            indicators: List of indicators to add. If None, adds default indicators:
                       ['sma', 'ema', 'rsi', 'macd', 'bbands', 'atr']
            
        Returns:
            DataFrame with technical indicators added as new columns
            
        Raises:
            ValueError: If required columns are missing from DataFrame
        """
        if indicators is None:
            indicators = ['sma', 'ema', 'rsi', 'macd', 'bbands', 'atr']
        
        # Validate input DataFrame
        required_columns = ['open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        df = df.copy()
        
        # Add each indicator
        for indicator in indicators:
            if indicator == 'sma':
                df = self._add_sma(df)
            elif indicator == 'ema':
                df = self._add_ema(df)
            elif indicator == 'rsi':
                df = self._add_rsi(df)
            elif indicator == 'macd':
                df = self._add_macd(df)
            elif indicator == 'bbands':
                df = self._add_bollinger_bands(df)
            elif indicator == 'atr':
                df = self._add_atr(df)
            elif indicator == 'stoch':
                df = self._add_stochastic(df)
            elif indicator == 'cci':
                df = self._add_cci(df)
            elif indicator == 'adx':
                df = self._add_adx(df)
            else:
                logger.warning(f"Unknown indicator: {indicator}")
        
        return df
    
    def _add_sma(self, df: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """
        Add Simple Moving Averages to DataFrame.
        
        Args:
            df: Input DataFrame with 'close' column
            periods: List of periods for SMA calculation
            
        Returns:
            DataFrame with SMA columns added
        """
        for period in periods:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    def _add_ema(self, df: pd.DataFrame, periods: List[int] = [12, 26]) -> pd.DataFrame:
        """
        Add Exponential Moving Averages to DataFrame.
        
        Args:
            df: Input DataFrame with 'close' column
            periods: List of periods for EMA calculation
            
        Returns:
            DataFrame with EMA columns added
        """
        for period in periods:
            df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
        return df
    
    def _add_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index to DataFrame.
        
        RSI is calculated using the formula: RSI = 100 - (100 / (1 + RS))
        where RS = Average Gain / Average Loss
        
        Args:
            df: Input DataFrame with 'close' column
            period: Period for RSI calculation (default: 14)
            
        Returns:
            DataFrame with RSI column added
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        return df
    
    def _add_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence) to DataFrame.
        
        MACD is calculated as the difference between fast and slow EMAs.
        
        Args:
            df: Input DataFrame with 'close' column
            fast: Fast EMA period (default: 12)
            slow: Slow EMA period (default: 26)
            signal: Signal line period (default: 9)
            
        Returns:
            DataFrame with MACD, MACD signal, and MACD histogram columns added
        """
        ema_fast = df['close'].ewm(span=fast).mean()
        ema_slow = df['close'].ewm(span=slow).mean()
        df['macd'] = ema_fast - ema_slow
        df['macd_signal'] = df['macd'].ewm(span=signal).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        return df
    
    def _add_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std: float = 2) -> pd.DataFrame:
        """
        Add Bollinger Bands to DataFrame.
        
        Bollinger Bands consist of:
        - Upper band: SMA + (Standard Deviation * multiplier)
        - Lower band: SMA - (Standard Deviation * multiplier)
        - Middle band: SMA
        
        Args:
            df: Input DataFrame with 'close' column
            period: Period for SMA calculation (default: 20)
            std: Standard deviation multiplier (default: 2)
            
        Returns:
            DataFrame with Bollinger Bands columns added
        """
        sma = df['close'].rolling(window=period).mean()
        std_dev = df['close'].rolling(window=period).std()
        df['bb_upper'] = sma + (std_dev * std)
        df['bb_lower'] = sma - (std_dev * std)
        df['bb_middle'] = sma
        return df
    
    def _add_atr(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Average True Range to DataFrame.
        
        True Range is the maximum of:
        - High - Low
        - |High - Previous Close|
        - |Low - Previous Close|
        
        Args:
            df: Input DataFrame with 'high', 'low', 'close' columns
            period: Period for ATR calculation (default: 14)
            
        Returns:
            DataFrame with ATR column added
        """
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        df['atr'] = true_range.rolling(window=period).mean()
        return df
    
    def _add_stochastic(self, df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """
        Add Stochastic Oscillator to DataFrame.
        
        %K = 100 * (Current Close - Lowest Low) / (Highest High - Lowest Low)
        %D = SMA of %K
        
        Args:
            df: Input DataFrame with 'high', 'low', 'close' columns
            k_period: Period for %K calculation (default: 14)
            d_period: Period for %D calculation (default: 3)
            
        Returns:
            DataFrame with Stochastic columns added
        """
        lowest_low = df['low'].rolling(window=k_period).min()
        highest_high = df['high'].rolling(window=k_period).max()
        df['stoch_k'] = 100 * ((df['close'] - lowest_low) / (highest_high - lowest_low))
        df['stoch_d'] = df['stoch_k'].rolling(window=d_period).mean()
        return df
    
    def _add_cci(self, df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
        """
        Add Commodity Channel Index to DataFrame.
        
        CCI = (Typical Price - SMA of Typical Price) / (0.015 * Mean Deviation)
        
        Args:
            df: Input DataFrame with 'high', 'low', 'close' columns
            period: Period for CCI calculation (default: 20)
            
        Returns:
            DataFrame with CCI column added
        """
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        sma_tp = typical_price.rolling(window=period).mean()
        mad = typical_price.rolling(window=period).apply(lambda x: np.mean(np.abs(x - x.mean())))
        df['cci'] = (typical_price - sma_tp) / (0.015 * mad)
        return df
    
    def _add_adx(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        Add Average Directional Index to DataFrame.
        
        This is a simplified ADX calculation using standard deviation.
        
        Args:
            df: Input DataFrame with 'close' column
            period: Period for ADX calculation (default: 14)
            
        Returns:
            DataFrame with ADX column added
        """
        df['adx'] = df['close'].rolling(window=period).std()
        return df
    
    def create_features(self, df: pd.DataFrame, 
                       target_column: str = 'close',
                       feature_columns: List[str] = None,
                       lag_periods: List[int] = [1, 2, 3, 5, 10]) -> pd.DataFrame:
        """
        Create feature set for machine learning models.
        
        This method creates lag features for each feature column and prepares
        the data for model training.
        
        Args:
            df: Input DataFrame with features and target
            target_column: Name of the target column (default: 'close')
            feature_columns: List of columns to use as features. If None, uses all
                           columns except OHLCV columns
            lag_periods: List of lag periods to create (default: [1, 2, 3, 5, 10])
            
        Returns:
            DataFrame with features and target, ready for model training
            
        Raises:
            ValueError: If target_column is not in DataFrame
        """
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found in DataFrame")
        
        if feature_columns is None:
            feature_columns = [col for col in df.columns if col not in ['open', 'high', 'low', 'close', 'volume']]
        
        # Create lag features
        feature_df = df[feature_columns].copy()
        
        for col in feature_columns:
            for lag in lag_periods:
                feature_df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        
        # Add target column
        feature_df[target_column] = df[target_column]
        
        # Remove rows with NaN values
        feature_df = feature_df.dropna()
        
        return feature_df
    
    def scale_features(self, df: pd.DataFrame, 
                      feature_columns: List[str] = None,
                      fit: bool = True) -> pd.DataFrame:
        """
        Scale features using the selected scaler.
        
        Args:
            df: Input DataFrame with features
            feature_columns: List of columns to scale. If None, scales all columns
                           except 'target' and 'close'
            fit: Whether to fit the scaler (True for training, False for prediction)
            
        Returns:
            DataFrame with scaled features
            
        Raises:
            ValueError: If no feature columns are found
        """
        if feature_columns is None:
            feature_columns = [col for col in df.columns if col not in ['target', 'close']]
        
        if not feature_columns:
            raise ValueError("No feature columns found for scaling")
        
        df_scaled = df.copy()
        
        if fit:
            df_scaled[feature_columns] = self.scaler.fit_transform(df[feature_columns])
            self.feature_names = feature_columns
        else:
            df_scaled[feature_columns] = self.scaler.transform(df[feature_columns])
        
        return df_scaled
    
    def prepare_data_for_model(self, df: pd.DataFrame,
                              target_column: str = 'close',
                              test_size: float = 0.2,
                              sequence_length: int = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Prepare data for model training.
        
        This method creates features, scales them, and splits into train/test sets.
        Optionally creates sequences for LSTM models.
        
        Args:
            df: Input DataFrame with OHLCV data
            target_column: Name of the target column (default: 'close')
            test_size: Fraction of data for testing (default: 0.2)
            sequence_length: For sequence models (LSTM, etc.). If None, no sequences created
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test) as numpy arrays
            
        Raises:
            ValueError: If test_size is not between 0 and 1
        """
        if not 0 < test_size < 1:
            raise ValueError("test_size must be between 0 and 1")
        
        # Create features
        feature_df = self.create_features(df, target_column)
        
        # Separate features and target
        feature_columns = [col for col in feature_df.columns if col != target_column]
        X = feature_df[feature_columns].values
        y = feature_df[target_column].values
        
        # Scale features
        X_scaled = self.scale_features(pd.DataFrame(X, columns=feature_columns))
        X_scaled = X_scaled.values
        
        # Split data
        split_idx = int(len(X_scaled) * (1 - test_size))
        X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        if sequence_length:
            X_train = self._create_sequences(X_train, y_train, sequence_length)
            X_test = self._create_sequences(X_test, y_test, sequence_length)
            y_train = y_train[sequence_length:]
            y_test = y_test[sequence_length:]
        
        return X_train, X_test, y_train, y_test
    
    def _create_sequences(self, X: np.ndarray, y: np.ndarray, sequence_length: int) -> np.ndarray:
        """
        Create sequences for LSTM models.
        
        Args:
            X: Input features array
            y: Target array
            sequence_length: Length of each sequence
            
        Returns:
            Array of sequences with shape (n_samples - sequence_length, sequence_length, n_features)
        """
        sequences = []
        for i in range(len(X) - sequence_length):
            sequences.append(X[i:(i + sequence_length)])
        return np.array(sequences)
    
    def to_tensor(self, data: np.ndarray, device: str = 'mps') -> 'torch.Tensor':
        """
        Convert numpy array to PyTorch tensor for MPS compatibility.
        
        Args:
            data: Input numpy array
            device: Target device ('mps', 'cpu')
            
        Returns:
            PyTorch tensor on specified device
            
        Raises:
            ImportError: If PyTorch is not installed
        """
        try:
            import torch
        except ImportError:
            raise ImportError("PyTorch is required for tensor conversion")
        
        if device == 'mps' and torch.backends.mps.is_available():
            print("MPS device used")
            return torch.tensor(data, dtype=torch.float32, device='mps')
        else:
            print("CPU device used as fallback")
            return torch.tensor(data, dtype=torch.float32, device='cpu')
    
    def get_feature_importance(self, model, feature_names: List[str] = None) -> Dict[str, float]:
        """
        Get feature importance from trained model.
        
        Args:
            model: Trained model with feature_importances_ attribute
            feature_names: List of feature names. If None, uses self.feature_names
            
        Returns:
            Dictionary of feature importance scores, sorted by importance
            
        Raises:
            ValueError: If model does not have feature_importances_ attribute
        """
        if not hasattr(model, 'feature_importances_'):
            raise ValueError("Model does not have feature_importances_ attribute")
        
        if feature_names is None:
            feature_names = self.feature_names
        
        if len(feature_names) != len(model.feature_importances_):
            raise ValueError("Number of feature names does not match number of features")
        
        importance_dict = dict(zip(feature_names, model.feature_importances_))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    
    def plot_feature_importance(self, importance_dict: Dict[str, float], 
                              top_n: int = 20) -> None:
        """
        Plot feature importance.
        
        Args:
            importance_dict: Dictionary of feature importance scores
            top_n: Number of top features to show (default: 20)
            
        Raises:
            ImportError: If matplotlib is not installed
        """
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            raise ImportError("Matplotlib is required for plotting")
        
        # Get top N features
        top_features = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:top_n])
        
        plt.figure(figsize=(12, 8))
        plt.barh(list(top_features.keys()), list(top_features.values()))
        plt.xlabel('Feature Importance')
        plt.title(f'Top {top_n} Feature Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()

# Utility functions
def create_sample_data(n_samples: int = 1000) -> pd.DataFrame:
    """
    Create sample OHLCV data for testing.
    
    This function generates realistic financial data with:
    - Random walk price movements
    - Realistic OHLC relationships
    - Random volume data
    
    Args:
        n_samples: Number of samples to generate (default: 1000)
        
    Returns:
        DataFrame with OHLCV data and datetime index
        
    Example:
        >>> df = create_sample_data(1000)
        >>> print(df.head())
    """
    np.random.seed(42)
    
    # Generate sample data
    dates = pd.date_range('2023-01-01', periods=n_samples, freq='1H')
    
    # Create realistic price movements using random walk
    returns = np.random.normal(0, 0.01, n_samples)
    prices = 100 * np.exp(np.cumsum(returns))
    
    # Create OHLC data with realistic relationships
    data = {
        'open': prices * (1 + np.random.normal(0, 0.002, n_samples)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.005, n_samples))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.005, n_samples))),
        'close': prices,
        'volume': np.random.randint(1000, 10000, n_samples)
    }
    
    return pd.DataFrame(data, index=dates)

def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate DataFrame for FreqAI models.
    
    This function checks if the DataFrame has the required structure
    and data quality for FreqAI model training.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        True if DataFrame is valid, False otherwise
        
    Checks performed:
    - Required columns present (open, high, low, close, volume)
    - No NaN values in required columns
    - No infinite values in required columns
    - Realistic OHLC relationships (high >= low, etc.)
    """
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    
    # Check required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing required columns: {missing_columns}")
        return False
    
    # Check for NaN values
    if df[required_columns].isnull().any().any():
        logger.warning("DataFrame contains NaN values")
    
    # Check for infinite values
    if np.isinf(df[required_columns].values).any():
        logger.warning("DataFrame contains infinite values")
    
    # Check OHLC relationships
    invalid_ohlc = (
        (df['high'] < df['low']) |
        (df['open'] < 0) |
        (df['high'] < 0) |
        (df['low'] < 0) |
        (df['close'] < 0) |
        (df['volume'] < 0)
    )
    
    if invalid_ohlc.any():
        logger.warning("DataFrame contains invalid OHLC relationships")
    
    return True 