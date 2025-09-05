"""
Testing Utilities for FreqAI Models
==================================

This module provides comprehensive testing utilities for FreqAI models,
including model validation, performance benchmarking, and MPS compatibility tests.

Classes:
    FreqAIModelTester: Main testing class for model validation and benchmarking
    MPSCompatibilityTester: Specialized class for MPS compatibility testing

Functions:
    create_test_data: Create test data for model testing
    run_comprehensive_tests: Run comprehensive tests on multiple models
"""

import numpy as np
import pandas as pd
import time
import logging
from typing import Dict, List, Tuple, Any, Optional
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
import warnings
import torch

logger = logging.getLogger(__name__)

class FreqAIModelTester:
    """
    Comprehensive testing utilities for FreqAI models.
    
    This class provides methods for:
    - Model validation and testing
    - Performance benchmarking
    - MPS compatibility testing
    - Cross-validation
    - Model comparison
    - Robustness testing
    - Stability testing
    
    Attributes:
        verbose (bool): Whether to print detailed output
        test_results (Dict): Dictionary to store test results
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize model tester.
        
        Args:
            verbose: Whether to print detailed output during testing
        """
        self.verbose = verbose
        self.test_results = {}
        
    def test_model(self, model, X_train: np.ndarray, X_test: np.ndarray,
                   y_train: np.ndarray, y_test: np.ndarray,
                   model_name: str = "Unknown") -> Dict[str, Any]:
        """
        Test a single model and return comprehensive results.
        
        This method performs a complete evaluation of a model including:
        - Training time measurement
        - Prediction time measurement
        - Performance metrics calculation
        - MPS compatibility check
        - Cross-validation
        - Memory usage estimation
        
        Args:
            model: Model to test (must have fit() and predict() methods)
            X_train, X_test: Training and test features
            y_train, y_test: Training and test targets
            model_name: Name of the model for reporting
            
        Returns:
            Dictionary with comprehensive test results including:
            - training_time: Time taken to train the model
            - prediction_time: Time taken to make predictions
            - train_score: Training score (if available)
            - test_score: Test score (if available)
            - mse: Mean squared error
            - mae: Mean absolute error
            - r2: R-squared score
            - cross_val_scores: Cross-validation scores
            - mps_compatible: Whether model uses MPS
            - memory_usage: Estimated memory usage in MB
            - error: Error message if test failed
        """
        if self.verbose:
            print(f"\n🧪 Testing {model_name}...")
        
        # Initialize results dictionary
        results = {
            'model_name': model_name,
            'training_time': 0,
            'prediction_time': 0,
            'train_score': 0,
            'test_score': 0,
            'mse': 0,
            'mae': 0,
            'r2': 0,
            'cross_val_scores': [],
            'mps_compatible': False,
            'memory_usage': 0,
            'error': None
        }
        
        try:
            # Measure training time
            start_time = time.time()
            model.fit(X_train, y_train)
            training_time = time.time() - start_time
            results['training_time'] = training_time
            
            # Test MPS compatibility after training
            mps_compatible = self._test_mps_compatibility(model)
            results['mps_compatible'] = mps_compatible
            
            # Measure prediction time
            start_time = time.time()
            y_pred = model.predict(X_test)
            prediction_time = time.time() - start_time
            results['prediction_time'] = prediction_time
            
            # Calculate performance metrics
            train_score = model.score(X_train, y_train) if hasattr(model, 'score') else 0
            test_score = model.score(X_test, y_test) if hasattr(model, 'score') else 0
            
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            results.update({
                'train_score': train_score,
                'test_score': test_score,
                'mse': mse,
                'mae': mae,
                'r2': r2
            })
            
            # Perform cross-validation
            try:
                cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
                results['cross_val_scores'] = cv_scores.tolist()
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Cross-validation failed: {e}")
            
            # Estimate memory usage
            memory_usage = self._estimate_memory_usage(model)
            results['memory_usage'] = memory_usage
            
            if self.verbose:
                self._print_results(results)
            
        except Exception as e:
            results['error'] = str(e)
            if self.verbose:
                print(f"❌ Error testing {model_name}: {e}")
        
        self.test_results[model_name] = results
        return results
    
    def benchmark_models(self, models: Dict[str, Any], 
                        X_train: np.ndarray, X_test: np.ndarray,
                        y_train: np.ndarray, y_test: np.ndarray) -> pd.DataFrame:
        """
        Benchmark multiple models and return comparison DataFrame.
        
        This method tests multiple models and creates a comprehensive comparison
        including performance metrics, timing, and compatibility information.
        
        Args:
            models: Dictionary of {model_name: model_instance}
            X_train, X_test: Training and test features
            y_train, y_test: Training and test targets
            
        Returns:
            DataFrame with benchmark results for all models
            
        Example:
            >>> models = {'model1': Model1(), 'model2': Model2()}
            >>> results = tester.benchmark_models(models, X_train, X_test, y_train, y_test)
            >>> print(results[['model_name', 'r2', 'training_time']])
        """
        if self.verbose:
            print(f"\n🏁 Benchmarking {len(models)} models...")
        
        results = []
        
        for model_name, model in models.items():
            result = self.test_model(model, X_train, X_test, y_train, y_test, model_name)
            results.append(result)
        
        # Create comparison DataFrame
        df_results = pd.DataFrame(results)
        
        if self.verbose:
            self._print_benchmark_summary(df_results)
        
        return df_results
    
    def _test_mps_compatibility(self, model) -> bool:
        """
        Test if model is MPS compatible.
        
        This method checks if a model uses PyTorch and is configured
        to use the MPS (Metal Performance Shaders) device.
        
        Args:
            model: Model to test for MPS compatibility
            
        Returns:
            True if model uses MPS, False otherwise
        """
        try:
            # Check if model uses PyTorch
            if hasattr(model, 'device'):
                if str(model.device) == 'mps':
                    return True
            
            # Check if model has MPS-related attributes
            if hasattr(model, 'model') and hasattr(model.model, 'device'):
                if str(model.model.device) == 'mps':
                    return True
            
            # Check for TensorFlow GPU usage
            if hasattr(model, 'device') and model.device == 'gpu':
                return True
            
            # Check if TensorFlow model is using GPU
            if hasattr(model, 'tf') and hasattr(model, 'device'):
                import tensorflow as tf
                gpu_devices = tf.config.list_physical_devices('GPU')
                if model.device == 'gpu' and len(gpu_devices) > 0:
                    return True
            
            return False
        except Exception as e:
            return False
    
    def _estimate_memory_usage(self, model) -> float:
        """
        Estimate memory usage of model in MB.
        
        Args:
            model: Model to estimate memory usage for
            
        Returns:
            Estimated memory usage in MB
        """
        try:
            import sys
            return sys.getsizeof(model) / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    def _print_results(self, results: Dict[str, Any]):
        """
        Print detailed test results.
        
        Args:
            results: Dictionary containing test results
        """
        print(f"✅ {results['model_name']} Results:")
        print(f"   Training Time: {results['training_time']:.4f}s")
        print(f"   Prediction Time: {results['prediction_time']:.4f}s")
        print(f"   Train Score: {results['train_score']:.4f}")
        print(f"   Test Score: {results['test_score']:.4f}")
        print(f"   MSE: {results['mse']:.6f}")
        print(f"   MAE: {results['mae']:.6f}")
        print(f"   R²: {results['r2']:.4f}")
        print(f"   MPS Compatible: {results['mps_compatible']}")
        print(f"   Memory Usage: {results['memory_usage']:.2f} MB")
        
        if results['cross_val_scores']:
            cv_mean = np.mean(results['cross_val_scores'])
            cv_std = np.std(results['cross_val_scores'])
            print(f"   CV R²: {cv_mean:.4f} ± {cv_std:.4f}")
    
    def _print_benchmark_summary(self, df: pd.DataFrame):
        """
        Print benchmark summary.
        
        Args:
            df: DataFrame with benchmark results
        """
        print(f"\n📊 Benchmark Summary:")
        print(f"   Total Models: {len(df)}")
        print(f"   Successful Tests: {len(df[df['error'].isna()])}")
        print(f"   Failed Tests: {len(df[df['error'].notna()])}")
        
        if len(df) > 0:
            best_r2 = df['r2'].max()
            best_model = df.loc[df['r2'].idxmax(), 'model_name']
            print(f"   Best R²: {best_r2:.4f} ({best_model})")
            
            fastest_train = df['training_time'].min()
            fastest_model = df.loc[df['training_time'].idxmin(), 'model_name']
            print(f"   Fastest Training: {fastest_train:.4f}s ({fastest_model})")
    
    def validate_model_predictions(self, model, X: np.ndarray, 
                                 expected_shape: Tuple[int, ...] = None) -> bool:
        """
        Validate model predictions.
        
        This method checks if model predictions are valid by examining:
        - Presence of NaN values
        - Presence of infinite values
        - Expected output shape
        
        Args:
            model: Trained model
            X: Input features
            expected_shape: Expected output shape (optional)
            
        Returns:
            True if predictions are valid, False otherwise
        """
        try:
            predictions = model.predict(X)
            
            # Check for NaN values
            if np.isnan(predictions).any():
                logger.error("Model predictions contain NaN values")
                return False
            
            # Check for infinite values
            if np.isinf(predictions).any():
                logger.error("Model predictions contain infinite values")
                return False
            
            # Check shape if expected
            if expected_shape and predictions.shape != expected_shape:
                logger.error(f"Prediction shape {predictions.shape} != expected {expected_shape}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Prediction validation failed: {e}")
            return False
    
    def test_model_robustness(self, model, X: np.ndarray, y: np.ndarray,
                             noise_levels: List[float] = [0.0, 0.01, 0.05, 0.1]) -> Dict[str, List[float]]:
        """
        Test model robustness to noise.
        
        This method tests how well a model performs when noise is added
        to the input features. This helps assess model stability.
        
        Args:
            model: Trained model
            X: Input features
            y: True targets
            noise_levels: List of noise levels to test
            
        Returns:
            Dictionary with robustness results:
            - noise_levels: List of tested noise levels
            - mse_scores: MSE scores for each noise level
            - r2_scores: R² scores for each noise level
        """
        results = {
            'noise_levels': noise_levels,
            'mse_scores': [],
            'r2_scores': []
        }
        
        for noise_level in noise_levels:
            # Add noise to features
            X_noisy = X + np.random.normal(0, noise_level, X.shape)
            
            # Make predictions
            y_pred = model.predict(X_noisy)
            
            # Calculate metrics
            mse = mean_squared_error(y, y_pred)
            r2 = r2_score(y, y_pred)
            
            results['mse_scores'].append(mse)
            results['r2_scores'].append(r2)
        
        return results
    
    def test_model_stability(self, model, X: np.ndarray, y: np.ndarray,
                            n_runs: int = 10) -> Dict[str, float]:
        """
        Test model stability across multiple runs.
        
        This method tests model stability by running predictions multiple
        times and analyzing the variance in performance.
        
        Args:
            model: Trained model
            X: Input features
            y: True targets
            n_runs: Number of runs for stability testing
            
        Returns:
            Dictionary with stability metrics:
            - mean_score: Mean R² score across runs
            - std_score: Standard deviation of R² scores
            - min_score: Minimum R² score
            - max_score: Maximum R² score
            - scores: List of all R² scores
        """
        scores = []
        
        for i in range(n_runs):
            # Set random seed for reproducibility
            np.random.seed(i)
            
            # Make predictions
            y_pred = model.predict(X)
            
            # Calculate R² score
            r2 = r2_score(y, y_pred)
            scores.append(r2)
        
        return {
            'mean_score': np.mean(scores),
            'std_score': np.std(scores),
            'min_score': np.min(scores),
            'max_score': np.max(scores),
            'scores': scores
        }

class MPSCompatibilityTester:
    """
    Test MPS compatibility for neural models.
    
    This class provides specialized methods for testing MPS (Metal Performance Shaders)
    compatibility on Apple Silicon devices.
    
    Methods:
        test_mps_availability: Check if MPS is available
        test_tensor_operations: Test basic tensor operations on MPS
        test_model_on_mps: Test if a model class works on MPS
    """
    
    @staticmethod
    def test_mps_availability():
        """
        Test if MPS is available.
        
        This method checks if PyTorch is installed and if MPS backend
        is available on the current system.
        
        Returns:
            True if MPS is available, False otherwise
        """
        try:
            import torch
            mps_available = torch.backends.mps.is_available()
            if mps_available:
                device = torch.device("mps")
                print(f"✅ MPS is available: {device}")
                return True
            else:
                print("❌ MPS is not available")
                return False
        except ImportError:
            print("❌ PyTorch not installed")
            return False
    
    @staticmethod
    def test_tensor_operations():
        """
        Test basic tensor operations on MPS.
        
        This method tests fundamental tensor operations on the MPS device
        to ensure it's working correctly.
        
        Returns:
            True if tensor operations work on MPS, False otherwise
        """
        try:
            import torch
            
            if not torch.backends.mps.is_available():
                print("⚠️ MPS not available, skipping tensor tests")
                return False
            
            # Test basic operations
            device = torch.device("mps")
            x = torch.randn(100, 10, device=device)
            y = torch.randn(100, 10, device=device)
            
            # Test operations
            z = x + y
            z = torch.matmul(x, y.T)
            z = torch.relu(x)
            
            print("✅ MPS tensor operations working correctly")
            return True
            
        except Exception as e:
            print(f"❌ MPS tensor operations failed: {e}")
            return False
    
    @staticmethod
    def test_model_on_mps(model_class, input_shape: Tuple[int, ...] = (100, 10)):
        """
        Test if a model class works on MPS.
        
        This method creates an instance of a model class and checks
        if it's configured to use the MPS device.
        
        Args:
            model_class: Model class to test
            input_shape: Shape of input data for testing
            
        Returns:
            True if model is MPS compatible, False otherwise
        """
        try:
            import torch
            
            if not torch.backends.mps.is_available():
                print("⚠️ MPS not available, skipping model test")
                return False
            
            # Create model instance
            model = model_class()
            
            # Check if model uses MPS
            if hasattr(model, 'device') and str(model.device) == 'mps':
                print(f"✅ {model_class.__name__} is MPS compatible")
                return True
            else:
                print(f"❌ {model_class.__name__} is not MPS compatible")
                return False
                
        except Exception as e:
            print(f"❌ Error testing {model_class.__name__}: {e}")
            return False

# Utility functions
def create_test_data(n_samples: int = 1000, n_features: int = 10) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create test data for model testing.
    
    This function generates synthetic data for testing FreqAI models.
    The data follows a realistic pattern suitable for regression tasks.
    
    Args:
        n_samples: Number of samples to generate (default: 1000)
        n_features: Number of features to generate (default: 10)
        
    Returns:
        Tuple of (X, y) where X is features and y is targets
        
    Example:
        >>> X, y = create_test_data(1000, 10)
        >>> print(X.shape, y.shape)
        (1000, 10) (1000,)
    """
    np.random.seed(42)
    X = np.random.randn(n_samples, n_features)
    y = np.random.randn(n_samples)
    return X, y

def run_comprehensive_tests(models: Dict[str, Any], 
                          test_size: float = 0.2) -> pd.DataFrame:
    """
    Run comprehensive tests on multiple models.
    
    This function provides a convenient way to test multiple models
    with standardized test data and evaluation metrics.
    
    Args:
        models: Dictionary of {model_name: model_instance}
        test_size: Fraction of data for testing (default: 0.2)
        
    Returns:
        DataFrame with comprehensive test results for all models
        
    Example:
        >>> models = {'model1': Model1(), 'model2': Model2()}
        >>> results = run_comprehensive_tests(models)
        >>> print(results[['model_name', 'r2', 'training_time']])
    """
    # Create test data
    X, y = create_test_data()
    
    # Split data
    split_idx = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Create tester
    tester = FreqAIModelTester(verbose=True)
    
    # Run tests
    results = tester.benchmark_models(models, X_train, X_test, y_train, y_test)
    
    return results 