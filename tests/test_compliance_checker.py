import pytest
import pandas as pd
from src.compliance_checker import check_compliance

def test_check_compliance():
    sample_data = pd.DataFrame({"Part": ["Resistor"], "Quantity": [10]})
    compliance = check_compliance(sample_data)
    assert "compliant" in compliance
