"""
Validation Utilities for FreqAI Models
=====================================

This module provides utilities for input/output validation, data quality checks,
and model health checks for all FreqAI models.
"""

import numpy as np
from typing import Optional, Tuple, Dict, Any


def validate_input(X: np.ndarray, y: Optional[np.ndarray] = None) -> None:
    """
    Validate input features and targets.
    Raises ValueError if validation fails.
    """
    if not isinstance(X, np.ndarray):
        raise ValueError("X must be a numpy array")
    if X.ndim != 2:
        raise ValueError("X must be 2-dimensional")
    if np.any(np.isnan(X)):
        raise ValueError("X contains NaN values")
    if np.any(np.isinf(X)):
        raise ValueError("X contains infinite values")
    if y is not None:
        if not isinstance(y, np.ndarray):
            raise ValueError("y must be a numpy array")
        if len(X) != len(y):
            raise ValueError("X and y must have the same number of samples")
        if np.any(np.isnan(y)):
            raise ValueError("y contains NaN values")
        if np.any(np.isinf(y)):
            raise ValueError("y contains infinite values")


def validate_output(y_pred: np.ndarray, expected_shape: Optional[Tuple[int, ...]] = None) -> None:
    """
    Validate model output predictions.
    Raises ValueError if validation fails.
    """
    if not isinstance(y_pred, np.ndarray):
        raise ValueError("Predictions must be a numpy array")
    if np.any(np.isnan(y_pred)):
        raise ValueError("Predictions contain NaN values")
    if np.any(np.isinf(y_pred)):
        raise ValueError("Predictions contain infinite values")
    if expected_shape is not None and y_pred.shape != expected_shape:
        raise ValueError(f"Predictions shape {y_pred.shape} does not match expected {expected_shape}")


def data_quality_report(X: np.ndarray, y: Optional[np.ndarray] = None) -> Dict[str, Any]:
    """
    Generate a data quality report for features and targets.
    Returns a dictionary with quality metrics.
    """
    report = {
        "X_shape": X.shape,
        "X_nan_count": int(np.isnan(X).sum()),
        "X_inf_count": int(np.isinf(X).sum()),
        "X_min": float(np.nanmin(X)),
        "X_max": float(np.nanmax(X)),
        "X_mean": float(np.nanmean(X)),
    }
    if y is not None:
        report.update({
            "y_shape": y.shape,
            "y_nan_count": int(np.isnan(y).sum()),
            "y_inf_count": int(np.isinf(y).sum()),
            "y_min": float(np.nanmin(y)),
            "y_max": float(np.nanmax(y)),
            "y_mean": float(np.nanmean(y)),
        })
    return report


def model_health_check(model) -> Dict[str, Any]:
    """
    Perform a health check on a trained model.
    Returns a dictionary with health metrics.
    """
    health = {
        "is_trained": getattr(model, 'is_trained', False),
        "has_parameters": hasattr(model, 'parameters'),
        "has_feature_names": hasattr(model, 'feature_names'),
        "model_type": getattr(model, 'model_type', None),
    }
    return health 