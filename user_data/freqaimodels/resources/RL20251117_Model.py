from freqtrade.freqai.prediction_models.ReinforcementLearner_multiproc import ReinforcementLearner_multiproc
from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv
from freqtrade.freqai.RL.BaseEnvironment import Positions

class RL20251117_Model(ReinforcementLearner_multiproc):
    """
    RL20251117 Model
    
    Uses Base5ActionRLEnv:
    0: Neutral
    1: Long Enter
    2: Long Exit
    3: Short Enter
    4: Short Exit
    """
    
    class MyRLEnv(Base5ActionRLEnv):
        def calculate_reward(self, action: int) -> float:
            # Load params from config
            params = self.rl_config["model_reward_parameters"]
            
            penalty_invalid = params.get("penalty_invalid_action", -2.0)
            penalty_liquidation = params.get("penalty_liquidation", -200.0)
            liquidation_threshold = params.get("liquidation_threshold", -0.8)
            heavy_loss_threshold = params.get("penalty_heavy_loss_threshold", -0.10)
            heavy_loss_factor = params.get("penalty_heavy_loss_factor", 20.0)
            heavy_loss_offset = params.get("penalty_heavy_loss_offset", 20.0)
            reward_profit_factor = params.get("reward_profit_factor", 10.0)
            time_factor = params.get("penalty_time_factor", 0.1)
            time_threshold = params.get("penalty_time_threshold", 100)
            penalty_inaction = params.get("penalty_inaction", -0.05)
            reward_entry = params.get("reward_entry", 25.0)

            # 1. 基礎檢查 (Basic Check)
            if not self._is_valid(action):
                return penalty_invalid
            
            # 2. 鼓勵進場交易 (Entry Rewards)
            if action == Actions.Long_enter.value and self._position == Positions.Neutral:
                return reward_entry
            if action == Actions.Short_enter.value and self._position == Positions.Neutral:
                return reward_entry
            
            # 3. 懲罰不作為 (Inaction Penalty)
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return penalty_inaction
                
            pnl = self.get_unrealized_profit()
            
            # 4. PNL 獎勵邏輯 (PNL-based Rewards)
            reward = 0.0
            
            # A. 強制平倉 (Liquidation) 或 極大虧損
            if pnl < liquidation_threshold: 
                return penalty_liquidation
                
            # B. 虧損超過閾值
            if pnl < heavy_loss_threshold:
                # 加重懲罰
                reward = (pnl * heavy_loss_factor) - heavy_loss_offset
                
            # C. 一般虧損
            elif pnl < 0:
                reward = pnl * reward_profit_factor
                
            # D. 獲利
            elif pnl > 0:
                reward = pnl * reward_profit_factor
                
            # E. 持倉時間懲罰 (Time Penalty)
            if self._position != Positions.Neutral:
                trade_duration = self._current_tick - self._last_trade_tick
                if trade_duration > time_threshold:
                    reward -= time_factor * (trade_duration / time_threshold)


            return reward
