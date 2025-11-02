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
            - feature_stats: Dictionary with feature statistics

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

    # Compute feature statistics
    feature_stats = {
        "n_features": len(X.columns),
        "missing_values": X.isna().sum().to_dict(),
        "constant_features": [],
        "high_correlation_pairs": []
    }

    # Identify constant features
    for col in X.columns:
        if X[col].nunique() == 1:
            feature_stats["constant_features"].append(col)

    # Identify highly correlated feature pairs (numeric only)
    numeric_X = X.select_dtypes(include=[np.number])
    if len(numeric_X.columns) > 1:
        corr_matrix = numeric_X.corr()
        high_corr = np.where(np.abs(corr_matrix) > 0.95)
        high_corr_pairs = [
            (numeric_X.columns[i], numeric_X.columns[j])
            for i, j in zip(*high_corr)
            if i != j and i < j
        ]
        feature_stats["high_correlation_pairs"] = high_corr_pairs

    return {"X": X, "y": y, "feature_stats": feature_stats}
