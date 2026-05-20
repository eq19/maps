import logging

import numpy as np

from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions


logger = logging.getLogger(__name__)


class RLDayTrader(ReinforcementLearner):
    """
    RL Day Trade Model with compressed reward [-10, +10] and leverage simulation.

    Inherits from ReinforcementLearner (Base5ActionRLEnv) and overrides MyRLEnv
    with a Base4ActionRLEnv customised for intraday leveraged futures trading.

    Key differences from existing models:
    - Compressed reward range [-10, +10] for stable training gradients
    - No entry reward (0) to prevent overtrading exploit
    - Asymmetric loss penalty (penalize losses harder than reward gains)
    - Time-aware exit rewards (quick profitable exits get bonus)
    - Liquidation check with configurable buffer

    rl_config custom parameters:
      leverage            (float) default 10.0
      liquidation_buffer  (float) default 0.025

    Usage:
      freqtrade backtesting --strategy RLDayTradeStrategy \
        --config user_data/config_daytrade.json \
        --freqaimodel RLDayTrader \
        --timerange 20240101-20260101 --export trades
    """

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom 4-action environment for leveraged intraday trading.
        Reward compressed to [-10, +10] following design doc Section 6.2.
        """

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.leverage = self.rl_config.get("leverage", 10.0)
            self.liquidation_buffer = self.rl_config.get("liquidation_buffer", 0.025)
            self._is_liquidated = False

        def reset(self, seed=None):
            self._is_liquidated = False
            return super().reset(seed)

        # --------------------------------------------------------------
        # Leverage-aware PNL
        # --------------------------------------------------------------

        def get_unrealized_profit(self) -> float:
            """Return unrealized PNL amplified by leverage."""
            if self._last_trade_tick is None or self._position == Positions.Neutral:
                return 0.0

            if self._position == Positions.Short:
                current_price = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (last_trade_price - current_price) / last_trade_price
            else:  # Long
                current_price = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (current_price - last_trade_price) / last_trade_price

            return base_pnl * self.leverage

        # --------------------------------------------------------------
        # Liquidation
        # --------------------------------------------------------------

        def _get_base_pnl(self) -> float:
            """Return base (non-leveraged) PNL for liquidation check."""
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
            """
            Check if position should be liquidated.

            Liquidation threshold = -(1/leverage - buffer).
            For leverage=10, buffer=0.025: threshold = -0.075 (-7.5% base PNL).
            """
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

        # --------------------------------------------------------------
        # Reward function  (compressed to [-10, +10])
        # --------------------------------------------------------------

        def calculate_reward(self, action: int) -> float:
            """
            Compressed reward function per design doc Section 6.2.

            All rewards are clamped to [-10, +10].

            Scenario mapping:
              Liquidation                          -> -10
              Invalid action                       -> -2
              Neutral while Neutral                -> 0
              Enter trade                          -> 0
              Holding + profitable                 -> clamp(pnl * 20, 0, 2)
              Holding + small loss (< aim)         -> clamp(pnl * 30, -3, 0)
              Holding + large loss (>= aim)        -> clamp(pnl * 50, -5, 0)
              Holding + duration > 70% max         -> additional -1
              Exit + profit                        -> clamp(pnl * 50, 1, 8)
              Exit + quick profit (< 30% max_dur)  -> above + 2
              Exit + small loss (> -aim)           -> -1
              Exit + medium loss (> -2x aim)       -> linear(-1, -5)
              Exit + large loss (> -3x aim)        -> -8
            """
            # --- Liquidation check (highest priority) ---
            if self._check_liquidation():
                self.tensorboard_log("liquidation", category="risk")
                return -10.0

            # --- Invalid action ---
            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return -2.0

            pnl = self.get_unrealized_profit()
            profit_aim = self.profit_aim * self.rr
            max_dur = self.rl_config.get("max_trade_duration_candles", 48)

            # --- Neutral while Neutral ---
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return 0.0

            # --- Enter trade ---
            if (
                action in (Actions.Long_enter.value, Actions.Short_enter.value)
                and self._position == Positions.Neutral
            ):
                return 0.0

            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            # --- Holding position (Neutral action while in position) ---
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

                # Duration penalty
                if max_dur > 0 and trade_duration > max_dur * 0.7:
                    hold_reward -= 1.0

                return float(np.clip(hold_reward, -10.0, 10.0))

            # --- Exit action ---
            if action == Actions.Exit.value and self._position in (
                Positions.Long,
                Positions.Short,
            ):
                if pnl > 0:
                    # Profitable exit
                    exit_reward = float(np.clip(pnl * 50.0, 1.0, 8.0))
                    # Quick profit bonus
                    if max_dur > 0 and trade_duration < max_dur * 0.3:
                        exit_reward += 2.0
                elif pnl == 0 or abs(pnl) < profit_aim:
                    # Small loss / break-even
                    exit_reward = -1.0
                elif abs(pnl) < profit_aim * 2:
                    # Medium loss: linear interpolation from -1 to -5
                    ratio = (abs(pnl) - profit_aim) / profit_aim if profit_aim > 0 else 0
                    exit_reward = -1.0 - 4.0 * ratio
                elif abs(pnl) < profit_aim * 3:
                    # Large loss
                    exit_reward = -8.0
                else:
                    # Extreme loss (should be rare due to liquidation)
                    exit_reward = -10.0

                # Logging
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
