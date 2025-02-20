import pytest
import pandas as pd
from src.llm_optimizer import optimize_bom

def test_optimize_bom():
    sample_data = pd.DataFrame({"Part": ["Resistor"], "Quantity": [10]})
    optimized = optimize_bom(sample_data)
    assert "Optimized" in optimized.columns
