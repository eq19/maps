"""
FreqAI Models Package
=====================

This package contains organized FreqAI models for different use cases:

1. Tree-based Models (CatBoost, LightGBM, XGBoost)
2. Neural Network Models (PyTorch LSTM, Transformer)
3. Traditional ML Models (Random Forest, SVM, etc.)
4. Ensemble Models (Voting, Stacking)
5. Custom Models (Strategy-specific)
6. FreqAI LSTM Models (Optimized implementations)

Each model type has its own module with utilities and base classes.
"""

import sys
import os

# Add the user_data directory to Python path
user_data_path = os.path.join(os.path.dirname(__file__), '..')
if user_data_path not in sys.path:
    sys.path.insert(0, user_data_path)

# Import base classes from FreqAI
try:
    from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
    BaseFreqAIModel = BaseRegressionModel
    # Create a simple ModelFactory class for compatibility
    class ModelFactory:
        @staticmethod
        def create_model(model_name: str, **kwargs):
            from . import get_model_class
            return get_model_class(model_name)(**kwargs)
except ImportError:
    # Fallback for when running directly
    try:
        from .base import BaseFreqAIModel, ModelFactory
    except ImportError:
        # Final fallback - create minimal base class
        class BaseFreqAIModel:
            def __init__(self, **kwargs):
                self.parameters = kwargs
                self.is_trained = False
        class ModelFactory:
            @staticmethod
            def create_model(model_name: str, **kwargs):
                raise NotImplementedError("ModelFactory not available")

# Import all model modules with error handling - using absolute imports
import sys
import os

# Add current directory to path for absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import all modules with comprehensive error handling
modules_to_import = [
    'tree_models',
    'neural_models', 
    'traditional_models',
    'custom_models',
    'freqai_lstm_models',
    'cx_smart_money_pipeline',
    'netanel_enhanced_lstm',
    'nateemma_neural_classifiers'
]

for module_name in modules_to_import:
    try:
        module = __import__(module_name)
        # Import all public attributes
        if hasattr(module, '__all__'):
            globals().update({name: getattr(module, name) for name in module.__all__})
        else:
            # Import common classes
            for attr_name in dir(module):
                if not attr_name.startswith('_'):
                    globals()[attr_name] = getattr(module, attr_name)
    except ImportError as e:
        print(f"Warning: Could not import {module_name}: {e}")
    except Exception as e:
        print(f"Warning: Error importing {module_name}: {e}")

__version__ = "1.0.0"
__author__ = "FreqAI Team"

# Model registry for easy access
MODEL_REGISTRY = {
    # Enhanced Tree-based models (avoiding conflicts with built-in)
    "EnhancedCatboostRegressor": "tree_models.EnhancedCatboostRegressor",
    "EnhancedLightGBMRegressor": "tree_models.EnhancedLightGBMRegressor", 
    "EnhancedXGBoostRegressor": "tree_models.EnhancedXGBoostRegressor",
    
    # Neural network models
    "PyTorchLSTMRegressor": "neural_models.PyTorchLSTMRegressor",
    "EnhancedPyTorchTransformerRegressor": "neural_models.EnhancedPyTorchTransformerRegressor",
    "LSTMRegressor": "neural_models.LSTMRegressor",
    
    # Traditional ML models
    "RandomForestRegressor": "traditional_models.RandomForestRegressor",
    "KNeighborsRegressor": "traditional_models.KNeighborsRegressor",
    "RidgeRegressor": "traditional_models.RidgeRegressor",
    "ExtraTreesRegressor": "traditional_models.ExtraTreesRegressor",
    
    # Ensemble models (standalone files)
    "VotingRegressor": "VotingRegressor.VotingRegressor",
    "StackingRegressor": "StackingRegressor.StackingRegressor", 
    "BlendingRegressor": "BlendingRegressor.BlendingRegressor",
    "AdvancedEnsembleRegressor": "AdvancedEnsembleRegressor.AdvancedEnsembleRegressor",
    
    # Custom models
    "SmartMoneyRegressor": "custom_models.SmartMoneyRegressor",
    "VolatilityRegressor": "custom_models.VolatilityRegressor",
    "MultiTimeframeRegressor": "custom_models.MultiTimeframeRegressor",
    
    # FreqAI LSTM Models (Optimized implementations)
    "FreqAILSTMRegressor": "freqai_lstm_models.FreqAILSTMRegressor",
    "FreqAILSTMCudaRegressor": "freqai_lstm_models.FreqAILSTMCudaRegressor",
    
    # NEW: Enhanced External Models for Better Crypto Performance
    "NetanelEnhancedLSTMRegressor": "NetanelEnhancedLSTMRegressor",
    "NateemmaNeuralClassifier": "NateemmaNeuralClassifier"
}

def get_model_class(model_name: str):
    """Get model class by name"""
    if model_name in MODEL_REGISTRY:
        module_path = MODEL_REGISTRY[model_name]
        
        # Handle standalone classes (enhanced models)
        if '.' not in module_path:
            # Direct class reference - check if it's already imported
            if model_name in globals():
                return globals()[model_name]
            else:
                # Try to import the enhanced models
                try:
                    if model_name == "NetanelEnhancedLSTMRegressor":
                        from netanel_enhanced_lstm import NetanelEnhancedLSTMRegressor
                        return NetanelEnhancedLSTMRegressor
                    elif model_name == "NateemmaNeuralClassifier":
                        from nateemma_neural_classifiers import NateemmaNeuralClassifier
                        return NateemmaNeuralClassifier
                    else:
                        raise ValueError(f"Unknown standalone model: {model_name}")
                except ImportError as e:
                    raise ValueError(f"Could not import {model_name}: {e}")
        else:
            # Handle module.class format
            module_name, class_name = module_path.split('.')
            try:
                module = __import__(module_name, fromlist=[class_name])
                return getattr(module, class_name)
            except ImportError:
                try:
                    exec(f"from {module_name} import {class_name}")
                    return locals()[class_name]
                except ImportError:
                    raise ValueError(f"Could not import {model_name} from {module_path}")
    else:
        raise ValueError(f"Model {model_name} not found in registry")

def list_available_models():
    """List all available models"""
    return list(MODEL_REGISTRY.keys())

def get_model_info(model_name: str):
    """Get detailed information about a model"""
    model_class = get_model_class(model_name)
    return {
        "name": model_name,
        "class": model_class,
        "description": getattr(model_class, "__doc__", "No description available"),
        "type": getattr(model_class, "model_type", "Unknown"),
        "parameters": getattr(model_class, "default_parameters", {})
    } 
