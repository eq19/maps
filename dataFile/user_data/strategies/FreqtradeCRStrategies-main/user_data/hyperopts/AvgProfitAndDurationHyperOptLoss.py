from datetime import datetime
from math import exp
from typing import Dict

from pandas import DataFrame

from freqtrade.optimize.hyperopt import IHyperOptLoss


# Define some constants:

# set TARGET_TRADES to suit your number concurrent trades so its realistic
# to the number of days
# TARGET_TRADES = 600
# This is assumed to be expected avg profit * expected trade count.
# For example, for 0.35% avg per trade (or 0.0035 as ratio) and 1100 trades,
# self.expected_max_profit = 3.85
# Check that the reported Σ% values do not exceed this!
# Note, this is ratio. 3.85 stated above means 385Σ%.
# EXPECTED_MAX_PROFIT = 3.0

# max average trade duration in minutes
# if eval ends with higher value, we consider it a failed eval
# MAX_ACCEPTED_TRADE_DURATION = 300


class AvgProfitAndDurationHyperOptLoss(IHyperOptLoss):
    """
    Defines the default loss function for hyperopt
    This is intended to give you some inspiration for your own loss function.

    The Function needs to return a number (float) - which becomes smaller for better backtest
    results.
    """

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Dict, processed: Dict[str, DataFrame],
                               *args, **kwargs) -> float:
        """
        Objective function, returns smaller number for better results
        """

        average_profit = results['profit_abs'].mean()
        average_profit_loss = -1 * average_profit

        trade_duration = results['profit_abs'].sum() / results['trade_duration'].sum()
        trade_duration_loss = -1 * trade_duration

        return average_profit_loss + trade_duration_loss
