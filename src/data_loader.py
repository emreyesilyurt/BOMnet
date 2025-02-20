import pandas as pd

def load_bom_data(file_path):
    """Loads BOM data from CSV."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading BOM data: {e}")
        return None
