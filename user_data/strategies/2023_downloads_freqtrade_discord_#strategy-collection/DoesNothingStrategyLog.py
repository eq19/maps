# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List, Optional
from functools import reduce
from pandas import DataFrame, Series
# --------------------------------
import talib.abstract as ta
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from freqtrade.persistence import Trade
import time

logger = logging.getLogger(__name__)


class DoesNothingStrategyLog(IStrategy):
    """

    author@: Gert Wohlgemuth

    just a skeleton

    """

    # Minimal ROI designed for the strategy.
    # adjust based on market conditions. We would recommend to keep it low for quick turn arounds
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "0": 0.01
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.05

    # Optimal timeframe for the strategy
    timeframe = '1m'

    startup_candle_count = 10
    process_only_new_candles = False

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.info('populate indicators')
        dataframe['rsi'] = ta.RSI(dataframe, 4)
        logger.info('last row of dataframe')
        logger.info(dataframe.iloc[-1])

        if self.dp.runmode.value in ('live', 'dry_run'):
            ticker = self.dp.ticker(metadata['pair'])
            last_price = ticker['last']
            logger.info(f"Last price is {last_price}")

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.info('populate entry')
        dataframe.loc[
            (
            ),
            'enter_long'] = 0
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        logger.info('populate exit')
        dataframe.loc[
            (
            ),
            'exit_long'] = 0
        return dataframe
