import logging

import numpy as np

from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions
from ReinforcementLearner4Action import ReinforcementLearner4Action


logger = logging.getLogger(__name__)


class RL4ActionLeverage(ReinforcementLearner4Action):
    """
    Reinforcement Learning Model with 10x Fixed Leverage Support
    
    Inherits from ReinforcementLearner4Action and modifies the environment
    to simulate 10x leverage trading with liquidation risk.
    
    Key Features:
    - 10x leverage amplification for all PNL calculations
    - Liquidation checking based on margin requirements
    - Adjusted reward structure for high-leverage trading
    - Severe penalty for liquidation events
    
    Usage:
    freqtrade backtesting --strategy RLStrategy4ActionLeverage --config user_data/config_rl_10x.json --freqaimodel RL4ActionLeverage --timerange 20230101-20251019 --export trades
    """

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom environment with 10x leverage support.
        Unified exit action for both long and short positions.
        """

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Fixed 10x leverage
            self.leverage = self.rl_config.get("leverage", 10.0)
            # Liquidation buffer (5% default)
            self.liquidation_buffer = self.rl_config.get("liquidation_buffer", 0.05)
            # Risk penalty multiplier for leverage
            self.leverage_risk_penalty = self.rl_config.get("leverage_risk_penalty", 0.15)
            # Track if liquidated
            self._is_liquidated = False

        def get_unrealized_profit(self):
            """
            Get the unrealized profit with 10x leverage amplification.
            
            Returns:
                float: PNL percentage multiplied by leverage (10x)
            """
            if self._last_trade_tick is None:
                return 0.0

            if self._position == Positions.Neutral:
                return 0.0
            elif self._position == Positions.Short:
                current_price = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (last_trade_price - current_price) / last_trade_price
                # Apply 10x leverage
                return base_pnl * self.leverage
            elif self._position == Positions.Long:
                current_price = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (current_price - last_trade_price) / last_trade_price
                # Apply 10x leverage
                return base_pnl * self.leverage
            else:
                return 0.0

        def _check_liquidation(self) -> bool:
            """
            Check if the current position should be liquidated.
            
            Liquidation occurs when unrealized loss exceeds:
            (1/leverage - liquidation_buffer)
            
            For 10x leverage with 5% buffer:
            - Liquidation threshold = -(0.1 - 0.05) = -0.05 = -5%
            - This means a -0.5% price move against position triggers liquidation
            
            Returns:
                bool: True if liquidated, False otherwise
            """
            if self._position == Positions.Neutral or self._is_liquidated:
                return False
            
            # Get base PNL (without leverage amplification)
            if self._position == Positions.Short:
                current_price = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (last_trade_price - current_price) / last_trade_price
            else:  # Long
                current_price = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                last_trade_price = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                base_pnl = (current_price - last_trade_price) / last_trade_price
            
            # Calculate liquidation threshold
            # For 10x leverage: can lose max 10% of position value before 100% margin loss
            liquidation_threshold = -(1.0 / self.leverage - self.liquidation_buffer)
            
            if base_pnl <= liquidation_threshold:
                self._is_liquidated = True
                # Force close position at liquidation
                self._position = Positions.Neutral
                # Apply liquidation loss to total profit
                self._total_profit *= (1 + liquidation_threshold)
                return True
            
            return False

        def reset(self, seed=None):
            """
            Reset the environment and liquidation flag.
            """
            self._is_liquidated = False
            return super().reset(seed)

        def calculate_reward(self, action: int) -> float:
            """
            Calculate reward for the current action with leverage awareness.
            
            Reward structure (modified for 10x leverage):
            - Liquidation: -1000 (severe penalty)
            - Invalid action: -2
            - Enter trade: +25
            - Neutral when not in position: -1
            - Exit with profit > profit_aim: PNL * factor * win_reward_factor
            - Exit with loss: PNL * factor * leverage_risk_penalty
            - Sitting in position doing nothing: -1 * (trade_duration / max_trade_duration)
            
            :param action: int = The action made by the agent
            :return: float = reward value
            """
            # Check liquidation FIRST (highest priority)
            if self._check_liquidation():
                self.tensorboard_log("liquidation", category="risk")
                self.tensorboard_log("liquidation_count", category="risk")
                logger.warning(f"LIQUIDATION at tick {self._current_tick}")
                return -1000.0  # Severe penalty for liquidation

            # Penalize invalid actions
            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return -2

            pnl = self.get_unrealized_profit()  # Already includes 10x leverage
            rew = pnl
            factor = 500.0

            # Reward agent for entering trades
            if (
                action in (Actions.Long_enter.value, Actions.Short_enter.value)
                and self._position == Positions.Neutral
            ):
                return 25

            # Discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return -1

            max_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)
            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            # Discourage sitting in position without action
            if (
                self._position in (Positions.Short, Positions.Long)
                and action == Actions.Neutral.value
            ):
                # With 10x leverage, time in position is riskier
                time_penalty = -1 * trade_duration / max_trade_duration
                # Apply leverage risk penalty
                return time_penalty * (1 + self.leverage_risk_penalty)

            # Unified Exit action for both Long and Short positions
            if action == Actions.Exit.value and self._position in (Positions.Long, Positions.Short):
                profit_aim = self.profit_aim * self.rr
                
                # === IMPROVEMENT 1: Continuous Time-based Reward ===
                if pnl > 0:
                    normalized_duration = min(trade_duration / max_trade_duration, 1.0)
                    time_multiplier = 3.0 - (2.0 * normalized_duration)
                    factor *= time_multiplier
                    self.tensorboard_log("time_multiplier", value=time_multiplier, category="rewards")
                else:
                    # Penalize long-duration losses more heavily (especially with leverage)
                    if trade_duration > max_trade_duration:
                        factor *= 0.5
                
                # === IMPROVEMENT 2: Multi-tier Profit Ladders (adjusted for 10x leverage) ===
                # Note: With 10x leverage, these thresholds are easier to reach
                leverage_adjusted_aim = profit_aim * self.leverage
                
                if pnl > leverage_adjusted_aim * 10:  # Massive win with leverage
                    factor *= 200
                    self.tensorboard_log("mega_win_10x", category="tier")
                elif pnl > leverage_adjusted_aim * 5:
                    factor *= 100
                    self.tensorboard_log("huge_win_10x", category="tier")
                elif pnl > leverage_adjusted_aim * 3:
                    factor *= 50
                    self.tensorboard_log("big_win_10x", category="tier")
                elif pnl > leverage_adjusted_aim * 1.5:
                    factor *= 25
                    self.tensorboard_log("medium_win_10x", category="tier")
                elif pnl > leverage_adjusted_aim:
                    factor *= 10
                    self.tensorboard_log("small_win_10x", category="tier")
                
                # === IMPROVEMENT 3: Progressive Bonus ===
                if pnl > leverage_adjusted_aim:
                    excess_profit = pnl - leverage_adjusted_aim
                    progressive_bonus = 1 + (excess_profit / (0.01 * self.leverage)) * 2
                    factor *= progressive_bonus
                    self.tensorboard_log("progressive_bonus_10x", value=progressive_bonus, category="rewards")
                
                # === IMPROVEMENT 4: Asymmetric Loss Penalty (MORE severe with leverage) ===
                if pnl > 0:
                    base_profit_bonus = 50
                    final_reward = rew * factor + base_profit_bonus
                else:
                    # Triple penalty for losses with 10x leverage (was 2x)
                    leverage_loss_penalty = 2 + self.leverage_risk_penalty
                    final_reward = rew * factor * leverage_loss_penalty
                    self.tensorboard_log("leverage_loss_penalty", value=leverage_loss_penalty, category="rewards")
                
                # === Logging ===
                position_type = "long" if self._position == Positions.Long else "short"
                self.tensorboard_log(f"{position_type}_exit_pnl_10x", value=pnl, category="pnl")
                self.tensorboard_log("exit_pnl_10x", value=pnl, category="pnl")
                self.tensorboard_log("total_pnl_sum_10x", value=pnl, category="pnl")
                
                # Log liquidation distance
                if self._position in (Positions.Long, Positions.Short):
                    # Calculate how close we are to liquidation
                    if self._position == Positions.Short:
                        current_price = self.add_entry_fee(self.prices.iloc[self._current_tick].open)
                        last_trade_price = self.add_exit_fee(self.prices.iloc[self._last_trade_tick].open)
                        base_pnl = (last_trade_price - current_price) / last_trade_price
                    else:
                        current_price = self.add_exit_fee(self.prices.iloc[self._current_tick].open)
                        last_trade_price = self.add_entry_fee(self.prices.iloc[self._last_trade_tick].open)
                        base_pnl = (current_price - last_trade_price) / last_trade_price
                    
                    liquidation_threshold = -(1.0 / self.leverage - self.liquidation_buffer)
                    liquidation_distance = base_pnl - liquidation_threshold
                    self.tensorboard_log("liquidation_distance", value=liquidation_distance, category="risk")
                
                if pnl > 0:
                    self.tensorboard_log("profitable_exit_10x", category="pnl")
                    self.tensorboard_log("profitable_pnl_sum_10x", value=pnl, category="pnl")
                else:
                    self.tensorboard_log("loss_exit_10x", category="pnl")
                    self.tensorboard_log("loss_pnl_sum_10x", value=pnl, category="pnl")
                
                self.tensorboard_log("final_reward_10x", value=final_reward, category="rewards")
                self.tensorboard_log("factor_used_10x", value=factor, category="rewards")
                self.tensorboard_log("leverage_used", value=self.leverage, category="config")
                
                return float(final_reward)

            return 0.0
