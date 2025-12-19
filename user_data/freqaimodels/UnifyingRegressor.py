import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class UnifyingRegressor(BaseRegressionModel):
    """
    Unifying Regressor using holdout set for meta-learner
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        self.meta_learner = None
        
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the unifying model
        """
        # Initialize base models
        self.base_models['rf'] = RandomForestRegressor(
            max_depth=8,
            random_state=42,
            **self.model_training_parameters
        )
        
        self.base_models['lr'] = LinearRegression(**self.model_training_parameters)
        
        # Fit base models on training data
        base_predictions = {}
        for name, model in self.base_models.items():
            model.fit(
                data_dictionary["train_features"],
                data_dictionary["train_labels"]
            )
            base_predictions[name] = model.predict(data_dictionary["train_features"])
            
        # Create meta-features
        meta_features = np.column_stack(list(base_predictions.values()))
        
        # Fit meta-learner
        self.meta_learner = LinearRegression()
        self.meta_learner.fit(meta_features, data_dictionary["train_labels"])
        
        return self
        
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Predict using unifying
        """
        features_filtered, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, dk.label_list, training_filter=False
        )
        
        # Get base model predictions
        base_predictions = {}
        for name, model in self.base_models.items():
            base_predictions[name] = model.predict(features_filtered)
            
        # Create meta-features
        meta_features = np.column_stack(list(base_predictions.values()))
        
        # Meta-learner prediction
        final_pred = self.meta_learner.predict(meta_features)
        
        # Create prediction dataframe
        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df['&-s_predict'] = final_pred
        
        # Create do_predict array
        do_predict = np.ones(len(unfiltered_df), dtype=np.int_)
        
        return pred_df, do_predict 
