import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_predict
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class StackingRegressor(BaseRegressionModel):
    """
    Stacking Regressor using cross-validation for meta-features
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None
        
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the stacking model
        """
        # Initialize base models
        self.base_models['rf'] = RandomForestRegressor(
            n_estimators=50,
            max_depth=8,
            random_state=42,
            **self.model_training_parameters
        )
        
        self.base_models['gb'] = GradientBoostingRegressor(
            n_estimators=50,
            max_depth=6,
            random_state=42,
            **self.model_training_parameters
        )
        
        # Generate meta-features using cross-validation
        meta_features = []
        for name, model in self.base_models.items():
            cv_pred = cross_val_predict(
                model, 
                data_dictionary["train_features"], 
                data_dictionary["train_labels"],
                cv=3
            )
            meta_features.append(cv_pred)
            
        # Stack meta-features
        meta_features = np.column_stack(meta_features)
        
        # Fit base models on full training data
        for name, model in self.base_models.items():
            model.fit(
                data_dictionary["train_features"],
                data_dictionary["train_labels"]
            )
            
        # Fit meta-learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, data_dictionary["train_labels"])
        
        return self
        
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Predict using stacking
        """
        features_filtered, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, dk.label_list, training_filter=False
        )
        
        # Get base model predictions
        base_predictions = []
        for name, model in self.base_models.items():
            pred = model.predict(features_filtered)
            base_predictions.append(pred)
            
        # Create meta-features
        meta_features = np.column_stack(base_predictions)
        
        # Meta-learner prediction
        final_pred = self.meta_learner.predict(meta_features)
        
        # Create prediction dataframe
        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df['&-s_predict'] = final_pred
        
        # Create do_predict array
        do_predict = np.ones(len(unfiltered_df), dtype=np.int_)
        
        return pred_df, do_predict 