import copy
import json
import logging
import random
import time
import warnings
from functools import cached_property
from pathlib import Path
from typing import Any, Callable, Optional

import numpy as np
import optuna
import pandas as pd
import scipy as sp
import skimage
import sklearn
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
from numpy.typing import NDArray

from Utils import (
    calculate_min_extrema,
    calculate_n_extrema,
    fit_regressor,
    format_number,
    get_min_max_label_period_candles,
    get_optuna_callbacks,
    get_optuna_study_model_parameters,
    soft_extremum,
    zigzag,
)

debug = False

TEST_SIZE = 0.1

EXTREMA_COLUMN = "&s-extrema"
MAXIMA_THRESHOLD_COLUMN = "&s-maxima_threshold"
MINIMA_THRESHOLD_COLUMN = "&s-minima_threshold"

warnings.simplefilter(action="ignore", category=FutureWarning)

logger = logging.getLogger(__name__)


class QuickAdapterRegressorV3(BaseRegressionModel):
    """
    The following freqaimodel is released to sponsors of the non-profit FreqAI open-source project.
    If you find the FreqAI project useful, please consider supporting it by becoming a sponsor.
    We use sponsor money to help stimulate new features and to pay for running these public
    experiments, with a an objective of helping the community make smarter choices in their
    ML journey.

    This freqaimodel is experimental (as with all models released to sponsors). Do *not* expect
    returns. The goal is to demonstrate gratitude to people who support the project and to
    help them find a good starting point for their own creativity.

    If you have questions, please direct them to our discord: https://discord.gg/xE4RMg4QYw

    https://github.com/sponsors/robcaulk
    """

    version = "3.7.112"

    @cached_property
    def _optuna_config(self) -> dict[str, Any]:
        optuna_default_config = {
            "enabled": False,
            "n_jobs": min(
                self.freqai_info.get("optuna_hyperopt", {}).get("n_jobs", 1),
                max(int(self.max_system_threads / 4), 1),
            ),
            "storage": "file",
            "continuous": True,
            "warm_start": True,
            "n_startup_trials": 15,
            "n_trials": 36,
            "timeout": 7200,
            "label_candles_step": 1,
            "train_candles_step": 10,
            "expansion_ratio": 0.4,
            "seed": 1,
        }
        return {
            **optuna_default_config,
            **self.freqai_info.get("optuna_hyperopt", {}),
        }

    @property
    def _optuna_label_candle_pool_full(self) -> list[int]:
        if not hasattr(self, "pairs") or not self.pairs:
            raise RuntimeError(
                "Failed to initialize optuna label candle pool full: pairs property is not defined or empty"
            )
        n_pairs = len(self.pairs)
        label_frequency_candles = max(
            2, 2 * n_pairs, int(self.ft_params.get("label_frequency_candles", 12))
        )
        cache_key = label_frequency_candles
        if cache_key not in self._optuna_label_candle_pool_full_cache:
            half_label_frequency_candles = int(label_frequency_candles / 2)
            min_offset = -half_label_frequency_candles
            max_offset = half_label_frequency_candles
            self._optuna_label_candle_pool_full_cache[cache_key] = [
                max(1, label_frequency_candles + offset)
                for offset in range(min_offset, max_offset + 1)
            ]
        return copy.deepcopy(self._optuna_label_candle_pool_full_cache[cache_key])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pairs: list[str] = self.config.get("exchange", {}).get("pair_whitelist")
        if not self.pairs:
            raise ValueError(
                "FreqAI model requires StaticPairList method defined in pairlists configuration and 'pair_whitelist' defined in exchange section configuration"
            )
        if (
            not isinstance(self.freqai_info.get("identifier"), str)
            or self.freqai_info.get("identifier").strip() == ""
        ):
            raise ValueError(
                "FreqAI model requires 'identifier' defined in the freqai section configuration"
            )
        self._optuna_hyperopt: Optional[bool] = (
            self.freqai_info.get("enabled", False)
            and self._optuna_config.get("enabled")
            and self.data_split_parameters.get("test_size", TEST_SIZE) > 0
        )
        self._optuna_hp_value: dict[str, float] = {}
        self._optuna_train_value: dict[str, float] = {}
        self._optuna_label_values: dict[str, list[float | int]] = {}
        self._optuna_hp_params: dict[str, dict[str, Any]] = {}
        self._optuna_train_params: dict[str, dict[str, Any]] = {}
        self._optuna_label_params: dict[str, dict[str, Any]] = {}
        self._optuna_label_candle_pool_full_cache: dict[int, list[int]] = {}
        self.init_optuna_label_candle_pool()
        self._optuna_label_candle: dict[str, int] = {}
        self._optuna_label_candles: dict[str, int] = {}
        self._optuna_label_incremented_pairs: list[str] = []
        for pair in self.pairs:
            self._optuna_hp_value[pair] = -1
            self._optuna_train_value[pair] = -1
            self._optuna_label_values[pair] = [-1, -1]
            self._optuna_hp_params[pair] = (
                self.optuna_load_best_params(pair, "hp")
                if self.optuna_load_best_params(pair, "hp")
                else {}
            )
            self._optuna_train_params[pair] = (
                self.optuna_load_best_params(pair, "train")
                if self.optuna_load_best_params(pair, "train")
                else {}
            )
            self._optuna_label_params[pair] = (
                self.optuna_load_best_params(pair, "label")
                if self.optuna_load_best_params(pair, "label")
                else {
                    "label_period_candles": self.ft_params.get(
                        "label_period_candles", 24
                    ),
                    "label_natr_ratio": float(
                        self.ft_params.get("label_natr_ratio", 6.0)
                    ),
                }
            )
            self.set_optuna_label_candle(pair)
            self._optuna_label_candles[pair] = 0

        logger.info(
            f"Initialized {self.__class__.__name__} {self.freqai_info.get('regressor', 'xgboost')} regressor model version {self.version}"
        )

    def get_optuna_params(self, pair: str, namespace: str) -> dict[str, Any]:
        if namespace == "hp":
            params = self._optuna_hp_params.get(pair)
        elif namespace == "train":
            params = self._optuna_train_params.get(pair)
        elif namespace == "label":
            params = self._optuna_label_params.get(pair)
        else:
            raise ValueError(f"Invalid namespace: {namespace}")
        return params

    def set_optuna_params(
        self, pair: str, namespace: str, params: dict[str, Any]
    ) -> None:
        if namespace == "hp":
            self._optuna_hp_params[pair] = params
        elif namespace == "train":
            self._optuna_train_params[pair] = params
        elif namespace == "label":
            self._optuna_label_params[pair] = params
        else:
            raise ValueError(f"Invalid namespace: {namespace}")

    def get_optuna_value(self, pair: str, namespace: str) -> float:
        if namespace == "hp":
            value = self._optuna_hp_value.get(pair)
        elif namespace == "train":
            value = self._optuna_train_value.get(pair)
        else:
            raise ValueError(f"Invalid namespace: {namespace}")
        return value

    def set_optuna_value(self, pair: str, namespace: str, value: float) -> None:
        if namespace == "hp":
            self._optuna_hp_value[pair] = value
        elif namespace == "train":
            self._optuna_train_value[pair] = value
        else:
            raise ValueError(f"Invalid namespace: {namespace}")

    def get_optuna_values(self, pair: str, namespace: str) -> list[float | int]:
        if namespace == "label":
            values = self._optuna_label_values.get(pair)
        else:
            raise ValueError(f"Invalid namespace: {namespace}")
        return values

    def set_optuna_values(
        self, pair: str, namespace: str, values: list[float | int]
    ) -> None:
        if namespace == "label":
            self._optuna_label_values[pair] = values
        else:
            raise ValueError(f"Invalid namespace: {namespace}")

    def init_optuna_label_candle_pool(self) -> None:
        optuna_label_candle_pool_full = self._optuna_label_candle_pool_full
        if len(optuna_label_candle_pool_full) == 0:
            raise RuntimeError("Failed to initialize optuna label candle pool full")
        self._optuna_label_candle_pool = optuna_label_candle_pool_full
        random.shuffle(self._optuna_label_candle_pool)
        if len(self._optuna_label_candle_pool) == 0:
            raise RuntimeError("Failed to initialize optuna label candle pool")

    def set_optuna_label_candle(self, pair: str) -> None:
        if len(self._optuna_label_candle_pool) == 0:
            logger.warning(
                "Optuna label candle pool is empty, reinitializing it ("
                f"{self._optuna_label_candle_pool=} ,"
                f"{self._optuna_label_candle_pool_full=} ,"
                f"{self._optuna_label_candle.values()=} ,"
                f"{self._optuna_label_candles.values()=} ,"
                f"{self._optuna_label_incremented_pairs=})"
            )
            self.init_optuna_label_candle_pool()
        optuna_label_candle_pool = copy.deepcopy(self._optuna_label_candle_pool)
        for p in self.pairs:
            if p == pair:
                continue
            optuna_label_candle = self._optuna_label_candle.get(p)
            optuna_label_candles = self._optuna_label_candles.get(p)
            if optuna_label_candle is not None and optuna_label_candles is not None:
                if (
                    self._optuna_label_incremented_pairs
                    and p not in self._optuna_label_incremented_pairs
                ):
                    optuna_label_candles += 1
                remaining_candles = optuna_label_candle - optuna_label_candles
                if remaining_candles in optuna_label_candle_pool:
                    optuna_label_candle_pool.remove(remaining_candles)
        optuna_label_candle = optuna_label_candle_pool.pop()
        self._optuna_label_candle[pair] = optuna_label_candle
        self._optuna_label_candle_pool.remove(optuna_label_candle)
        optuna_label_available_candles = (
            set(self._optuna_label_candle_pool_full)
            - set(self._optuna_label_candle_pool)
            - set(self._optuna_label_candle.values())
        )
        if len(optuna_label_available_candles) > 0:
            self._optuna_label_candle_pool.extend(optuna_label_available_candles)
            random.shuffle(self._optuna_label_candle_pool)

    def fit(
        self, data_dictionary: dict[str, Any], dk: FreqaiDataKitchen, **kwargs
    ) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :param data_dictionary: the dictionary constructed by DataHandler to hold
                                all the training and test data/labels.
        :param dk: the FreqaiDataKitchen object
        """

        X = data_dictionary.get("train_features")
        y = data_dictionary.get("train_labels")
        train_weights = data_dictionary.get("train_weights")

        X_test = data_dictionary.get("test_features")
        y_test = data_dictionary.get("test_labels")
        test_weights = data_dictionary.get("test_weights")

        model_training_parameters = self.model_training_parameters

        start_time = time.time()
        if self._optuna_hyperopt:
            self.optuna_optimize(
                pair=dk.pair,
                namespace="hp",
                objective=lambda trial: hp_objective(
                    trial,
                    str(self.freqai_info.get("regressor", "xgboost")),
                    X,
                    y,
                    train_weights,
                    X_test,
                    y_test,
                    test_weights,
                    self.get_optuna_params(dk.pair, "hp"),
                    model_training_parameters,
                    self._optuna_config.get("expansion_ratio"),
                ),
                direction=optuna.study.StudyDirection.MINIMIZE,
            )

            optuna_hp_params = self.get_optuna_params(dk.pair, "hp")
            if optuna_hp_params:
                model_training_parameters = {
                    **model_training_parameters,
                    **optuna_hp_params,
                }

            train_study = self.optuna_optimize(
                pair=dk.pair,
                namespace="train",
                objective=lambda trial: train_objective(
                    trial,
                    str(self.freqai_info.get("regressor", "xgboost")),
                    X,
                    y,
                    train_weights,
                    X_test,
                    y_test,
                    test_weights,
                    self.data_split_parameters.get("test_size", TEST_SIZE),
                    self.freqai_info.get("fit_live_predictions_candles", 100),
                    self._optuna_config.get("train_candles_step"),
                    model_training_parameters,
                ),
                direction=optuna.study.StudyDirection.MINIMIZE,
            )

            optuna_train_params = self.get_optuna_params(dk.pair, "train")
            if optuna_train_params and self.optuna_params_valid(
                dk.pair, "train", train_study
            ):
                train_period_candles = optuna_train_params.get("train_period_candles")
                if isinstance(train_period_candles, int) and train_period_candles > 0:
                    X = X.iloc[-train_period_candles:]
                    y = y.iloc[-train_period_candles:]
                    train_weights = train_weights[-train_period_candles:]

                test_period_candles = optuna_train_params.get("test_period_candles")
                if isinstance(test_period_candles, int) and test_period_candles > 0:
                    X_test = X_test.iloc[-test_period_candles:]
                    y_test = y_test.iloc[-test_period_candles:]
                    test_weights = test_weights[-test_period_candles:]

        eval_set, eval_weights = QuickAdapterRegressorV3.eval_set_and_weights(
            X_test,
            y_test,
            test_weights,
            self.data_split_parameters.get("test_size", TEST_SIZE),
        )

        model = fit_regressor(
            regressor=str(self.freqai_info.get("regressor", "xgboost")),
            X=X,
            y=y,
            train_weights=train_weights,
            eval_set=eval_set,
            eval_weights=eval_weights,
            model_training_parameters=model_training_parameters,
            init_model=self.get_init_model(dk.pair),
        )
        time_spent = time.time() - start_time
        self.dd.update_metric_tracker("fit_time", time_spent, dk.pair)

        return model

    def optuna_throttle_callback(
        self,
        pair: str,
        namespace: str,
        callback: Callable[[], None],
    ) -> None:
        if namespace != "label":
            raise ValueError(f"Invalid namespace: {namespace}")
        self._optuna_label_candles[pair] += 1
        if pair not in self._optuna_label_incremented_pairs:
            self._optuna_label_incremented_pairs.append(pair)
        optuna_label_remaining_candles = self._optuna_label_candle.get(
            pair
        ) - self._optuna_label_candles.get(pair)
        if optuna_label_remaining_candles <= 0:
            try:
                callback()
            except Exception as e:
                logger.error(
                    f"Error executing optuna {pair} {namespace} callback: {repr(e)}",
                    exc_info=True,
                )
            finally:
                self.set_optuna_label_candle(pair)
                self._optuna_label_candles[pair] = 0
        else:
            logger.info(
                f"Optuna {pair} {namespace} callback throttled, still {optuna_label_remaining_candles} candles to go"
            )
        if len(self._optuna_label_incremented_pairs) >= len(self.pairs):
            self._optuna_label_incremented_pairs = []

    def fit_live_predictions(self, dk: FreqaiDataKitchen, pair: str) -> None:
        warmed_up = True

        fit_live_predictions_candles = self.freqai_info.get(
            "fit_live_predictions_candles", 100
        )

        if self._optuna_hyperopt:
            self.optuna_throttle_callback(
                pair=pair,
                namespace="label",
                callback=lambda: self.optuna_optimize(
                    pair=pair,
                    namespace="label",
                    objective=lambda trial: label_objective(
                        trial,
                        self.data_provider.get_pair_dataframe(
                            pair=pair, timeframe=self.config.get("timeframe")
                        ),
                        fit_live_predictions_candles,
                        self._optuna_config.get("label_candles_step"),
                    ),
                    directions=[
                        optuna.study.StudyDirection.MAXIMIZE,
                        optuna.study.StudyDirection.MAXIMIZE,
                    ],
                ),
            )

        if self.live:
            if not hasattr(self, "exchange_candles"):
                self.exchange_candles = len(self.dd.model_return_values[pair].index)
            candles_diff = len(self.dd.historic_predictions[pair].index) - (
                fit_live_predictions_candles + self.exchange_candles
            )
            if candles_diff < 0:
                logger.warning(
                    f"{pair}: fit live predictions not warmed up yet, still {abs(candles_diff)} candles to go"
                )
                warmed_up = False

        pred_df = (
            self.dd.historic_predictions[pair]
            .iloc[-fit_live_predictions_candles:]
            .reset_index(drop=True)
        )

        if not warmed_up:
            dk.data["extra_returns_per_train"][MINIMA_THRESHOLD_COLUMN] = -2
            dk.data["extra_returns_per_train"][MAXIMA_THRESHOLD_COLUMN] = 2
        else:
            min_pred, max_pred = self.min_max_pred(
                pred_df,
                fit_live_predictions_candles,
                self.get_optuna_params(pair, "label").get("label_period_candles"),
            )
            dk.data["extra_returns_per_train"][MINIMA_THRESHOLD_COLUMN] = min_pred
            dk.data["extra_returns_per_train"][MAXIMA_THRESHOLD_COLUMN] = max_pred

        dk.data["labels_mean"], dk.data["labels_std"] = {}, {}
        for label in dk.label_list + dk.unique_class_list:
            pred_df_label = pred_df.get(label)
            if pred_df_label is None or pred_df_label.dtype == object:
                continue
            if not warmed_up:
                f = [0, 0]
            else:
                f = sp.stats.norm.fit(pred_df_label)
            dk.data["labels_mean"][label], dk.data["labels_std"][label] = f[0], f[1]

        di_values = pred_df.get("DI_values")

        # fit the DI_threshold
        if not warmed_up:
            f = [0, 0, 0]
            cutoff = 2
        else:
            f = sp.stats.weibull_min.fit(
                pd.to_numeric(di_values, errors="coerce").dropna()
            )
            cutoff = sp.stats.weibull_min.ppf(
                self.freqai_info.get("outlier_threshold", 0.999), *f
            )

        dk.data["DI_value_mean"] = di_values.mean()
        dk.data["DI_value_std"] = di_values.std()
        dk.data["extra_returns_per_train"]["DI_value_param1"] = f[0]
        dk.data["extra_returns_per_train"]["DI_value_param2"] = f[1]
        dk.data["extra_returns_per_train"]["DI_value_param3"] = f[2]
        dk.data["extra_returns_per_train"]["DI_cutoff"] = cutoff

        dk.data["extra_returns_per_train"]["label_period_candles"] = (
            self.get_optuna_params(pair, "label").get("label_period_candles")
        )
        dk.data["extra_returns_per_train"]["label_natr_ratio"] = self.get_optuna_params(
            pair, "label"
        ).get("label_natr_ratio")

        dk.data["extra_returns_per_train"]["hp_rmse"] = self.get_optuna_value(
            pair, "hp"
        )
        dk.data["extra_returns_per_train"]["train_rmse"] = self.get_optuna_value(
            pair, "train"
        )

    @staticmethod
    def eval_set_and_weights(
        X_test: pd.DataFrame,
        y_test: pd.DataFrame,
        test_weights: NDArray[np.float64],
        test_size: float,
    ) -> tuple[
        Optional[list[tuple[pd.DataFrame, pd.DataFrame]]],
        Optional[list[NDArray[np.float64]]],
    ]:
        if test_size == 0:
            eval_set = None
            eval_weights = None
        else:
            eval_set = [(X_test, y_test)]
            eval_weights = [test_weights]

        return eval_set, eval_weights

    def min_max_pred(
        self,
        pred_df: pd.DataFrame,
        fit_live_predictions_candles: int,
        label_period_candles: int,
    ) -> tuple[float, float]:
        label_period_cycles = fit_live_predictions_candles / label_period_candles
        thresholds_candles = int(
            self.freqai_info.get(
                "prediction_thresholds_candles",
                max(2, int(label_period_cycles)) * label_period_candles,
            )
        )
        pred_extrema = pred_df.get(EXTREMA_COLUMN).iloc[-thresholds_candles:].copy()
        thresholds_smoothing = str(
            self.freqai_info.get("prediction_thresholds_smoothing", "mean")
        )
        skimage_thresholds_smoothing_methods = {
            "isodata",
            "li",
            "mean",
            "minimum",
            "otsu",
            "triangle",
            "yen",
        }
        thresholds_smoothing_methods = skimage_thresholds_smoothing_methods.union(
            {"soft_extremum"}
        )
        if thresholds_smoothing == "soft_extremum":
            thresholds_alpha = float(
                self.freqai_info.get("prediction_thresholds_alpha", 12.0)
            )
            return QuickAdapterRegressorV3.soft_extremum_min_max(
                pred_extrema, thresholds_alpha
            )
        elif thresholds_smoothing in skimage_thresholds_smoothing_methods:
            return QuickAdapterRegressorV3.skimage_min_max(
                pred_extrema, thresholds_smoothing
            )
        else:
            raise ValueError(
                f"Unsupported thresholds smoothing method: {thresholds_smoothing}. Supported methods are {', '.join(thresholds_smoothing_methods)}"
            )

    @staticmethod
    def get_pred_min_max(pred_extrema: pd.Series) -> tuple[pd.Series, pd.Series]:
        pred_extrema = (
            pd.to_numeric(pred_extrema, errors="coerce")
            .where(np.isfinite, np.nan)
            .dropna()
        )
        if pred_extrema.empty:
            return pd.Series(dtype=float), pd.Series(dtype=float)
        n_pred_minima = max(1, sp.signal.find_peaks(-pred_extrema)[0].size)
        n_pred_maxima = max(1, sp.signal.find_peaks(pred_extrema)[0].size)

        sorted_pred_extrema = pred_extrema.sort_values(ascending=True)
        return sorted_pred_extrema.iloc[:n_pred_minima], sorted_pred_extrema.iloc[
            -n_pred_maxima:
        ]

    @staticmethod
    def safe_min_pred(pred_extrema: pd.Series) -> float:
        try:
            pred_minimum = pred_extrema.min()
        except Exception:
            pred_minimum = None
        if (
            pred_minimum is not None
            and isinstance(pred_minimum, (int, float, np.number))
            and np.isfinite(pred_minimum)
        ):
            return pred_minimum
        return -2.0

    @staticmethod
    def safe_max_pred(pred_extrema: pd.Series) -> float:
        try:
            pred_maximum = pred_extrema.max()
        except Exception:
            pred_maximum = None
        if (
            pred_maximum is not None
            and isinstance(pred_maximum, (int, float, np.number))
            and np.isfinite(pred_maximum)
        ):
            return pred_maximum
        return 2.0

    @staticmethod
    def soft_extremum_min_max(
        pred_extrema: pd.Series, alpha: float
    ) -> tuple[float, float]:
        if alpha < 0:
            raise ValueError("alpha must be non-negative")
        pred_minima, pred_maxima = QuickAdapterRegressorV3.get_pred_min_max(
            pred_extrema
        )
        soft_minimum = soft_extremum(pred_minima, alpha=-alpha)
        if not np.isfinite(soft_minimum):
            soft_minimum = QuickAdapterRegressorV3.safe_min_pred(pred_extrema)
        soft_maximum = soft_extremum(pred_maxima, alpha=alpha)
        if not np.isfinite(soft_maximum):
            soft_maximum = QuickAdapterRegressorV3.safe_max_pred(pred_extrema)
        return soft_minimum, soft_maximum

    @staticmethod
    def skimage_min_max(pred_extrema: pd.Series, method: str) -> tuple[float, float]:
        pred_minima, pred_maxima = QuickAdapterRegressorV3.get_pred_min_max(
            pred_extrema
        )

        method_functions = {
            "isodata": QuickAdapterRegressorV3.apply_skimage_threshold,
            "li": QuickAdapterRegressorV3.apply_skimage_threshold,
            "mean": QuickAdapterRegressorV3.apply_skimage_threshold,
            "minimum": QuickAdapterRegressorV3.apply_skimage_threshold,
            "otsu": QuickAdapterRegressorV3.apply_skimage_threshold,
            "triangle": QuickAdapterRegressorV3.apply_skimage_threshold,
            "yen": QuickAdapterRegressorV3.apply_skimage_threshold,
        }

        if method not in method_functions:
            raise ValueError(f"Unsupported method: {method}")

        min_func = method_functions[method]
        max_func = method_functions[method]

        try:
            threshold_func = getattr(skimage.filters, f"threshold_{method}")
        except AttributeError:
            raise ValueError(f"Unknown skimage threshold function: threshold_{method}")

        min_val = min_func(pred_minima, threshold_func)
        if not np.isfinite(min_val):
            min_val = QuickAdapterRegressorV3.safe_min_pred(pred_extrema)
        max_val = max_func(pred_maxima, threshold_func)
        if not np.isfinite(max_val):
            max_val = QuickAdapterRegressorV3.safe_max_pred(pred_extrema)

        return min_val, max_val

    @staticmethod
    def apply_skimage_threshold(
        series: pd.Series, threshold_func: Callable[[NDArray[np.float64]], float]
    ) -> float:
        values = series.to_numpy()

        if values.size == 0:
            return np.nan
        if (
            values.size == 1
            or np.unique(values).size < 3
            or np.allclose(values, values[0])
        ):
            return np.median(values)
        try:
            return threshold_func(values)
        except Exception as e:
            logger.warning(
                f"Failed to apply skimage threshold function {threshold_func.__name__} on series {series.name}: {repr(e)}. Falling back to median",
                exc_info=True,
            )
            return np.median(values)

    def get_multi_objective_study_best_trial(
        self, namespace: str, study: optuna.study.Study
    ) -> Optional[optuna.trial.FrozenTrial]:
        if namespace != "label":
            raise ValueError(f"Invalid namespace: {namespace}")
        n_objectives = len(study.directions)
        if n_objectives < 2:
            raise ValueError(
                f"Multi-objective study must have at least 2 objectives, but got {n_objectives}"
            )
        if not QuickAdapterRegressorV3.optuna_study_has_best_trials(study):
            return None

        metrics = {
            "braycurtis",
            "canberra",
            "chebyshev",
            "cityblock",
            "correlation",
            "cosine",
            # "dice",
            "euclidean",
            # "hamming",
            # "jaccard",
            "jensenshannon",
            # "kulczynski1",
            "mahalanobis",
            # "matching",
            "minkowski",
            # "rogerstanimoto",
            # "russellrao",
            "seuclidean",
            # "sokalmichener",
            # "sokalsneath",
            "sqeuclidean",
            # "yule",
            "hellinger",
            "shellinger",
            "geometric_mean",
            "harmonic_mean",
            "power_mean",
            "weighted_sum",
            "kmeans",
            "kmeans2",
            "knn_d1",
            "knn_d2_mean",
            "knn_d2_median",
            "knn_d2_max",
        }
        label_metric = self.ft_params.get("label_metric", "seuclidean")
        if label_metric not in metrics:
            raise ValueError(
                f"Unsupported label metric: {label_metric}. Supported metrics are {', '.join(metrics)}"
            )

        best_trials = [
            trial
            for trial in study.best_trials
            if (
                isinstance(trial.values, list)
                and len(trial.values) == n_objectives
                and all(
                    isinstance(value, (int, float)) and not np.isnan(value)
                    for value in trial.values
                )
            )
        ]
        if not best_trials:
            return None

        def calculate_distances(
            normalized_matrix: NDArray[np.float64], metric: str
        ) -> NDArray[np.float64]:
            n_objectives = normalized_matrix.shape[1]
            n_samples = normalized_matrix.shape[0]
            label_p_order = float(self.ft_params.get("label_p_order", 2.0))
            np_weights = np.array(
                self.ft_params.get("label_weights", [1.0] * n_objectives)
            )
            if np_weights.size != n_objectives:
                raise ValueError("label_weights length must match number of objectives")
            if np.any(np_weights < 0):
                raise ValueError("label_weights values must be non-negative")
            label_weights_sum = np.sum(np_weights)
            if np.isclose(label_weights_sum, 0.0):
                raise ValueError("label_weights sum cannot be zero")
            np_weights = np_weights / label_weights_sum
            knn_kwargs = {}
            label_knn_metric = self.ft_params.get("label_knn_metric", "euclidean")
            if label_knn_metric == "minkowski" and isinstance(label_p_order, float):
                knn_kwargs["p"] = label_p_order

            ideal_point = np.ones(n_objectives)
            ideal_point_2d = ideal_point.reshape(1, -1)

            if metric in {
                "braycurtis",
                "canberra",
                "chebyshev",
                "cityblock",
                "correlation",
                "cosine",
                # "dice",
                "euclidean",
                # "hamming",
                # "jaccard",
                "jensenshannon",
                # "kulczynski1",  # deprecated since version 1.15.0
                "mahalanobis",
                # "matching",
                "minkowski",
                # "rogerstanimoto",
                # "russellrao",
                "seuclidean",
                # "sokalmichener",  # deprecated since version 1.15.0
                # "sokalsneath",
                "sqeuclidean",
                # "yule",
            }:
                cdist_kwargs = {"w": np_weights}
                if metric in {
                    "jensenshannon",
                    "mahalanobis",
                    "seuclidean",
                }:
                    del cdist_kwargs["w"]
                if metric == "minkowski" and isinstance(label_p_order, float):
                    cdist_kwargs["p"] = label_p_order
                return sp.spatial.distance.cdist(
                    normalized_matrix,
                    ideal_point_2d,
                    metric=metric,
                    **cdist_kwargs,
                ).flatten()
            elif metric in {"hellinger", "shellinger"}:
                np_sqrt_normalized_matrix = np.sqrt(normalized_matrix)
                if metric == "shellinger":
                    np_weights = 1 / np.var(np_sqrt_normalized_matrix, axis=0, ddof=1)
                return np.sqrt(
                    np.sum(
                        np_weights
                        * (np_sqrt_normalized_matrix - np.sqrt(ideal_point)) ** 2,
                        axis=1,
                    )
                ) / np.sqrt(2.0)
            elif metric in {"geometric_mean", "harmonic_mean", "power_mean"}:
                p = {
                    "geometric_mean": 0.0,
                    "harmonic_mean": -1.0,
                    "power_mean": label_p_order,
                }[metric]
                return sp.stats.pmean(
                    ideal_point, p=p, weights=np_weights
                ) - sp.stats.pmean(normalized_matrix, p=p, weights=np_weights, axis=1)
            elif metric == "weighted_sum":
                return np.sum(np_weights * (ideal_point - normalized_matrix), axis=1)
            elif metric in {"kmeans", "kmeans2"}:
                if n_samples < 2:
                    return np.full(n_samples, np.inf)
                n_clusters = min(max(2, int(np.sqrt(n_samples / 2))), 10, n_samples)
                if metric == "kmeans":
                    kmeans = sklearn.cluster.KMeans(
                        n_clusters=n_clusters, random_state=42, n_init=10
                    )
                    cluster_labels = kmeans.fit_predict(normalized_matrix)
                    cluster_centers = kmeans.cluster_centers_
                elif metric == "kmeans2":
                    cluster_centers, cluster_labels = sp.cluster.vq.kmeans2(
                        normalized_matrix, n_clusters, rng=42, minit="++"
                    )
                label_kmeans_metric = self.ft_params.get(
                    "label_kmeans_metric", "seuclidean"
                )
                cdist_kwargs = {}
                if label_kmeans_metric == "minkowski" and isinstance(
                    label_p_order, float
                ):
                    cdist_kwargs["p"] = label_p_order
                cluster_distances_to_ideal = sp.spatial.distance.cdist(
                    cluster_centers,
                    ideal_point_2d,
                    metric=label_kmeans_metric,
                    **cdist_kwargs,
                ).flatten()
                return cluster_distances_to_ideal[cluster_labels]
            elif metric == "knn_d1":
                if n_samples < 2:
                    return np.full(n_samples, np.inf)
                nbrs = sklearn.neighbors.NearestNeighbors(
                    n_neighbors=2, metric=label_knn_metric, **knn_kwargs
                ).fit(normalized_matrix)
                distances, _ = nbrs.kneighbors(normalized_matrix)
                return distances[:, 1]
            elif metric in {"knn_d2_mean", "knn_d2_median", "knn_d2_max"}:
                if n_samples < 2:
                    return np.full(n_samples, np.inf)
                n_neighbors = (
                    min(
                        int(self.ft_params.get("label_knn_d2_n_neighbors", 4)),
                        n_samples - 1,
                    )
                    + 1
                )
                nbrs = sklearn.neighbors.NearestNeighbors(
                    n_neighbors=n_neighbors, metric=label_knn_metric, **knn_kwargs
                ).fit(normalized_matrix)
                distances, _ = nbrs.kneighbors(normalized_matrix)
                if metric == "knn_d2_mean":
                    return np.mean(distances[:, 1:], axis=1)
                elif metric == "knn_d2_median":
                    return np.median(distances[:, 1:], axis=1)
                elif metric == "knn_d2_max":
                    return np.max(distances[:, 1:], axis=1)
            else:
                raise ValueError(
                    f"Unsupported label metric: {metric}. Supported metrics are {', '.join(metrics)}"
                )

        objective_values_matrix = np.array([trial.values for trial in best_trials])
        normalized_matrix = np.zeros_like(objective_values_matrix, dtype=float)

        for i in range(objective_values_matrix.shape[1]):
            current_column = objective_values_matrix[:, i]
            current_direction = study.directions[i]

            is_neg_inf_mask = np.isneginf(current_column)
            is_pos_inf_mask = np.isposinf(current_column)
            if current_direction == optuna.study.StudyDirection.MAXIMIZE:
                normalized_matrix[is_neg_inf_mask, i] = 0.0
                normalized_matrix[is_pos_inf_mask, i] = 1.0
            else:
                normalized_matrix[is_neg_inf_mask, i] = 1.0
                normalized_matrix[is_pos_inf_mask, i] = 0.0

            is_finite_mask = np.isfinite(current_column)

            if np.any(is_finite_mask):
                finite_col = current_column[is_finite_mask]
                finite_min_val = np.min(finite_col)
                finite_max_val = np.max(finite_col)
                finite_range_val = finite_max_val - finite_min_val

                if np.isclose(finite_range_val, 0.0):
                    if np.any(is_pos_inf_mask) and np.any(is_neg_inf_mask):
                        normalized_matrix[is_finite_mask, i] = 0.5
                    elif np.any(is_pos_inf_mask):
                        normalized_matrix[is_finite_mask, i] = (
                            0.0
                            if current_direction == optuna.study.StudyDirection.MAXIMIZE
                            else 1.0
                        )
                    elif np.any(is_neg_inf_mask):
                        normalized_matrix[is_finite_mask, i] = (
                            1.0
                            if current_direction == optuna.study.StudyDirection.MAXIMIZE
                            else 0.0
                        )
                    else:
                        normalized_matrix[is_finite_mask, i] = 0.5
                else:
                    if current_direction == optuna.study.StudyDirection.MAXIMIZE:
                        normalized_matrix[is_finite_mask, i] = (
                            finite_col - finite_min_val
                        ) / finite_range_val
                    else:
                        normalized_matrix[is_finite_mask, i] = (
                            finite_max_val - finite_col
                        ) / finite_range_val

        trial_distances = calculate_distances(normalized_matrix, metric=label_metric)

        return best_trials[np.argmin(trial_distances)]

    def optuna_optimize(
        self,
        pair: str,
        namespace: str,
        objective: Callable[[optuna.trial.Trial], float],
        direction: Optional[optuna.study.StudyDirection] = None,
        directions: Optional[list[optuna.study.StudyDirection]] = None,
    ) -> Optional[optuna.study.Study]:
        is_study_single_objective = direction is not None and directions is None
        if (
            not is_study_single_objective
            and isinstance(directions, list)
            and len(directions) < 2
        ):
            raise ValueError(
                "Multi-objective study must have at least 2 directions specified"
            )

        study = self.optuna_create_study(
            pair=pair,
            namespace=namespace,
            direction=direction,
            directions=directions,
        )
        if not study:
            return

        if self._optuna_config.get("warm_start"):
            self.optuna_enqueue_previous_best_params(pair, namespace, study)

        if is_study_single_objective is True:
            objective_type = "single"
        else:
            objective_type = "multi"
        logger.info(
            f"Optuna {pair} {namespace} {objective_type} objective hyperopt started"
        )
        start_time = time.time()
        try:
            study.optimize(
                objective,
                n_trials=self._optuna_config.get("n_trials"),
                n_jobs=self._optuna_config.get("n_jobs"),
                timeout=self._optuna_config.get("timeout"),
                gc_after_trial=True,
            )
        except Exception as e:
            time_spent = time.time() - start_time
            logger.error(
                f"Optuna {pair} {namespace} {objective_type} objective hyperopt failed ({time_spent:.2f} secs): {repr(e)}",
                exc_info=True,
            )
            return

        time_spent = time.time() - start_time
        if is_study_single_objective:
            if not QuickAdapterRegressorV3.optuna_study_has_best_trial(study):
                logger.error(
                    f"Optuna {pair} {namespace} {objective_type} objective hyperopt failed ({time_spent:.2f} secs): no study best trial found"
                )
                return
            self.set_optuna_value(pair, namespace, study.best_value)
            self.set_optuna_params(pair, namespace, study.best_params)
            study_best_results = {
                "value": self.get_optuna_value(pair, namespace),
                **self.get_optuna_params(pair, namespace),
            }
            metric_log_msg = ""
        else:
            best_trial = self.get_multi_objective_study_best_trial("label", study)
            if not best_trial:
                logger.error(
                    f"Optuna {pair} {namespace} {objective_type} objective hyperopt failed ({time_spent:.2f} secs): no study best trial found"
                )
                return
            self.set_optuna_values(pair, namespace, best_trial.values)
            self.set_optuna_params(pair, namespace, best_trial.params)
            study_best_results = {
                "values": self.get_optuna_values(pair, namespace),
                **self.get_optuna_params(pair, namespace),
            }
            metric_log_msg = (
                f" using {self.ft_params.get('label_metric', 'seuclidean')} metric"
            )
        logger.info(
            f"Optuna {pair} {namespace} {objective_type} objective hyperopt done{metric_log_msg} ({time_spent:.2f} secs)"
        )
        for key, value in study_best_results.items():
            if isinstance(value, list):
                formatted_value = (
                    f"[{', '.join([format_number(item) for item in value])}]"
                )
            elif isinstance(value, (int, float)):
                formatted_value = format_number(value)
            else:
                formatted_value = repr(value)
            logger.info(
                f"Optuna {pair} {namespace} {objective_type} objective hyperopt | {key:>20s} : {formatted_value}"
            )
        if not self.optuna_params_valid(pair, namespace, study):
            logger.warning(
                f"Optuna {pair} {namespace} {objective_type} objective hyperopt best params found has invalid optimization target value(s)"
            )
        self.optuna_save_best_params(pair, namespace)
        return study

    def optuna_storage(self, pair: str) -> optuna.storages.BaseStorage:
        storage_dir = self.full_path
        storage_filename = f"optuna-{pair.split('/')[0]}"
        storage_backend = self._optuna_config.get("storage")
        if storage_backend == "sqlite":
            storage = optuna.storages.RDBStorage(
                url=f"sqlite:///{storage_dir}/{storage_filename}.sqlite",
                heartbeat_interval=60,
                failed_trial_callback=optuna.storages.RetryFailedTrialCallback(
                    max_retry=3
                ),
            )
        elif storage_backend == "file":
            storage = optuna.storages.JournalStorage(
                optuna.storages.journal.JournalFileBackend(
                    f"{storage_dir}/{storage_filename}.log"
                )
            )
        else:
            raise ValueError(
                f"Unsupported optuna storage backend: {storage_backend}. Supported backends are 'sqlite' and 'file'"
            )
        return storage

    def optuna_create_study(
        self,
        pair: str,
        namespace: str,
        direction: Optional[optuna.study.StudyDirection] = None,
        directions: Optional[list[optuna.study.StudyDirection]] = None,
    ) -> Optional[optuna.study.Study]:
        identifier = self.freqai_info.get("identifier")
        study_name = f"{identifier}-{pair}-{namespace}"
        try:
            storage = self.optuna_storage(pair)
        except Exception as e:
            logger.error(
                f"Failed to create optuna storage for study {study_name}: {repr(e)}",
                exc_info=True,
            )
            return None

        continuous = self._optuna_config.get("continuous")
        if continuous:
            QuickAdapterRegressorV3.optuna_study_delete(study_name, storage)

        try:
            return optuna.create_study(
                study_name=study_name,
                sampler=optuna.samplers.TPESampler(
                    n_startup_trials=self._optuna_config.get("n_startup_trials"),
                    multivariate=True,
                    group=True,
                    seed=self._optuna_config.get("seed"),
                ),
                pruner=optuna.pruners.HyperbandPruner(min_resource=3),
                direction=direction,
                directions=directions,
                storage=storage,
                load_if_exists=not continuous,
            )
        except Exception as e:
            logger.error(
                f"Failed to create optuna study {study_name}: {repr(e)}", exc_info=True
            )
            return None

    def optuna_params_valid(
        self, pair: str, namespace: str, study: Optional[optuna.study.Study]
    ) -> bool:
        if not study:
            return False
        n_objectives = len(study.directions)
        if n_objectives > 1:
            best_values = self.get_optuna_values(pair, namespace)
            return (
                isinstance(best_values, list)
                and len(best_values) == n_objectives
                and all(
                    isinstance(value, (int, float)) and np.isfinite(value)
                    for value in best_values
                )
            )
        else:
            best_value = self.get_optuna_value(pair, namespace)
            return isinstance(best_value, (int, float)) and np.isfinite(best_value)

    def optuna_enqueue_previous_best_params(
        self, pair: str, namespace: str, study: Optional[optuna.study.Study]
    ) -> None:
        best_params = self.get_optuna_params(pair, namespace)
        if best_params and self.optuna_params_valid(pair, namespace, study):
            study.enqueue_trial(best_params)

    def optuna_save_best_params(self, pair: str, namespace: str) -> None:
        best_params_path = Path(
            self.full_path / f"optuna-{namespace}-best-params-{pair.split('/')[0]}.json"
        )
        try:
            with best_params_path.open("w", encoding="utf-8") as write_file:
                json.dump(self.get_optuna_params(pair, namespace), write_file, indent=4)
        except Exception as e:
            logger.error(
                f"Failed to save optuna {namespace} best params for {pair}: {repr(e)}",
                exc_info=True,
            )
            raise

    def optuna_load_best_params(
        self, pair: str, namespace: str
    ) -> Optional[dict[str, Any]]:
        best_params_path = Path(
            self.full_path / f"optuna-{namespace}-best-params-{pair.split('/')[0]}.json"
        )
        if best_params_path.is_file():
            with best_params_path.open("r", encoding="utf-8") as read_file:
                return json.load(read_file)
        return None

    @staticmethod
    def optuna_study_delete(
        study_name: str, storage: optuna.storages.BaseStorage
    ) -> None:
        try:
            optuna.delete_study(study_name=study_name, storage=storage)
        except Exception:
            pass

    @staticmethod
    def optuna_study_load(
        study_name: str, storage: optuna.storages.BaseStorage
    ) -> Optional[optuna.study.Study]:
        try:
            study = optuna.load_study(study_name=study_name, storage=storage)
        except Exception:
            study = None
        return study

    @staticmethod
    def optuna_study_has_best_trial(study: Optional[optuna.study.Study]) -> bool:
        if not study:
            return False
        try:
            _ = study.best_trial
            return True
        except (ValueError, KeyError):
            return False

    @staticmethod
    def optuna_study_has_best_trials(study: Optional[optuna.study.Study]) -> bool:
        if not study:
            return False
        try:
            _ = study.best_trials
            return True
        except (ValueError, KeyError):
            return False


def train_objective(
    trial: optuna.trial.Trial,
    regressor: str,
    X: pd.DataFrame,
    y: pd.DataFrame,
    train_weights: NDArray[np.float64],
    X_test: pd.DataFrame,
    y_test: pd.DataFrame,
    test_weights: NDArray[np.float64],
    test_size: float,
    fit_live_predictions_candles: int,
    candles_step: int,
    model_training_parameters: dict[str, Any],
) -> float:
    test_ok = True
    test_length = len(X_test)
    if debug:
        test_extrema = y_test.get(EXTREMA_COLUMN)
        n_test_extrema: int = calculate_n_extrema(test_extrema)
        min_test_extrema: int = calculate_min_extrema(
            test_length, fit_live_predictions_candles
        )
        logger.info(f"{test_length=}, {n_test_extrema=}, {min_test_extrema=}")
    min_test_period_candles: int = fit_live_predictions_candles * 2
    if test_length < min_test_period_candles:
        logger.warning(
            f"Insufficient test data: {test_length} < {min_test_period_candles}"
        )
        test_ok = False
    max_test_period_candles: int = test_length
    test_period_candles: int = trial.suggest_int(
        "test_period_candles",
        min_test_period_candles,
        max_test_period_candles,
        step=candles_step,
    )
    X_test = X_test.iloc[-test_period_candles:]
    y_test = y_test.iloc[-test_period_candles:]
    test_extrema = y_test.get(EXTREMA_COLUMN)
    n_test_extrema: int = calculate_n_extrema(test_extrema)
    min_test_extrema: int = calculate_min_extrema(
        test_period_candles, fit_live_predictions_candles
    )
    if n_test_extrema < min_test_extrema:
        if debug:
            logger.warning(
                f"Insufficient extrema in test data with {test_period_candles=}: {n_test_extrema=} < {min_test_extrema=}"
            )
        test_ok = False
    test_weights = test_weights[-test_period_candles:]

    train_ok = True
    train_length = len(X)
    if debug:
        train_extrema = y.get(EXTREMA_COLUMN)
        n_train_extrema: int = calculate_n_extrema(train_extrema)
        min_train_extrema: int = calculate_min_extrema(
            train_length, fit_live_predictions_candles
        )
        logger.info(f"{train_length=}, {n_train_extrema=}, {min_train_extrema=}")
    min_train_period_candles: int = min_test_period_candles * int(
        round(1 / test_size - 1)
    )
    if train_length < min_train_period_candles:
        logger.warning(
            f"Insufficient train data: {train_length} < {min_train_period_candles}"
        )
        train_ok = False
    max_train_period_candles: int = train_length
    train_period_candles: int = trial.suggest_int(
        "train_period_candles",
        min_train_period_candles,
        max_train_period_candles,
        step=candles_step,
    )
    X = X.iloc[-train_period_candles:]
    y = y.iloc[-train_period_candles:]
    train_extrema = y.get(EXTREMA_COLUMN)
    n_train_extrema: int = calculate_n_extrema(train_extrema)
    min_train_extrema: int = calculate_min_extrema(
        train_period_candles, fit_live_predictions_candles
    )
    if n_train_extrema < min_train_extrema:
        if debug:
            logger.warning(
                f"Insufficient extrema in train data with {train_period_candles=}: {n_train_extrema=} < {min_train_extrema=}"
            )
        train_ok = False
    train_weights = train_weights[-train_period_candles:]

    if not test_ok or not train_ok:
        return np.inf

    model = fit_regressor(
        regressor=regressor,
        X=X,
        y=y,
        train_weights=train_weights,
        eval_set=[(X_test, y_test)],
        eval_weights=[test_weights],
        model_training_parameters=model_training_parameters,
        callbacks=get_optuna_callbacks(trial, regressor),
    )
    y_pred = model.predict(X_test)

    return sklearn.metrics.root_mean_squared_error(
        y_test, y_pred, sample_weight=test_weights
    )


def hp_objective(
    trial: optuna.trial.Trial,
    regressor: str,
    X: pd.DataFrame,
    y: pd.DataFrame,
    train_weights: NDArray[np.float64],
    X_test: pd.DataFrame,
    y_test: pd.DataFrame,
    test_weights: NDArray[np.float64],
    model_training_best_parameters: dict[str, Any],
    model_training_parameters: dict[str, Any],
    expansion_ratio: float,
) -> float:
    study_model_parameters = get_optuna_study_model_parameters(
        trial, regressor, model_training_best_parameters, expansion_ratio
    )
    model_training_parameters = {**model_training_parameters, **study_model_parameters}

    model = fit_regressor(
        regressor=regressor,
        X=X,
        y=y,
        train_weights=train_weights,
        eval_set=[(X_test, y_test)],
        eval_weights=[test_weights],
        model_training_parameters=model_training_parameters,
        callbacks=get_optuna_callbacks(trial, regressor),
    )
    y_pred = model.predict(X_test)

    return sklearn.metrics.root_mean_squared_error(
        y_test, y_pred, sample_weight=test_weights
    )


def label_objective(
    trial: optuna.trial.Trial,
    df: pd.DataFrame,
    fit_live_predictions_candles: int,
    candles_step: int,
) -> tuple[float, int]:
    min_label_period_candles, max_label_period_candles, candles_step = (
        get_min_max_label_period_candles(fit_live_predictions_candles, candles_step)
    )

    label_period_candles = trial.suggest_int(
        "label_period_candles",
        min_label_period_candles,
        max_label_period_candles,
        step=candles_step,
    )
    label_natr_ratio = trial.suggest_float("label_natr_ratio", 2.0, 48.0, step=0.01)

    label_period_cycles = fit_live_predictions_candles / label_period_candles
    df = df.iloc[-(max(2, int(label_period_cycles)) * label_period_candles) :]

    if df.empty:
        return -np.inf, -np.inf

    _, pivots_values, _, pivots_thresholds = zigzag(
        df,
        natr_period=label_period_candles,
        natr_ratio=label_natr_ratio,
    )

    return np.median(pivots_thresholds), len(pivots_values)
