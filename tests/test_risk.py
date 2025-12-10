import pandas as pd

from bomer.engines.risk import analyze_risk


def test_analyze_risk_basic():
    bom = pd.DataFrame(
        {
            "PartNumber": ["P1", "P2", "P3"],
            "LifecycleStatus": ["Active", "Obsolete", ""],
        }
    )

    suppliers_data = {
        "suppliers": [
            {"name": "A", "prices": {"P1": 0.5}},
            {"name": "B", "prices": {"P1": 0.4, "P2": 1.0}},
        ]
    }

    risk_summary = analyze_risk(
        bom,
        suppliers_data,
        config={"risk": {"single_source_weight": 0.4, "missing_price_weight": 0.3, "lifecycle_weight": 0.3}},
    )

    assert 0.0 <= risk_summary.risk_score <= 100.0
    # P2 has a supplier, P3 has no price -> at least one missing_price
    assert any(line.missing_price for line in risk_summary.lines)
    # P2 is obsolete
    assert any(line.obsolete and line.PartNumber == "P2" for line in risk_summary.lines)
