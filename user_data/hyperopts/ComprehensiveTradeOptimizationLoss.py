from datetime import datetime
from typing import Any, Dict
from math import exp
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.data.metrics import calculate_max_drawdown

# # 5-Minute Timeframe
# DRAWDOWN_MULT = 0.15
# TARGET_TRADES = 2000
# EXPECTED_MAX_PROFIT = 1.0
# MAX_ACCEPTED_TRADE_DURATION = 300  # 5 minutes

# 15-Minute Timeframe
DRAWDOWN_MULT = 0.12
TARGET_TRADES = 1500
EXPECTED_MAX_PROFIT = 1.2
MAX_ACCEPTED_TRADE_DURATION = 900  # 15 minutes

# # 1-Hour Timeframe
# DRAWDOWN_MULT = 0.1
# TARGET_TRADES = 1000
# EXPECTED_MAX_PROFIT = 1.5
# MAX_ACCEPTED_TRADE_DURATION = 3600  # 1 hour

class ComprehensiveTradeOptimizationLoss(IHyperOptLoss):
    """
    Combined loss function for optimizing:
    - Total Profit
    - Drawdown
    - Trade Duration Efficiency
    """

    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int,
                               min_date: datetime, max_date: datetime,
                               config: Config, processed: Dict[str, DataFrame],
                               backtest_stats: Dict[str, Any],
                               *args, **kwargs) -> float:
        
        profit_weight   = 0.3
        duration_weight = 0.25
        trade_weight    = 0.25
        drawdown_weight = 0.2
        # trade_distribution_weight = 0.167
    
        total_profit = results["profit_abs"].sum()
        trade_duration = results["trade_duration"].mean()

        # Calculate drawdown
        try:
            drawdown = calculate_max_drawdown(
                results, starting_balance=config["dry_run_wallet"], value_col="profit_abs"
            )
            relative_drawdown = drawdown.relative_account_drawdown
        except ValueError:
            relative_drawdown = 0

        # Profit and Drawdown component
        profit_drawdown_score = -1 * (
            total_profit - (relative_drawdown * total_profit) * (1 - DRAWDOWN_MULT)
        )

        # Trade Duration component
        duration_penalty = 0.4 * min(trade_duration / MAX_ACCEPTED_TRADE_DURATION, 1)

        # Trade Count and Profit component
        trade_loss = 1 - 0.25 * exp(-(trade_count - TARGET_TRADES) ** 2 / 10 ** 5.8)
        profit_loss = max(0, 1 - (results["profit_ratio"].sum() / EXPECTED_MAX_PROFIT))

        # Penalty for unbalanced trade distribution
        trade_counts = results['pair'].value_counts()
        avg_trades = trade_counts.mean()
        trade_distribution_penalty = sum(abs(trade_count - avg_trades) for trade_count in trade_counts) / len(trade_counts)

        # Combine components
        combined_score = (
            profit_weight * profit_loss +
            duration_weight * duration_penalty + 
            trade_weight * trade_loss +
            drawdown_weight * profit_drawdown_score
            # trade_distribution_weight * trade_distribution_penalty
        )
        #combined_score = profit_drawdown_score + duration_penalty + trade_loss + profit_loss + trade_distribution_penalty
        return combined_score

# Create an alias for this loss function to use in hyperopt
DefaultHyperOptLoss = ComprehensiveTradeOptimizationLoss