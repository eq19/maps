"""
ProfitDrawDownHyperOptLossWithTradePenalty

This module defines the alternative HyperOptLoss class based on Profit &
Drawdown objective which can be used for Hyperoptimization, with a trade distribution penalty.

Possible to change `DRAWDOWN_MULT` to penalize drawdown objective for
individual needs.
"""

from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_max_drawdown
from freqtrade.optimize.hyperopt import IHyperOptLoss

# smaller numbers penalize drawdowns more severely
DRAWDOWN_MULT = 0.075

class ProfitDrawDownHyperOptLossWithTradePenalty(IHyperOptLoss):
    @staticmethod
    def hyperopt_loss_function(results: DataFrame, config: Config, *args, **kwargs) -> float:
        total_profit = results["profit_abs"].sum()

        try:
            drawdown = calculate_max_drawdown(
                results, starting_balance=config["dry_run_wallet"], value_col="profit_abs"
            )
            relative_account_drawdown = drawdown.relative_account_drawdown
        except ValueError:
            relative_account_drawdown = 0

        # Penalty for unbalanced trade distribution
        trade_counts = results['pair'].value_counts()
        avg_trades = trade_counts.mean()
        trade_distribution_penalty = sum(abs(trade_count - avg_trades) for trade_count in trade_counts) / len(trade_counts)

        return -1 * (
            total_profit - (relative_account_drawdown * total_profit) * (1 - DRAWDOWN_MULT)
        ) + trade_distribution_penalty
