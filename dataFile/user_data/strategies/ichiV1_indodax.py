# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd  # noqa
pd.options.mode.chained_assignment = None  # default='warn'
import technical.indicators as ftt
from functools import reduce
from datetime import datetime, timedelta
from freqtrade.strategy import merge_informative_pair
import numpy as np
from freqtrade.strategy import stoploss_from_open


class ichiV1_indodax(IStrategy):

    # NOTE: settings as of the 12th jan 2025
    # Buy hyperspace params:
    buy_params = {
        "buy_trend_above_senkou_level": 1,
        "buy_trend_bullish_level": 6,
        "buy_fan_magnitude_shift_value": 3,
        "buy_min_fan_magnitude_gain": 1.002 # NOTE: Good value (Win% ~70%), alot of trades
        #"buy_min_fan_magnitude_gain": 1.008 # NOTE: Very save value (Win% ~90%), only the biggest moves 1.008,
    }

    # Sell hyperspace params:
    # NOTE: was 15m but kept bailing out in dryrun
    sell_params = {
        "sell_trend_indicator": "trend_close_2h",
    }

    # ROI table:
    minimal_roi = {
        "0": 0.059,
        "10": 0.037,
        "41": 0.012,
        "114": 0
    }

    # Stoploss:
    stoploss = -0.275

    # Optimal timeframe for the strategy
    timeframe = '15m'

    # Why 96?
    # On a 15m timeframe, there are 96 candles in 24 hours (24 hours * 60 minutes / 15 minutes).
    startup_candle_count = 96
    process_only_new_candles = False

    trailing_stop = False
    #trailing_stop_positive = 0.002
    #trailing_stop_positive_offset = 0.025
    #trailing_only_offset_is_reached = True

    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    plot_config = {
        'main_plot': {
            # fill area between senkou_a and senkou_b
            'senkou_a': {
                'color': 'green', #optional
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud', #optional
                'fill_color': 'rgba(255,76,46,0.2)', #optional
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {},
            'trend_close_5m': {'color': '#FF5733'},
            'trend_close_15m': {'color': '#FF8333'},
            'trend_close_30m': {'color': '#FFB533'},
            'trend_close_1h': {'color': '#FFE633'},
            'trend_close_2h': {'color': '#E3FF33'},
            'trend_close_4h': {'color': '#C4FF33'},
            'trend_close_6h': {'color': '#61FF33'},
            'trend_close_8h': {'color': '#33FF7D'}
        },
        'subplots': {
            'fan_magnitude': {
                'fan_magnitude': {}
            },
            'fan_magnitude_gain': {
                'fan_magnitude_gain': {}
            }
        }
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['open'] = heikinashi['open']
        dataframe['close'] = heikinashi['close']
        dataframe['high'] = heikinashi['high']
        dataframe['low'] = heikinashi['low']

        dataframe['trend_open_15m'] = dataframe['open']
        dataframe['trend_open_1h'] = ta.EMA(dataframe['open'], timeperiod=4)
        dataframe['trend_open_1d'] = ta.EMA(dataframe['open'], timeperiod=96)
        dataframe['trend_open_1w'] = ta.EMA(dataframe['open'], timeperiod=672)

        dataframe['trend_close_15m'] = dataframe['close']
        dataframe['trend_close_1h'] = ta.EMA(dataframe['close'], timeperiod=4)
        dataframe['trend_close_1d'] = ta.EMA(dataframe['close'], timeperiod=96)
        dataframe['trend_close_1w'] = ta.EMA(dataframe['close'], timeperiod=672)

        dataframe['fan_magnitude'] = (dataframe['trend_close_1h'] / dataframe['trend_close_1d'])
        dataframe['fan_magnitude_gain'] = dataframe['fan_magnitude'] / dataframe['fan_magnitude'].shift(1)

        ichimoku = ftt.ichimoku(dataframe, conversion_line_period=20, base_line_periods=60, laggin_span=120, displacement=30)
        dataframe['chikou_span'] = ichimoku['chikou_span']
        dataframe['tenkan_sen'] = ichimoku['tenkan_sen']
        dataframe['kijun_sen'] = ichimoku['kijun_sen']
        dataframe['senkou_a'] = ichimoku['senkou_span_a']
        dataframe['senkou_b'] = ichimoku['senkou_span_b']
        dataframe['leading_senkou_span_a'] = ichimoku['leading_senkou_span_a']
        dataframe['leading_senkou_span_b'] = ichimoku['leading_senkou_span_b']
        dataframe['cloud_green'] = ichimoku['cloud_green']
        dataframe['cloud_red'] = ichimoku['cloud_red']

        dataframe['atr'] = ta.ATR(dataframe)

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price above key trends
                (dataframe['close'] > dataframe['trend_close_1h']) &
                (dataframe['close'] > dataframe['trend_close_1d']) &

                # Trends are aligned
                (dataframe['trend_close_15m'] > dataframe['trend_close_1h']) &
                (dataframe['trend_close_1h'] > dataframe['trend_close_1d']) &

                # Positive 24-hour price prediction
                (dataframe['price_change_24h'] > 2) &

                # RSI oversold
                (dataframe['rsi'] < 30) &

                # Sufficient volume
                (dataframe['volume'] > dataframe['volume'].rolling(window=10).mean())
            ),
            'buy'
        ] = 1
        return dataframe


    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price below key trends
                (dataframe['close'] < dataframe['trend_close_1h']) &
                (dataframe['close'] < dataframe['trend_close_1d']) &

                # Trends are misaligned (downward trend confirmation)
                (dataframe['trend_close_15m'] < dataframe['trend_close_1h']) &
                (dataframe['trend_close_1h'] < dataframe['trend_close_1d']) &

                # Negative 24-hour price prediction
                (dataframe['price_change_24h'] < -2) &

                # RSI overbought
                (dataframe['rsi'] > 70) &

                # Declining volume
                (dataframe['volume'] < dataframe['volume'].rolling(window=10).mean())
            ),
            'sell'
        ] = 1
        return dataframe
