from datetime import datetime
import json
import logging
import select
import sys
from pathlib import Path
import time
from typing import Any, Dict
from io import StringIO
from neptune.types import File

from catboost import CatBoostRegressor, EFeaturesSelectionAlgorithm, EShapCalcType, Pool

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
import numpy as np
import numpy.typing as npt
import pandas as pd
import psutil
from pandas import DataFrame
from typing import Any, Dict, List, Optional, Tuple
from datasieve.transforms import SKLearnWrapper, DissimilarityIndex
from datasieve.pipeline import Pipeline
from sklearn.preprocessing import QuantileTransformer, RobustScaler, StandardScaler
import datasieve.transforms as ds
import neptune
from neptune.utils import stringify_unsupported
from freqtrade.freqai.base_models.FreqaiMultiOutputRegressor import FreqaiMultiOutputRegressor


logger = logging.getLogger(__name__)


class CatboostFeatureSelectedRegressorV1(BaseRegressionModel):
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


    def neptune_init_run(self):
        run = neptune.init_run(
            project='roma/TrendMaster',
            api_token="eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJiZGUxMjJkOS1iMzg1LTQwMGQtYTQwZC1iZWJiZTA0NzI2YjIifQ==",
            # capture_hardware_metrics=True,
            # capture_stderr=True,
            # capture_stdout=True,
        )
        return run

    def fit(self, data_dictionary: Dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :param data_dictionary: the dictionary constructed by DataHandler to hold
                                all the training and test data/labels.
        """
        # select features
        selected_features = self.feature_select(data_dictionary)
        # selected_features = data_dictionary["train_features"].columns.tolist()
        dk.data['selected_features'] = selected_features

        # run = self.neptune_init_run()

        X = data_dictionary["train_features"][selected_features]
        y = data_dictionary["train_labels"]

        eval_sets = [None] * y.shape[1]

        # transform and prepare data
        train_data = Pool(
            data=X,
            label=y,
            weight=data_dictionary["train_weights"],
        )
        if self.freqai_info.get('data_split_parameters', {}).get('test_size', 0.1) == 0:
            test_data = None
        else:
            test_data = Pool(
                data=data_dictionary["test_features"][selected_features],
                label=data_dictionary["test_labels"],
                weight=data_dictionary["test_weights"],
            )

        # train final model
        estimator = CatBoostRegressor(
            allow_writing_files=True,
            train_dir=Path(dk.data_path),
            **self.model_training_parameters,
        )

        # plot_file = "training_plot_catboost.html"

        init_models = [None] * y.shape[1]
        fit_params = []
        for i in range(len(eval_sets)):
            fit_params.append({
                    'eval_set': eval_sets[i],  'init_model': init_models[i],
                    'log_cout': sys.stdout, 'log_cerr': sys.stderr,

                 })

        multi_model = FreqaiMultiOutputRegressor(estimator=estimator)
        # multi_model.n_jobs = y.shape[1]
        multi_model.fit(X=X, y=y, sample_weight=data_dictionary["train_weights"], fit_params=fit_params)


        # final_model.fit(X=train_data,
        #                 eval_set=test_data,
        #                 log_cout=sys.stdout,
        #                 log_cerr=sys.stderr,
        #                 # plot config
        #                 plot=True,
        #                 plot_file=plot_file)

        # self.neptune_model_fit(run, final_model, plot_file)

        return multi_model

    def neptune_model_fit(self, run: neptune.init_run, model: CatBoostRegressor, plot_file: str):
        run["training/plot"].upload(plot_file)

        run["training/best_score"] = stringify_unsupported(model.get_best_score())
        run["training/best_iteration"] = stringify_unsupported(model.get_best_iteration())

        # upload the model
        # model.save_model("model.cbm")
        # run["model/binary"].upload("model.cbm")

        run["model/attributes/tree_count"] = model.tree_count_
        run["model/attributes/feature_importances"] = dict(
            zip([name.replace('/', '') for name in model.feature_names_], model.get_feature_importance())
        )
        # run["model/attributes/probability_threshold"] = model.get_probability_threshold()

        # the rest attributes
        run["model/parameters"] = stringify_unsupported(model.get_all_params())

        run.stop()


    def feature_select(self, data_dictionary):
        run = self.neptune_init_run()

        # transform and prepare data
        x_train = data_dictionary["train_features"].copy().rename(columns=lambda x: x.replace('-', ':'))
        y_train = data_dictionary["train_labels"].copy().iloc[:, 0]

        # prepare eval data
        test_data = None

        if self.config["freqai"].get('data_split_parameters', {}).get('test_size', 0.05) > 0:
            # replace '-' with ':' in test labels
            x_eval = data_dictionary["test_features"].copy().rename(columns=lambda x: x.replace('-', ':'))
            y_eval = data_dictionary["test_labels"].copy().iloc[:, 0]

            test_data = Pool(
                data=x_eval,
                label=y_eval
            )


        # create model & select features
        # feature_select_model = CatBoostRegressor(
        #     task_type="CPU" ,
        #     eval_metric='MultiRMSE',
        #     loss_function='MultiRMSE',
        #     n_estimators=self.SELECT_FEATURES_ITERATIONS,
        #     thread_count=10,
        #     random_seed=42
        # )

        feature_select_model = CatBoostRegressor(iterations=self.SELECT_FEATURES_ITERATIONS,
                                task_type="CPU",
                                eval_metric='RMSE',
                                colsample_bylevel=0.3,
                                depth=6,
                                boosting_type="Plain",
                                bootstrap_type="MVS",
                                l2_leaf_reg=9.0,
                                learning_rate=0.05,
                                save_snapshot=False,
                                allow_writing_files=False,
                                random_seed=42)



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
            logger.info(f'Now optimal number of features = {optimal_features}')

            # fig = loss_graph.plot(x='removed_features_count', y='loss_values', title=f'Loss values over removed features count')
            # run["training/loss_graph"].upload(fig)
            csv_buffer = StringIO()
            loss_graph.to_csv(csv_buffer, index=False)
            run["training/loss_over_removed_features"].upload(File.from_stream(csv_buffer, extension="csv"))

            # run["training/loss_values"] = stringify_unsupported(best_f['loss_graph']['loss_values'])
            # run["training/removed_features_count"] = stringify_unsupported(best_f['loss_graph']['removed_features_count'])

            # run["training/selected_features_names"] = stringify_unsupported(best_f['selected_features_names'])
            # run["training/eliminated_features_names"] = stringify_unsupported(best_f['eliminated_features_names'])
        except:
            pass

        # save best_f to json file
        with open(f'user_data/artifacts/{str(self.config["freqai"].get("identifier"))}_best_features_{datetime.now()}.json', 'w') as f:
            json.dump(best_f, f)

        run.stop()

        new_best_features = [x.replace(':', '-') for x in best_f['selected_features_names']]
        return new_best_features


    def predict(self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
        """
        Filter the prediction features data and predict with it.
        :param unfiltered_df: Full dataframe for the current backtest period.
        :return:
        :pred_df: dataframe containing the predictions
        :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
        data (NaNs) or felt uncertain about data (PCA and DI index)
        """
        logger.info("ENTER CatboostFeatureSelectedRegressorV1.predict()")

        # Feature finding, filtering, and transformation
        dk.find_features(unfiltered_df)
        dk.data_dictionary["prediction_features"], _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, training_filter=False
        )
        dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
            dk.data_dictionary["prediction_features"], outlier_check=True)

        # Selecting specific features for prediction
        selected_feature_names = dk.data['selected_features']
        selected_features = dk.data_dictionary["prediction_features"][selected_feature_names].copy()

        # Model prediction with selected features
        predictions = self.model.predict(selected_features)

        # Post-processing predictions
        pred_df = DataFrame(predictions, columns=dk.label_list)
        pred_df, _, _ = dk.label_pipeline.inverse_transform(pred_df)

        # print(predictions)
        # print(dk.do_predict)

        # Handling outliers and DI values
        if dk.feature_pipeline["di"]:
            dk.DI_values = dk.feature_pipeline["di"].di_values
        else:
            dk.DI_values = np.zeros(outliers.shape[0])
        dk.do_predict = outliers

        print("Predictions: ", pred_df)
        print("do_predict: ", dk.do_predict)

        return (pred_df, dk.do_predict)


    # def predict(
    #     self, unfiltered_df: DataFrame, dk: FreqaiDataKitchen, **kwargs
    # ) -> Tuple[DataFrame, npt.NDArray[np.int_]]:
    #     """
    #     Filter the prediction features data and predict with it.
    #     :param unfiltered_df: Full dataframe for the current backtest period.
    #     :return:
    #     :pred_df: dataframe containing the predictions
    #     :do_predict: np.array of 1s and 0s to indicate places where freqai needed to remove
    #     data (NaNs) or felt uncertain about data (PCA and DI index)
    #     """

    #     dk.find_features(unfiltered_df)
    #     dk.data_dictionary["prediction_features"], _ = dk.filter_features(
    #         unfiltered_df, dk.training_features_list, training_filter=False
    #     )

    #     dk.data_dictionary["prediction_features"], outliers, _ = dk.feature_pipeline.transform(
    #         dk.data_dictionary["prediction_features"], outlier_check=True)

    #     selected_feature_names = dk.data['selected_features']
    #     selected_features = dk.data_dictionary["prediction_features"][selected_feature_names].copy()

    #     predictions = self.model.predict(selected_features)
    #     if self.CONV_WIDTH == 1:
    #         predictions = np.reshape(predictions, (-1, len(dk.label_list)))

    #     pred_df = DataFrame(predictions, columns=dk.label_list)

    #     pred_df, _, _ = dk.label_pipeline.inverse_transform(pred_df)
    #     if dk.feature_pipeline["di"]:
    #         dk.DI_values = dk.feature_pipeline["di"].di_values
    #     else:
    #         dk.DI_values = np.zeros(outliers.shape[0])
    #     dk.do_predict = outliers

    #     return (pred_df, dk.do_predict)


    def predict_old(
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
        filtered_df = dk.normalize_data_from_metadata(filtered_df)
        dk.data_dictionary["prediction_features"] = filtered_df

        selected_feature_names = dk.data['selected_features']
        selected_features = dk.data_dictionary["prediction_features"][selected_feature_names]

        # optional additional data cleaning/analysis
        self.data_cleaning_predict(dk)

        start = time.time()
        predictions = self.model.predict(selected_features)
        time_spent = (time.time() - start)
        self.dd.update_metric_tracker('predict_time', time_spent, dk.pair)

        pred_df = DataFrame(predictions, columns=dk.label_list)

        print("Predictions: ", pred_df)
        pred_df = dk.denormalize_labels_from_metadata(pred_df)

        return (pred_df, dk.do_predict)

    def define_data_pipeline(self, threads) -> Pipeline:
        """
        User defines their custom feature pipeline here (if they wish)
        """
        feature_pipeline = Pipeline([
            ('scaler', SKLearnWrapper(RobustScaler())),
            ('di', ds.DissimilarityIndex(di_threshold=10, n_jobs=threads))
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