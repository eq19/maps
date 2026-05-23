import logging

import numpy as np
import torch as th

from freqtrade.freqai.prediction_models.ReinforcementLearner_multiproc import (
    ReinforcementLearner_multiproc,
)
from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions


logger = logging.getLogger(__name__)


class RLDayTrader_multiproc(ReinforcementLearner_multiproc):
    """
    Multi-process version of RLDayTrader.

    Uses SubprocVecEnv for parallel environment training.
    Same MyRLEnv (compressed reward + leverage) as RLDayTrader.

    Note: Tensorboard metrics are unreliable with multiple environments
    (see ReinforcementLearner_multiproc.py line 82-83).
    Use single-env RLDayTrader for reward debugging, then switch to
    this multiproc version for production training.

    Usage:
      freqtrade backtesting --strategy RLDayTradeStrategy \
        --config user_data/config_daytrade.json \
        --freqaimodel RLDayTrader_multiproc \
        --timerange 20240101-20260101 --export trades
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        # Override max_threads cap (base class limits to system_threads/2)
        configured_cpu_count = self.freqai_info["rl_config"].get("cpu_count", 1)
        if configured_cpu_count > self.max_threads:
            logger.info(
                f"RLDayTrader_multiproc: Overriding max_threads from "
                f"{self.max_threads} to {configured_cpu_count}"
            )
            self.max_threads = configured_cpu_count
            th.set_num_threads(self.max_threads)

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom 4-action environment for leveraged intraday trading.
        Identical reward logic to RLDayTrader.MyRLEnv.
        Reward compressed to [-10, +10].
        """

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.leverage = self.rl_config.get("leverage", 10.0)
            self.liquidation_buffer = self.rl_config.get("liquidation_buffer", 0.025)
            self._is_liquidated = False

        def reset(self, seed=None):
            self._is_liquidated = False
            return super().reset(seed)

        def get_unrealized_profit(self) -> float:
            if self._last_trade_tick is None or self._position == Positions.Neutral:
                return 0.0

            if self._position == Positions.Short:
                cp = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                tp = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (tp - cp) / tp
            else:
                cp = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                tp = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (cp - tp) / tp

            return base_pnl * self.leverage

        def _get_base_pnl(self) -> float:
            if self._last_trade_tick is None or self._position == Positions.Neutral:
                return 0.0

            if self._position == Positions.Short:
                cp = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                tp = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                return (tp - cp) / tp
            else:
                cp = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                tp = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                return (cp - tp) / tp

        def _check_liquidation(self) -> bool:
            if self._position == Positions.Neutral or self._is_liquidated:
                return False

            base_pnl = self._get_base_pnl()
            threshold = -(1.0 / self.leverage - self.liquidation_buffer)

            if base_pnl <= threshold:
                self._is_liquidated = True
                self._position = Positions.Neutral
                self._total_profit *= (1 + threshold)
                return True

            return False

        def calculate_reward(self, action: int) -> float:
            """
            Compressed reward [-10, +10] identical to RLDayTrader.MyRLEnv.
            Duplicated here because SubprocVecEnv requires the env class
            to be defined in the same module as the model.
            """
            if self._check_liquidation():
                self.tensorboard_log("liquidation", category="risk")
                return -10.0

            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return -2.0

            pnl = self.get_unrealized_profit()
            profit_aim = self.profit_aim * self.rr
            max_dur = self.rl_config.get("max_trade_duration_candles", 48)

            # Neutral while Neutral
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return 0.0

            # Enter trade
            if (
                action in (Actions.Long_enter.value, Actions.Short_enter.value)
                and self._position == Positions.Neutral
            ):
                return 0.0

            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            # Holding position
            if (
                self._position in (Positions.Short, Positions.Long)
                and action == Actions.Neutral.value
            ):
                if pnl >= 0:
                    hold_reward = float(np.clip(pnl * 20.0, 0.0, 2.0))
                elif abs(pnl) < profit_aim:
                    hold_reward = float(np.clip(pnl * 30.0, -3.0, 0.0))
                else:
                    hold_reward = float(np.clip(pnl * 50.0, -5.0, 0.0))

                if max_dur > 0 and trade_duration > max_dur * 0.7:
                    hold_reward -= 1.0

                return float(np.clip(hold_reward, -10.0, 10.0))

            # Exit action
            if action == Actions.Exit.value and self._position in (
                Positions.Long,
                Positions.Short,
            ):
                if pnl > 0:
                    exit_reward = float(np.clip(pnl * 50.0, 1.0, 8.0))
                    if max_dur > 0 and trade_duration < max_dur * 0.3:
                        exit_reward += 2.0
                elif pnl == 0 or abs(pnl) < profit_aim:
                    exit_reward = -1.0
                elif abs(pnl) < profit_aim * 2:
                    ratio = (abs(pnl) - profit_aim) / profit_aim if profit_aim > 0 else 0
                    exit_reward = -1.0 - 4.0 * ratio
                elif abs(pnl) < profit_aim * 3:
                    exit_reward = -8.0
                else:
                    exit_reward = -10.0

                pos = "long" if self._position == Positions.Long else "short"
                self.tensorboard_log(f"{pos}_exit_pnl", value=pnl, category="pnl")
                self.tensorboard_log("exit_pnl", value=pnl, category="pnl")
                if pnl > 0:
                    self.tensorboard_log("profitable_exit", category="pnl")
                else:
                    self.tensorboard_log("loss_exit", category="pnl")
                self.tensorboard_log("exit_reward", value=exit_reward, category="rewards")
                self.tensorboard_log("trade_duration", value=trade_duration, category="rewards")

                return float(np.clip(exit_reward, -10.0, 10.0))

            return 0.0
