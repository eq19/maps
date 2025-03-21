from datetime import datetime
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_sharpe, calculate_sortino
from freqtrade.optimize.hyperopt import IHyperOptLoss

class SharpeSortinoCombinedHyperOptLoss(IHyperOptLoss):
    """
    Defines a combined loss function for hyperopt.

    This implementation uses both Sharpe Ratio and Sortino Ratio calculations.
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
        Objective function, returns a smaller number for more optimal results.

        Combines Sharpe Ratio and Sortino Ratio calculations.
        """
        starting_balance = config["dry_run_wallet"]
        
        # Calculate Sharpe Ratio
        sharp_ratio = calculate_sharpe(results, min_date, max_date, starting_balance)
        
        # Calculate Sortino Ratio
        sortino_ratio = calculate_sortino(results, min_date, max_date, starting_balance)
        
        # Combine the two ratios
        combined_metric = (sharp_ratio + sortino_ratio) / 2
        
        # Return the negative combined metric for optimization
        return -combined_metric
