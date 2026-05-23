"""
自定义强化学习模型
==================

这个模型继承自FreqAI的ReinforcementLearner，使用PPO算法进行强化学习训练。

主要特点:
- 使用PPO (Proximal Policy Optimization) 算法
- 自定义奖励函数优化交易表现
- 支持持续学习和模型保存
- 包含自定义交易环境

作者: FreqAI Team
版本: 1.0
"""

import logging
from pathlib import Path
from typing import Any

import torch as th
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback, ProgressBarCallback
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.RL.Base3ActionRLEnv import Base3ActionRLEnv, Actions, Positions
from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner


logger = logging.getLogger(__name__)


class RLModel(ReinforcementLearner):
    """
    自定义强化学习模型
    
    这个模型使用PPO算法训练一个能够在加密货币市场中做出交易决策的智能体。
    智能体学习在给定市场状态下选择最优的行动（买入/卖出/持有）。
    """

    def fit(self, data_dictionary: dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
        """
        训练强化学习模型
        
        Args:
            data_dictionary: 包含训练和测试数据的字典
            dk: FreqAI数据厨房对象，包含数据处理工具
            **kwargs: 其他参数
            
        Returns:
            训练好的模型
        """
        # 获取训练数据
        train_df = data_dictionary["train_features"]
        total_timesteps = self.freqai_info["rl_config"]["train_cycles"] * len(train_df)
        
        logger.info(f"开始训练RL模型，总时间步数: {total_timesteps}")
        
        # === 配置神经网络架构 ===
        # 使用多层感知机作为策略网络
        policy_kwargs = dict(
            activation_fn=th.nn.ReLU,       # 激活函数：ReLU
            net_arch=[256, 256, 128]        # 网络结构：三层全连接网络
        )
        
        # === 设置Tensorboard日志路径 ===
        if self.activate_tensorboard:
            tb_path = Path(dk.full_path / "tensorboard" / dk.pair.split("/")[0])
            logger.info(f"Tensorboard日志路径: {tb_path}")
        else:
            tb_path = None
        
        # === 创建或加载模型 ===
        if dk.pair not in self.dd.model_dictionary or not self.continual_learning:
            # 创建新模型
            logger.info("创建新的PPO模型")
            # 获取训练参数，避免重复参数
            training_params = self.freqai_info.get("model_training_parameters", {}).copy()
            
            # 设置默认值，但不覆盖已有配置
            default_params = {
                "learning_rate": 0.00025,
                "gamma": 0.9,
                "verbose": 1
            }
            
            # 合并参数，配置文件优先
            final_params = {**default_params, **training_params}
            
            model = PPO(
                self.policy_type,                    # 策略类型 (MlpPolicy)
                self.train_env,                      # 训练环境
                policy_kwargs=policy_kwargs,         # 策略网络参数
                tensorboard_log=tb_path,             # Tensorboard日志
                **final_params,
            )
        else:
            # 使用持续学习：加载之前的模型继续训练
            logger.info("启用持续学习 - 从之前训练的模型开始")
            model = self.dd.model_dictionary[dk.pair]
            model.set_env(self.train_env)
        
        # === 设置训练回调函数 ===
        callbacks = [self.eval_callback, self.tensorboard_callback]
        
        # 可选：添加进度条
        progressbar_callback: ProgressBarCallback | None = None
        if self.rl_config.get("progress_bar", False):
            progressbar_callback = ProgressBarCallback()
            callbacks.insert(0, progressbar_callback)
        
        # === 开始训练模型 ===
        try:
            logger.info("开始模型训练...")
            model.learn(
                total_timesteps=int(total_timesteps),
                callback=callbacks,
            )
            logger.info("模型训练完成")
        finally:
            # 清理进度条资源
            if progressbar_callback:
                progressbar_callback.on_training_end()
        
        # === 加载最佳模型 ===
        best_model_path = dk.data_path / "best_model.zip"
        if best_model_path.is_file():
            logger.info("找到最佳模型，加载中...")
            best_model = PPO.load(dk.data_path / "best_model")
            return best_model
        
        logger.info("未找到最佳模型，使用最终训练模型")
        return model

    class MyRLEnv(Base3ActionRLEnv):
        """
        自定义强化学习交易环境
        
        这个环境定义了智能体与市场交互的方式，包括:
        - 状态表示：市场的当前状态
        - 动作空间：买入/卖出/持有
        - 奖励函数：评估动作的好坏
        """

        def calculate_reward(self, action: int) -> float:
            """
            自定义奖励函数
            
            这是强化学习中最关键的部分，定义了什么样的行为会得到奖励。
            好的奖励函数应该：
            1. 鼓励盈利的交易
            2. 惩罚亏损的交易
            3. 考虑交易频率和风险
            4. 平衡短期和长期收益
            
            Args:
                action: 智能体的动作 (0=持有, 1=买入, 2=卖出)
                
            Returns:
                奖励值（正数=好的行为，负数=坏的行为）
            """
            
            # === 基础验证 ===
            if not self._is_valid(action):
                logger.warning(f"无效动作: {action}")
                return -2  # 严重惩罚无效动作
            
            # === 获取当前市场状态 ===
            current_profit_pct = self.get_unrealized_profit()  # 当前未实现盈亏
            current_position = self._position                   # 当前仓位状态
            
            # === 初始化奖励 ===
            reward = 0
            
            # === 买入动作的奖励逻辑 ===
            if action == Actions.Buy.value:
                if current_position == Positions.Neutral:
                    # 从空仓买入：根据后续价格变化给奖励
                    if current_profit_pct > 0:
                        # 买入后价格上涨：给予正奖励
                        reward = current_profit_pct * 100
                        logger.debug(f"买入后盈利: {current_profit_pct:.4f}, 奖励: {reward:.4f}")
                    else:
                        # 买入后价格下跌：给予负奖励，但不要太严重
                        reward = current_profit_pct * 50
                        logger.debug(f"买入后亏损: {current_profit_pct:.4f}, 奖励: {reward:.4f}")
                elif current_position == Positions.Short:
                    # 从空头转为多头：平仓并开新仓
                    reward = current_profit_pct * 80  # 平仓收益
                else:
                    # 已经持有多头仓位时再买入：给予小惩罚
                    reward = -0.5
                    logger.debug("重复买入操作，小幅惩罚")
            
            # === 卖出动作的奖励逻辑 ===
            elif action == Actions.Sell.value:
                if current_position == Positions.Long:
                    # 从多头卖出：实现利润
                    reward = current_profit_pct * 100  # 实现的利润/亏损
                    logger.debug(f"卖出多头，实现盈亏: {current_profit_pct:.4f}, 奖励: {reward:.4f}")
                elif current_position == Positions.Neutral:
                    # 空仓时卖出：如果支持做空且后续价格下跌则奖励
                    if self.can_short:
                        reward = -current_profit_pct * 80  # 做空收益
                    else:
                        reward = -1  # 不支持做空时惩罚
                        logger.debug("空仓时卖出操作，惩罚")
                else:
                    # 已经持有空头时再卖出：小惩罚
                    reward = -0.5
            
            # === 持有动作的奖励逻辑 ===
            elif action == Actions.Neutral.value:
                # 持有动作的奖励取决于市场状态
                if abs(current_profit_pct) < 0.005:  # 市场横盘时
                    reward = 0.1  # 小幅正奖励，鼓励在不确定时保持观望
                elif current_position == Positions.Long and current_profit_pct > 0:
                    # 持有盈利的多头仓位：小幅正奖励
                    reward = 0.2
                elif current_position == Positions.Short and current_profit_pct < 0:
                    # 持有盈利的空头仓位：小幅正奖励  
                    reward = 0.2
                else:
                    # 其他情况：根据市场趋势给予小幅奖励/惩罚
                    reward = -abs(current_profit_pct) * 10
            
            # === 交易频率控制 ===
            # 惩罚过于频繁的交易
            if self._last_trade_tick is not None:
                ticks_since_last_trade = self._current_tick - self._last_trade_tick
                if ticks_since_last_trade < 5:  # 5个时间单位内的频繁交易
                    frequency_penalty = 0.5 * (5 - ticks_since_last_trade) / 5
                    reward -= frequency_penalty
                    logger.debug(f"频繁交易惩罚: {frequency_penalty:.4f}")
            
            # === 持仓时间奖励 ===
            # 奖励适度的持仓时间（避免过度交易）
            trade_duration = self.get_trade_duration()
            if trade_duration > 10 and current_profit_pct > 0:
                # 持仓时间长且盈利：额外奖励
                duration_bonus = min(0.3, trade_duration * 0.02)
                reward += duration_bonus
                logger.debug(f"持仓时间奖励: {duration_bonus:.4f}")
            
            # === 风险控制奖励 ===
            # 如果当前亏损超过一定阈值，鼓励止损
            if current_profit_pct < -0.03:  # 亏损超过3%
                if action == Actions.Sell.value and current_position == Positions.Long:
                    reward += 0.5  # 奖励及时止损
                    logger.debug("及时止损奖励")
                elif action == Actions.Buy.value and current_position == Positions.Short:
                    reward += 0.5  # 奖励及时止损
                    logger.debug("及时止损奖励")
            
            # === 趋势跟随奖励 ===
            # 简单的趋势判断：如果价格连续上涨/下跌，奖励顺势操作
            if hasattr(self, '_price_history') and len(self._price_history) >= 3:
                recent_prices = self._price_history[-3:]
                if all(recent_prices[i] < recent_prices[i+1] for i in range(len(recent_prices)-1)):
                    # 上升趋势：奖励买入，惩罚卖出
                    if action == Actions.Buy.value:
                        reward += 0.2
                        logger.debug("顺势买入奖励")
                    elif action == Actions.Sell.value and current_position == Positions.Long:
                        reward -= 0.1  # 轻微惩罚逆势操作
                elif all(recent_prices[i] > recent_prices[i+1] for i in range(len(recent_prices)-1)):
                    # 下降趋势：奖励卖出，惩罚买入
                    if action == Actions.Sell.value:
                        reward += 0.2
                        logger.debug("顺势卖出奖励")
                    elif action == Actions.Buy.value and current_position == Positions.Neutral:
                        reward -= 0.1  # 轻微惩罚逆势操作
            
            # === 记录价格历史（用于趋势判断） ===
            if not hasattr(self, '_price_history'):
                self._price_history = []
            self._price_history.append(self.current_price())
            if len(self._price_history) > 10:  # 只保留最近10个价格
                self._price_history.pop(0)
            
            # === 最终奖励调整 ===
            # 将奖励限制在合理范围内，避免过大的奖励值影响训练稳定性
            reward = np.clip(reward, -10, 10)
            
            logger.debug(f"最终奖励: {reward:.4f}, 动作: {action}, 仓位: {current_position}, 盈亏: {current_profit_pct:.4f}")
            
            return float(reward)

        def _is_valid(self, action: int) -> bool:
            """
            检查动作是否有效
            
            Args:
                action: 要检查的动作
                
            Returns:
                动作是否有效
            """
            # 检查动作是否在有效范围内
            if action not in [Actions.Neutral.value, Actions.Buy.value, Actions.Sell.value]:
                return False
            
            # 可以添加更多的有效性检查，比如：
            # - 检查是否有足够的资金买入
            # - 检查是否有仓位可以卖出
            # - 检查市场是否开放等
            
            return True

        def reset(self, **kwargs):
            """
            重置环境到初始状态
            
            在每个训练episode开始时调用
            """
            # 调用父类的reset方法
            obs = super().reset(**kwargs)
            
            # 重置自定义变量
            self._price_history = []
            
            logger.debug("环境已重置")
            return obs

        def step(self, action: int):
            """
            执行一个动作并返回新的状态
            
            Args:
                action: 要执行的动作
                
            Returns:
                (observation, reward, terminated, truncated, info): 新状态、奖励、是否终止、是否截断、额外信息
            """
            # 调用父类的step方法
            result = super().step(action)
            
            # 处理不同版本的返回值
            if len(result) == 4:
                # 旧版本：observation, reward, done, info
                observation, reward, done, info = result
                terminated = done
                truncated = False
            elif len(result) == 5:
                # 新版本：observation, reward, terminated, truncated, info
                observation, reward, terminated, truncated, info = result
                done = terminated or truncated
            else:
                raise ValueError(f"Unexpected number of return values: {len(result)}")
            
            # 可以在这里添加额外的逻辑，比如记录统计信息
            if done:
                logger.info(f"Episode结束, 总奖励: {self.total_reward:.4f}")
            
            return observation, reward, terminated, truncated, info 
