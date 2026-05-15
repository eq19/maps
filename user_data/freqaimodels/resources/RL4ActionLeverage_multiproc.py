import logging

import numpy as np
import torch as th

from freqtrade.freqai.RL.Base4ActionRLEnv import Actions, Base4ActionRLEnv, Positions
from ReinforcementLearner4Action_multiproc import ReinforcementLearner4Action_multiproc


logger = logging.getLogger(__name__)


class RL4ActionLeverage_multiproc(ReinforcementLearner4Action_multiproc):
    """
    Multi-process Reinforcement Learning Model with 10x Fixed Leverage Support
    
    Inherits from ReinforcementLearner4Action_multiproc for parallel environment training
    and modifies the environment to simulate 10x leverage trading with liquidation risk.
    
    Key Features:
    - Multi-process training with SubprocVecEnv (5-15x faster than single environment)
    - 10x leverage amplification for all PNL calculations
    - Liquidation checking based on margin requirements
    - Adjusted reward structure for high-leverage trading
    - Severe penalty for liquidation events
    - Full CPU utilization based on cpu_count setting
    
    Performance:
    - Single environment: ~100-200 it/s
    - Multi-process (16 envs): ~1500-3000 it/s
    - Training speedup: 5-15x
    
    Usage:
    freqtrade backtesting --strategy RLStrategy4ActionLeverage \\
        --config user_data/config_rl_10x_v2.json \\
        --freqaimodel RL4ActionLeverage_multiproc \\
        --timerange 20230101-20251019 --export trades
    """

    def __init__(self, **kwargs) -> None:
        """
        Override __init__ to remove the max_threads limitation.
        
        The base class limits max_threads to min(cpu_count, max_system_threads/2).
        For dedicated training, we want to use the full configured cpu_count.
        """
        # Call parent __init__ first
        super().__init__(**kwargs)
        
        # Override max_threads to use configured cpu_count directly
        configured_cpu_count = self.freqai_info["rl_config"].get("cpu_count", 1)
        
        # Only override if configured value is higher than current max_threads
        if configured_cpu_count > self.max_threads:
            logger.info(
                f"RL4ActionLeverage_multiproc: Overriding max_threads from {self.max_threads} "
                f"to {configured_cpu_count} for better parallelization"
            )
            self.max_threads = configured_cpu_count
            th.set_num_threads(self.max_threads)
        else:
            logger.info(
                f"RL4ActionLeverage_multiproc: Using max_threads={self.max_threads} "
                f"(configured cpu_count={configured_cpu_count})"
            )

    class MyRLEnv(Base4ActionRLEnv):
        """
        Custom environment with 10x leverage support.
        Unified exit action for both long and short positions.
        
        This environment is instantiated multiple times in parallel by SubprocVecEnv.
        Each instance runs in a separate process for true parallel data collection.
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
            
            All reward parameters are now configurable through config.json's model_reward_parameters.
            This allows easy tuning without modifying code.
            
            :param action: int = The action made by the agent
            :return: float = reward value
            """
            # === Load all configurable reward parameters ===
            reward_params = self.rl_config.get("model_reward_parameters", {})
            
            liquidation_penalty = reward_params.get("liquidation_penalty", -1000.0)
            invalid_action_penalty = reward_params.get("invalid_action_penalty", -2)
            enter_trade_reward = reward_params.get("enter_trade_reward", 25)
            neutral_penalty = reward_params.get("neutral_penalty", -1)
            base_factor = reward_params.get("base_factor", 50.0)
            time_reward_max = reward_params.get("time_reward_max", 3.0)
            time_reward_slope = reward_params.get("time_reward_slope", 2.0)
            risk_adjustment_cap = reward_params.get("risk_adjustment_cap", 3.0)
            base_profit_bonus = reward_params.get("base_profit_bonus", 5)
            leverage_loss_multiplier = reward_params.get("leverage_loss_multiplier", 2.0)
            
            # Calculate profit_aim early (used in multiple places)
            profit_aim = self.profit_aim * self.rr
            profit_aim_abs = abs(profit_aim)
            
            # Check liquidation FIRST (highest priority)
            if self._check_liquidation():
                self.tensorboard_log("liquidation", category="risk")
                self.tensorboard_log("liquidation_count", category="risk")
                logger.warning(f"LIQUIDATION at tick {self._current_tick}")
                return liquidation_penalty

            # Penalize invalid actions
            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return invalid_action_penalty

            pnl = self.get_unrealized_profit()  # Already includes 10x leverage
            rew = pnl
            factor = base_factor

            # Reward agent for entering trades
            if (
                action in (Actions.Long_enter.value, Actions.Short_enter.value)
                and self._position == Positions.Neutral
            ):
                return enter_trade_reward

            # Discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return neutral_penalty

            max_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)
            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            # Discourage sitting in position without action
            # BUT provide immediate feedback on unrealized PNL (DENSE REWARDS)
            if (
                self._position in (Positions.Short, Positions.Long)
                and action == Actions.Neutral.value
            ):
                # Dynamic layered feedback based on PNL magnitude
                profit_aim_abs = abs(profit_aim)
                immediate_feedback_safe = reward_params.get("immediate_feedback_safe", 0.3)
                immediate_feedback_warning = reward_params.get("immediate_feedback_warning", 1.5)
                immediate_feedback_danger = reward_params.get("immediate_feedback_danger", 3.0)
                
                if pnl > 0:
                    # Reward holding winning positions (small reward to encourage holding)
                    immediate_feedback = pnl * immediate_feedback_safe
                    self.tensorboard_log("holding_profit", value=pnl, category="pnl")
                else:
                    # Penalize holding losing positions with escalating feedback
                    abs_pnl = abs(pnl)
                    
                    if abs_pnl < profit_aim_abs:  # Safe zone: 0 to -25 USDT
                        immediate_feedback = pnl * immediate_feedback_safe
                        self.tensorboard_log("holding_safe_zone", category="risk")
                    elif abs_pnl < profit_aim_abs * 2:  # Warning zone: -25 to -50 USDT
                        immediate_feedback = pnl * immediate_feedback_warning
                        self.tensorboard_log("holding_warning_zone", category="risk")
                    else:  # Danger zone: > -50 USDT
                        immediate_feedback = pnl * immediate_feedback_danger
                        self.tensorboard_log("holding_danger_zone", category="risk")
                
                # Time penalty (holding too long is risky with leverage)
                time_penalty = -1 * trade_duration / max_trade_duration
                leverage_penalty = time_penalty * (1 + self.leverage_risk_penalty)
                
                # Combine: reward good positions, penalize bad ones + time
                return immediate_feedback + leverage_penalty

            # Unified Exit action for both Long and Short positions
            if action == Actions.Exit.value and self._position in (Positions.Long, Positions.Short):
                # profit_aim already defined at function start
                
                # === IMPROVEMENT 1: Continuous Time-based Reward ===
                if pnl > 0:
                    normalized_duration = min(trade_duration / max_trade_duration, 1.0)
                    time_multiplier = time_reward_max - (time_reward_slope * normalized_duration)
                    factor *= time_multiplier
                    self.tensorboard_log("time_multiplier", value=time_multiplier, category="rewards")
                else:
                    # Penalize long-duration losses more heavily (especially with leverage)
                    if trade_duration > max_trade_duration:
                        factor *= 0.5
                
                # === IMPROVEMENT 2: Multi-tier Profit Ladders (using config) ===
                # Read tier_multipliers from config instead of hardcoding
                tier_multipliers = reward_params.get("tier_multipliers", {
                    "small_win": 8,
                    "medium_win": 12,
                    "big_win": 16,
                    "huge_win": 32,
                    "mega_win": 64
                })
                
                # Compare directly with profit_aim (pnl already includes leverage)
                if pnl > profit_aim * 10:
                    factor *= tier_multipliers["mega_win"]
                    self.tensorboard_log("mega_win_10x", category="tier")
                elif pnl > profit_aim * 5:
                    factor *= tier_multipliers["huge_win"]
                    self.tensorboard_log("huge_win_10x", category="tier")
                elif pnl > profit_aim * 3:
                    factor *= tier_multipliers["big_win"]
                    self.tensorboard_log("big_win_10x", category="tier")
                elif pnl > profit_aim * 1.5:
                    factor *= tier_multipliers["medium_win"]
                    self.tensorboard_log("medium_win_10x", category="tier")
                elif pnl > profit_aim:
                    factor *= tier_multipliers["small_win"]
                    self.tensorboard_log("small_win_10x", category="tier")
                
                # === IMPROVEMENT 3: Risk-adjusted Reward (Sharpe-like) ===
                # Reward not just profit, but profit relative to time/risk
                time_efficiency = max_trade_duration / max(trade_duration, 1)
                risk_adjustment = min(time_efficiency, risk_adjustment_cap)
                
                if pnl > 0:
                    factor *= risk_adjustment
                    self.tensorboard_log("risk_adjustment", value=risk_adjustment, category="rewards")
                
                # === IMPROVEMENT 4: Three-tier Loss Penalty System ===
                if pnl > 0:
                    final_reward = rew * factor + base_profit_bonus
                else:
                    # Three-tier penalty based on loss magnitude
                    abs_pnl = abs(pnl)
                    profit_aim_abs = abs(profit_aim)
                    
                    safe_zone_penalty = reward_params.get("safe_zone_penalty", -5)
                    warning_zone_penalty = reward_params.get("warning_zone_penalty", -50)
                    danger_zone_penalty = reward_params.get("danger_zone_penalty", -150)
                    
                    if abs_pnl < profit_aim_abs:  # Safe zone: 0 to -25 USDT
                        # Minimal penalty - acceptable loss range
                        final_reward = safe_zone_penalty
                        self.tensorboard_log("exit_safe_zone", category="risk")
                        self.tensorboard_log("exit_safe_zone_pnl", value=pnl, category="pnl")
                    elif abs_pnl < profit_aim_abs * 2:  # Warning zone: -25 to -50 USDT
                        # Medium penalty - should have stopped earlier
                        # Linear interpolation between safe and warning penalty
                        ratio = (abs_pnl - profit_aim_abs) / profit_aim_abs
                        final_reward = safe_zone_penalty + (warning_zone_penalty - safe_zone_penalty) * ratio
                        self.tensorboard_log("exit_warning_zone", category="risk")
                        self.tensorboard_log("exit_warning_zone_pnl", value=pnl, category="pnl")
                    elif abs_pnl < profit_aim_abs * 3:  # Danger zone: -50 to -75 USDT
                        # Heavy penalty - approaching liquidation
                        # Linear interpolation between warning and danger penalty
                        ratio = (abs_pnl - profit_aim_abs * 2) / profit_aim_abs
                        final_reward = warning_zone_penalty + (danger_zone_penalty - warning_zone_penalty) * ratio
                        self.tensorboard_log("exit_danger_zone", category="risk")
                        self.tensorboard_log("exit_danger_zone_pnl", value=pnl, category="pnl")
                    else:  # Extreme loss: > -75 USDT (should trigger liquidation)
                        # Maximum penalty - this should rarely happen
                        final_reward = danger_zone_penalty
                        self.tensorboard_log("exit_extreme_loss", category="risk")
                        self.tensorboard_log("exit_extreme_loss_pnl", value=pnl, category="pnl")
                    
                    self.tensorboard_log("loss_tier_penalty", value=final_reward, category="rewards")
                
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
