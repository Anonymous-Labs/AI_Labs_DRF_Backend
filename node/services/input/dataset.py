import pandas as pd
import os

def dataset(file_path: str) -> dict:
    """
    Uploads and validates a CSV dataset file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: The loaded dataset
    
    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If the file is not a valid CSV or cannot be read.
    """
    
    # ✅ Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # ✅ Validate file extension
    if not file_path.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported.")
    
    # ✅ Read CSV file safely
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")
    
    return df
