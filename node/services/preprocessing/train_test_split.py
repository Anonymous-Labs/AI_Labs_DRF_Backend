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
        dict: Dictionary containing:
            - X_train, X_test, y_train, y_test
            - split_info: Dictionary with statistics and details of the split.

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

    # Compute split statistics
    split_info = {
        "train_size": len(X_train),
        "test_size": len(X_test),
        "train_ratio": len(X_train) / (len(X_train) + len(X_test)),
        "n_features": X.shape[1],
        "feature_names": X.columns.tolist(),
        "parameters": {"test_size": test_size}
    }

    # Add target distribution stats
    if y_train.dtype in ['object', 'category'] or y_train.nunique() < 10:
        split_info["train_target_distribution"] = y_train.value_counts(normalize=True).to_dict()
        split_info["test_target_distribution"] = y_test.value_counts(normalize=True).to_dict()
    else:
        split_info["train_target_stats"] = {
            "mean": float(y_train.mean()),
            "std": float(y_train.std()),
            "min": float(y_train.min()),
            "max": float(y_train.max())
        }
        split_info["test_target_stats"] = {
            "mean": float(y_test.mean()),
            "std": float(y_test.std()),
            "min": float(y_test.min()),
            "max": float(y_test.max())
        }

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "split_info": split_info
    }
