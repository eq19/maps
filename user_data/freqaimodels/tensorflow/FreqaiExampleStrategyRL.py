import logging
from functools import reduce

import pandas as pd
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.strategy import CategoricalParameter, IStrategy, merge_informative_pair


logger = logging.getLogger(__name__)


class FreqaiExampleStrategyRL(IStrategy):
    """
    Example strategy showing how the user connects their own
    IFreqaiModel to the strategy. Namely, the user uses:
    self.freqai.start(dataframe, metadata)

    to make predictions on their data. populate_any_indicators() automatically
    generates the variety of features indicated by the user in the
    canonical freqtrade configuration file under config['freqai'].
    """

    minimal_roi = {"0": 0.1, "240": -1}

    plot_config = {
        "main_plot": {},
        "subplots": {
            "prediction": {"prediction": {"color": "blue"}},
            "do_predict": {
                "do_predict": {"color": "brown"},
            },
        },
    }

    stoploss = -0.05
    use_exit_signal = True
    # this is the maximum period fed to talib (timeframe independent)
    startup_candle_count: int = 40

    def populate_any_indicators(
        self, pair, df, tf, informative=None, set_generalized_indicators=False
    ):

        if informative is None:
            informative = self.dp.get_pair_dataframe(pair, tf)

        # for t in self.freqai_info["feature_parameters"]["indicator_periods_candles"]:
            # t = int(t)
            # informative[f"%-{pair}rsi-period_{t}"] = ta.RSI(informative, timeperiod=t)
            # informative[f"%-{pair}mfi-period_{t}"] = ta.MFI(informative, timeperiod=t)
            # informative[f"%-{pair}adx-period_{t}"] = ta.ADX(informative, window=t)

        informative[f"%-{pair}raw_close"] = informative["close"]
        informative[f"%-{pair}raw_open"] = informative["open"]
        informative[f"%-{pair}raw_high"] = informative["high"]
        informative[f"%-{pair}raw_low"] = informative["low"]

        indicators = [col for col in informative if col.startswith("%")]
        # for n in range(self.freqai_info["feature_parameters"]["include_shifted_candles"] + 1):
            # if n == 0:
                # continue
            # informative_shift = informative[indicators].shift(n)
            # informative_shift = informative_shift.add_suffix("_shift-" + str(n))
            # informative = pd.concat((informative, informative_shift), axis=1)

        df = merge_informative_pair(df, informative, self.config["timeframe"], tf, ffill=True)
        skip_columns = [
            (s + "_" + tf) for s in ["date", "open", "high", "low", "close", "volume"]
        ]
        df = df.drop(columns=skip_columns)

        # Add generalized indicators here (because in live, it will call this
        # function to populate indicators during training). Notice how we ensure not to
        # add them multiple times
        if set_generalized_indicators:

            # For RL, there are no direct targets to set. This is filler (neutral)
            # until the agent sends an action.
            df["&-action"] = 0

        return df

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.freqai.start(dataframe, metadata, self)
        return dataframe

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:

        enter_long_conditions = [df["do_predict"] == 1, df["&-action"] == 1]

        if enter_long_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_long_conditions), ["enter_long", "enter_tag"]
            ] = (1, "long")

        enter_short_conditions = [df["do_predict"] == 1, df["&-action"] == 3]

        if enter_short_conditions:
            df.loc[
                reduce(lambda x, y: x & y, enter_short_conditions), ["enter_short", "enter_tag"]
            ] = (1, "short")

        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        exit_long_conditions = [df["do_predict"] == 1, df["&-action"] == 2]
        if exit_long_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_long_conditions), "exit_long"] = 1

        exit_short_conditions = [df["do_predict"] == 1, df["&-action"] == 4]
        if exit_short_conditions:
            df.loc[reduce(lambda x, y: x & y, exit_short_conditions), "exit_short"] = 1

        return df

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time,
        entry_tag,
        side: str,
        **kwargs,
    ) -> bool:

        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = df.iloc[-1].squeeze()

        if side == "long":
            if rate > (last_candle["close"] * (1 + 0.0025)):
                return False
        else:
            if rate < (last_candle["close"] * (1 - 0.0025)):
                return False

        return True
