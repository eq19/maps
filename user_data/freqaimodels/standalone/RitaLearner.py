import gc
import logging
from typing import Any, Dict

import numpy as np

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner
from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv, Positions


logger = logging.getLogger(__name__)


class RitaLearner(ReinforcementLearner):
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
        """Add memory management to training"""
        try:
            model = super().fit(data_dictionary, dk, **kwargs)
            gc.collect()  # Force garbage collection after training
            logger.info(f"Model trained and in use: {dk.data_path}")
            return model
        except Exception as e:
            logger.error(f"Error during training: {str(e)}")
            gc.collect()  # Ensure memory is freed even on error
            raise

    class MyRLEnv(Base5ActionRLEnv):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.win_streak = 0
            self.lose_streak = 0
            self.consecutive_neutral_actions = 0
            self.max_consecutive_neutral = 5  # Maximum allowed consecutive neutral actions

            self.win_factor = self.rl_config["model_reward_parameters"].get("win_reward_factor", 2)
            self.designated_trade_duration = self.rl_config.get("max_trade_duration_candles", 300)

            """
            Use this matrix to define the valid of the action bsed on the current position
            """
            # 0: Neutral, 1: Long Enter, 2: Long Eixt, 3: Short Enter, 4: Short Exit
            self.action_matrix = np.array(
                [
                    [+1, -1, -1, -1, +1],  # Short position
                    [+1, -1, +1, -1, -1],  # Long position
                    [-1, +1, -1, +1, -1],  # Neutral position
                ]
            )

        # Function to get the matrix value based on row and column Enums
        def get_matrix_value(self, position: Positions, action: Actions):
            row_index = int(position.value)  # Convert Enum value to index
            col_index = action.value
            return self.action_matrix[row_index, col_index]

        def step(self, action: int):
            """Step with streak updates only on trade completion"""
            # Get the current position before step
            previous_position = self._position

            if action == Actions.Neutral.value:
                self.consecutive_neutral_actions += 1
            else:
                self.consecutive_neutral_actions = 0

            # Execute main step logic
            observation, reward, done, truncated, info = super().step(action)

            # Update streaks only when a trade is closed
            if (
                previous_position in (Positions.Long, Positions.Short)
                and self._position == Positions.Neutral
            ):
                # A trade was just closed
                last_trade = self.trade_history[-1] if self.trade_history else None
                if last_trade:
                    profit = last_trade.get("profit", 0)
                    if profit > 0:
                        self.win_streak = min(self.win_streak + 1, 10)
                        self.lose_streak = 0
                    else:
                        self.lose_streak = min(self.lose_streak + 1, 10)
                        self.win_streak = 0

            return observation, reward, done, truncated, info

        def reset(self, seed=None):
            """Reset environment state including streaks"""

            # Reset streak counters
            self.win_streak = 0
            self.lose_streak = 0

            # Call base reset
            return super().reset(seed)

        def get_last_trade(self):
            if len(self.trade_history) > 0:
                return self.trade_history[-1]
            return None

        def _is_valid(self, action):
            """Determine if the action is valid"""
            return self.get_matrix_value(self._position, Actions(action)) == 1

        def calculate_reward(self, action: int) -> float:
            if not self._is_valid(action):
                return -2000

            trade_duration = self._current_tick - (
                self._last_trade_tick if self._last_trade_tick is not None else self._current_tick
            )

            # For entering trades
            if action in (Actions.Long_enter.value, Actions.Short_enter.value):
                return self.calculate_entry_reward(action)

            p = self.get_unrealized_profit()
            g = self.profit_aim
            m = self.designated_trade_duration
            w = self.win_factor
            s = self.win_streak
            l_o = self.lose_streak
            t = trade_duration
            h = abs(self._total_profit)

            # For exiting positions
            if action in (Actions.Long_exit.value, Actions.Short_exit.value):
                if p == 0:
                    return -20
                elif p > 0:
                    return self.calculate_win_reward(t, p, g, m, w, h, s)
                else:
                    return self.calculate_loose_reward(
                        t,
                        p,
                        g,
                        m,
                        w,
                        h,
                        l_o,
                    )

            # For neutral actions
            return self.calculate_neutral_reward(trade_duration)

        def calculate_entry_reward(self, action: int) -> float:
            """
            Enhanced entry reward calculation
            - Rewards entry more after longer neutral periods
            - Considers win/loss streaks for adaptive entry rewards
            """
            base_reward = 10  # Increased base reward for entry

            # Add bonus for entering after being neutral for a while
            time_since_last_trade = self._current_tick - (
                self._last_trade_tick if self._last_trade_tick is not None else self._current_tick
            )
            neutral_bonus = min(15, time_since_last_trade / 10)  # Cap at +15

            # Add streak-based component
            streak_bonus = (
                self.win_streak * 2 - self.lose_streak
            )  # Encourage entries during winning streaks

            return base_reward + neutral_bonus + streak_bonus

        def calculate_neutral_reward(self, t):
            """
            Enhanced penalty for neutral actions
            - Increases penalty based on time spent neutral
            - Adds base penalty for choosing neutral
            """
            m = self.designated_trade_duration
            base_penalty = -5  # Base penalty for choosing neutral
            time_penalty = -(((40 * t + 1) / (5 * m)) ** 2)  # Increased time-based penalty
            return base_penalty + time_penalty

        def calculate_win_reward(self, t, p, g, m, w, h, s):
            """
            Enhanced reward for winning trades
            """
            # Term 1: (p/g + 1)
            term1 = (p / g) + 1

            # Term 2: (m / (t^2 + m))
            term2 = m / ((t / 1.5) ** 2 + (2 * m))

            # Term 3: w × (h+1)^2 × (s+1)
            term3 = w * (((3 * h) + 1) ** 4) * ((s + 1) ** 2)

            # Final result: product of all terms
            return term1 * term2 * term3

        def calculate_loose_reward(self, t, p, g, m, w, h, l_o):
            """
            Enhanced penalty for losing trades
            """
            # Term 1: (|p| / g + 1)
            term1 = (abs(p) / g) + 1

            # Term 2: (t / m)
            term2 = t / m

            # Term 3: w * (h+1)^2 * (l+1)
            term3 = w * ((1 / h) + 1) ** 2 * (l_o + 1)

            # Combine the terms, take absolute value, then negate
            return -abs(term1 * term2 * term3)
