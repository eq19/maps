import logging
import numpy as np
import pandas as pd
from typing import Any, Dict
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen

logger = logging.getLogger(__name__)

class YieldedEnsembleRegressor(BaseRegressionModel):
    """
    Yielded Ensemble Regressor combining multiple models with adaptive weighting
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.models = {}
        self.weights = {}
        self.scaler = StandardScaler()
        
    def fit(self, data_dictionary: Dict[str, Any], dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Fit the ensemble model
        """
        # Initialize base models
        self.models['rf'] = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            **self.model_training_parameters
        )
        
        self.models['lr'] = LinearRegression(**self.model_training_parameters)
        
        # Fit each model
        for name, model in self.models.items():
            model.fit(
                data_dictionary["train_features"],
                data_dictionary["train_labels"]
            )
            
        # Initialize equal weights
        self.weights = {name: 1.0 / len(self.models) for name in self.models.keys()}
        
        return self
        
    def predict(self, unfiltered_df: pd.DataFrame, dk: FreqaiDataKitchen, **kwargs) -> tuple[pd.DataFrame, np.ndarray]:
        """
        Predict using ensemble
        """
        features_filtered, _ = dk.filter_features(
            unfiltered_df, dk.training_features_list, dk.label_list, training_filter=False
        )
        
        # Get predictions from each model
        predictions = {}
        for name, model in self.models.items():
            pred = model.predict(features_filtered)
            predictions[name] = pred
            
        # Weighted ensemble prediction
        ensemble_pred = np.zeros_like(list(predictions.values())[0])
        for name, pred in predictions.items():
            ensemble_pred += pred * self.weights[name]
            
        # Create prediction dataframe
        pred_df = pd.DataFrame(index=unfiltered_df.index)
        pred_df['&-s_predict'] = ensemble_pred
        
        # Create do_predict array (1 for all predictions)
        do_predict = np.ones(len(unfiltered_df), dtype=np.int_)
        
        return pred_df, do_predict 
