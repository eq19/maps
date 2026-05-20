import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Type

import torch as th
from stable_baselines3.common.callbacks import ProgressBarCallback

from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from freqtrade.freqai.RL.Base3ActionRLEnv import Actions, Base3ActionRLEnv, Positions
from freqtrade.freqai.RL.BaseEnvironment import BaseEnvironment
from freqtrade.freqai.RL.BaseReinforcementLearningModel import BaseReinforcementLearningModel
from freqtrade.data.metrics import calculate_max_drawdown
import mlflow
import copy

logger = logging.getLogger(__name__)


class ChronosRLMLflow(BaseReinforcementLearningModel):
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

        mlflow.set_tracking_uri("/freqtrade/user_data/mlruns")
        # logger.info(Path(dk.data_path / "mlruns"))
        mlflow.set_experiment("PAPER")
        # mlflow.autolog()

        with mlflow.start_run(run_name=f"tarl-{self.model_type}_{dk.pair}") as run:
            train_df = data_dictionary["train_features"]
            total_timesteps = self.freqai_info["rl_config"]["train_cycles"] * len(
                train_df)
            # logger.info(train_df.head())
            dataset = mlflow.data.from_pandas(
                train_df)
            with open("/freqtrade/user_data/data/ml/train_df.csv", "w") as f:
                f.write(train_df.to_csv())
            mlflow.log_artifact("/freqtrade/user_data/data/ml/train_df.csv")
            mlflow.log_input(dataset, context="training")

            policy_kwargs = dict(activation_fn=th.nn.ReLU,
                                 net_arch=self.net_arch)

            if self.activate_tensorboard:
                tb_path = Path(dk.full_path / "tensorboard" /
                               dk.pair.split("/")[0])
            else:
                tb_path = None

            if dk.pair not in self.dd.model_dictionary or not self.continual_learning:
                model = self.MODELCLASS(
                    self.policy_type,
                    self.train_env,
                    policy_kwargs=policy_kwargs,
                    tensorboard_log=tb_path,
                    **self.freqai_info.get("model_training_parameters", {}),
                )
                logger.info(model)
                logger.info(policy_kwargs)
                # logger.info(**self.freqai_info.get(
                #     "freqai", {}))
                mlflow.log_params(policy_kwargs)
                params = model.get_parameters()

                cfg = copy.deepcopy(self.config)
                cfg.pop('api_server')
                cfg.pop('telegram')
                cfg.pop('original_config')
                fai = cfg.pop('freqai')
                rl = fai.pop('rl_config')
                mlflow.log_params(cfg)
                mlflow.log_params(fai)
                mlflow.log_params(rl)

            else:
                logger.info(
                    "Continual training activated - starting training from previously trained agent."
                )
                model = self.dd.model_dictionary[dk.pair]
                logger.info(model)
                model.set_env(self.train_env)
            callbacks: List[Any] = [
                self.eval_callback, self.tensorboard_callback]
            progressbar_callback: Optional[ProgressBarCallback] = None
            if self.rl_config.get("progress_bar", False):
                progressbar_callback = ProgressBarCallback()
                callbacks.insert(0, progressbar_callback)

            try:
                model.learn(
                    total_timesteps=int(total_timesteps),
                    callback=callbacks
                )
            finally:
                if progressbar_callback:
                    progressbar_callback.on_training_end()

            if Path(dk.data_path / "best_model.zip").is_file():
                logger.info("Callback found a best model.")
                best_model = self.MODELCLASS.load(dk.data_path / "best_model")
                logger.info(dk)
                mlflow.log_artifact(dk.data_path / "best_model.zip")
                return best_model

            logger.info("Couldn't find best model, using final model instead.")

            return model

    MyRLEnv: Type[BaseEnvironment]

    class MyRLEnv(Base3ActionRLEnv):  # type: ignore[no-redef]
        """
        User can override any function in BaseRLEnv and gym.Env. Here the user
        sets a custom reward based on profit and trade duration.
        """

        def calculate_reward(self, action: int) -> float:
            """
            An example reward function. This is the one function that users will likely
            wish to inject their own creativity into.

            Warning!
            This is function is a showcase of functionality designed to show as many possible
            environment control features as possible. It is also designed to run quickly
            on small computers. This is a benchmark, it is *not* for live production.

            :param action: int = The action made by the agent for the current candle.
            :return:
            float = the reward to give to the agent for current step (used for optimization
                of weights in NN)
            """
            # first, penalize if the action is not valid
            if not self._is_valid(action):
                self.tensorboard_log("invalid", category="actions")
                return -1

            pnl = self.get_unrealized_profit()
            factor = 100.0

            pair = self.pair.replace(':', '')

            # reward agent for entering trades
            if action == Actions.Buy.value and self._position == Positions.Neutral:
                self.tensorboard_log("enter_trade", category="actions")
                return 1
            # discourage agent from not entering trades
            if action == Actions.Neutral.value and self._position == Positions.Neutral:
                self.tensorboard_log("not_enter_trade", category="actions")
                return -1

            max_trade_duration = self.rl_config.get(
                "max_trade_duration_candles", 300)
            trade_duration = self._current_tick - self._last_trade_tick  # type: ignore

            # if trade_duration <= max_trade_duration:
            #     factor *= 1.5
            # elif trade_duration > max_trade_duration:
            #     factor *= 0.5

            # discourage sitting in position
            if (
                self._position == Positions.Long
                and action == Actions.Neutral.value
            ):
                return -1 * trade_duration / max_trade_duration

            # close long
            if action == Actions.Sell.value and self._position == Positions.Long:
                if pnl > self.profit_aim * self.rr:
                    factor *= self.rl_config["model_reward_parameters"].get(
                        "profit_aim_reward", 1)
                    # pnl *= self.rl_config["model_reward_parameters"].get(
                    #     "win_reward_factor", 1)
                else:
                    factor *= self.rl_config["model_reward_parameters"].get(
                        "lose_reward_factor", -1)
                self.tensorboard_log(
                    "profit_reward", pnl*factor, category="profit")
                # return float(pnl * factor)
                return float(pnl) * factor
            return 0.0

            # risk trade long
            if action == Actions.Sell.value and self._position == Positions.Long:
                # calculate max drawdown for this trade
                # retrieve all prices for the current trade
                prices = self.prices.iloc[self._last_trade_tick:self._current_tick]
                current_price = self.prices.iloc[self._current_tick]['close']
                open_price = self.prices.iloc[self._last_trade_tick]['close']
                min_price = prices['close'].min()
                drawdown = (min_price - open_price)
                self.tensorboard_log(
                    "max_drawdown", drawdown, category="drawdown")
                return drawdown * 1  # drawndown x peso
