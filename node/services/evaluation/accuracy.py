import numpy as np
import pandas as pd
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error,
    accuracy_score, precision_score, recall_score, f1_score
)

def accuracy_metric(y_true: pd.Series, y_pred: pd.Series, metric_type: str):
    """
    Calculates a specific evaluation metric based on metric_type.

    Args:
        y_true (pd.Series): True values.
        y_pred (pd.Series): Predicted values.
        metric_type (str): Type of metric to calculate. 
                           Options: ['r2', 'mse', 'rmse', 'mae', 
                                     'accuracy', 'precision', 'recall', 'f1']

    Returns:
        float: Computed metric value.

    Raises:
        ValueError: If inputs are invalid or metric_type is unsupported.
    """

    if y_true is None or y_pred is None:
        raise ValueError("Both y_true and y_pred must be provided.")
    if not isinstance(y_true, pd.Series) or not isinstance(y_pred, pd.Series):
        raise ValueError("Both y_true and y_pred must be pandas Series.")
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length.")
    if y_true.isna().any() or y_pred.isna().any():
        raise ValueError("Input data contains NaN values.")

    metric_type = metric_type.lower()

    if metric_type == "r2":
        return r2_score(y_true, y_pred)
    elif metric_type == "mse":
        return mean_squared_error(y_true, y_pred)
    elif metric_type == "rmse":
        return np.sqrt(mean_squared_error(y_true, y_pred))
    elif metric_type == "mae":
        return mean_absolute_error(y_true, y_pred)

    else:
        raise ValueError(f"Unsupported metric type: {metric_type}")
