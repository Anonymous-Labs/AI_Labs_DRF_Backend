import pandas as pd
import numpy as np

def feature_selection(dataframe: pd.DataFrame, target_column: str, feature_columns: list):
    """
    Selects features and target column from a DataFrame and computes feature statistics.

    Args:
        dataframe (pd.DataFrame): Input dataset containing all columns.
        target_column (str): Name of the target variable column.
        feature_columns (list): List of feature column names to select.

    Returns:
        dict: Dictionary containing:
            - X: DataFrame with selected feature columns
            - y: Series with target values

    Raises:
        ValueError: If required columns are missing or inputs are invalid.
    """
    if dataframe is None:
        raise ValueError("A valid dataframe must be provided.")
    if not isinstance(dataframe, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    if not isinstance(feature_columns, list) or not feature_columns:
        raise ValueError("feature_columns must be a non-empty list.")
    if target_column not in dataframe.columns:
        raise ValueError(f"Target column '{target_column}' not found in DataFrame.")

    missing_features = [col for col in feature_columns if col not in dataframe.columns]
    if missing_features:
        raise ValueError(f"Missing feature columns: {missing_features}")

    X = dataframe[feature_columns]
    y = dataframe[target_column]

    return {"X": X, "y": y}
