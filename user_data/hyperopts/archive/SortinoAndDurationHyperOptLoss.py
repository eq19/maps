"""
SortinoAndDurationHyperOptLoss

This module defines the alternative HyperOptLoss class which can be used for
Hyperoptimization.
"""

from datetime import datetime
from math import exp

from pandas import DataFrame

from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_sortino
from freqtrade.optimize.hyperopt import IHyperOptLoss


# Constants
TARGET_TRADES = 600
EXPECTED_MAX_PROFIT = 3.0
MAX_ACCEPTED_TRADE_DURATION = 300


class SortinoAndDurationHyperOptLoss(IHyperOptLoss):
    """
    Defines the loss function for hyperopt.

    This implementation uses the Sortino Ratio calculation and
    penalizes long trade durations.
    """

    @staticmethod
    def hyperopt_loss_function(
        results: DataFrame,
        trade_count: int,
        min_date: datetime,
        max_date: datetime,
        config: Config,
        *args,
        **kwargs,
    ) -> float:
        """
        Objective function, returns smaller number for more optimal results.

        Uses Sortino Ratio calculation and trade duration penalties.
        """
        starting_balance = config["dry_run_wallet"]
        sortino_ratio = calculate_sortino(results, min_date, max_date, starting_balance)

        # Additional penalties for trade duration
        total_profit = results["profit_ratio"].sum()
        trade_duration = results["trade_duration"].mean()

        trade_loss = 1 - 0.25 * exp(-((trade_count - TARGET_TRADES) ** 2) / 10**5.8)
        profit_loss = max(0, 1 - total_profit / EXPECTED_MAX_PROFIT)
        duration_loss = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)

        duration_penalty = trade_loss + profit_loss + duration_loss

        # Return combined loss: negative Sortino ratio + duration penalty
        return -sortino_ratio + duration_penalty


# Create an alias for this to allow the legacy method to work as well.
DefaultHyperOptLoss = SortinoAndDurationHyperOptLoss