from typing import Any, Dict, List, Optional

import pandas as pd

from bomer.engines.models import RiskLine, RiskSummary


def _supplier_count_for_part(part: str, suppliers_data: Dict[str, Any]) -> int:
    count = 0
    for supplier in suppliers_data.get("suppliers", []):
        prices = supplier.get("prices", {})
        if part in prices:
            count += 1
    return count


def analyze_risk(
    bom: pd.DataFrame,
    suppliers_data: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> RiskSummary:
    """
    Basic risk model:

    - penalize single-sourced parts
    - penalize missing prices
    - penalize 'Obsolete' lifecycle status if present

    Returns a RiskSummary dataclass.
    """
    if config is None:
        config = {}

    risk_cfg = config.get("risk", {})
    w_single = float(risk_cfg.get("single_source_weight", 0.4))
    w_missing_price = float(risk_cfg.get("missing_price_weight", 0.3))
    w_lifecycle = float(risk_cfg.get("lifecycle_weight", 0.3))

    line_risks: List[RiskLine] = []
    total_single_source = 0
    total_missing_price = 0
    total_obsolete = 0

    for _, row in bom.iterrows():
        part = str(row.get("PartNumber", "")).strip()
        lifecycle = str(row.get("LifecycleStatus", "")).strip().lower()

        supplier_count = _supplier_count_for_part(part, suppliers_data)
        single_source = supplier_count == 1
        missing_price = supplier_count == 0
        obsolete = lifecycle in {"obsolete", "eol", "end of life"}

        if single_source:
            total_single_source += 1
        if missing_price:
            total_missing_price += 1
        if obsolete:
            total_obsolete += 1

        line_risks.append(
            RiskLine(
                PartNumber=part,
                supplier_count=supplier_count,
                single_source=single_source,
                missing_price=missing_price,
                obsolete=obsolete,
            )
        )

    n_parts = max(len(bom), 1)
    single_source_ratio = total_single_source / n_parts
    missing_price_ratio = total_missing_price / n_parts
    obsolete_ratio = total_obsolete / n_parts

    risk_score = 100 * (
        w_single * single_source_ratio
        + w_missing_price * missing_price_ratio
        + w_lifecycle * obsolete_ratio
    )

    return RiskSummary(
        risk_score=round(risk_score, 2),
        single_source_ratio=single_source_ratio,
        missing_price_ratio=missing_price_ratio,
        obsolete_ratio=obsolete_ratio,
        lines=line_risks,
    )
