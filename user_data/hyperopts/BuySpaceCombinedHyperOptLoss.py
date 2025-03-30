from pandas import DataFrame
from freqtrade.optimize.hyperopt import IHyperOptLoss

class BuySpaceCombinedHyperOptLoss(IHyperOptLoss):
    @staticmethod
    def hyperopt_loss_function(results: DataFrame, trade_count: int, *args, **kwargs) -> float:
        total_profit = results["profit_abs"].sum()
        trade_duration = results["trade_duration"].mean()
        duration_loss = 0.4 * min(trade_duration / 300, 1)
        return -1 * total_profit + duration_loss
