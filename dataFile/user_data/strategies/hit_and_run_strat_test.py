# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
# --------------------------------
import talib.abstract as ta
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib
# ---------- Commands -----------
# Commands for backtesting etc.:
# /opt/freqtrade/.env/bin/freqtrade backtesting --config user_data/configs/backtest_conf.json --strategy new_strat
# /opt/freqtrade/.env/bin/freqtrade backtesting --config user_data/configs/backtest_conf.json --timerange=20210201-20210310 --strategy new_strat --export trades --export-filename=user_data/backtest_results/simple_strat_30m_test.json
# /opt/freqtrade/.env/bin/freqtrade plot-dataframe --config user_data/configs/backtest_conf.json --strategy new_strat  --export-filename=user_data/backtest_results/new_strat-2021-05-13_19-29-25.json
# /opt/freqtrade/.env/bin/freqtrade plot-profit --config user_data/configs/backtest_conf.json  --strategy new_strat --export-filename=user_data/backtest_results/new_strat-2021-05-13_19-29-25.json
# --------------------------------

class hit_and_run_strat_test(IStrategy):
    stoploss = -0.009
    timeframe = "1d"

    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }
    
    # # Trailing stoploss
    # trailing_stop = True
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.009
    # trailing_stop_positive_offset = 0.01
    # Trailing stoploss
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.01

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Indicatoren
        # dataframe['supertrend'] = pta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], length=7, multiplier=2.0)['SUPERT_7_2.0']
        dataframe['supertrend'] = pta.supertrend(high=dataframe['high'], low=dataframe['low'], close=dataframe['close'], length=10, multiplier=3.5)['SUPERT_10_3.5']

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe['close'] > dataframe['supertrend'])
            ),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe['close'] < dataframe['supertrend'])            ),
            "sell",
        ] = 1
        return dataframe


