import pandas as pd
from sklearn.model_selection import train_test_split

def train_test_split(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2):
    """
    Splits dataset into training and testing sets and computes split statistics.

    Args:
        X (pd.DataFrame): Feature DataFrame.
        y (pd.Series): Target Series.
        test_size (float): Proportion of dataset for testing. Default is 0.2.

    Returns:
        dict: Dictionary containing X_train, X_test, y_train, y_test

    Raises:
        ValueError: If inputs are invalid or contain NaN values.
    """
    if X is None or y is None:
        raise ValueError("Both X and y must be provided.")
    if not isinstance(X, pd.DataFrame) or not isinstance(y, pd.Series):
        raise ValueError("X must be a DataFrame and y must be a Series.")
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    if X.isna().any().any() or y.isna().any():
        raise ValueError("Input data contains NaN values.")
    if len(X) != len(y):
        raise ValueError("Number of samples in X and y must match.")

    # Perform train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test
    }
