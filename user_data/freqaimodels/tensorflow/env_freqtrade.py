import gym.envs.registration
from freqtrade.freqai.RL.Base5ActionRLEnv import Base5ActionRLEnv
# from freqtrade.freqai.RL.BaseReinforcementLearningModel import make_env

gym.envs.registration.register(
    id='Base5ActionRLEnv-v0',
    entry_point=__name__ + ':Base5ActionRLEnv',
    max_episode_steps=10,
)
