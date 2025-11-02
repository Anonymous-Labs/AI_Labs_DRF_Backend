from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd

def linear_regression(X_train: pd.DataFrame, y_train: pd.Series, fit_intercept: bool = True):
    """
    Trains a Linear Regression model on the given dataset.

    Args:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target values.
        fit_intercept (bool): Whether to fit the intercept term. Default is True.

    Returns:
        dict: Dictionary containing trained model, coefficients, intercept, and R² score.

    Raises:
        ValueError: If input data is missing, dimensions mismatch, or contains NaN values.
    """
    if X_train is None or y_train is None:
        raise ValueError("Both X_train and y_train must be provided.")

    if not isinstance(X_train, pd.DataFrame) or not isinstance(y_train, pd.Series):
        raise ValueError("X_train must be a DataFrame and y_train must be a Series.")

    if X_train.shape[0] != len(y_train):
        raise ValueError("Number of samples in X_train and y_train must match.")

    if X_train.isna().any().any() or y_train.isna().any():
        raise ValueError("Input data contains NaN values.")

    # Train the Linear Regression model
    model = LinearRegression(fit_intercept=fit_intercept)
    model.fit(X_train, y_train)

    # Prepare model info
    model_info = {
        "coefficients": dict(zip(X_train.columns, model.coef_)),
        "intercept": model.intercept_,
        "r2_score": r2_score(y_train, model.predict(X_train))
    }

    return {"model": model, "model_info": model_info}
