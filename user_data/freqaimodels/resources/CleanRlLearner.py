from typing import Any, Dict, Optional, Union

import gymnasium as gym
import numpy as np
import torch
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.RL.BaseReinforcementLearningModel import (
    BaseReinforcementLearningModel,
)
from pandas import DataFrame
from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor

from user_data.rl.agents.simple_nn import ActorCriticAgent, SimpleNnActorCriticModel
from user_data.rl.env.my_rl_env import MyRLEnv as UserMyRLEnv
from user_data.rl.trainer.args import Args
from user_data.rl.trainer.ppo import PpoTrainer


class CleanRlLearner(BaseReinforcementLearningModel):
    def __init__(self, **kwargs) -> None:
        super().__init__(config=kwargs["config"])
        self.max_threads = min(
            self.freqai_info["rl_config"].get("cpu_count", 1),
            max(int(self.max_system_threads / 2), 1),
        )
        torch.set_num_threads(self.max_threads)
        self.reward_params = self.freqai_info["rl_config"]["model_reward_parameters"]
        self.train_env: Union[VecMonitor, SubprocVecEnv, gym.Env] = gym.Env()
        self.eval_env: Union[VecMonitor, SubprocVecEnv, gym.Env] = gym.Env()
        self.eval_callback: Optional[MaskableEvalCallback] = None
        self.model_type = self.freqai_info["rl_config"]["model_type"]
        self.rl_config: Dict[str, Any] = self.freqai_info["rl_config"]
        self.df_raw: DataFrame = DataFrame()
        self.continual_learning = self.freqai_info.get("continual_learning", False)

        self.unset_outlier_removal()
        self.dd.model_type = "pytorch"

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
        max_steps = self.rl_config.get("max_trade_duration_candles", 300)
        args = Args()
        args.track = self.rl_config.get("enable_wandb", False)
        args.num_steps = max_steps
        args.num_envs = 1
        args.wandb_project_name = self.config.get("bot_name", "Freqtrade")

        model = SimpleNnActorCriticModel(
            input_dim=np.array(self.train_env.observation_space.shape).prod(),
            output_dim=self.train_env.action_space.n,
            hidden_dim=self.rl_config.get("hidden_dim", 128),
        )
        agent = ActorCriticAgent(model)

        trainer = PpoTrainer(
            lambda render_mode: self.train_env,
            agent.model,
            args=args,
        )
        trainer.train()
        return agent

    # def define_data_pipeline(self, threads=-1) -> Pipeline:
    #     pipe_steps = [
    #         # ("const", ds.VarianceThreshold(threshold=0)),
    #         # ("scaler", SKLearnWrapper(MinMaxScaler(feature_range=(-1, 1)))),
    #     ]
    #     return Pipeline(pipe_steps)

    class MyRLEnv(UserMyRLEnv):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
