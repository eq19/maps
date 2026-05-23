import logging

import numpy as np

from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions


logger = logging.getLogger(__name__)


class RL4Action(ReinforcementLearner):
    """
    Reinforcement Learning Model using Base4ActionRLEnv (4 actions).
    
    This model uses a unified Exit action instead of separate Long_exit and Short_exit.
    
    Actions:
    - 0: Neutral
    - 1: Exit (unified exit for both Long and Short)
    - 2: Long_enter
    - 3: Short_enter
    
    Usage:
    freqtrade backtesting --strategy RLStrategy4Action --config user_data/config_dqn_gpu.json --freqaimodel ReinforcementLearner4Action --timerange 20231201-20240130
    """

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom environment using Base4ActionRLEnv.
        Unified exit action for both long and short positions.
        """

        def calculate_reward(self, action: int) -> float:
            """
            Calculate reward for the current action.
            
            Reward structure:
            - Invalid action: -2
            - Enter trade: +25
            - Neutral when not in position: -1
            - Exit with profit > profit_aim: PNL * factor * win_reward_factor
            - Exit: PNL * factor
            - Sitting in position doing nothing: -1 * (trade_duration / max_trade_duration)
            
            :param action: int = The action made by the agent
            :return: float = reward value
            """
            # Penalize invalid actions
            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return -2

            pnl = self.get_unrealized_profit()
            rew = pnl
            factor = 1000.0  # Increased base factor to compensate for removing +1 offset

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
                return -1 * trade_duration / max_trade_duration

            # Unified Exit action for both Long and Short positions
            if action == Actions.Exit.value and self._position in (Positions.Long, Positions.Short):
                profit_aim = self.profit_aim * self.rr
                
                # === IMPROVEMENT 1: Continuous Time-based Reward ===
                if pnl > 0:
                    normalized_duration = min(trade_duration / max_trade_duration, 1.0)
                    time_multiplier = 3.0 - (2.0 * normalized_duration)  # 3.0x for quick, 1.0x for slow
                    factor *= time_multiplier
                    self.tensorboard_log("time_multiplier", value=time_multiplier, category="rewards")
                else:
                    # Penalize long-duration losses more heavily
                    if trade_duration > max_trade_duration:
                        factor *= 0.5
                
                # === IMPROVEMENT 2: Multi-tier Profit Ladders ===
                if pnl > profit_aim * 10:  # 20%+ mega win
                    factor *= 200
                    self.tensorboard_log("mega_win", category="tier")
                elif pnl > profit_aim * 5:  # 10%+ huge win
                    factor *= 100
                    self.tensorboard_log("huge_win", category="tier")
                elif pnl > profit_aim * 3:  # 6%+ big win
                    factor *= 50
                    self.tensorboard_log("big_win", category="tier")
                elif pnl > profit_aim * 1.5:  # 3%+ medium win
                    factor *= 25
                    self.tensorboard_log("medium_win", category="tier")
                elif pnl > profit_aim:  # 2%+ small win
                    factor *= 10
                    self.tensorboard_log("small_win", category="tier")
                
                # === IMPROVEMENT 3: Progressive Bonus (continuous scaling) ===
                if pnl > profit_aim:
                    excess_profit = pnl - profit_aim
                    progressive_bonus = 1 + (excess_profit / 0.01) * 2  # +2x per 1% excess
                    factor *= progressive_bonus
                    self.tensorboard_log("progressive_bonus", value=progressive_bonus, category="rewards")
                
                # === IMPROVEMENT 4: Asymmetric Loss Penalty ===
                if pnl > 0:
                    base_profit_bonus = 50  # Base reward for any profit
                    final_reward = rew * factor + base_profit_bonus
                else:
                    final_reward = rew * factor * 2  # Double penalty for losses
                
                # === Logging ===
                position_type = "long" if self._position == Positions.Long else "short"
                self.tensorboard_log(f"{position_type}_exit_pnl", value=pnl, category="pnl")
                self.tensorboard_log("exit_pnl", value=pnl, category="pnl")
                self.tensorboard_log("total_pnl_sum", value=pnl, category="pnl")
                
                if pnl > 0:
                    self.tensorboard_log("profitable_exit", category="pnl")
                    self.tensorboard_log("profitable_pnl_sum", value=pnl, category="pnl")
                else:
                    self.tensorboard_log("loss_exit", category="pnl")
                    self.tensorboard_log("loss_pnl_sum", value=pnl, category="pnl")
                
                self.tensorboard_log("final_reward", value=final_reward, category="rewards")
                self.tensorboard_log("factor_used", value=factor, category="rewards")
                
                return float(final_reward)

            return 0.0
