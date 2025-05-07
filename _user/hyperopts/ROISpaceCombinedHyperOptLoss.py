from datetime import datetime
from pandas import DataFrame
from freqtrade.constants import Config
from freqtrade.data.metrics import calculate_sharpe, calculate_sortino, calculate_underwater
from freqtrade.optimize.hyperopt import IHyperOptLoss
from freqtrade.persistence import Trade


class ROISpaceCombinedHyperOptLoss(IHyperOptLoss):
    """
    Defines the combined loss function for hyperopt.

    This implementation uses weighted profit, Sharpe ratio, Sortino ratio, and drawdown.
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
        profit_weight = 0.4
        sharpe_weight = 0.3
        sortino_weight = 0.2
        drawdown_weight = 0.1

        starting_balance = config["dry_run_wallet"]

        # Calculate profit
        total_profit = results["profit_abs"].sum()
        profit_loss = -total_profit

        # Calculate Sharpe ratio
        sharpe_ratio = calculate_sharpe(results, min_date, max_date, starting_balance)
        sharpe_loss = -sharpe_ratio

        # Calculate Sortino ratio
        sortino_ratio = calculate_sortino(results, min_date, max_date, starting_balance)
        sortino_loss = -sortino_ratio

        # Calculate drawdown
        try:
            drawdown_df = calculate_underwater(results, value_col="profit_abs", starting_balance=starting_balance)
            max_drawdown = abs(min(drawdown_df["drawdown"]))
            relative_drawdown = max(drawdown_df["drawdown_relative"])
            drawdown_loss = -total_profit / max_drawdown / relative_drawdown if max_drawdown != 0 else profit_loss
        except (Exception, ValueError):
            drawdown_loss = profit_loss

        # Combine losses with weights
        combined_loss = (
            profit_weight * profit_loss +
            sharpe_weight * sharpe_loss +
            sortino_weight * sortino_loss +
            drawdown_weight * drawdown_loss
        )

        return combined_loss
    

    def get_minimal_roi(self, trade: Trade) -> dict:
        pair = trade.pair
        custom_roi = self.custom_params.get(pair, self.minimal_roi).get("minimal_roi", self.minimal_roi)
        print(custom_roi)
        return custom_roi
