import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class VotingRegressor(BaseRegressionModel):
    """
    Voting Regressor combining multiple models with equal weights
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.base_models = {}
        
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the voting model
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
        
        self.base_models['lr'] = LinearRegression(**self.model_training_parameters)
        
        # Fit all base models
        for name, model in self.base_models.items():
            model.fit(
                data_dictionary["train_features"],
                data_dictionary["train_labels"]
            )
            
        return self
        
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Predict using voting (average of all models)
        """
        features_filtered, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, dk.label_list, training_filter=False
        )
        
        # Get predictions from all models
        predictions = []
        for name, model in self.base_models.items():
            pred = model.predict(features_filtered)
            predictions.append(pred)
            
        # Average the predictions (voting)
        final_pred = np.mean(predictions, axis=0)
        
        # Create prediction dataframe
        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df['&-s_predict'] = final_pred
        
        # Create do_predict array
        do_predict = np.ones(len(unfiltered_df), dtype=np.int_)
        
        return pred_df, do_predict 