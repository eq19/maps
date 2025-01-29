from freqtrade.strategy import IStrategy
from pandas import DataFrame
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class ichiV2_15M1H(IStrategy):
    timeframe = '15m'
    minimal_roi = {"0": 0.1}
    stoploss = -0.1
    trailing_stop = False
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Critical check for column names with hidden characters
        cols_repr = [repr(col) for col in dataframe.columns]
        logger.debug(f"Columns with hidden characters: {cols_repr}")
        
        # Validate core OHLCV columns exist
        required = ['open', 'high', 'low', 'close', 'volume']
        missing = [col for col in required if col not in dataframe.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
            
        # Ensure numeric types
        dataframe = dataframe.astype({
            'open': 'float64',
            'high': 'float64', 
            'low': 'float64',
            'close': 'float64',
            'volume': 'float64'
        })
        
        # Calculate Ichimoku
        dataframe = self.calculate_ichimoku(dataframe)
        
        return dataframe

    def calculate_ichimoku(self, dataframe):
        # Final safeguard against empty data
        if dataframe.empty:
            logger.error("Received empty dataframe in Ichimoku calculation!")
            return dataframe
            
        try:
            # Ichimoku parameters
            tenkan = 9
            kijun = 26
            senkou = 52
            
            # Tenkan-sen (Conversion Line)
            dataframe['tenkan'] = (
                dataframe['high'].rolling(window=tenkan).max() + 
                dataframe['low'].rolling(window=tenkan).min()
            ) / 2
            
            # Kijun-sen (Base Line)
            dataframe['kijun'] = (
                dataframe['high'].rolling(window=kijun).max() + 
                dataframe['low'].rolling(window=kijun).min()
            ) / 2
            
            # Senkou Span A (Leading Span A)
            dataframe['senkou_a'] = (
                (dataframe['tenkan'] + dataframe['kijun']) / 2
            ).shift(kijun)
            
            # Senkou Span B (Leading Span B)
            dataframe['senkou_b'] = (
                dataframe['high'].rolling(window=senkou).max() + 
                dataframe['low'].rolling(window=senkou).min()
            ) / 2.shift(kijun)
            
        except KeyError as e:
            logger.error(f"Critical column error: {e}")
            logger.error(f"Available columns: {dataframe.columns.tolist()}")
            raise
        
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Your entry logic here (unchanged)
        dataframe.loc[
            (
                (dataframe['close'] > dataframe['senkou_a']) &
                (dataframe['close'] > dataframe['senkou_b']) &
                (dataframe['tenkan'] > dataframe['kijun'])
            ),
            'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Your exit logic here (unchanged)
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['senkou_a']) |
                (dataframe['close'] < dataframe['senkou_b']) |
                (dataframe['tenkan'] < dataframe['kijun'])
            ),
            'exit_long'] = 1
        return dataframe
