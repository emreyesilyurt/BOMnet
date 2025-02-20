import pytest
import pandas as pd
from src.cost_analysis import analyze_costs

def test_analyze_costs():
    sample_data = pd.DataFrame({"Part": ["Resistor"], "Quantity": [10]})
    suppliers = {"Suppliers": [{"name": "Supplier A", "parts": ["Resistor"], "price": {"Resistor": 0.02}}]}
    cost = analyze_costs(sample_data, suppliers)
    assert "total_cost" in cost
