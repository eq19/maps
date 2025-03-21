from datetime import datetime
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_max_drawdown, calculate_sharpe, calculate_sortino
from freqtrade.optimize.hyperopt import IHyperOptLoss

# Define a drawdown multiplier to penalize drawdown
DRAWDOWN_MULT = 0.12

class DefaultSpaceCombinedHyperOptLoss(IHyperOptLoss):
    """
    Combined loss function considering Profit, Drawdown, Sharpe ratio, and Sortino ratio.
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
        # Calculate total profit
        total_profit = results["profit_abs"].sum()

        # Calculate maximum drawdown
        try:
            drawdown = calculate_max_drawdown(
                results, starting_balance=config["dry_run_wallet"], value_col="profit_abs"
            )
            relative_account_drawdown = drawdown.relative_account_drawdown
        except ValueError:
            relative_account_drawdown = 0

        # Calculate Sharpe ratio
        sharpe_ratio = calculate_sharpe(results, min_date, max_date, config["dry_run_wallet"])

        # Calculate Sortino ratio
        sortino_ratio = calculate_sortino(results, min_date, max_date, config["dry_run_wallet"])

        # Combine the loss components
        profit_drawdown_component = total_profit - (relative_account_drawdown * total_profit) * (1 - DRAWDOWN_MULT)
        sharpe_sortino_component = sharpe_ratio + sortino_ratio

        # The combined loss function: higher is better, so negate it
        return -1 * (profit_drawdown_component + sharpe_sortino_component)
