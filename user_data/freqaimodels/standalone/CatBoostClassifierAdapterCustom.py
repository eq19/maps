import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, Tuple
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame
import scipy as spy
import random

np.random.seed(42)
random.seed(42)

from sklearn.metrics import roc_auc_score, f1_score, accuracy_score

from catboost import CatBoostClassifier, Pool

sys.path.append('/com.docker.devenvironments.code/user_data')
sys.path.append('/home/freqtrade/user_data')
sys.path.append('/Users/nikitatolstakov/Desktop/Python/freqtrade/user_data')

from lib import helpers

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

from datetime import datetime

import pickle


logger = logging.getLogger(__name__)

class CatBoostClassifierAdapterCustom(BaseClassifierModel):
    """
    User created prediction model. The class needs to override three necessary
    functions, predict(), train(), fit(). The class inherits ModelHandler which
    has its own DataHandler where data is held, saved, loaded, and managed.
    """

    TARGET_VAR = "ohlc4_log"

    @property
    def PREDICT_TARGET(self):
        return self.config["sagemaster"].get("PREDICT_TARGET", 6)

    def roc_auc_file_create(self, dk: FreqaiDataKitchen, pair:str, file_type:str, **kwargs):
        ind_name = dk.freqai_config.get('identifier', "")
        pair = pair.replace("/", "_").replace(":", "")
        roc_auc_file = Path(f"user_data/results/roc_auc_{ind_name}_{pair}_{file_type}.csv")
        if not roc_auc_file.exists():
            roc_auc_file.touch(exist_ok=True)
            roc_auc_file.write_text("date;pair;roc_auc_long;roc_auc_short;rolling_roc_auc_long;rolling_roc_auc_short;real_trend_long;real_trend_short\n")

        return roc_auc_file

    def write_roc_auc(self, file: Path, date, pair:str, roc_auc_long:float, roc_auc_short:float,rolling_roc_auc_val_long:float, rolling_roc_auc_val_short:float, real_trend_long:float, real_trend_short:float):
        with file.open("a") as f:
            f.write(f"{date};{pair};{roc_auc_long};{roc_auc_short};{rolling_roc_auc_val_long};{rolling_roc_auc_val_short};{real_trend_long};{real_trend_short}\n")
        return True


    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        logger.info(f"ENTER .fit() {data_dictionary['train_features'].shape} {data_dictionary['train_labels'].shape}")
        start_time = time.time()
        models_dict = {}
        dk.feature_select(data_dictionary)

        logger.info("start training")
        roc_auc_l = []
        for lable_col in data_dictionary["train_labels"].columns:
            logger.info(f"start training for label: {lable_col}")

            # roc_auc_file = self.roc_auc_file_create(dk, dk.pair, 'train')

            x_train = data_dictionary["train_features"].loc[:, dk.data[lable_col + "_selected_features"]].copy()
            logger.info(f"x_train shape: {x_train.shape}")
            train_data = Pool(
                data=x_train,
                label=data_dictionary["train_labels"][lable_col],
            )


            if self.freqai_info.get('data_split_parameters', {}).get('test_size', 0.1) == 0:
                test_data = None
            else:
                x_test = data_dictionary["test_features"].loc[:, dk.data[lable_col + "_selected_features"]].copy()
                test_data = Pool(
                    data=x_test,
                    label=data_dictionary["test_labels"][lable_col],
                    #weight=data_dictionary["test_weights"],
                )


            init_model = self.get_init_model(dk.pair)

            model = CatBoostClassifier(
                allow_writing_files=False,
                **self.model_training_parameters,
                random_seed=42
            )

            start = time.time()
            model.fit(X=train_data, eval_set=test_data, init_model=init_model)
            time_spent = (time.time() - start)
            self.dd.update_metric_tracker('fit_time', time_spent, dk.pair)

            roc_auc_v = roc_auc_score(data_dictionary["train_labels"][lable_col], model.predict_proba(x_train)[:, 1])

            # dk.data['extra_returns_per_train'][lable_col + '_roc_auc'] =roc_auc_v
            # roc_auc_l.append(roc_auc_v)

            logger.info(f"Train Roc Auc Score: {roc_auc_v}")

            models_dict[lable_col + '_model'] = model

        # with roc_auc_file.open("a") as f:
        #     f.write(f"{datetime.now()};{dk.pair};{roc_auc_l[0]};{roc_auc_l[1]}\n")

        dk.data["fit_moment"] = int(time.time())

        logger.info(f"EXIT .fit(): fit_moment={dk.data['fit_moment']}, execution time: {time.time() - start_time:.2f} seconds")

        return models_dict


    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> Tuple[DataFrame, npt.NDArray[np.int_]]:

        logger.info(f"ENTER .predict() {unfiltered_df.shape}")
        start_time = time.time()

        dk.find_features(unfiltered_df)
        filtered_df, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, training_filter=False
        )
        filtered_df = dk.normalize_data_from_metadata(filtered_df)
        dk.data_dictionary["prediction_features"] = filtered_df

        self.data_cleaning_predict(dk)

        pred_df = pd.DataFrame()
        for label_col in dk.label_list:
            x_test = dk.data_dictionary["prediction_features"].loc[:, dk.data[label_col + "_selected_features"]].copy()
            self.fit_moment = dk.data[label_col + "_fit_moment"]
            logger.info(f"predict for model: {label_col}")
            predictions = self.model[label_col + '_model'].predict(x_test)
            pred_df_sample = DataFrame(predictions, columns=[label_col])

            predictions_prob = self.model[label_col + '_model'].predict_proba(x_test)
            pred_df_sample_prob = DataFrame(predictions_prob, columns=self.model[label_col + '_model'].classes_)

            pred_df = pd.concat([pred_df, pred_df_sample, pred_df_sample_prob], axis=1)

        # self.get_roc_auc_pred(unfiltered_df, dk, pred_df)

        logger.info(f"EXIT .predict() {pred_df.shape}, execution time: {time.time() - start_time:.2f} seconds")

        return (pred_df, dk.do_predict)


    def get_roc_auc_pred(self, unfiltered_df: Dict, dk: FreqaiDataKitchen, preds, **kwargs) -> None:
        # file_type = 'live' if dk.live else 'backtest'

        print(f"get_roc_auc_pred: fit_moment={self.fit_moment}")
        for pair in self.dd.historic_data.keys():
            if (pair not in self.dd.historic_predictions) or (len(self.dd.historic_predictions[pair]) == 0):
                continue

            # roc_auc_file = self.roc_auc_file_create(dk, pair, file_type)

            df_pred = self.dd.historic_predictions[pair]
            df_all = self.dd.historic_data[pair]
            df_all = df_all[list(df_all.keys())[0]]

            # print(f"df_pred: \n{df_pred}")
            # print(f"df_all: \n{df_all}")

            last_trend_long = df_pred['trend_long'].iloc[-1].squeeze()
            last_trend_short = df_pred['trend_short'].iloc[-1].squeeze()
            last_date = df_all['date'].iloc[-1]

            # minus candle size (5m on dev test)
            adjusted_fit_moment = self.fit_moment - 5 * 60

            # add ohlc4
            df_all['ohlc4'] = (df_all['open'] + df_all['high'] + df_all['low'] + df_all['close']) / 4
            df_all['ohlc4_log'] = np.log(df_all['ohlc4'])
            df_all = df_all[['ohlc4_log', 'date']]

            ### create df for target
            df_all['timestamp'] = pd.to_datetime(df_all['date'], utc=True).view(int) // 10 ** 9

            # print(f"df_all timestamp: {df_all['timestamp']}")

            # filter dataframe and take only data after fit moment
            df_all = df_all[df_all['timestamp'] >= adjusted_fit_moment].copy()
            df_all = df_all.sort_values('date').set_index('date')

            # print(f"df_all:")
            # print(df_all)
            # create true values for data after fit moment
            target = helpers.create_target(df_all, self.PREDICT_TARGET, method='polyfit', polyfit_var = self.TARGET_VAR)

            # transform target to long/short
            target = target[['trend', 'start_windows']].set_index('start_windows')
            target['trend_long_true'] = np.where(target['trend'] == 1, 1, 0)
            target['trend_short_true'] = np.where(target['trend'] == -1, 1, 0)

            # filter dataframe and take only data after fit moment
            df_pred['timestamp_pred'] = df_pred['date_pred'].view(int) // 10 ** 9
            print(f"df_pred timestamp: \n{df_pred['timestamp_pred']}")
            df_pred = df_pred[df_pred['timestamp_pred'] >= adjusted_fit_moment].copy()
            # remove column timestamp_pred
            df_pred = df_pred.drop(['timestamp_pred'], axis=1)

            # print(f"df_pred matched:")
            # print(df_pred)

            # set index to date for merge
            df_pred = df_pred.set_index(df_pred['date_pred'])
            # merge with target
            df_pred = pd.concat([df_pred, target[['trend_long_true', 'trend_short_true']].copy()], axis=1)
            # reset index
            df_pred = df_pred.reset_index(drop=True)
            df_pred = df_pred.dropna()

            # print(f"df_pred merged:")
            # print(df_pred)

            roc_auc_val_long = 0
            roc_auc_val_short = 0
            rolling_roc_auc_val_long = 0
            rolling_roc_auc_val_short = 0

            if df_pred.shape[0] == 0:
                logger.info("No data to roc_auc score")
                # self.write_roc_auc(roc_auc_file, last_date, pair, roc_auc_val_long, roc_auc_val_short, rolling_roc_auc_val_long, rolling_roc_auc_val_short, last_trend_long, last_trend_short)
                continue


            if df_pred['trend_long_true'].nunique() == 1:
                logger.info("Can't calculate roc_auc score, only one class in trend_long")
            else:
                try:
                    roc_auc_val_long = roc_auc_score(df_pred['trend_long_true'], df_pred['trend_long'])
                    rolling_roc_auc_val_long = roc_auc_score(df_pred['trend_long_true'].tail(6), df_pred['trend_long'].tail(6))
                except:
                    pass
                logger.info(f"Live long_roc_auc score {pair}:  {str(roc_auc_val_long)}")

            if df_pred['trend_short_true'].nunique() == 1:
                logger.info("Can't calculate roc_auc score, only one class in trend_short")
            else:
                try:
                    roc_auc_val_short = roc_auc_score(df_pred['trend_short_true'], df_pred['trend_short'])
                    rolling_roc_auc_val_short = roc_auc_score(df_pred['trend_short_true'].tail(6), df_pred['trend_short'].tail(6))
                except:
                    pass

                logger.info(f"Live short_roc_auc score {pair}:  {str(roc_auc_val_short)}")

            # self.write_roc_auc(roc_auc_file, last_date, pair, roc_auc_val_long, roc_auc_val_short, rolling_roc_auc_val_long, rolling_roc_auc_val_short, last_trend_long, last_trend_short)

        # backtesting roc auc score
        if dk.live == False:
            first_date = unfiltered_df.loc[:, 'date'].iloc[0]
            df_pred = pd.DataFrame()
            df_pred['trend_long'] = preds['trend_long']
            df_pred['trend_short'] = preds['trend_short']

            df_pred['trend_long_true'] = unfiltered_df['&-trend_long'].values
            df_pred['trend_short_true'] = unfiltered_df['&-trend_short'].values

            df_pred['trend_long_true'] = df_pred['trend_long_true'].replace('trend_long', 1)
            df_pred['trend_long_true'] = df_pred['trend_long_true'].replace('trend_not_long', 0)

            df_pred['trend_short_true'] = df_pred['trend_long_true'].replace('trend_short', 1)
            df_pred['trend_short_true'] = df_pred['trend_long_true'].replace('trend_not_short', 0)

            df_pred = df_pred.dropna()

            roc_auc_val_long = 0
            roc_auc_val_short = 0

            if df_pred.shape[0] == 0:
                logger.info("No data to roc auc score")
                # self.write_roc_auc(roc_auc_file, first_date, pair, roc_auc_val_long, roc_auc_val_short, 0, 0, last_trend_long, last_trend_short)
                return

            # LONG roc_auc
            if df_pred['trend_long_true'].nunique() == 1:
                logger.info("Can't calculate roc auc score, only one class in trend_long")
                roc_auc_val_long = 0
            else:
                roc_auc_val_long = roc_auc_score(df_pred['trend_long_true'], df_pred['trend_long'])
                logger.info(f"Live Roc Auc Score Long, {self.temp_pair}: {str(roc_auc_val_long)}")


            # SHORT roc_auc
            if df_pred['trend_short_true'].nunique() == 1:
                logger.info("Can't calculate roc auc score, only one class in trend_short")
                roc_auc_val_short = 0
            else:
                roc_auc_val_short = roc_auc_score(df_pred['trend_short_true'], df_pred['trend_short'])
                logger.info(f"Live Roc Auc Score Short {self.temp_pair}:  {str(roc_auc_val_short)}")

            # self.write_roc_auc(roc_auc_file, first_date, pair, roc_auc_val_long, roc_auc_val_short, 0, 0, last_trend_long, last_trend_short)

        return



    def fit_live_di(self, dk: FreqaiDataKitchen, pair: str) -> None:
        '''
        Fit live Dissimiliy Index based on predictions
        '''
        warmed_up = True
        num_candles = self.freqai_info.get('fit_live_predictions_candles', 100)

        candle_diff = len(self.dd.historic_predictions[pair].index) - \
            (self.freqai_info.get('fit_live_predictions_candles', 600) + 1000)
        if candle_diff < 0:
            logger.warning(
                f'Fit live predictions not warmed up yet for DI. Still {abs(candle_diff)} candles to go')
            warmed_up = False

        pred_df_full = self.dd.historic_predictions[pair].tail(num_candles).reset_index(drop=True)

        # fit the DI_threshold
        if not warmed_up:
            f = [0, 0, 0]
            cutoff = 2
        else:
            f = spy.stats.weibull_min.fit(pred_df_full['DI_values'])
            cutoff = spy.stats.weibull_min.ppf(0.999, *f)

        dk.data["DI_value_mean"] = pred_df_full['DI_values'].mean()
        dk.data["DI_value_std"] = pred_df_full['DI_values'].std()
        dk.data['extra_returns_per_train']['DI_value_param1'] = f[0]
        dk.data['extra_returns_per_train']['DI_value_param2'] = f[1]
        dk.data['extra_returns_per_train']['DI_value_param3'] = f[2]
        dk.data['extra_returns_per_train']['DI_cutoff'] = cutoff

        logger.info(f"fit_live_di {pair}({num_candles}) candle_diff={candle_diff} F={f} cutoff={cutoff}")


    def get_features_df(self, pair:str, num_candles:int) -> pd.DataFrame:
        # pred_df_full = self.dd.historic_predictions[pair].tail(num_candles).reset_index(drop=True)
        df_all = self.dd.historic_data[pair]
        df_all = df_all[list(df_all.keys())[0]]
        df_all = df_all.tail(num_candles)#.reset_index(drop=True)
        df_all['ohlc4'] = (df_all['open'] + df_all['high'] + df_all['low'] + df_all['close']) / 4
        df_all['ohlc4_log'] = np.log(df_all['ohlc4'])

        return df_all

    def create_target(self, features_df: pd.DataFrame) -> pd.DataFrame:
        # create true values for data after fit moment
        target = helpers.create_target(features_df, self.PREDICT_TARGET, method='polyfit', polyfit_var = self.TARGET_VAR)

        # transform target to long/short
        target = target.set_index(target['start_windows'])
        target['trend_long_true'] = np.where(target['trend'] == 1, 1, 0)
        target['trend_short_true'] = np.where(target['trend'] == -1, 1, 0)
        return target

    def fit_live_roc_auc(self, dk: FreqaiDataKitchen, pair: str, num_candles = 24) -> None:
        '''
        Fit ROC AUC score based on predictions into the live trading
        ROC AUC will serve as indicator to reduce risk when the model is not performing well
        '''

        # get dataframe with live predictions
        # pred_df_full = self.dd.historic_predictions[pair][self.dd.historic_predictions[pair]['do_predict'] == 1].copy()
        pred_df_full = self.dd.historic_predictions[pair].copy()
        pred_df_full = pred_df_full.tail(num_candles).reset_index(drop=True)

        # get dataframe with candle data for actual trend
        features_df = self.get_features_df(pair, pred_df_full.shape[0] + self.PREDICT_TARGET - 1)

        # generate target
        target = self.create_target(features_df).tail(num_candles).reset_index(drop=True)

        # in case of warmup or some issues, set value to mean to avoid any turbulence
        roc_auc_val_long = pred_df_full[f'roc_auc_long_{num_candles}'].mean()
        roc_auc_val_short = pred_df_full[f'roc_auc_short_{num_candles}'].mean()

        # LONG roc_auc
        # if only 1 class in target, roc_auc_score will return error
        if target['trend_long_true'].nunique() > 1:
            roc_auc_val_long = roc_auc_score(target['trend_long_true'], pred_df_full['trend_long'])
            logger.info(f"Live Roc Auc Score Long, {pair}: {str(roc_auc_val_long)}")

        # SHORT roc_auc
        # if only 1 class in target, roc_auc_score will return error
        if target['trend_short_true'].nunique() > 1:
            roc_auc_val_short = roc_auc_score(target['trend_short_true'], pred_df_full['trend_short'])
            logger.info(f"Live Roc Auc Score Short {pair}:  {str(roc_auc_val_short)}")

        roc_auc_val_long_gini = 2 * roc_auc_val_long - 1
        roc_auc_val_short_gini = 2 * roc_auc_val_short - 1

        dk.data['extra_returns_per_train'][f'roc_auc_long_{num_candles}'] = roc_auc_val_long
        dk.data['extra_returns_per_train'][f'roc_auc_short_{num_candles}'] = roc_auc_val_short

        dk.data['extra_returns_per_train'][f'roc_auc_long_gini_{num_candles}'] = roc_auc_val_long_gini
        dk.data['extra_returns_per_train'][f'roc_auc_short_gini_{num_candles}'] = roc_auc_val_short_gini

        logger.info(f"fit_live_roc_auc {pair}({num_candles})  long: {roc_auc_val_long_gini} short: {roc_auc_val_short_gini}")

    def fit_live_f1(self, dk: FreqaiDataKitchen, pair: str, num_candles = 24) -> None:
        # fit F1

        # get dataframe with live predictions
        # pred_df_full = self.dd.historic_predictions[pair][self.dd.historic_predictions[pair]['do_predict'] == 1].copy()
        pred_df_full = self.dd.historic_predictions[pair].copy()
        pred_df_full = pred_df_full.tail(num_candles).reset_index(drop=True)

        # get dataframe with candle data for actual trend
        features_df = self.get_features_df(pair, pred_df_full.shape[0] + self.PREDICT_TARGET - 1)

        # generate target
        target = self.create_target(features_df).tail(num_candles).reset_index(drop=True)

        # create labels for predictions
        pred_df_full['trend_long_signal'] = np.where(pred_df_full['trend_long'] >= 0.5, 1, 0)
        pred_df_full['trend_short_signal'] = np.where(pred_df_full['trend_short'] >= 0.5, 1, 0)

        # calculate f1 score
        f1_long = f1_score(target['trend_long_true'], pred_df_full['trend_long_signal'])
        f1_short = f1_score(target['trend_short_true'], pred_df_full['trend_short_signal'])

        dk.data['extra_returns_per_train'][f'f1_long_{num_candles}'] = f1_long
        dk.data['extra_returns_per_train'][f'f1_short_{num_candles}'] = f1_short

        logger.info(f"fit_live_f1 {pair}({num_candles})  long: {f1_long} short: {f1_short}")


    def fit_live_accuracy(self, dk: FreqaiDataKitchen, pair: str, num_candles = 24) -> None:
        # get dataframe with live predictions
        # pred_df_full = self.dd.historic_predictions[pair][self.dd.historic_predictions[pair]['do_predict'] == 1].copy()
        pred_df_full = self.dd.historic_predictions[pair].copy()
        pred_df_full = pred_df_full.tail(num_candles).reset_index(drop=True)

        # get dataframe with candle data for actual trend
        features_df = self.get_features_df(pair, pred_df_full.shape[0] + self.PREDICT_TARGET - 1)

        # generate target
        target = self.create_target(features_df).tail(num_candles).reset_index(drop=True)

        # create labels for predictions
        pred_df_full['trend_long_signal'] = np.where(pred_df_full['trend_long'] >= 0.5, 1, 0)
        pred_df_full['trend_short_signal'] = np.where(pred_df_full['trend_short'] >= 0.5, 1, 0)

        # calculate f1 score
        accuracy_long = accuracy_score(target['trend_long_true'], pred_df_full['trend_long_signal'])
        accuracy_short = accuracy_score(target['trend_short_true'], pred_df_full['trend_short_signal'])

        dk.data['extra_returns_per_train'][f'accuracy_long_{num_candles}'] = accuracy_long
        dk.data['extra_returns_per_train'][f'accuracy_short_{num_candles}'] = accuracy_short

        logger.info(f"fit_live_accuracy {pair}({num_candles})  long: {accuracy_long} short: {accuracy_short}")

    def fit_live_predictions(self, dk: FreqaiDataKitchen, pair: str) -> None:
        logger.info(f"ENTER .fit_live_predictions()")
        start_time = time.time()

        # call base method
        super().fit_live_predictions(dk, pair)

        # fit Dissimilarity Index
        self.fit_live_di(dk, pair)

        # fit roc_auc
        self.fit_live_roc_auc(dk, pair, 6)
        self.fit_live_roc_auc(dk, pair, 12)
        self.fit_live_roc_auc(dk, pair, 24)

        # fit F1
        self.fit_live_f1(dk, pair, 12)
        self.fit_live_f1(dk, pair, 24)

        # fit accuracy
        self.fit_live_accuracy(dk, pair, 6)
        self.fit_live_accuracy(dk, pair, 12)
        self.fit_live_accuracy(dk, pair, 24)

        logger.info(f"EXIT .fit_live_predictions() execution time: {time.time() - start_time:.2f} seconds")


    def feature_select(self, data_dictionary):
        logger.info(f"ENTER .feature_select() {data_dictionary['train_features'].shape} {data_dictionary['train_labels'].shape}")
        start_time = time.time()

        logger.info("Selecting features...")
        logger.info(f"Available Labels: {data_dictionary['train_labels'].columns}")
        for lable_col in data_dictionary["train_labels"].columns:
            logger.info("Selecting for Label: " + lable_col)
            # prepare train data
            x_train = data_dictionary["train_features"].copy()
            y_train = data_dictionary["train_labels"][lable_col].copy()
            x_train = x_train.rename(columns=lambda x: x.replace('-', ':'))

            # prepare eval data
            test_data = None

            if self.freqai_config.get('data_split_parameters', {}).get('test_size', 0.05) > 0:
                # replace '-' with ':' in test labels
                x_eval = data_dictionary["test_features"].copy().rename(columns=lambda x: x.replace('-', ':'))
                y_eval = data_dictionary["test_labels"][lable_col].copy()

                test_data = Pool(
                    data=x_eval,
                    label=y_eval
                )

            # create model & select features
            model = CatBoostClassifier(iterations=self.SELECT_FEATURES_ITERATIONS,
                                       task_type="CPU", eval_metric='AUC',
                                         auto_class_weights='Balanced', objective="Logloss",
                                         colsample_bylevel= 0.096, depth= 4, boosting_type="Plain",
                                         bootstrap_type="MVS", l2_leaf_reg=5.0, learning_rate=0.09,
                                         save_snapshot=False, allow_writing_files=False, random_seed=42)

            # autodetelct number of features to select
            if self.AUTODETECT_NUM_FEATURES_TO_SELECT:
                logger.info("Start autodetect NUM_FEATURES_TO_SELECT for Label: " + lable_col)
                best_f = model.select_features(
                    x_train,
                    y_train,
                    eval_set=test_data,
                    features_for_select=x_train.columns,
                    num_features_to_select=512,
                    steps=self.SELECT_FEATURES_STEPS,
                    algorithm=EFeaturesSelectionAlgorithm.RecursiveByLossFunctionChange,
                    shap_calc_type=EShapCalcType.Regular,
                    train_final_model=False,
                    logging_level=self.config["freqai"]["model_training_parameters"].get("logging_level", "Silent"),
                    plot=False
                )

                try:
                    with open(f'user_data/artifacts/{str(self.freqai_config.get("identifier"))}_{self.pair.replace("/", "").replace(":", "")}_autodetect_features_{lable_col}_{datetime.now()}.json', 'w') as f:
                        json.dump(best_f, f)

                    loss_graph = pd.DataFrame({"loss_values": best_f['loss_graph']['loss_values'], "removed_features_count": best_f['loss_graph']['removed_features_count']})
                    optimal_features = x_train.shape[1] - loss_graph[loss_graph['loss_values'] == loss_graph['loss_values'].min()]['removed_features_count'].max()
                    logger.info(f'Found optimal number of features for label {lable_col} is: {optimal_features}')

                    if (optimal_features > x_train.shape[0]):
                        optimal_features = x_train.shape[0]
                        logger.info('too many features selected, model performance might be unpredictable, setting optimal features to number of rows of train dataframe: ' + str(optimal_features))
                except:
                    optimal_features = self.NUM_FEATURES_TO_SELECT
            else:
                optimal_features = self.NUM_FEATURES_TO_SELECT

            # make final selection
            best_f = model.select_features(
                x_train,
                y_train,
                eval_set=test_data,
                features_for_select=x_train.columns,
                num_features_to_select=optimal_features,
                steps=self.SELECT_FEATURES_STEPS,
                algorithm=EFeaturesSelectionAlgorithm.RecursiveByLossFunctionChange,
                shap_calc_type=EShapCalcType.Exact,
                train_final_model=False,
                logging_level=self.config["freqai"]["model_training_parameters"].get("logging_level", "Silent"),
                plot=False
            )

            try:
                loss_graph = pd.DataFrame({"loss_values": best_f['loss_graph']['loss_values'], "removed_features_count": best_f['loss_graph']['removed_features_count']})
                optimal_features = x_train.shape[1] - loss_graph[loss_graph['loss_values'] == loss_graph['loss_values'].min()]['removed_features_count'].max()
                logger.info(f'Now optimal number of features for label {lable_col} is: {optimal_features}')
            except:
                pass

            # save best_f to json file
            with open(f'user_data/artifacts/{str(self.freqai_config.get("identifier"))}_{self.pair.replace("/", "").replace(":", "")}_best_features_{lable_col}_{datetime.now()}.json', 'w') as f:
                json.dump(best_f, f)

            del x_train
            del y_train
            new_best_features = [x.replace(':', '-') for x in best_f['selected_features_names']]
            self.data[lable_col + "_selected_features"] = new_best_features
            self.data[lable_col + "_fit_moment"] = int(time.time())

            logger.info(f"EXIT .feature_select() {len(new_best_features)}, execution {time.time() - start_time} seconds")

        return