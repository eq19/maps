import logging
import warnings
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import torch as th
from pandas import DataFrame
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import SubprocVecEnv
from gymnasium import spaces

from freqtrade.freqai.RL.BaseReinforcementLearningModel import BaseReinforcementLearningModel
from freqtrade.freqai.RL.Base3ActionRLEnv import Base3ActionRLEnv, Actions, Positions

logger = logging.getLogger(__name__)


class RLModelOptimized(BaseReinforcementLearningModel):
    """
    优化的强化学习模型
    
    此模型基于PPO算法，包含了多种优化：
    1. 改进的奖励函数
    2. 动态风险管理
    3. 多目标优化
    4. 更好的特征工程
    5. 自适应学习策略
    
    用户需要在配置文件中设置:
    "rl_config": {
        "train_cycles": 25,
        "cpu_count": 4,
        "max_training_drawdown_pct": 0.05,
        "model_type": "PPO",
        "policy_type": "MlpPolicy",
        "max_trade_duration_candles": 300,
        "model_reward_parameters": {
            "rr": 1.5,
            "profit_aim": 0.025,
            "win_reward_factor": 2.5,
            "sharpe_ratio_reward_factor": 0.5,
            "calmar_ratio_reward_factor": 0.3
        }
    }
    """

    def fit(self, data_dictionary: Dict[str, Any], dk: Any, **kwargs) -> Any:
        """
        训练强化学习模型
        
        Args:
            data_dictionary: 包含训练数据的字典
            dk: DataKitchen对象
            **kwargs: 额外参数
            
        Returns:
            训练好的模型
        """
        train_df = data_dictionary["train_features"]
        total_timesteps = self.freqai_info["rl_config"]["train_cycles"] * len(train_df)

        # 设置策略参数
        policy_kwargs = dict(
            activation_fn=th.nn.ReLU,
            net_arch=self.freqai_info["rl_config"].get("net_arch", [128, 128, 64]),
            normalize_images=False
        )

        if dk.pair not in self.dd.model_dictionary or not self.continual_learning:
            # 创建新模型
            model = PPO(
                self.policy_type,
                self.train_env,
                policy_kwargs=policy_kwargs,
                tensorboard_log=Path(dk.full_path / "tensorboard" / dk.pair.split('/')[0]),
                learning_rate=self.freqai_info["model_training_parameters"].get("learning_rate", 0.00025),
                gamma=self.freqai_info["model_training_parameters"].get("gamma", 0.9),
                verbose=1,
                device='auto'
            )
        else:
            # 加载现有模型进行持续学习
            logger.info('持续学习模式：加载现有模型进行增量训练')
            model = self.dd.model_dictionary[dk.pair]
            model.set_env(self.train_env)

        # 设置回调函数
        eval_callback = EvalCallback(
            self.eval_env,
            best_model_save_path=str(dk.data_path),
            log_path=str(dk.data_path),
            eval_freq=int(len(train_df) / 5),  # 每1/5的数据评估一次
            deterministic=True,
            render=False
        )

        # 设置早停回调
        stop_callback = StopTrainingOnRewardThreshold(
            reward_threshold=0.95,  # 当平均奖励达到0.95时停止训练
            verbose=1
        )

        # 训练模型
        try:
            model.learn(
                total_timesteps=int(total_timesteps),
                callback=[eval_callback, stop_callback],
                tb_log_name=f"{dk.pair.split('/')[0]}_{self.timestamp}"
            )
        except Exception as e:
            logger.warning(f"训练过程中出现警告: {e}")

        if Path(dk.data_path / "best_model.zip").exists():
            logger.info("加载最佳模型")
            model = PPO.load(dk.data_path / "best_model")

        logger.info(f"训练完成。总步数: {total_timesteps}")

        return model

    class MyRLEnv(Base3ActionRLEnv):
        """
        优化的强化学习环境
        
        继承自Base3ActionRLEnv，包含了改进的奖励函数和风险管理机制
        """

        def calculate_reward(self, action: int) -> float:
            """
            计算奖励函数
            
            Args:
                action: 执行的动作 (0=持有, 1=买入, 2=卖出)
                
            Returns:
                float: 计算得到的奖励值
            """
            if self._current_tick == self._end_tick:
                return 0

            # 基础变量
            step_reward = 0
            trade_type = None
            
            # 获取当前价格和特征
            current_price = self.prices.iloc[self._current_tick].open
            last_trade_tick = max(0, self._current_tick - 1)
            last_price = self.prices.iloc[last_trade_tick].open if last_trade_tick >= 0 else current_price
            
            # 计算价格变化
            price_diff = current_price - last_price
            price_change_pct = price_diff / last_price if last_price != 0 else 0

            # 动作执行
            if action == Actions.Buy.value and self._position == Positions.Neutral:
                self._position = Positions.Long
                self._last_trade_tick = self._current_tick
                trade_type = "enter_long"
                
            elif action == Actions.Sell.value and self._position == Positions.Long:
                self._position = Positions.Neutral
                trade_type = "exit_long"
                
            elif action == Actions.Neutral.value:
                trade_type = "hold"

            # 1. 基础奖励：基于持仓收益
            if self._position == Positions.Long:
                # 持有多头仓位的收益
                if self._last_trade_tick is not None and self._last_trade_tick < self._current_tick:
                    entry_price = self.prices.iloc[self._last_trade_tick].open
                    unrealized_profit = (current_price - entry_price) / entry_price
                    step_reward += unrealized_profit * 10  # 放大收益信号
            
            # 2. 交易行为奖励
            if trade_type == "enter_long":
                # 买入奖励：鼓励在好时机买入
                features = self.df.iloc[self._current_tick]
                
                # RSI在超卖区域买入
                if hasattr(features, '%-rsi-period_14') and features['%-rsi-period_14'] < 35:
                    step_reward += 0.1
                
                # MACD金叉
                if (hasattr(features, '%-macd_14') and hasattr(features, '%-macdsignal_14') and
                    features['%-macd_14'] > features['%-macdsignal_14']):
                    step_reward += 0.1
                
                # 在布林带下轨附近买入
                if (hasattr(features, '%-bb_percent_20') and 
                    0.1 < features['%-bb_percent_20'] < 0.3):
                    step_reward += 0.1
                    
                # 成交量放大
                if hasattr(features, '%-volume_ratio') and features['%-volume_ratio'] > 1.2:
                    step_reward += 0.05
                    
            elif trade_type == "exit_long":
                # 卖出奖励：基于实际收益
                if self._last_trade_tick is not None:
                    entry_price = self.prices.iloc[self._last_trade_tick].open
                    profit_pct = (current_price - entry_price) / entry_price
                    
                    # 盈利奖励
                    if profit_pct > 0:
                        profit_aim = self.rl_config.get("profit_aim", 0.025)
                        win_reward_factor = self.rl_config.get("win_reward_factor", 2.5)
                        
                        # 达到目标利润给额外奖励
                        if profit_pct >= profit_aim:
                            step_reward += win_reward_factor * (profit_pct / profit_aim)
                        else:
                            step_reward += profit_pct * 5  # 正常盈利奖励
                    else:
                        # 亏损惩罚
                        step_reward += profit_pct * 8  # 亏损惩罚比盈利奖励更重
                    
                    # 持仓时长奖励/惩罚
                    holding_duration = self._current_tick - self._last_trade_tick
                    max_duration = self.rl_config.get("max_trade_duration_candles", 300)
                    
                    if holding_duration < 5:  # 持仓时间太短
                        step_reward -= 0.1
                    elif holding_duration > max_duration * 0.8:  # 持仓时间太长
                        step_reward -= 0.05
                        
            elif trade_type == "hold":
                # 持有奖励/惩罚
                if self._position == Positions.Long:
                    # 在上涨趋势中持有的奖励
                    if price_change_pct > 0:
                        step_reward += price_change_pct * 2
                    else:
                        step_reward += price_change_pct * 3  # 下跌时的惩罚更重
                        
                elif self._position == Positions.Neutral:
                    # 空仓时的小奖励（避免过度交易）
                    step_reward += 0.001
                    
                    # 如果市场下跌而我们空仓，给小奖励
                    if price_change_pct < -0.01:
                        step_reward += abs(price_change_pct) * 0.5

            # 3. 风险调整奖励
            try:
                features = self.df.iloc[self._current_tick]
                
                # 波动率调整
                if hasattr(features, '%-atr_14'):
                    volatility = features['%-atr_14'] / current_price
                    if volatility > 0.05:  # 高波动率时降低奖励
                        step_reward *= (1 - volatility)
                
                # 趋势强度调整
                if hasattr(features, '%-adx-period_14'):
                    trend_strength = features['%-adx-period_14'] / 100
                    if self._position == Positions.Long:
                        # 强趋势中持有多头给额外奖励
                        step_reward *= (1 + trend_strength * 0.1)
                        
            except (KeyError, IndexError):
                pass

            # 4. 夏普比率相关奖励
            if len(self.history) > 30:  # 有足够历史数据
                recent_returns = np.array(self.history[-30:])
                if len(recent_returns) > 1 and np.std(recent_returns) > 0:
                    sharpe_ratio = np.mean(recent_returns) / np.std(recent_returns)
                    sharpe_reward_factor = self.rl_config.get("sharpe_ratio_reward_factor", 0.5)
                    step_reward += sharpe_ratio * sharpe_reward_factor * 0.01

            # 5. 最大回撤惩罚
            max_drawdown_pct = self.rl_config.get("max_training_drawdown_pct", 0.05)
            if hasattr(self, '_max_portfolio_value'):
                current_value = self._total_profit + 1.0
                if current_value < self._max_portfolio_value * (1 - max_drawdown_pct):
                    # 超过最大回撤时给予重惩罚
                    drawdown = (self._max_portfolio_value - current_value) / self._max_portfolio_value
                    step_reward -= drawdown * 5
                else:
                    self._max_portfolio_value = max(self._max_portfolio_value, current_value)
            else:
                self._max_portfolio_value = self._total_profit + 1.0

            # 6. 交易频率调整
            if not hasattr(self, '_trade_count'):
                self._trade_count = 0
            
            if trade_type in ["enter_long", "exit_long"]:
                self._trade_count += 1
                
                # 过度交易惩罚
                avg_trades_per_100_candles = self._trade_count / max(1, self._current_tick / 100)
                if avg_trades_per_100_candles > 10:  # 每100根K线超过10次交易
                    step_reward -= 0.05

            # 7. 风险收益比调整
            rr_factor = self.rl_config.get("rr", 1.5)
            if trade_type == "exit_long" and self._last_trade_tick is not None:
                entry_price = self.prices.iloc[self._last_trade_tick].open
                profit_pct = (current_price - entry_price) / entry_price
                
                # 根据风险收益比调整奖励
                if profit_pct > 0:
                    step_reward *= (1 + profit_pct * rr_factor)

            # 记录历史
            if not hasattr(self, 'history'):
                self.history = []
            self.history.append(step_reward)
            
            # 限制历史长度
            if len(self.history) > 1000:
                self.history = self.history[-500:]

            # 奖励范围限制
            step_reward = np.clip(step_reward, -2.0, 2.0)
            
            return float(step_reward)

        def _is_valid(self, action: int) -> bool:
            """
            检查动作是否有效
            
            Args:
                action: 要执行的动作
                
            Returns:
                bool: 动作是否有效
            """
            # 基础有效性检查
            if action == Actions.Buy.value:
                return self._position == Positions.Neutral
            elif action == Actions.Sell.value:
                return self._position == Positions.Long
            elif action == Actions.Neutral.value:
                return True
            return False

        def reset(self) -> np.ndarray:
            """
            重置环境到初始状态
            
            Returns:
                np.ndarray: 初始观察状态
            """
            self._done = False
            self._current_tick = self._start_tick
            self._last_trade_tick = None
            self._position = Positions.Neutral
            self._position_history = (self.window_size * [None]) + [self._position]
            self._total_reward = 0.0
            self._total_profit = 0.0
            self._first_rendering = True
            self.history = []
            self._trade_count = 0
            self._max_portfolio_value = 1.0
            
            return self._get_observation()

        def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
            """
            执行一个动作步骤
            
            Args:
                action: 要执行的动作
                
            Returns:
                Tuple: (下一个状态, 奖励, 是否终止, 是否截断, 信息字典)
            """
            self._done = False
            self._current_tick += 1

            if self._current_tick == self._end_tick:
                self._done = True
                
                # 如果仍有持仓，强制平仓
                if self._position == Positions.Long:
                    self._position = Positions.Neutral
                    if self._last_trade_tick is not None:
                        entry_price = self.prices.iloc[self._last_trade_tick].open
                        current_price = self.prices.iloc[self._current_tick - 1].open
                        final_profit = (current_price - entry_price) / entry_price
                        self._total_profit += final_profit

            step_reward = self.calculate_reward(action)
            self._total_reward += step_reward

            # 更新持仓历史
            self._position_history.append(self._position)
            
            observation = self._get_observation()
            info = dict(
                total_reward=self._total_reward,
                total_profit=self._total_profit,
                position=self._position.value,
                trade_count=getattr(self, '_trade_count', 0)
            )
            
            # 为了兼容新版本的 Stable-Baselines3，将 done 分为 terminated 和 truncated
            terminated = self._done
            truncated = False
            
            return observation, step_reward, terminated, truncated, info 
