# Commands for backtesting etc.:
# /opt/freqtrade/.env/bin/freqtrade backtesting --config user_data/configs/backtest_conf.json --timerange=20210201-20210310 --strategy simple_strat_30m_test
# /opt/freqtrade/.env/bin/freqtrade backtesting --config user_data/configs/backtest_conf.json --timerange=20210201-20210310 --strategy simple_strat_30m_test --export trades --export-filename=user_data/backtest_results/simple_strat_30m_test.json
# /opt/freqtrade/.env/bin/freqtrade plot-dataframe --config user_data/configs/backtest_conf.json --strategy simple_strat_30m_test  --export-filename=user_data/backtest_results/simple_strat_30m_test-2021-05-13_19-29-25.json
# /opt/freqtrade/.env/bin/freqtrade plot-profit --config user_data/configs/backtest_conf.json  --strategy simple_strat_30m_test --export-filename=user_data/backtest_results/simple_strat_30m_test-2021-05-13_19-29-25.json

# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame

# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class keep_simple_strat_30m_test_copy_2336(IStrategy):
    stoploss = -0.25
    timeframe = "30m"

    order_types = {
        "buy": "limit",
        "sell": "limit",
        "emergencysell": "market",
        "stoploss": "market",
        "stoploss_on_exchange": True,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_limit_ratio": 0.99,
    }

   # Trailing stoploss
    trailing_stop = True
    # trailing_only_offset_is_reached = True
    # trailing_stop_positive = 0.2
    # trailing_stop_positive_offset = 0.24

    minimal_roi = {
        "0": 0.34543,
        "73": 0.11828,
        "124": 0.05279,
        "350": 0
    }
#     minimal_roi = {
#         "60": 0.7,  # Take profit when price rises 8% after 1 hour
 #        "120": 0.06,  # Take profit when price rises 7% after 1 hours
  #       "180": 0.05,  # Take profit when price rises 7% after 3 hours
   #      "240": 0.04,  # Take profit when price rises 5% after 4 hours
    #     "600": 0.035,  # Take profit when price rises 4,5% after 10 hours
 #        "630": 0.012,  # Take profit when price rises 1,2% after 11 hours
 #        "0": 0.5  # Just take profit when price rises 15%
  #   }

    plot_config = {
        "main_plot": {
            "SMA": {"color": "red"},
        },
        "subplots": {
            "STOCH": {
                "slowd": {"color": "blue"},
                "slowk": {"color": "orange"},
            },
            "RSI":{
                "RSI": {"color": "blue"},
                "RSI_SMA": {"color": "orange"},
            } 
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Instapsignalen
        dataframe["RSI"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["RSI_SMA"] = dataframe["RSI"].rolling(window=50).mean()

        dataframe["SMA"] = ta.SMA(dataframe, timeperiod=23)

        stoch = ta.STOCH(
            dataframe,
            fastk_period=14,
            slowk_period=4,
            slowk_matype=0,
            slowd_period=6,
            slowd_matype=0,
        )
        dataframe['slowd'] = stoch['slowd']
        dataframe['slowk'] = stoch['slowk']

        dataframe['stoch_sell_cross']=(dataframe['slowd']>75)&(dataframe['slowk']>75)&(qtpylib.crossed_above(dataframe['slowd'], dataframe['slowk']))
        # dataframe['stoch_sell_cross']=(dataframe['slowd']>75)&(dataframe['slowk']>75)&(dataframe['slowk']<dataframe['slowd'])
        
        # Uitstapsignalen
        dataframe['last_lowest'] = dataframe['low'].rolling(100).min().shift(1)
        dataframe['lower_low'] = dataframe['close'] < dataframe['last_lowest']

        # Print stuff
        # print(dataframe[['date','close','low','last_lowest','lower_low']].loc[dataframe['lower_low'] == True].tail(55))
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe["close"] > dataframe["SMA"])
            #& (dataframe['growing_sma'])
            & (dataframe["RSI"] > dataframe["RSI_SMA"])
            # & (dataframe["slowd"] < 60)
            ),
            "buy",
        ] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
            (dataframe['stoch_sell_cross']==True)
            |(dataframe['lower_low'] == True)
            ),
            "sell",
        ] = 1
        return dataframe
