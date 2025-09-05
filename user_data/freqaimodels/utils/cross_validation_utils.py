"""
Cross-Validation Utilities for FreqAI Models

This module provides comprehensive cross-validation functionality for all FreqAI models,
including different fold configurations, stability validation, and performance metrics.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import logging
from datetime import datetime
import json
import os

from .logging_utils import FreqAILogger

# Create logger instance
logger = FreqAILogger("CrossValidation").logger


class CrossValidationManager:
    """
    Comprehensive cross-validation manager for FreqAI models.
    
    Features:
    - Multiple fold configurations (3, 5, 10 folds)
    - Stability validation across folds
    - Performance metrics calculation
    - Detailed reporting and logging
    """
    
    def __init__(self, 
                 fold_configs: List[int] = [3, 5, 10],
                 random_state: int = 42,
                 n_jobs: int = -1):
        """
        Initialize cross-validation manager.
        
        Args:
            fold_configs: List of fold configurations to test
            random_state: Random state for reproducibility
            n_jobs: Number of jobs for parallel processing (-1 for all cores)
        """
        self.fold_configs = fold_configs
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.results = {}
        
        logger.info(f"CrossValidationManager initialized with fold_configs={fold_configs}")
    
    def validate_model(self, 
                      model: Any, 
                      X: np.ndarray, 
                      y: np.ndarray,
                      model_name: str) -> Dict[str, Any]:
        """
        Perform comprehensive cross-validation for a model.
        
        Args:
            model: FreqAI model instance
            X: Feature matrix
            y: Target vector
            model_name: Name of the model for logging
            
        Returns:
            Dictionary containing cross-validation results
        """
        logger.info(f"Starting cross-validation for {model_name}")
        
        results = {
            'model_name': model_name,
            'fold_results': {},
            'stability_metrics': {},
            'overall_metrics': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Validate input data
        if not self._validate_data(X, y):
            logger.error(f"Data validation failed for {model_name}")
            return results
        
        # Perform cross-validation for each fold configuration
        for n_folds in self.fold_configs:
            logger.info(f"Testing {model_name} with {n_folds}-fold CV")
            
            fold_result = self._perform_cross_validation(
                model, X, y, n_folds, model_name
            )
            results['fold_results'][f'{n_folds}_folds'] = fold_result
        
        # Calculate stability metrics
        results['stability_metrics'] = self._calculate_stability_metrics(results['fold_results'])
        
        # Calculate overall metrics
        results['overall_metrics'] = self._calculate_overall_metrics(results['fold_results'])
        
        logger.info(f"Cross-validation completed for {model_name}")
        return results
    
    def _validate_data(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Validate input data for cross-validation."""
        try:
            if X.shape[0] != y.shape[0]:
                logger.error(f"Shape mismatch: X={X.shape}, y={y.shape}")
                return False
            
            if np.any(np.isnan(X)) or np.any(np.isnan(y)):
                logger.error("Data contains NaN values")
                return False
            
            if np.any(np.isinf(X)) or np.any(np.isinf(y)):
                logger.error("Data contains infinite values")
                return False
            
            if X.shape[0] < 10:
                logger.warning(f"Small dataset: {X.shape[0]} samples")
            
            return True
            
        except Exception as e:
            logger.error(f"Data validation error: {str(e)}")
            return False
    
    def _perform_cross_validation(self, 
                                 model: Any, 
                                 X: np.ndarray, 
                                 y: np.ndarray,
                                 n_folds: int,
                                 model_name: str) -> Dict[str, Any]:
        """
        Perform cross-validation for a specific fold configuration.
        
        Args:
            model: Model instance
            X: Feature matrix
            y: Target vector
            n_folds: Number of folds
            model_name: Model name for logging
            
        Returns:
            Cross-validation results for this fold configuration
        """
        try:
            # Create KFold splitter
            kf = KFold(n_splits=n_folds, shuffle=True, random_state=self.random_state)
            
            # Initialize metrics storage
            mse_scores = []
            mae_scores = []
            r2_scores = []
            training_times = []
            prediction_times = []
            
            # Perform cross-validation
            for fold_idx, (train_idx, test_idx) in enumerate(kf.split(X)):
                logger.debug(f"Processing fold {fold_idx + 1}/{n_folds} for {model_name}")
                
                # Split data
                X_train, X_test = X[train_idx], X[test_idx]
                y_train, y_test = y[train_idx], y[test_idx]
                
                # Train model
                start_time = datetime.now()
                model_copy = self._clone_model(model)
                model_copy.fit(X_train, y_train)
                training_time = (datetime.now() - start_time).total_seconds()
                training_times.append(training_time)
                
                # Make predictions
                start_time = datetime.now()
                y_pred = model_copy.predict(X_test)
                prediction_time = (datetime.now() - start_time).total_seconds()
                prediction_times.append(prediction_time)
                
                # Calculate metrics
                mse = mean_squared_error(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                mse_scores.append(mse)
                mae_scores.append(mae)
                r2_scores.append(r2)
                
                logger.debug(f"Fold {fold_idx + 1} - MSE: {mse:.6f}, MAE: {mae:.6f}, R²: {r2:.6f}")
            
            # Calculate summary statistics
            result = {
                'n_folds': n_folds,
                'mse': {
                    'mean': np.mean(mse_scores),
                    'std': np.std(mse_scores),
                    'min': np.min(mse_scores),
                    'max': np.max(mse_scores),
                    'scores': mse_scores
                },
                'mae': {
                    'mean': np.mean(mae_scores),
                    'std': np.std(mae_scores),
                    'min': np.min(mae_scores),
                    'max': np.max(mae_scores),
                    'scores': mae_scores
                },
                'r2': {
                    'mean': np.mean(r2_scores),
                    'std': np.std(r2_scores),
                    'min': np.min(r2_scores),
                    'max': np.max(r2_scores),
                    'scores': r2_scores
                },
                'timing': {
                    'training_time_mean': np.mean(training_times),
                    'training_time_std': np.std(training_times),
                    'prediction_time_mean': np.mean(prediction_times),
                    'prediction_time_std': np.std(prediction_times)
                }
            }
            
            logger.info(f"{n_folds}-fold CV completed for {model_name} - "
                       f"MSE: {result['mse']['mean']:.6f}±{result['mse']['std']:.6f}, "
                       f"R²: {result['r2']['mean']:.6f}±{result['r2']['std']:.6f}")
            
            return result
            
        except Exception as e:
            logger.error(f"Cross-validation error for {model_name} with {n_folds} folds: {str(e)}")
            return {
                'n_folds': n_folds,
                'error': str(e),
                'mse': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'scores': []},
                'mae': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'scores': []},
                'r2': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan, 'scores': []},
                'timing': {'training_time_mean': np.nan, 'training_time_std': np.nan, 
                          'prediction_time_mean': np.nan, 'prediction_time_std': np.nan}
            }
    
    def _clone_model(self, model: Any) -> Any:
        """Create a clone of the model for cross-validation."""
        try:
            # Get model parameters
            params = model.get_params() if hasattr(model, 'get_params') else {}
            
            # Create new instance with same parameters
            model_class = type(model)
            new_model = model_class(**params)
            
            return new_model
            
        except Exception as e:
            logger.warning(f"Model cloning failed, using original: {str(e)}")
            return model
    
    def _calculate_stability_metrics(self, fold_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate stability metrics across different fold configurations."""
        stability_metrics = {}
        
        try:
            # Extract metrics for each fold configuration
            metrics_data = {}
            for fold_key, result in fold_results.items():
                if 'error' not in result:
                    metrics_data[fold_key] = {
                        'mse_mean': result['mse']['mean'],
                        'mse_std': result['mse']['std'],
                        'mae_mean': result['mae']['mean'],
                        'mae_std': result['mae']['std'],
                        'r2_mean': result['r2']['mean'],
                        'r2_std': result['r2']['std']
                    }
            
            if len(metrics_data) > 1:
                # Calculate coefficient of variation (stability metric)
                mse_cv = np.std([data['mse_mean'] for data in metrics_data.values()]) / np.mean([data['mse_mean'] for data in metrics_data.values()])
                mae_cv = np.std([data['mae_mean'] for data in metrics_data.values()]) / np.mean([data['mae_mean'] for data in metrics_data.values()])
                r2_cv = np.std([data['r2_mean'] for data in metrics_data.values()]) / np.mean([data['r2_mean'] for data in metrics_data.values()])
                
                stability_metrics = {
                    'mse_coefficient_of_variation': mse_cv,
                    'mae_coefficient_of_variation': mae_cv,
                    'r2_coefficient_of_variation': r2_cv,
                    'overall_stability_score': (1 - (mse_cv + mae_cv + abs(r2_cv)) / 3)
                }
            else:
                stability_metrics = {
                    'mse_coefficient_of_variation': np.nan,
                    'mae_coefficient_of_variation': np.nan,
                    'r2_coefficient_of_variation': np.nan,
                    'overall_stability_score': np.nan
                }
                
        except Exception as e:
            logger.error(f"Error calculating stability metrics: {str(e)}")
            stability_metrics = {
                'mse_coefficient_of_variation': np.nan,
                'mae_coefficient_of_variation': np.nan,
                'r2_coefficient_of_variation': np.nan,
                'overall_stability_score': np.nan,
                'error': str(e)
            }
        
        return stability_metrics
    
    def _calculate_overall_metrics(self, fold_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall metrics across all fold configurations."""
        overall_metrics = {}
        
        try:
            # Aggregate all scores across fold configurations
            all_mse_scores = []
            all_mae_scores = []
            all_r2_scores = []
            
            for fold_key, result in fold_results.items():
                if 'error' not in result:
                    all_mse_scores.extend(result['mse']['scores'])
                    all_mae_scores.extend(result['mae']['scores'])
                    all_r2_scores.extend(result['r2']['scores'])
            
            if all_mse_scores:
                overall_metrics = {
                    'total_folds_tested': len(all_mse_scores),
                    'overall_mse': {
                        'mean': np.mean(all_mse_scores),
                        'std': np.std(all_mse_scores),
                        'min': np.min(all_mse_scores),
                        'max': np.max(all_mse_scores)
                    },
                    'overall_mae': {
                        'mean': np.mean(all_mae_scores),
                        'std': np.std(all_mae_scores),
                        'min': np.min(all_mae_scores),
                        'max': np.max(all_mae_scores)
                    },
                    'overall_r2': {
                        'mean': np.mean(all_r2_scores),
                        'std': np.std(all_r2_scores),
                        'min': np.min(all_r2_scores),
                        'max': np.max(all_r2_scores)
                    }
                }
            else:
                overall_metrics = {
                    'total_folds_tested': 0,
                    'overall_mse': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan},
                    'overall_mae': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan},
                    'overall_r2': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan}
                }
                
        except Exception as e:
            logger.error(f"Error calculating overall metrics: {str(e)}")
            overall_metrics = {
                'total_folds_tested': 0,
                'overall_mse': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan},
                'overall_mae': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan},
                'overall_r2': {'mean': np.nan, 'std': np.nan, 'min': np.nan, 'max': np.nan},
                'error': str(e)
            }
        
        return overall_metrics
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save cross-validation results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/ml_models/cv_results_{results['model_name']}_{timestamp}.json"
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Cross-validation results saved to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return ""
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a human-readable report from cross-validation results."""
        report = []
        report.append("=" * 60)
        report.append(f"CROSS-VALIDATION REPORT: {results['model_name']}")
        report.append("=" * 60)
        report.append(f"Timestamp: {results['timestamp']}")
        report.append("")
        
        # Overall metrics
        if 'overall_metrics' in results:
            overall = results['overall_metrics']
            report.append("OVERALL METRICS:")
            report.append(f"  Total folds tested: {overall.get('total_folds_tested', 0)}")
            report.append("")
            
            if 'overall_mse' in overall:
                mse = overall['overall_mse']
                report.append(f"  MSE: {mse.get('mean', 'N/A'):.6f} ± {mse.get('std', 'N/A'):.6f}")
                report.append(f"    Range: [{mse.get('min', 'N/A'):.6f}, {mse.get('max', 'N/A'):.6f}]")
            
            if 'overall_mae' in overall:
                mae = overall['overall_mae']
                report.append(f"  MAE: {mae.get('mean', 'N/A'):.6f} ± {mae.get('std', 'N/A'):.6f}")
                report.append(f"    Range: [{mae.get('min', 'N/A'):.6f}, {mae.get('max', 'N/A'):.6f}]")
            
            if 'overall_r2' in overall:
                r2 = overall['overall_r2']
                report.append(f"  R²:  {r2.get('mean', 'N/A'):.6f} ± {r2.get('std', 'N/A'):.6f}")
                report.append(f"    Range: [{r2.get('min', 'N/A'):.6f}, {r2.get('max', 'N/A'):.6f}]")
        
        report.append("")
        
        # Stability metrics
        if 'stability_metrics' in results:
            stability = results['stability_metrics']
            report.append("STABILITY METRICS:")
            report.append(f"  MSE CV: {stability.get('mse_coefficient_of_variation', 'N/A'):.6f}")
            report.append(f"  MAE CV: {stability.get('mae_coefficient_of_variation', 'N/A'):.6f}")
            report.append(f"  R² CV:  {stability.get('r2_coefficient_of_variation', 'N/A'):.6f}")
            report.append(f"  Overall Stability: {stability.get('overall_stability_score', 'N/A'):.6f}")
        
        report.append("")
        
        # Per-fold results
        if 'fold_results' in results:
            report.append("PER-FOLD RESULTS:")
            for fold_key, fold_result in results['fold_results'].items():
                report.append(f"  {fold_key}:")
                if 'error' in fold_result:
                    report.append(f"    ERROR: {fold_result['error']}")
                else:
                    report.append(f"    MSE: {fold_result['mse']['mean']:.6f} ± {fold_result['mse']['std']:.6f}")
                    report.append(f"    MAE: {fold_result['mae']['mean']:.6f} ± {fold_result['mae']['std']:.6f}")
                    report.append(f"    R²:  {fold_result['r2']['mean']:.6f} ± {fold_result['r2']['std']:.6f}")
                    if 'timing' in fold_result:
                        timing = fold_result['timing']
                        report.append(f"    Training time: {timing.get('training_time_mean', 'N/A'):.3f}s")
                        report.append(f"    Prediction time: {timing.get('prediction_time_mean', 'N/A'):.3f}s")
                report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)


def run_cross_validation_for_all_models(models_dict: Dict[str, Any], 
                                       X: np.ndarray, 
                                       y: np.ndarray,
                                       fold_configs: List[int] = [3, 5, 10]) -> Dict[str, Any]:
    """
    Run cross-validation for all models in the dictionary.
    
    Args:
        models_dict: Dictionary of model instances
        X: Feature matrix
        y: Target vector
        fold_configs: List of fold configurations to test
        
    Returns:
        Dictionary containing cross-validation results for all models
    """
    cv_manager = CrossValidationManager(fold_configs=fold_configs)
    all_results = {}
    
    logger.info(f"Starting cross-validation for {len(models_dict)} models")
    
    for model_name, model in models_dict.items():
        logger.info(f"Processing {model_name}...")
        
        try:
            result = cv_manager.validate_model(model, X, y, model_name)
            all_results[model_name] = result
            
            # Save individual results
            cv_manager.save_results(result)
            
            # Generate and log report
            report = cv_manager.generate_report(result)
            logger.info(f"\n{report}")
            
        except Exception as e:
            logger.error(f"Error processing {model_name}: {str(e)}")
            all_results[model_name] = {
                'model_name': model_name,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    # Save combined results
    combined_filename = f"logs/ml_models/cv_results_all_models_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        os.makedirs(os.path.dirname(combined_filename), exist_ok=True)
        with open(combined_filename, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        logger.info(f"Combined results saved to {combined_filename}")
    except Exception as e:
        logger.error(f"Error saving combined results: {str(e)}")
    
    return all_results 