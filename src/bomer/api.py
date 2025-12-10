from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from bomer.core.config import load_config
from bomer.core.loader import load_bom, load_suppliers
from bomer.core.schema import normalize_bom_columns, validate_bom
from bomer.engines.cost import analyze_costs
from bomer.engines.optimizer import optimize_bom
from bomer.engines.risk import analyze_risk


def run_analysis(
    bom_path: Path,
    suppliers_path: Optional[Path] = None,
    config_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    High-level analysis pipeline.

    - Loads config (bomer.yaml or given path)
    - Loads BOM and suppliers
    - Normalizes and validates the BOM
    - Optimizes BOM (aggregation)
    - Runs cost and risk analysis

    Returns a dictionary with:
      - normalized_bom: pd.DataFrame
      - optimized_bom: pd.DataFrame
      - issues: list[dict]
      - cost_summary: CostSummary
      - risk_summary: RiskSummary
      - config: dict
      - bom_path: Path
      - suppliers_path: Path
    """
    # 1) Load config
    cfg_path_str = str(config_path) if config_path is not None else None
    config = load_config(cfg_path_str)

    # 2) Load BOM
    bom_df = load_bom(bom_path)

    # 3) Normalize columns (passing config in case of schema.aliases)
    normalized_bom = normalize_bom_columns(bom_df, config=config)

    # 4) Validate
    issues = validate_bom(normalized_bom)

    # 5) Resolve suppliers path if not given
    if suppliers_path is None:
        suppliers_cfg = config.get("suppliers", {})
        suppliers_path_str = suppliers_cfg.get("path", "data/suppliers.json")
        suppliers_path = Path(suppliers_path_str)

    # 6) Load suppliers
    suppliers_data = load_suppliers(suppliers_path)

    # 7) Optimize BOM
    optimized_bom = optimize_bom(normalized_bom)

    # 8) Analyze cost and risk
    cost_summary = analyze_costs(optimized_bom, suppliers_data, config=config)
    risk_summary = analyze_risk(optimized_bom, suppliers_data, config=config)

    return {
        "normalized_bom": normalized_bom,
        "optimized_bom": optimized_bom,
        "issues": issues,
        "cost_summary": cost_summary,
        "risk_summary": risk_summary,
        "config": config,
        "bom_path": bom_path,
        "suppliers_path": suppliers_path,
    }
