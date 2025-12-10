from typing import Any, Dict, List, Optional

import pandas as pd


def _build_price_index(suppliers_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Build a simple part_number -> unit_price index across all suppliers.

    Expected supplier JSON structure (example):

    {
      "currency": "USD",
      "suppliers": [
        {
          "name": "SupplierA",
          "prices": {
            "RES-10K-1%": 0.01,
            "CAP-100NF-50V": 0.02
          }
        },
        ...
      ]
    }
    """
    index: Dict[str, float] = {}
    for supplier in suppliers_data.get("suppliers", []):
        prices = supplier.get("prices", {})
        for part_number, price in prices.items():
            # First one wins; later we could support multiple or min price.
            index.setdefault(part_number, float(price))
    return index


def analyze_costs(bom: pd.DataFrame, suppliers_data: Dict[str, Any]) -> Dict[str, Any]:
    price_index = _build_price_index(suppliers_data)
    currency = suppliers_data.get("currency", "USD")

    line_items: List[Dict[str, Any]] = []
    total_cost = 0.0
    missing_prices: List[str] = []

    for _, row in bom.iterrows():
        part = str(row.get("PartNumber", "")).strip()
        qty = float(row.get("Quantity", 0))
        unit_price: Optional[float] = price_index.get(part)
        line_cost: Optional[float] = None

        if unit_price is not None:
            line_cost = qty * unit_price
            total_cost += line_cost
        else:
            missing_prices.append(part)

        line_items.append(
            {
                "PartNumber": part,
                "Quantity": qty,
                "UnitPrice": unit_price,
                "LineCost": line_cost,
            }
        )

    return {
        "currency": currency,
        "total_cost": round(total_cost, 4),
        "line_items": line_items,
        "missing_prices": sorted(set(missing_prices)),
    }
