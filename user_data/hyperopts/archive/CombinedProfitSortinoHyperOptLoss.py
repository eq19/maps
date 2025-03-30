"""
CombinedProfitSortinoHyperOptLoss

This module defines the combined HyperOptLoss class which can be used for
Hyperoptimization, combining OnlyProfitHyperOptLoss and SortinoHyperOptLoss.
"""

from datetime import datetime
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_sortino
from freqtrade.optimize.hyperopt import IHyperOptLoss

MAX_ACCEPTED_TRADE_DURATION = 900  # 15 minutes

class CombinedProfitSortinoHyperOptLoss(IHyperOptLoss):
    """
    Defines the combined loss function for hyperopt.

    This implementation optimizes for both absolute profit and Sortino Ratio.
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
        Objective function.

        Combines logic of both absolute profit and Sortino Ratio loss functions.
        """
        total_profit = results["profit_abs"].sum()
        starting_balance = config["dry_run_wallet"]

        # Calculate Sortino Ratio
        sortino_ratio = calculate_sortino(results, min_date, max_date, starting_balance)

        # Trade Duration component
        trade_duration = results["trade_duration"].mean()
        duration_penalty = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)

        # Combine both losses (you can adjust the weights if needed)
        combined_loss = -1 * total_profit - sortino_ratio - duration_penalty
        return combined_loss