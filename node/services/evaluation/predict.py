import pandas as pd
import numpy as np
from typing import Any, Dict

def predict(model: Any, X: pd.DataFrame) -> Dict[str, Any]:
    """
    Generates predictions using any trained scikit-learn compatible model.
    
    Args:
        model: Trained scikit-learn model (supports both regression and classification).
        X (pd.DataFrame): Feature DataFrame for prediction.
    
    Returns:
        dict: {
            'predictions': pd.Series,
            'prediction_probs': Optional[pd.DataFrame]
        }
    
    Raises:
        ValueError: If model or input data are invalid.
    """

    # ✅ Validation
    if model is None:
        raise ValueError("A trained model must be provided.")
    if X is None or not isinstance(X, pd.DataFrame):
        raise ValueError("Input X must be a pandas DataFrame.")
    if X.isna().any().any():
        raise ValueError("Input features contain NaN values.")

    # ✅ Predictions
    try:
        y_pred = model.predict(X)
    except Exception as e:
        raise ValueError(f"Model prediction failed: {e}")

    y_pred_series = pd.Series(y_pred, name="Predictions")

    # ✅ If classification model supports probabilities
    y_prob = None
    if hasattr(model, "predict_proba"):
        try:
            probs = model.predict_proba(X)
            y_prob = pd.DataFrame(probs, columns=[f"Class_{i}" for i in range(probs.shape[1])])
        except Exception:
            y_prob = None

    return {
        "predictions": y_pred_series,
        "prediction_probs": y_prob
    }
