from datetime import datetime
import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict

from catboost import CatBoostClassifier, EFeaturesSelectionAlgorithm, EShapCalcType, Pool

from freqtrade.freqai.base_models.BaseClassifierModel import BaseClassifierModel
from freqtrade.freqai.base_models.FreqaiMultiOutputClassifier import FreqaiMultiOutputClassifier
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas import DataFrame
from typing import Any, Dict, Tuple
from datasieve.transforms import SKLearnWrapper
from datasieve.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler
import datasieve.transforms as ds
import wandb
from freqaimodels.MultiOutputClassifierWithFeatureSelect import MultiOutputClassifierWithFeatureSelect


logger = logging.getLogger(__name__)


class CatboostFeatureSelectMultiTargetBinaryClassifierV1(BaseClassifierModel):
    """
    User created prediction model. The class needs to override three necessary
    functions, predict(), train(), fit(). The class inherits ModelHandler which
    has its own DataHandler where data is held, saved, loaded, and managed.
    """

    @property
    def SELECT_FEATURES_ITERATIONS(self):
        return self.config["sagemaster"].get("CATBOOST_SELECT_FEATURES_ITERATIONS", 100)

    @property
    def NUM_FEATURES_TO_SELECT(self):
        return  self.config["sagemaster"].get("CATBOOST_NUM_FEATURES_TO_SELECT", 1024)

    @property
    def SELECT_FEATURES_STEPS(self):
        return self.config["sagemaster"].get("CATBOOST_SELECT_FEATURES_STEPS", 10)

    @property
    def AUTODETECT_NUM_FEATURES_TO_SELECT(self):
        return self.config["sagemaster"].get("CATBOOST_AUTODETECT_NUM_FEATURES_TO_SELECT", False)

    @property
    def FEATURE_SELECT_LABEL(self):
        return self.config["sagemaster"].get("CATBOOST_FEATURE_SELECT_LABEL", "&-trend_long")

    @property
    def MODEL_IDENTIFIER(self):
        return self.config["freqai"].get("identifier", "default")

    def wandb_init(self, project:str = "TM3", name: str = None, job_type: str = None, config: Dict = None):
        wandb.init(
            # set the wandb project where this run will be logged
            project=project,
            job_type=job_type,
            name=name + " " + datetime.now().strftime("%Y%m%d_%H%M%S"),

            # track hyperparameters and run metadata
            config=config
        )


    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :param data_dictionary: the dictionary constructed by DataHandler to hold
                                all the training and test data/labels.
        """
        # select features
        selected_features_all_labels = self.feature_select(data_dictionary)
        labels = list(selected_features_all_labels.keys())

        # selected_features = data_dictionary["train_features"].columns.tolist()
        dk.data['selected_features'] = selected_features_all_labels

        X = data_dictionary["train_features"].copy()
        y = data_dictionary["train_labels"]

        if self.freqai_info.get('data_split_parameters', {}).get('test_size', 0.1) != 0:
            eval_sets = [None] * data_dictionary['test_labels'].shape[1]

            for i, label in enumerate(data_dictionary['test_labels'].columns):
                eval_sets[i] = Pool(
                    data=data_dictionary["test_features"][selected_features_all_labels[label]].copy(),
                    label=data_dictionary["test_labels"][label],
                    # weight=data_dictionary["test_weights"],
                )

        self.wandb_init(name=self.MODEL_IDENTIFIER + ".fit",
                        job_type="fit",
                        config=self.model_training_parameters)

        # train final model
        estimator = CatBoostClassifier(
            allow_writing_files=True,
            train_dir=Path(dk.data_path),
            **self.model_training_parameters,
        )

        init_models = [None] * y.shape[1]
        fit_params = []
        for i in range(len(eval_sets)):
            fit_params.append({
                    'eval_set': eval_sets[i],  'init_model': init_models[i],
                    'log_cout': sys.stdout, 'log_cerr': sys.stderr,
                    'callbacks': [wandb.catboost.WandbCallback()],
                 })

        multi_model = MultiOutputClassifierWithFeatureSelect(estimator=estimator)
        multi_model.fit(X=X, y=y, sample_weight=data_dictionary["train_weights"], selected_features_all_labels=selected_features_all_labels, fit_params=fit_params)

        # for i, estim in enumerate(multi_model.estimators_):
            # wandb.catboost.plot_feature_importances(estim, labels[i])

        wandb.finish()

        return multi_model

    def feature_select(self, data_dictionary):

        select_model_config = {
            "task_type": "CPU",
            "eval_metric": 'AUC',
            "auto_class_weights": 'Balanced',
            "colsample_bylevel": 0.096,
            "depth": 4,
            "boosting_type": "Plain",
            "bootstrap_type": "MVS",
            "l2_leaf_reg": 5.0,
            "learning_rate": 0.09,
            "save_snapshot": False,
            "allow_writing_files": False,
            "random_seed": 42,
        }

        selected_features_all_labels = {}
        for label in data_dictionary["train_labels"].columns:
            logger.info(f'Selecting features for label = {label}')

            self.wandb_init(name=f"{self.MODEL_IDENTIFIER}.feature_select[{label}]",
                job_type="feature_select",
                config={
                    "SELECT_FEATURES_ITERATIONS": self.SELECT_FEATURES_ITERATIONS,
                    "NUM_FEATURES_TO_SELECT": self.NUM_FEATURES_TO_SELECT,
                    "SELECT_FEATURES_STEPS": self.SELECT_FEATURES_STEPS,
                    "AUTODETECT_NUM_FEATURES_TO_SELECT": self.AUTODETECT_NUM_FEATURES_TO_SELECT,
                    "FEATURE_SELECT_LABEL": self.FEATURE_SELECT_LABEL,
                    "MODEL_IDENTIFIER": self.MODEL_IDENTIFIER,
                    **select_model_config
                    })

            # transform and prepare data
            x_train = data_dictionary["train_features"].copy().rename(columns=lambda x: x.replace('-', ':'))
            y_train = data_dictionary["train_labels"][label].copy()

            # prepare eval data
            test_data = None

            if self.config["freqai"].get('data_split_parameters', {}).get('test_size', 0.05) > 0:
                # replace '-' with ':' in test labels
                x_eval = data_dictionary["test_features"].copy().rename(columns=lambda x: x.replace('-', ':'))
                y_eval = data_dictionary["test_labels"][label].copy()

                test_data = Pool(
                    data=x_eval,
                    label=y_eval
                )

            feature_select_model = CatBoostClassifier(
                iterations=self.SELECT_FEATURES_ITERATIONS,
                **select_model_config
            )

            best_f = feature_select_model.select_features(
                x_train,
                y_train,
                eval_set=test_data,
                features_for_select=list(x_train.columns),
                num_features_to_select=self.NUM_FEATURES_TO_SELECT,
                steps=self.SELECT_FEATURES_STEPS,
                algorithm=EFeaturesSelectionAlgorithm.RecursiveByLossFunctionChange,
                shap_calc_type=EShapCalcType.Exact,
                train_final_model=False,
                logging_level=self.config["freqai"]["model_training_parameters"].get("logging_level", "Silent"),
                plot=False,
            )

            try:
                loss_graph = pd.DataFrame({"loss_values": best_f['loss_graph']['loss_values'], "removed_features_count": best_f['loss_graph']['removed_features_count']})
                optimal_features = x_train.shape[1] - loss_graph[loss_graph['loss_values'] == loss_graph['loss_values'].min()]['removed_features_count'].max()
                min_loss_value = loss_graph["loss_values"].min()

                logger.info(f'Now optimal number of features = {optimal_features} with value = {min_loss_value}')

                # Convert DataFrame to wandb.Table
                loss_table = wandb.Table(dataframe=loss_graph)

                # Log the table to wandb
                wandb.log({"Loss Graph": loss_table})
                wandb.log({"Optimal Features": optimal_features, "Minimum Loss Value": min_loss_value})

                # Convert selected and eliminated features to wandb.Table
                selected_features_table = wandb.Table(data=[best_f['selected_features_names']], columns=["Selected Features"])
                eliminated_features_table = wandb.Table(data=[best_f['eliminated_features_names']], columns=["Eliminated Features"])

                # Log the tables to wandb
                wandb.log({"Selected Features": selected_features_table, "Eliminated Features": eliminated_features_table})
            except:
                pass

            selected_features_all_labels[label] = [x.replace(':', '-') for x in best_f['selected_features_names']]

            wandb.finish()

        return selected_features_all_labels

    def predict(
        self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    ) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
        """
        Filter the prediction features data and predict with it.
        :param unfiltered_df: Full dataframe for the current backtest period.
        :return:
        :pred_df: dataframe containing the predictions
        :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
        data (NaNs) or felt uncertain about data (PCA and DI index)
        """

        dk.find_features(unfiltered_df)
        filtered_df, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, training_filter=False
        )

        dk.data_dictionary["prediction_features"] = filtered_df

        selected_features_all_labels = dk.data['selected_features']

        dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
            dk.data_dictionary["prediction_features"], outlier_check=True)

        predictions = self.model.predict(dk.data_dictionary["prediction_features"], selected_features_all_labels)
        if self.CONV_WIDTH == 1:
            predictions = np.reshape(predictions, (-1, len(dk.label_list)))

        pred_df = DataFrame(predictions, columns=dk.label_list)

        predictions_prob = self.model.predict_proba(dk.data_dictionary["prediction_features"], selected_features_all_labels)
        if self.CONV_WIDTH == 1:
            predictions_prob = np.reshape(predictions_prob, (-1, len(self.model.classes_)))
        pred_df_prob = DataFrame(predictions_prob, columns=self.model.classes_)

        pred_df = pd.concat([pred_df, pred_df_prob], axis=1)

        if dk.feature_pipeline["di"]:
            dk.DI_values = dk.feature_pipeline["di"].di_values
        else:
            dk.DI_values = np.zeros(outliers.shape[0])
        dk.do_predict = outliers

        return (pred_df, dk.do_predict)

    def define_data_pipeline(self, threads) -> Pipeline:
        """
        User defines their custom feature pipeline here (if they wish)
        """
        feature_pipeline = Pipeline([
            ('scaler', SKLearnWrapper(RobustScaler())),
            # ('di', ds.DissimilarityIndex(di_threshold=10, n_jobs=threads))
        ])

        return feature_pipeline

    def define_label_pipeline(self, threads) -> Pipeline:
        """
        User defines their custom label pipeline here (if they wish)
        """
        label_pipeline = Pipeline([
            ('scaler', SKLearnWrapper(RobustScaler())),
        ])

        return label_pipeline