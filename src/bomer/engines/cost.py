from typing import Any, Dict, List, Optional

import pandas as pd

from bomer.engines.models import CostLineItem, CostSummary


def _build_price_index(suppliers_data: Dict[str, Any]) -> Dict[str, float]:
    """
    Build a simple PartNumber -> UnitPrice index using the
    minimum price found across all suppliers.
    """
    index: Dict[str, float] = {}

    for supplier in suppliers_data.get("suppliers", []):
        prices = supplier.get("prices", {})
        for part, price in prices.items():
            try:
                p = float(price)
            except (TypeError, ValueError):
                continue
            if part not in index or p < index[part]:
                index[part] = p

    return index


def analyze_costs(
    bom: pd.DataFrame,
    suppliers_data: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> CostSummary:
    """
    Compute per-line and total cost from a BOM and supplier pricing.

    Returns a CostSummary dataclass with:
    - currency
    - total_cost
    - line_items (list of CostLineItem)
    - missing_prices (list of PartNumber)
    """
    if config is None:
        config = {}

    cost_cfg = config.get("cost", {})
    currency = cost_cfg.get("currency") or suppliers_data.get("currency", "USD")

    price_index = _build_price_index(suppliers_data)

    line_items: List[CostLineItem] = []
    missing_prices: List[str] = []
    total_cost = 0.0

    for _, row in bom.iterrows():
        part = str(row.get("PartNumber", "")).strip()
        try:
            qty = float(row.get("Quantity", 0))
        except (TypeError, ValueError):
            qty = 0.0

        unit_price = price_index.get(part)

        if unit_price is None:
            missing_prices.append(part)
            continue

        line_cost = qty * unit_price
        total_cost += line_cost

        line_items.append(
            CostLineItem(
                PartNumber=part,
                Quantity=qty,
                UnitPrice=unit_price,
                LineCost=line_cost,
            )
        )

    return CostSummary(
        currency=str(currency),
        total_cost=float(round(total_cost, 4)),
        line_items=line_items,
        missing_prices=missing_prices,
    )
