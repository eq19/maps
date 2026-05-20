import logging
from typing import Any

import torch as th
from pandas import DataFrame

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.prediction_models.ReinforcementLearner_multiproc import (
    ReinforcementLearner_multiproc,
)
from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions


logger = logging.getLogger(__name__)


class ReinforcementLearner4Action(ReinforcementLearner_multiproc):
    
    def __init__(self, **kwargs) -> None:
        """
        Override __init__ to remove the max_threads limitation.
        
        The base class limits max_threads to min(cpu_count, max_system_threads/2).
        For dedicated training servers, we want to use the full configured cpu_count.
        """
        # Call parent __init__ first
        super().__init__(**kwargs)
        
        # Override max_threads to use configured cpu_count directly
        configured_cpu_count = self.freqai_info["rl_config"].get("cpu_count", 1)
        
        # Only override if configured value is higher than current max_threads
        if configured_cpu_count > self.max_threads:
            logger.info(
                f"Overriding max_threads from {self.max_threads} to {configured_cpu_count} "
                f"for better parallelization on dedicated training server"
            )
            self.max_threads = configured_cpu_count
            th.set_num_threads(self.max_threads)
        else:
            logger.info(
                f"Using default max_threads={self.max_threads} "
                f"(configured cpu_count={configured_cpu_count})"
            )
    
    """
    Multi-process version of ReinforcementLearner4Action for improved training speed.
    
    Uses SubprocVecEnv to create multiple parallel environments based on cpu_count setting.
    Expected speed improvement: 5-15x compared to single-environment version.
    
    Key optimization: Overrides max_threads calculation to use full configured cpu_count
    instead of being limited to max_system_threads/2.
    
    Usage:
    freqtrade backtesting --strategy RLStrategy4Action --config user_data/config_v3.json \
        --freqaimodel ReinforcementLearner4Action_multiproc --timerange 20230101-20251019 \
        --export trades
    """

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom 4-action RL environment with user-defined reward function.
        """

        def calculate_reward(self, action: int) -> float:
            """
            Custom reward function based on profit, trade duration, and risk management.
            
            This function is called after each step in the environment to calculate
            the reward for the agent's action.
            """
            # Base reward/penalty
            if self._position == Positions.Neutral:
                return 0

            # Get current profit ratio
            pnl = self.get_unrealized_profit()
            
            # Reward parameters from rl_config (multiprocessing-safe)
            reward_params = self.rl_config.get("model_reward_parameters", {})
            
            profit_aim = reward_params.get("profit_aim", 0.02)
            base_factor = reward_params.get("base_factor", 50000)
            time_reward_max = reward_params.get("time_reward_max", 1.0)
            progressive_bonus_rate = reward_params.get("progressive_bonus_rate", 5.0)
            asymmetric_loss_penalty = reward_params.get("asymmetric_loss_penalty", 3.0)
            base_profit_bonus = reward_params.get("base_profit_bonus", 100)
            
            tier_multipliers = reward_params.get("tier_multipliers", {
                "small_win": 25,
                "medium_win": 50,
                "big_win": 100,
                "huge_win": 200,
                "mega_win": 500
            })

            # Calculate base reward
            factor = base_factor if pnl > 0 else base_factor * asymmetric_loss_penalty
            
            # Trade duration component
            trade_duration = self._current_tick - self._last_trade_tick
            max_trade_duration = self.rl_config.get("max_trade_duration_candles", 50)
            time_factor = max(0, 1 - (trade_duration / max_trade_duration))
            time_reward = time_reward_max * time_factor

            # Progressive profit bonus (tiered rewards)
            profit_ratio = pnl / profit_aim if profit_aim > 0 else 0
            
            if pnl > 0:
                if profit_ratio >= 5.0:  # Mega win (500%+)
                    profit_bonus = base_profit_bonus * tier_multipliers["mega_win"]
                elif profit_ratio >= 3.0:  # Huge win (300%+)
                    profit_bonus = base_profit_bonus * tier_multipliers["huge_win"]
                elif profit_ratio >= 2.0:  # Big win (200%+)
                    profit_bonus = base_profit_bonus * tier_multipliers["big_win"]
                elif profit_ratio >= 1.5:  # Medium win (150%+)
                    profit_bonus = base_profit_bonus * tier_multipliers["medium_win"]
                else:  # Small win
                    profit_bonus = base_profit_bonus * tier_multipliers["small_win"] * profit_ratio
                
                progressive_bonus = profit_bonus * (1 + progressive_bonus_rate * profit_ratio)
            else:
                progressive_bonus = 0

            # Calculate total reward
            reward = (pnl * factor) + time_reward + progressive_bonus

            # Penalty for holding losing positions too long
            if pnl < 0 and trade_duration > max_trade_duration * 0.7:
                reward *= 1.5  # Extra penalty

            # Penalty for exceeding max drawdown
            max_drawdown = self.rl_config.get("max_training_drawdown_pct", 0.05)
            if pnl < -max_drawdown:
                reward *= 2.0  # Severe penalty for excessive drawdown

            return float(reward)

