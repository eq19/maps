"""
Example Usage for NetanelEnhancedLSTMRegressorV2
Demonstrates all the enhanced features and capabilities
"""

import numpy as np
import pandas as pd
from netanel_enhanced_lstm_v2 import NetanelEnhancedLSTMRegressorV2, create_ensemble_model
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sample_crypto_data(n_samples=1000):
    """Generate sample crypto trading data for demonstration"""
    np.random.seed(42)
    
    # Base price movement
    price_changes = np.random.randn(n_samples) * 0.02
    prices = 50000 * np.exp(np.cumsum(price_changes))
    
    # Technical indicators
    data = {
        'close': prices,
        'ma': pd.Series(prices).rolling(window=20).mean().fillna(method='bfill'),
        'rsi': 50 + 25 * np.sin(np.linspace(0, 4*np.pi, n_samples)) + np.random.randn(n_samples) * 5,
        'macd': np.random.randn(n_samples) * 0.1,
        'bb_upperband': prices * 1.02,
        'bb_lowerband': prices * 0.98,
        'bb_middleband': prices,
        'atr': np.abs(np.random.randn(n_samples) * 0.01 * prices),
        'volume': np.random.exponential(1000000, n_samples),
    }
    
    # Normalized indicators
    for indicator in ['ma', 'rsi', 'macd', 'atr']:
        if indicator in data:
            values = np.array(data[indicator])
            normalized = (values - np.mean(values)) / (np.std(values) + 1e-8)
            data[f'normalized_{indicator}'] = normalized
    
    # Additional normalized indicators
    for indicator in ['roc', 'cci', 'momentum', 'stoch', 'bb_width']:
        data[f'normalized_{indicator}'] = np.random.randn(n_samples) * 0.5
    
    df = pd.DataFrame(data)
    
    # Target: next period return
    target = df['close'].pct_change().shift(-1).fillna(0)
    
    return df, target

def example_basic_usage():
    """Basic usage example"""
    logger.info("=== Basic Usage Example ===")
    
    # Generate sample data
    X, y = generate_sample_crypto_data(1000)
    
    # Create model with default parameters
    model = NetanelEnhancedLSTMRegressorV2(
        epochs=50,  # Reduced for demo
        plot_training=True
    )
    
    # Train model
    model.fit(X, y)
    
    # Make predictions
    predictions = model.predict(X[:100])
    logger.info(f"Predictions shape: {predictions.shape}")
    
    # Save model
    save_path = model.save_model()
    logger.info(f"Model saved to: {save_path}")
    
    # Load model
    new_model = NetanelEnhancedLSTMRegressorV2()
    new_model.load_model(save_path)
    logger.info("Model loaded successfully")
    
    return model

def example_uncertainty_estimation():
    """Example with uncertainty estimation"""
    logger.info("=== Uncertainty Estimation Example ===")
    
    X, y = generate_sample_crypto_data(500)
    
    # Create model with uncertainty estimation
    model = NetanelEnhancedLSTMRegressorV2(
        uncertainty_estimation=True,
        epochs=30,
        plot_training=True
    )
    
    model.fit(X, y)
    
    # Get predictions with uncertainty
    result = model.predict(X[:50], return_uncertainty=True)
    
    if isinstance(result, dict):
        predictions = result['mean']
        uncertainties = result['std']
        
        logger.info(f"Predictions: {predictions[:5]}")
        logger.info(f"Uncertainties: {uncertainties[:5]}")
        
        # Calculate confidence intervals
        lower_bound = predictions - 1.96 * uncertainties
        upper_bound = predictions + 1.96 * uncertainties
        
        logger.info("95% Confidence Intervals (first 5):")
        for i in range(5):
            logger.info(f"  Pred {i}: {predictions[i]:.4f} [{lower_bound[i]:.4f}, {upper_bound[i]:.4f}]")
    
    return model

def example_ensemble_model():
    """Example with ensemble modeling"""
    logger.info("=== Ensemble Model Example ===")
    
    X, y = generate_sample_crypto_data(400)
    
    # Create ensemble model
    ensemble_model = create_ensemble_model(
        n_models=3,  # Small ensemble for demo
        epochs=20,
        plot_training=False  # Disable plotting for ensemble
    )
    
    ensemble_model.fit(X, y)
    
    # Get ensemble predictions with uncertainty
    result = ensemble_model.predict(X[:30], return_uncertainty=True)
    
    if isinstance(result, dict):
        logger.info(f"Ensemble predictions (first 5): {result['mean'][:5]}")
        logger.info(f"Ensemble uncertainties (first 5): {result['std'][:5]}")
    
    return ensemble_model

def example_advanced_features():
    """Example showcasing advanced features"""
    logger.info("=== Advanced Features Example ===")
    
    X, y = generate_sample_crypto_data(600)
    
    # Create model with all advanced features
    model = NetanelEnhancedLSTMRegressorV2(
        hidden_dim=256,
        num_lstm_layers=4,
        use_attention=True,
        attention_heads=8,
        uncertainty_estimation=True,
        mixed_precision=True,
        epochs=40,
        plot_training=True,
        calculate_shap=True  # Enable explainability
    )
    
    model.fit(X, y)
    
    # Get model information
    info = model.get_model_info()
    logger.info("Model Information:")
    logger.info(f"  Model trained: {info['model_trained']}")
    logger.info(f"  Final validation R²: {info.get('final_metrics', {}).get('validation_r2', 'N/A')}")
    logger.info(f"  Final hit rate: {info.get('final_metrics', {}).get('validation_hit_rate', 'N/A')}")
    
    # Feature importance (if SHAP is available)
    if info.get('explainability_available', False):
        try:
            importance = model.get_feature_importance(X[:100])
            if importance:
                logger.info("Feature importance calculated successfully")
                # Plot feature importance
                model.plot_feature_importance(X[:50])
        except Exception as e:
            logger.warning(f"Could not calculate feature importance: {e}")
    
    return model

def example_trading_metrics():
    """Example focusing on trading-specific metrics"""
    logger.info("=== Trading Metrics Example ===")
    
    from netanel_enhanced_lstm_v2 import TradingMetrics
    
    # Generate sample returns
    np.random.seed(42)
    returns = np.random.randn(252) * 0.02  # Daily returns for 1 year
    
    # Calculate trading metrics
    hit_rate = TradingMetrics.calculate_hit_rate(returns[1:], returns[:-1])
    sharpe_ratio = TradingMetrics.calculate_sharpe_ratio(returns)
    max_drawdown = TradingMetrics.calculate_max_drawdown(np.cumsum(returns))
    profit_factor = TradingMetrics.calculate_profit_factor(returns)
    
    logger.info("Trading Metrics:")
    logger.info(f"  Hit Rate: {hit_rate:.4f}")
    logger.info(f"  Sharpe Ratio: {sharpe_ratio:.4f}")
    logger.info(f"  Max Drawdown: {max_drawdown:.4f}")
    logger.info(f"  Profit Factor: {profit_factor:.4f}")

def example_hyperparameter_suggestions():
    """Example of hyperparameter optimization setup"""
    logger.info("=== Hyperparameter Optimization Setup ===")
    
    try:
        import optuna
        from netanel_enhanced_lstm_v2 import suggest_hyperparameters_optuna
        
        def objective(trial):
            # Get suggested hyperparameters
            params = suggest_hyperparameters_optuna(trial)
            
            # Generate data
            X, y = generate_sample_crypto_data(300)
            
            # Create and train model
            model = NetanelEnhancedLSTMRegressorV2(
                epochs=20,  # Reduced for optimization
                plot_training=False,
                **params
            )
            
            model.fit(X, y)
            
            # Return validation R² as optimization target
            if model.training_history:
                return model.training_history[-1].get('val_r2', 0)
            return 0
        
        # Create study
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=3)  # Small number for demo
        
        logger.info("Best hyperparameters:")
        for key, value in study.best_params.items():
            logger.info(f"  {key}: {value}")
        logger.info(f"Best validation R²: {study.best_value:.4f}")
        
    except ImportError:
        logger.info("Optuna not available. Install with: pip install optuna")
        logger.info("Suggested hyperparameters for manual tuning:")
        logger.info("  hidden_dim: [64, 128, 256, 512]")
        logger.info("  num_lstm_layers: [2, 3, 4, 5]")
        logger.info("  dropout_percent: [0.1, 0.3, 0.5, 0.7]")
        logger.info("  learning_rate: [1e-5, 1e-4, 1e-3, 1e-2]")

def main():
    """Run all examples"""
    logger.info("Starting NetanelEnhancedLSTMRegressorV2 Examples")
    logger.info("=" * 60)
    
    try:
        # Basic usage
        basic_model = example_basic_usage()
        
        # Uncertainty estimation
        uncertainty_model = example_uncertainty_estimation()
        
        # Ensemble modeling
        ensemble_model = example_ensemble_model()
        
        # Advanced features
        advanced_model = example_advanced_features()
        
        # Trading metrics
        example_trading_metrics()
        
        # Hyperparameter optimization
        example_hyperparameter_suggestions()
        
        logger.info("=" * 60)
        logger.info("All examples completed successfully!")
        
        # Compare models
        logger.info("\n=== Model Comparison ===")
        models = {
            'Basic': basic_model,
            'Uncertainty': uncertainty_model,
            'Advanced': advanced_model
        }
        
        for name, model in models.items():
            if model.training_history:
                final_r2 = model.training_history[-1].get('val_r2', 0)
                final_hit_rate = model.training_history[-1].get('val_hit_rate', 0)
                logger.info(f"{name} Model - R²: {final_r2:.4f}, Hit Rate: {final_hit_rate:.4f}")
        
        logger.info(f"Ensemble Model - Active: {ensemble_model.ensemble_size > 1}")
        
    except Exception as e:
        logger.error(f"Example execution failed: {e}")
        raise

if __name__ == "__main__":
    main()