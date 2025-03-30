from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_underwater
from freqtrade.optimize.hyperopt import IHyperOptLoss


class MaxDrawDownRelativeHyperOptLossWithTradePenalty(IHyperOptLoss):
    """
    Defines the loss function for hyperopt.

    This implementation optimizes for max draw down and profit
    Less max drawdown more profit -> Lower return value
    """

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, config: Config, *args, **kwargs) -> float:
        """
        Objective function.

        Uses profit ratio weighted max_drawdown when drawdown is available.
        Otherwise directly optimizes profit ratio.
        """
        total_profit = results["profit_abs"].sum()

        # Calculate drawdown
        try:
            drawdown_df = calculate_underwater(
                results, value_col="profit_abs", starting_balance=config["dry_run_wallet"]
            )
            max_drawdown = abs(min(drawdown_df["drawdown"]))
            relative_drawdown = max(drawdown_df["drawdown_relative"])
            if max_drawdown == 0:
                profit_drawdown_ratio = -total_profit
            else:
                profit_drawdown_ratio = -total_profit / max_drawdown / relative_drawdown
        except (Exception, ValueError):
            profit_drawdown_ratio = -total_profit

        # Penalty for unbalanced trade distribution
        trade_counts = results['pair'].value_counts()
        avg_trades = trade_counts.mean()
        trade_distribution_penalty = sum(abs(trade_count - avg_trades) for trade_count in trade_counts) / len(trade_counts)

        # Combine profit/drawdown ratio and trade distribution penalty
        loss_value = profit_drawdown_ratio + trade_distribution_penalty

        return loss_value
