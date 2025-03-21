from datetime import datetime
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_max_drawdown, calculate_calmar
from freqtrade.optimize.hyperopt import IHyperOptLoss

# Define constants for trade duration and drawdown control
TARGET_TRADES = 1500
EXPECTED_MAX_PROFIT = 1.2
MAX_ACCEPTED_TRADE_DURATION = 900

class TradeDurDrawDownCombinedHyperOptLoss(IHyperOptLoss):
    """
    Defines a combined loss function for hyperopt, optimizing for profit while controlling
    for both maximum drawdown and Calmar Ratio.
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
            max_drawdown = calculate_max_drawdown(
                results, starting_balance=config["dry_run_wallet"], value_col="profit_abs"
            ).drawdown_abs
        except ValueError:
            max_drawdown = 1  # Avoid division by zero

        # Calculate Calmar Ratio
        starting_balance = config["dry_run_wallet"]
        calmar_ratio = calculate_calmar(results, min_date, max_date, starting_balance)

        # Define constants for weighting
        CALMAR_WEIGHT = 0.5
        DRAWDOWN_WEIGHT = 0.5
        
        # Penalize based on Calmar Ratio and Drawdown
        calmar_loss = -calmar_ratio  # More negative is worse
        drawdown_loss = -total_profit / max_drawdown if max_drawdown != 0 else -total_profit
        
        # Combine losses
        result = (CALMAR_WEIGHT * calmar_loss) + (DRAWDOWN_WEIGHT * drawdown_loss)
        
        return result
