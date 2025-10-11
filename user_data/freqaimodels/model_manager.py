
#!/usr/bin/env python3
"""
FreqAI Model Manager
====================

Provides model management for FreqAI, including testing, benchmarking,
and MPS compatibility verification.
"""

import os
import sys
import argparse
import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

# Ensure parent directory is in path (for standalone execution)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Import core package ---
try:
    from freqaimodels import get_model_class, list_available_models
    from freqaimodels import *
    from freqaimodels.netanel_enhanced_lstm import NetanelEnhancedLSTMRegressor
    from freqaimodels.nateemma_neural_classifiers import NateemmaNeuralClassifier
except ImportError as e:
    print(f"Warning: Could not import freqaimodels package: {e}")

# --- Import utilities ---
try:
    from freqaimodels.utils.dataframe_utils import FreqAIDataFrameUtils, create_sample_data
except ImportError as e:
    print(f"Warning: Could not import dataframe_utils: {e}")
    FreqAIDataFrameUtils = None
    create_sample_data = None

try:
    from freqaimodels.utils.testing_utils import FreqAIModelTester, MPSCompatibilityTester
except ImportError as e:
    print(f"Warning: Could not import testing_utils: {e}")
    FreqAIModelTester = None
    MPSCompatibilityTester = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FreqAIModelManager:
    """
    Comprehensive model manager for FreqAI models.
    
    This class provides a unified interface for managing FreqAI models including:
    - Model creation and instantiation
    - Model testing and benchmarking
    - MPS compatibility verification
    - Model optimization with hyperparameter tuning
    - Performance analysis and comparison
    - Results storage and reporting
    
    Attributes:
        verbose (bool): Whether to print detailed output
        df_utils (FreqAIDataFrameUtils): DataFrame utilities instance
        tester (FreqAIModelTester): Model testing instance
        models (Dict): Dictionary of created model instances
        results (Dict): Dictionary of test results
    """
    
    def __init__(self, verbose: bool = True):
        """
        Initialize model manager.
        
        Args:
            verbose: Whether to print detailed output during operations
        """
        self.verbose = verbose
        self.df_utils = FreqAIDataFrameUtils()
        self.tester = FreqAIModelTester(verbose=verbose)
        self.models = {}
        self.results = {}
        
    def list_available_models(self) -> List[str]:
        """
        List all available models in the registry.
        
        Returns:
            List of model names available in the registry
        """
        return list_available_models()
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a model.
        
        Args:
            model_name: Name of the model to get info for
            
        Returns:
            Dictionary containing model information including:
            - name: Model name
            - description: Model description
            - type: Model type
            - parameters: Default parameters
            
        Raises:
            ValueError: If model is not found in registry
        """
        return get_model_info(model_name)
    
    def create_model(self, model_name: str, **kwargs) -> Any:
        """
        Create a model instance.
        
        This method creates an instance of the specified model with the given
        parameters and stores it in the internal models dictionary.
        
        Args:
            model_name: Name of the model to create
            **kwargs: Model parameters to pass to the model constructor
            
        Returns:
            Model instance if successful, None if failed
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> model = manager.create_model('CatboostRegressor', iterations=100)
        """
        try:
            model_class = get_model_class(model_name)
            model = model_class(**kwargs)
            self.models[model_name] = model
            return model
        except Exception as e:
            logger.error(f"Error creating model {model_name}: {e}")
            return None
    
    def test_single_model(self, model_name: str, **kwargs) -> Dict[str, Any]:
        """
        Test a single model with comprehensive evaluation.
        
        This method creates a model, generates test data, and performs
        a complete evaluation including performance metrics and timing.
        
        Args:
            model_name: Name of the model to test
            **kwargs: Model parameters
            
        Returns:
            Dictionary with comprehensive test results including:
            - training_time: Time taken to train
            - prediction_time: Time taken to predict
            - performance metrics (mse, mae, r2)
            - mps_compatibility: Whether model uses MPS
            - error: Error message if test failed
        """
        if self.verbose:
            print(f"\n🧪 Testing {model_name}...")
        
        # Create model
        model = self.create_model(model_name, **kwargs)
        if model is None:
            return {'error': f'Failed to create model {model_name}'}
        
        # Create test data
        X, y = self.tester.create_test_data()
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Test model
        results = self.tester.test_model(model, X_train, X_test, y_train, y_test, model_name)
        
        self.results[model_name] = results
        return results
    
    def benchmark_all_models(self, model_names: List[str] = None) -> pd.DataFrame:
        """
        Benchmark all available models.
        
        This method tests multiple models and creates a comprehensive comparison
        including performance metrics, timing, and compatibility information.
        
        Args:
            model_names: List of model names to test. If None, tests all available models
            
        Returns:
            DataFrame with benchmark results for all models
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> results = manager.benchmark_all_models()
            >>> print(results[['model_name', 'r2', 'training_time']])
        """
        if model_names is None:
            model_names = self.list_available_models()
        
        if self.verbose:
            print(f"\n🏁 Benchmarking {len(model_names)} models...")
        
        # Create models
        models = {}
        for model_name in model_names:
            try:
                model = self.create_model(model_name)
                if model is not None:
                    models[model_name] = model
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Failed to create {model_name}: {e}")
        
        # Create test data
        X, y = self.tester.create_test_data()
        
        # Split data
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Benchmark models
        results = self.tester.benchmark_models(models, X_train, X_test, y_train, y_test)
        
        return results
    
    def test_mps_compatibility(self) -> Dict[str, bool]:
        """
        Test MPS compatibility for all neural models.
        
        This method tests whether neural models are properly configured
        to use the MPS (Metal Performance Shaders) device on Apple Silicon.
        
        Returns:
            Dictionary mapping model names to MPS compatibility status
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> mps_results = manager.test_mps_compatibility()
            >>> print(mps_results)
        """
        if self.verbose:
            print("\n🔍 Testing MPS compatibility...")
        
        # Test MPS availability
        mps_available = MPSCompatibilityTester.test_mps_availability()
        
        if not mps_available:
            print("❌ MPS not available on this system")
        else:
            print("✅ MPS available on this system")
            return {}
        
        # Test tensor operations
        tensor_ops_working = MPSCompatibilityTester.test_tensor_operations()
        
        # Test neural models
        neural_models = ['PyTorchLSTMRegressor', 'PyTorchTransformerRegressor', 'LSTMRegressor']
        results = {}
        
        for model_name in neural_models:
            try:
                model_class = get_model_class(model_name)
                mps_compatible = MPSCompatibilityTester.test_model_on_mps(model_class)
                results[model_name] = mps_compatible
            except Exception as e:
                results[model_name] = False
                if self.verbose:
                    print(f"❌ Error testing {model_name}: {e}")
        
        return results
    
    def test_with_real_data(self, data_path: str = None) -> pd.DataFrame:
        """
        Test models with real financial data.
        
        This method loads or creates financial data, adds technical indicators,
        and tests all models with realistic data.
        
        Args:
            data_path: Path to data file. If None, creates sample data
            
        Returns:
            DataFrame with test results for all models
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> results = manager.test_with_real_data('data.csv')
        """
        if self.verbose:
            print("\n📊 Testing with real data...")
        
        # Load or create data
        if data_path and os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            df = create_sample_data(1000)
        
        # Add technical indicators
        df = self.df_utils.add_technical_indicators(df)
        
        # Prepare data for models
        X_train, X_test, y_train, y_test = self.df_utils.prepare_data_for_model(df)
        
        # Test all models
        model_names = self.list_available_models()
        models = {}
        
        for model_name in model_names:
            try:
                model = self.create_model(model_name)
                if model is not None:
                    models[model_name] = model
            except Exception as e:
                if self.verbose:
                    print(f"⚠️ Failed to create {model_name}: {e}")
        
        # Benchmark models
        results = self.tester.benchmark_models(models, X_train, X_test, y_train, y_test)
        
        return results
    
    def optimize_model(self, model_name: str, param_grid: Dict[str, List[Any]] = None) -> Dict[str, Any]:
        """
        Optimize model hyperparameters using grid search.
        
        This method performs hyperparameter optimization using scikit-learn's
        GridSearchCV with cross-validation.
        
        Args:
            model_name: Name of the model to optimize
            param_grid: Parameter grid for optimization. If None, uses default grid
            
        Returns:
            Dictionary with optimization results including:
            - best_params: Best parameters found
            - best_score: Best cross-validation score
            - best_model: Best model instance
            - cv_results: Full cross-validation results
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> results = manager.optimize_model('CatboostRegressor')
            >>> print(results['best_params'])
        """
        if self.verbose:
            print(f"\n🔧 Optimizing {model_name}...")
        
        try:
            from sklearn.model_selection import GridSearchCV
            
            # Create model
            model = self.create_model(model_name)
            if model is None:
                return {'error': f'Failed to create model {model_name}'}
            
            # Create test data
            X, y = self.tester.create_test_data()
            
            # Default parameter grid
            if param_grid is None:
                param_grid = self._get_default_param_grid(model_name)
            
            # Perform grid search
            grid_search = GridSearchCV(
                model, param_grid, cv=5, scoring='r2', n_jobs=-1, verbose=1
            )
            grid_search.fit(X, y)
            
            results = {
                'best_params': grid_search.best_params_,
                'best_score': grid_search.best_score_,
                'best_model': grid_search.best_estimator_,
                'cv_results': grid_search.cv_results_
            }
            
            if self.verbose:
                print(f"✅ Best parameters: {results['best_params']}")
                print(f"✅ Best score: {results['best_score']:.4f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error optimizing {model_name}: {e}")
            return {'error': str(e)}
    
    def _get_default_param_grid(self, model_name: str) -> Dict[str, List[Any]]:
        """
        Get default parameter grid for a model.
        
        This method provides sensible default parameter grids for common
        hyperparameter optimization tasks.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Dictionary mapping parameter names to lists of values to try
        """
        param_grids = {
            'CatboostRegressor': {
                'iterations': [100, 200],
                'depth': [4, 6],
                'learning_rate': [0.1, 0.3]
            },
            'LightGBMRegressor': {
                'n_estimators': [100, 200],
                'max_depth': [4, 6],
                'learning_rate': [0.1, 0.3]
            },
            'RandomForestRegressor': {
                'n_estimators': [50, 100],
                'max_depth': [5, 10],
                'min_samples_split': [2, 5]
            },
            'PyTorchLSTMRegressor': {
                'hidden_size': [32, 64],
                'num_layers': [1, 2],
                'learning_rate': [0.001, 0.01]
            }
        }
        
        return param_grids.get(model_name, {})
    
    def save_results(self, filename: str = 'model_results.csv'):
        """
        Save test results to CSV file.
        
        Args:
            filename: Name of the file to save results to
            
        Example:
            >>> manager = FreqAIModelManager()
            >>> manager.test_single_model('CatboostRegressor')
            >>> manager.save_results('results.csv')
        """
        if self.results:
            df = pd.DataFrame(list(self.results.values()))
            df.to_csv(filename, index=False)
            if self.verbose:
                print(f"✅ Results saved to {filename}")
    
    def print_summary(self):
        """
        Print summary of all results.
        
        This method provides a comprehensive summary of all test results
        including best performers, fastest models, and error analysis.
        """
        if not self.results:
            print("No results to summarize")
            return
        
        print("\n📊 Results Summary:")
        print("=" * 50)
        
        # Convert results to DataFrame
        df = pd.DataFrame(list(self.results.values()))
        
        # Print best models
        if 'r2' in df.columns:
            best_r2 = df.loc[df['r2'].idxmax()]
            print(f"🏆 Best R²: {best_r2['model_name']} ({best_r2['r2']:.4f})")
        
        if 'training_time' in df.columns:
            fastest = df.loc[df['training_time'].idxmin()]
            print(f"⚡ Fastest Training: {fastest['model_name']} ({fastest['training_time']:.4f}s)")
        
        # Print MPS compatibility
        mps_models = df[df['mps_compatible'] == True]['model_name'].tolist()
        if mps_models:
            print(f"🔧 MPS Compatible Models: {', '.join(mps_models)}")
        
        # Print failed models
        failed_models = df[df['error'].notna()]['model_name'].tolist()
        if failed_models:
            print(f"❌ Failed Models: {', '.join(failed_models)}")

def main():
    """
    Main function for command-line interface.
    
    This function provides a command-line interface for the FreqAI Model Manager
    with various actions including listing models, testing, benchmarking,
    MPS compatibility testing, and optimization.
    
    Command-line arguments:
        --action: Action to perform (list, test, benchmark, mps, optimize, real-data)
        --model: Model name for single model operations
        --verbose: Enable verbose output
        --save-results: Save results to specified file
    """
    parser = argparse.ArgumentParser(description='FreqAI Model Manager')
    parser.add_argument('--action', choices=['list', 'test', 'benchmark', 'mps', 'optimize', 'real-data'],
                       default='list', help='Action to perform')
    parser.add_argument('--model', type=str, help='Model name for single model operations')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--save-results', type=str, help='Save results to file')
    
    args = parser.parse_args()
    
    # Create model manager
    manager = FreqAIModelManager(verbose=args.verbose)
    
    if args.action == 'list':
        print("📋 Available Models:")
        print("=" * 30)
        for model_name in manager.list_available_models():
            info = manager.get_model_info(model_name)
            print(f"• {model_name}: {info['description']}")
    
    elif args.action == 'test':
        if not args.model:
            print("❌ Please specify a model with --model")
            return
        
        results = manager.test_single_model(args.model)
        if args.save_results:
            manager.save_results(args.save_results)
    
    elif args.action == 'benchmark':
        results = manager.benchmark_all_models()
        if args.save_results:
            results.to_csv(args.save_results, index=False)
            print(f"✅ Results saved to {args.save_results}")
    
    elif args.action == 'mps':
        results = manager.test_mps_compatibility()
        print("\n🔍 MPS Compatibility Results:")
        for model, compatible in results.items():
            status = "✅" if compatible else "❌"
            print(f"{status} {model}")
    
    elif args.action == 'optimize':
        if not args.model:
            print("❌ Please specify a model with --model")
            return
        
        results = manager.optimize_model(args.model)
        if 'error' in results:
            print(f"❌ Optimization failed: {results['error']}")
    
    elif args.action == 'real-data':
        results = manager.test_with_real_data()
        if args.save_results:
            results.to_csv(args.save_results, index=False)
            print(f"✅ Results saved to {args.save_results}")
    
    # Print summary
    manager.print_summary()

if __name__ == "__main__":
    main() 
