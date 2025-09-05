"""
Logging Utilities for FreqAI Models
==================================

This module provides comprehensive logging functionality for all FreqAI models,
including log levels, rotation, performance tracking, and error handling.
"""

import logging
import logging.handlers
import os
import time
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from functools import wraps
import numpy as np


class FreqAILogger:
    """
    Comprehensive logger for FreqAI models with multiple log levels,
    rotation, and performance tracking.
    """
    
    def __init__(self, name: str, log_dir: str = "logs/ml_models", 
                 max_bytes: int = 10 * 1024 * 1024,  # 10MB
                 backup_count: int = 5):
        """
        Initialize the FreqAI logger.
        
        Args:
            name: Logger name (usually model class name)
            log_dir: Directory to store log files
            max_bytes: Maximum size of log file before rotation
            backup_count: Number of backup files to keep
        """
        self.name = name
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count
        
        # Create log directory
        os.makedirs(log_dir, exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(f"freqai.{name}")
        self.logger.setLevel(logging.DEBUG)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Console handler (INFO level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for all levels
        log_file = os.path.join(log_dir, f"{name.lower()}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_file = os.path.join(log_dir, f"{name.lower()}_errors.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_file, maxBytes=max_bytes, backupCount=backup_count
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(error_handler)
        
        # Performance file handler
        perf_file = os.path.join(log_dir, f"{name.lower()}_performance.log")
        perf_handler = logging.handlers.RotatingFileHandler(
            perf_file, maxBytes=max_bytes, backupCount=backup_count
        )
        perf_handler.setLevel(logging.INFO)
        perf_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(perf_handler)
        
        self.logger.info(f"FreqAI Logger initialized for {name}")
    
    def debug(self, message: str) -> None:
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log info message"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = True) -> None:
        """Log error message with optional exception info"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = True) -> None:
        """Log critical error message"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_performance(self, operation: str, duration: float, 
                       data_shape: Optional[tuple] = None, 
                       additional_info: Optional[Dict[str, Any]] = None) -> None:
        """
        Log performance metrics.
        
        Args:
            operation: Name of the operation (e.g., 'training', 'prediction')
            duration: Duration in seconds
            data_shape: Shape of input data
            additional_info: Additional performance metrics
        """
        message = f"PERFORMANCE - {operation}: {duration:.4f}s"
        if data_shape:
            message += f" | Data shape: {data_shape}"
        if additional_info:
            message += f" | Additional: {additional_info}"
        
        self.logger.info(message)
    
    def log_model_info(self, model_info: Dict[str, Any]) -> None:
        """Log model information"""
        self.logger.info(f"MODEL INFO - {model_info}")
    
    def log_data_validation(self, X_shape: tuple, y_shape: Optional[tuple] = None,
                           validation_result: str = "PASSED") -> None:
        """Log data validation results"""
        message = f"DATA VALIDATION - X shape: {X_shape}"
        if y_shape:
            message += f", y shape: {y_shape}"
        message += f" | Status: {validation_result}"
        self.logger.info(message)
    
    def log_training_start(self, X_shape: tuple, y_shape: tuple, 
                          parameters: Dict[str, Any]) -> None:
        """Log training start information"""
        self.logger.info(f"TRAINING START - X: {X_shape}, y: {y_shape}, params: {parameters}")
    
    def log_training_end(self, duration: float, final_metrics: Optional[Dict[str, float]] = None) -> None:
        """Log training completion"""
        message = f"TRAINING END - Duration: {duration:.4f}s"
        if final_metrics:
            message += f" | Metrics: {final_metrics}"
        self.logger.info(message)
    
    def log_prediction_start(self, X_shape: tuple) -> None:
        """Log prediction start"""
        self.logger.info(f"PREDICTION START - X shape: {X_shape}")
    
    def log_prediction_end(self, duration: float, predictions_shape: tuple) -> None:
        """Log prediction completion"""
        self.logger.info(f"PREDICTION END - Duration: {duration:.4f}s, Output shape: {predictions_shape}")
    
    def log_error(self, error: Exception, context: str = "") -> None:
        """Log error with full stack trace"""
        error_msg = f"ERROR in {context}: {str(error)}"
        self.logger.error(error_msg, exc_info=True)
    
    def log_memory_usage(self, memory_mb: float, operation: str = "") -> None:
        """Log memory usage"""
        self.logger.info(f"MEMORY USAGE - {operation}: {memory_mb:.2f} MB")


def performance_logger(operation: str):
    """
    Decorator to log performance metrics for model operations.
    
    Args:
        operation: Name of the operation to log
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get logger from model instance
            logger = getattr(self, 'logger', None)
            if logger is None:
                # Create logger if it doesn't exist
                logger = FreqAILogger(self.__class__.__name__)
                self.logger = logger
            
            # Log start
            start_time = time.time()
            logger.info(f"Starting {operation}")
            
            try:
                # Execute function
                result = func(self, *args, **kwargs)
                
                # Log success
                duration = time.time() - start_time
                logger.log_performance(operation, duration)
                
                return result
                
            except Exception as e:
                # Log error
                duration = time.time() - start_time
                logger.log_error(e, f"{operation} failed after {duration:.4f}s")
                raise
                
        return wrapper
    return decorator


def error_handler(logger: FreqAILogger):
    """
    Decorator to handle errors with comprehensive logging.
    
    Args:
        logger: FreqAI logger instance
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log_error(e, f"Error in {func.__name__}")
                raise
        return wrapper
    return decorator


class LoggingMixin:
    """
    Mixin to add comprehensive logging to any model class.
    """
    
    def _setup_logging(self) -> None:
        """Setup logging for the model"""
        if not hasattr(self, 'logger'):
            self.logger = FreqAILogger(self.__class__.__name__)
    
    def _log_data_validation(self, X: np.ndarray, y: Optional[np.ndarray] = None) -> None:
        """Log data validation"""
        self._setup_logging()
        self.logger.log_data_validation(X.shape, y.shape if y is not None else None)
    
    def _log_training_start(self, X: np.ndarray, y: np.ndarray) -> None:
        """Log training start"""
        self._setup_logging()
        self.logger.log_training_start(X.shape, y.shape, self.parameters)
    
    def _log_training_end(self, duration: float, metrics: Optional[Dict[str, float]] = None) -> None:
        """Log training end"""
        self._setup_logging()
        self.logger.log_training_end(duration, metrics)
    
    def _log_prediction_start(self, X: np.ndarray) -> None:
        """Log prediction start"""
        self._setup_logging()
        self.logger.log_prediction_start(X.shape)
    
    def _log_prediction_end(self, duration: float, predictions: np.ndarray) -> None:
        """Log prediction end"""
        self._setup_logging()
        self.logger.log_prediction_end(duration, predictions.shape)
    
    def _log_error(self, error: Exception, context: str = "") -> None:
        """Log error"""
        self._setup_logging()
        self.logger.log_error(error, context)
    
    def _log_memory_usage(self, memory_mb: float, operation: str = "") -> None:
        """Log memory usage"""
        self._setup_logging()
        self.logger.log_memory_usage(memory_mb, operation)


def get_memory_usage() -> float:
    """
    Get current memory usage in MB.
    
    Returns:
        Memory usage in MB
    """
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    except ImportError:
        return 0.0  # Return 0 if psutil not available


def log_model_operation(operation: str):
    """
    Decorator to log model operations with timing and error handling.
    
    Args:
        operation: Name of the operation
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Setup logging
            if not hasattr(self, 'logger'):
                self.logger = FreqAILogger(self.__class__.__name__)
            
            start_time = time.time()
            start_memory = get_memory_usage()
            
            try:
                # Log operation start
                if operation == "fit":
                    self._log_training_start(args[0], args[1])
                elif operation == "predict":
                    self._log_prediction_start(args[0])
                
                # Execute function
                result = func(self, *args, **kwargs)
                
                # Calculate metrics
                duration = time.time() - start_time
                end_memory = get_memory_usage()
                memory_delta = end_memory - start_memory
                
                # Log operation end
                if operation == "fit":
                    self._log_training_end(duration)
                elif operation == "predict":
                    self._log_prediction_end(duration, result)
                
                # Log performance
                self.logger.log_performance(
                    operation, duration,
                    data_shape=args[0].shape if args else None,
                    additional_info={"memory_delta_mb": memory_delta}
                )
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                self._log_error(e, f"{operation} failed after {duration:.4f}s")
                raise
                
        return wrapper
    return decorator 