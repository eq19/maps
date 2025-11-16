import logging
from pathlib import Path
from typing import Any, Dict

import torch as th

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.RL.Base5ActionRLEnv import Actions, Base5ActionRLEnv, Positions
# from freqtrade.freqai.RL.BaseReinforcementLearningModel import BaseReinforcementLearningModel
from BaseReinforcementLearningModelSRL import BaseReinforcementLearningModelSRL

import srl
from srl import runner
from srl.rl.models.alphazero_image_block import AlphaZeroImageBlock
from srl.envs import grid
from srl.algorithms import stochastic_muzero

logger = logging.getLogger(__name__)

import gym
# gym.envs.registration.register(
    # id='MyRLEnv-v0',
    # entry_point=__name__ + ':MyRLEnv',
    # max_episode_steps=10,
# )
# gym.envs.registration.register(
    # id='Base5ActionRLEnv-v0',
    # entry_point=__name__ + ':Base5ActionRLEnv',
    # max_episode_steps=10,
# )
# import env_freqtrade

class ReinforcementLearnerSRL(BaseReinforcementLearningModelSRL):
    """
    Reinforcement Learning Model prediction model.

    Users can inherit from this class to make their own RL model with custom
    environment/training controls. Define the file as follows:

    ```
    from freqtrade.freqai.prediction_models.ReinforcementLearner import ReinforcementLearner

    class MyCoolRLModel(ReinforcementLearner):
    ```

    Save the file to `user_data/freqaimodels`, then run it with:

    freqtrade trade --freqaimodel MyCoolRLModel --config config.json --strategy SomeCoolStrat

    Here the users can override any of the functions
    available in the `IFreqaiModel` inheritance tree. Most importantly for RL, this
    is where the user overrides `MyRLEnv` (see below), to define custom
    `calculate_reward()` function, or to override any other parts of the environment.

    This class also allows users to override any other part of the IFreqaiModel tree.
    For example, the user can override `def fit()` or `def train()` or `def predict()`
    to take fine-tuned control over these processes.

    Another common override may be `def data_cleaning_predict()` where the user can
    take fine-tuned control over the data handling pipeline.
    """

    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs):
        """
        User customizable fit method
        :param data_dictionary: dict = common data dictionary containing all train/test
            features/labels/weights.
        :param dk: FreqaiDatakitchen = data kitchen for current pair.
        :return:
        model Any = trained model to be used for inference in dry/live/backtesting
        """
        train_df = data_dictionary["train_features"]
        total_timesteps = self.freqai_info["rl_config"]["train_cycles"] * len(train_df)

        # policy_kwargs = dict(activation_fn=th.nn.ReLU,
                             # net_arch=self.net_arch)

        if dk.pair not in self.dd.model_dictionary or not self.continual_learning:
            # model = self.MODELCLASS(self.policy_type, self.train_env, policy_kwargs=policy_kwargs,
                                    # tensorboard_log=Path(
                                        # dk.full_path / "tensorboard" / dk.pair.split('/')[0]),
                                    # **self.freqai_info.get('model_training_parameters', {})
                                    # )

            rl_config = stochastic_muzero.Config(
                num_simulations=10,
                discount=0.9,
                batch_size=16,
                memory_warmup_size=200,
                memory_name="ReplayMemory",
                lr_init=0.01,
                lr_decay_steps=10_000,
                v_min=-2,
                v_max=2,
                unroll_steps=1,
                input_image_block=AlphaZeroImageBlock,
                input_image_block_kwargs={"n_blocks": 1, "filters": 16},
                dynamics_blocks=1,
                enable_rescale=False,
                codebook_size=4,
            )
            rl_config.processors = [grid.LayerProcessor()]
            env_config = srl.EnvConfig('MyRLEnv-v0')
            # env_config = gym.make('Base5ActionRLEnv-v0')
            # env_config = gym.make('MyRLEnv-v0')
            # env_config = self.train_env
            # env_config = self.MyRLEnv
            config = runner.Config(env_config, rl_config)
            config.model_summary()

        else:
            logger.info('Continual training activated - starting training from previously '
                        'trained agent.')
            model = self.dd.model_dictionary[dk.pair]
            model.set_env(self.train_env)

        # model.learn(
            # total_timesteps=int(total_timesteps),
            # callback=[self.eval_callback, self.tensorboard_callback]
        # )

        parameter, memory, history = runner.train(config, max_episodes=total_timesteps,
                                                  callbacks=[self.eval_callback])  # self.tensorboard_callback
        print(parameter)
        print(memory)
        print(history)

        # rewards = runner.evaluate(config, parameter, max_episodes=10, print_progress=True)
        # print("mean", np.mean(rewards))

        if Path(dk.data_path / "best_model.zip").is_file():
            logger.info('Callback found a best model.')
            best_model = self.MODELCLASS.load(dk.data_path / "best_model")
            return best_model

        logger.info('Couldnt find best model, using final model instead.')

        return model

    class MyRLEnv(Base5ActionRLEnv):

        """
        User can override any function in BaseRLEnv and gym.Env. Here the user
        sets a custom reward based on profit and trade duration.
        """

        def calculate_reward(self, action: int) -> float:
            """
            An example reward function. This is the one function that users will likely
            wish to inject their own creativity into.
            :param action: int = The action made by the agent for the current candle.
            :return:
            float = the reward to give to the agent for current step (used for optimization
                of weights in NN)
            """
            # first, penalize if the action is not valid
            if not self._is_valid(action):
                self.tensorboard_log("is_valid")
                return -2

            pnl = self.get_unrealized_profit()
            factor = 100.

            # reward agent for entering trades
            if (action == Actions.Long_enter.value
                    and self._position == Positions.Neutral):
                return 25
            if (action == Actions.Short_enter.value
                    and self._position == Positions.Neutral):
                return 25
            # discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                return -1

            max_trade_duration = self.rl_config.get('max_trade_duration_candles', 300)
            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            if trade_duration <= max_trade_duration:
                factor *= 1.5
            elif trade_duration > max_trade_duration:
                factor *= 0.5

            # discourage sitting in position
            if (self._position in (Positions.Short, Positions.Long) and
                    action == Actions.Neutral.value):
                return -1 * trade_duration / max_trade_duration

            # close long
            if action == Actions.Long_exit.value and self._position == Positions.Long:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)

            # close short
            if action == Actions.Short_exit.value and self._position == Positions.Short:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config['model_reward_parameters'].get('win_reward_factor', 2)
                return float(pnl * factor)

            return 0.
