import pytest
from src.data_loader import load_bom_data

def test_load_bom_data():
    data = load_bom_data("data/sample_bom.csv")
    assert data is not None
    assert "Part" in data.columns
