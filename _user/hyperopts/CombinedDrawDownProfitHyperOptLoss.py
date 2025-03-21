"""
CombinedDrawDownProfitHyperOptLoss

This module defines the combined HyperOptLoss class which can be used for
Hyperoptimization, combining MaxDrawDownRelativeHyperOptLoss and ProfitDrawDownHyperOptLoss.
"""

from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_max_drawdown, calculate_underwater
from freqtrade.optimize.hyperopt import IHyperOptLoss

# Smaller numbers penalize drawdowns more severely
DRAWDOWN_MULT = 0.075

class CombinedDrawDownProfitHyperOptLoss(IHyperOptLoss):
    """
    Defines the combined loss function for hyperopt.

    This implementation optimizes for both max drawdown, relative drawdown, and profit.
    """

    @staticmethod
    def hyperopt_loss_function(
        results: DataFrame,
        config: Config,
        *args,
        **kwargs,
    ) -> float:
        """
        Objective function.

        Combines logic of both max drawdown relative and profit drawdown loss functions.
        """
        total_profit = results["profit_abs"].sum()

        try:
            # Calculate drawdowns
            drawdown_df = calculate_underwater(
                results, value_col="profit_abs", starting_balance=config["dry_run_wallet"]
            )
            max_drawdown = abs(min(drawdown_df["drawdown"]))
            relative_drawdown = max(drawdown_df["drawdown_relative"])

            drawdown = calculate_max_drawdown(
                results, starting_balance=config["dry_run_wallet"], value_col="profit_abs"
            )
            relative_account_drawdown = drawdown.relative_account_drawdown

            if max_drawdown == 0:
                max_drawdown_loss = -total_profit
            else:
                max_drawdown_loss = -total_profit / max_drawdown / relative_drawdown

            profit_drawdown_loss = -1 * (
                total_profit - (relative_account_drawdown * total_profit) * (1 - DRAWDOWN_MULT)
            )

            # Combine both losses (you can adjust the weights if needed)
            combined_loss = max_drawdown_loss + profit_drawdown_loss
            return combined_loss

        except (Exception, ValueError):
            return -total_profit