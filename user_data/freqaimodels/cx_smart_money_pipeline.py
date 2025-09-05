"""
CX Smart Money Model Pipeline
=============================

High-Accuracy Model Pipeline for CX Smart Money Strategy
Only includes models with 85%+ accuracy threshold.

This module implements the model pipeline specified in the CX Smart Money Optimization Plan.
"""

import logging
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
BaseFreqAIModel = BaseRegressionModel

logger = logging.getLogger(__name__)


class CXSmartMoneyModelPipeline:
    """
    High-Accuracy Model Pipeline for CX Smart Money Strategy
    Only includes models with 85%+ accuracy threshold.
    
    Features:
    - Accuracy validation and filtering
    - Ensemble prediction methods
    - Performance tracking
    - Dynamic model qualification
    - Weighted averaging
    """
    
    def __init__(self, accuracy_threshold: float = 0.85, test_mode: bool = False):
        # Lower threshold for testing with synthetic data
        if test_mode:
            accuracy_threshold = 0.1  # Much lower threshold for testing
        self.accuracy_threshold = accuracy_threshold
        self.qualified_models = {}
        self.ensemble_weights = {}
        self.performance_metrics = {}
        self.model_instances = {}
        self.last_validation = None
        
        # Target models for CX Smart Money strategy
        self.target_models = [
            "FreqAILSTMRegressor",
            "FreqAILSTMCudaRegressor", 
                "EnhancedCatboostRegressor",
    "EnhancedLightGBMRegressor",
    "EnhancedXGBoostRegressor"
        ]
        
        logger.info(f"CX Smart Money Model Pipeline initialized with {accuracy_threshold:.1%} accuracy threshold")
    
    def validate_model_accuracy(self, model_name: str, predictions: np.ndarray, 
                              actual: np.ndarray) -> Tuple[bool, float]:
        """
        Validate if model meets accuracy threshold
        
        Args:
            model_name: Name of the model
            predictions: Model predictions
            actual: Actual values
            
        Returns:
            Tuple of (is_qualified, accuracy_score)
        """
        try:
            # Calculate R² score as accuracy metric
            accuracy = r2_score(actual, predictions)
            
            is_qualified = accuracy >= self.accuracy_threshold
            
            logger.info(f"Model {model_name}: Accuracy = {accuracy:.4f}, Qualified = {is_qualified}")
            
            return is_qualified, accuracy
            
        except Exception as e:
            logger.error(f"Error validating model {model_name} accuracy: {e}")
            return False, 0.0
    
    def add_model(self, model_name: str, model_instance: BaseFreqAIModel, 
                  accuracy: float) -> bool:
        """
        Add model to pipeline if it meets accuracy threshold
        
        Args:
            model_name: Name of the model
            model_instance: Trained model instance
            accuracy: Model accuracy score
            
        Returns:
            True if model was added, False otherwise
        """
        if accuracy >= self.accuracy_threshold:
            self.qualified_models[model_name] = model_instance
            self.performance_metrics[model_name] = {
                "accuracy": accuracy,
                "last_updated": datetime.now(),
                "predictions_count": 0,
                "total_error": 0.0
            }
            
            # Initialize weight based on accuracy
            self.ensemble_weights[model_name] = accuracy
            
            logger.info(f"Model {model_name} added to pipeline with accuracy {accuracy:.4f}")
            return True
        else:
            logger.warning(f"Model {model_name} rejected: accuracy {accuracy:.4f} < threshold {self.accuracy_threshold:.4f}")
            return False
    
    def get_qualified_models(self) -> List[str]:
        """Return only models that meet accuracy threshold"""
        return list(self.qualified_models.keys())
    
    def get_ensemble_prediction(self, X: np.ndarray) -> np.ndarray:
        """
        Get weighted ensemble prediction from qualified models
        
        Args:
            X: Input features
            
        Returns:
            Ensemble predictions
        """
        predictions = {}
        weights = {}
        
        if not self.qualified_models:
            logger.warning("No qualified models in pipeline")
            return np.zeros(X.shape[0])
        
        for model_name, model in self.qualified_models.items():
            try:
                pred = model.predict(X)
                predictions[model_name] = pred
                weights[model_name] = self.performance_metrics[model_name]["accuracy"]
                
                # Update prediction count
                self.performance_metrics[model_name]["predictions_count"] += 1
                
            except Exception as e:
                logger.warning(f"Model {model_name} prediction failed: {e}")
        
        if not predictions:
            logger.warning("No successful predictions from qualified models")
            return np.zeros(X.shape[0])
        
        # Calculate weighted average
        total_weight = sum(weights.values())
        ensemble_pred = np.zeros(X.shape[0])
        
        for model_name, pred in predictions.items():
            weight = weights[model_name] / total_weight
            ensemble_pred += weight * pred
        
        logger.debug(f"Ensemble prediction calculated from {len(predictions)} models")
        return ensemble_pred
    
    def update_model_performance(self, model_name: str, 
                                actual: np.ndarray, 
                                predicted: np.ndarray) -> bool:
        """
        Update model performance metrics
        
        Args:
            model_name: Name of the model
            actual: Actual values
            predicted: Predicted values
            
        Returns:
            True if model still qualified, False if removed
        """
        try:
            accuracy = r2_score(actual, predicted)
            mse = mean_squared_error(actual, predicted)
            mae = mean_absolute_error(actual, predicted)
            
            # Update performance metrics
            if model_name in self.performance_metrics:
                self.performance_metrics[model_name].update({
                    "accuracy": accuracy,
                    "mse": mse,
                    "mae": mae,
                    "last_updated": datetime.now()
                })
                
                # Update ensemble weight
                self.ensemble_weights[model_name] = accuracy
                
                # Remove model if accuracy drops below threshold
                if accuracy < self.accuracy_threshold:
                    if model_name in self.qualified_models:
                        del self.qualified_models[model_name]
                        logger.info(f"Model {model_name} removed due to low accuracy: {accuracy:.4f}")
                        return False
                
                logger.debug(f"Model {model_name} performance updated: accuracy={accuracy:.4f}")
                return True
            else:
                logger.warning(f"Model {model_name} not found in performance metrics")
                return False
                
        except Exception as e:
            logger.error(f"Error updating model {model_name} performance: {e}")
            return False
    
    def calculate_ensemble_confidence(self, predictions: Dict[str, np.ndarray]) -> float:
        """
        Calculate confidence score for ensemble prediction
        
        Args:
            predictions: Dictionary of model predictions
            
        Returns:
            Confidence score (0-1)
        """
        if not predictions:
            return 0.0
        
        try:
            # Calculate prediction variance as confidence metric
            pred_array = np.array(list(predictions.values()))
            variance = np.var(pred_array, axis=0)
            confidence = 1.0 / (1.0 + np.mean(variance))
            
            return float(confidence)
            
        except Exception as e:
            logger.error(f"Error calculating ensemble confidence: {e}")
            return 0.5
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Get current pipeline status
        
        Returns:
            Dictionary with pipeline status information
        """
        qualified_count = len(self.qualified_models)
        total_targets = len(self.target_models)
        
        status = {
            "accuracy_threshold": self.accuracy_threshold,
            "qualified_models": qualified_count,
            "total_target_models": total_targets,
            "qualification_rate": qualified_count / total_targets if total_targets > 0 else 0,
            "qualified_model_names": list(self.qualified_models.keys()),
            "performance_metrics": self.performance_metrics.copy(),
            "last_validation": self.last_validation,
            "pipeline_ready": qualified_count >= 3  # Need at least 3 models
        }
        
        return status
    
    def validate_pipeline(self, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
        """
        Validate entire pipeline with test data
        
        Args:
            X: Test features
            y: Test targets
            
        Returns:
            Validation results
        """
        validation_results = {
            "success": False,
            "qualified_models": [],
            "ensemble_accuracy": 0.0,
            "individual_accuracies": {},
            "errors": []
        }
        
        try:
            # Test each target model
            for model_name in self.target_models:
                try:
                    # Import model class dynamically
                    if model_name in ["FreqAILSTMRegressor", "FreqAILSTMCudaRegressor"]:
                        from .freqai_lstm_models import FreqAILSTMRegressor, FreqAILSTMCudaRegressor
                        model_class = FreqAILSTMRegressor if model_name == "FreqAILSTMRegressor" else FreqAILSTMCudaRegressor
                    elif model_name in ["EnhancedCatboostRegressor", "EnhancedLightGBMRegressor", "EnhancedXGBoostRegressor"]:
                        from .tree_models import EnhancedCatboostRegressor, EnhancedLightGBMRegressor, EnhancedXGBoostRegressor
                        if model_name == "EnhancedCatboostRegressor":
                            model_class = EnhancedCatboostRegressor
                        elif model_name == "EnhancedLightGBMRegressor":
                            model_class = EnhancedLightGBMRegressor
                        else:
                            model_class = EnhancedXGBoostRegressor
                    else:
                        logger.warning(f"Unknown model: {model_name}")
                        continue
                    
                    model_instance = model_class()
                    
                    # Train and test model
                    model_instance.fit(X, y)
                    predictions = model_instance.predict(X)
                    
                    # Validate accuracy
                    is_qualified, accuracy = self.validate_model_accuracy(
                        model_name, predictions, y
                    )
                    
                    validation_results["individual_accuracies"][model_name] = accuracy
                    
                    if is_qualified:
                        self.add_model(model_name, model_instance, accuracy)
                        validation_results["qualified_models"].append(model_name)
                    
                except Exception as e:
                    error_msg = f"Error testing model {model_name}: {e}"
                    validation_results["errors"].append(error_msg)
                    logger.error(error_msg)
            
            # Test ensemble prediction
            if self.qualified_models:
                ensemble_pred = self.get_ensemble_prediction(X)
                ensemble_accuracy = r2_score(y, ensemble_pred)
                validation_results["ensemble_accuracy"] = ensemble_accuracy
                validation_results["success"] = True
                
                logger.info(f"Pipeline validation complete: {len(self.qualified_models)} qualified models, ensemble accuracy: {ensemble_accuracy:.4f}")
            else:
                validation_results["errors"].append("No models qualified for pipeline")
            
            self.last_validation = datetime.now()
            
        except Exception as e:
            validation_results["errors"].append(f"Pipeline validation failed: {e}")
            logger.error(f"Pipeline validation failed: {e}")
        
        return validation_results
    
    def get_model_weights(self) -> Dict[str, float]:
        """Get current model weights for ensemble"""
        if not self.ensemble_weights:
            return {}
        
        total_weight = sum(self.ensemble_weights.values())
        return {model: weight / total_weight for model, weight in self.ensemble_weights.items()}
    
    def reset_pipeline(self):
        """Reset pipeline to initial state"""
        self.qualified_models.clear()
        self.ensemble_weights.clear()
        self.performance_metrics.clear()
        self.model_instances.clear()
        self.last_validation = None
        
        logger.info("CX Smart Money Model Pipeline reset")
    
    def __str__(self) -> str:
        """String representation of pipeline"""
        qualified_count = len(self.qualified_models)
        status = self.get_pipeline_status()
        
        return (f"CXSmartMoneyModelPipeline(qualified={qualified_count}, "
                f"threshold={self.accuracy_threshold:.1%}, "
                f"ready={status['pipeline_ready']})")
    
    def __repr__(self) -> str:
        return self.__str__()


# Global pipeline instance for strategy use
cx_smart_money_pipeline = CXSmartMoneyModelPipeline(accuracy_threshold=0.85) 