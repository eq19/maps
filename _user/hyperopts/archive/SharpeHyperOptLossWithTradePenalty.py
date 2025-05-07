"""
SharpeHyperOptLossWithTradePenalty

This module defines the alternative HyperOptLoss class which can be used for
Hyperoptimization.
"""

from datetime import datetime
from pandas import DataFrame
from math import exp
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_sharpe
from freqtrade.optimize.hyperopt import IHyperOptLoss

# 15-Minute Timeframe
DRAWDOWN_MULT = 0.12
TARGET_TRADES = 1500
EXPECTED_MAX_PROFIT = 1.2
MAX_ACCEPTED_TRADE_DURATION = 900  # 15 minutes

class SharpeHyperOptLossWithTradePenalty(IHyperOptLoss):
    """
    Defines the loss function for hyperopt.

    This implementation uses the Sharpe Ratio calculation with a trade distribution penalty.
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

        Uses Sharpe Ratio calculation with a penalty for unbalanced trade distribution.
        """
        starting_balance = config["dry_run_wallet"]
        sharpe_ratio = calculate_sharpe(results, min_date, max_date, starting_balance)

        trade_duration = results["trade_duration"].mean()

        # Trade Duration component
        duration_penalty = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)

        # Trade Count and Profit component
        trade_loss = 1 - 0.25 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - (results["profit_ratio"].sum() / EXPECTED_MAX_PROFIT))

        # Penalty for unbalanced trade distribution
        trade_counts = results['pair'].value_counts()
        avg_trades = trade_counts.mean()
        trade_distribution_penalty = sum(abs(trade_count - avg_trades) for trade_count in trade_counts) / len(trade_counts)

        # Combine Sharpe ratio and trade distribution penalty
        combined_loss = -sharpe_ratio + duration_penalty + trade_loss #+ profit_loss #+ trade_distribution_penalty

        return combined_loss
