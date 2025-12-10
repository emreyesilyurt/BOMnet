import pandas as pd

from bomer.engines.cost import analyze_costs


def test_analyze_costs_basic():
    bom = pd.DataFrame(
        {
            "PartNumber": ["P1", "P2"],
            "Quantity": [10, 5],
        }
    )

    suppliers_data = {
        "currency": "USD",
        "suppliers": [
            {"name": "A", "prices": {"P1": 0.5}},
            {"name": "B", "prices": {"P1": 0.4, "P2": 1.0}},
        ],
    }

    cost_summary = analyze_costs(bom, suppliers_data, config={"cost": {"currency": "USD"}})

    # P1: qty=10, best price=0.4 => 4.0
    # P2: qty=5, price=1.0 => 5.0
    # total = 9.0
    assert cost_summary.total_cost == 9.0
    assert cost_summary.currency == "USD"
    # P2 should not be missing
    assert "P2" not in cost_summary.missing_prices
