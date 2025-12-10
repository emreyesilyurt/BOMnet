# src/bomer/api.py
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from bomer.core.config import load_config
from bomer.core.loader import load_bom, load_suppliers
from bomer.core.schema import normalize_bom_columns, validate_bom
from bomer.engines.cost import analyze_costs
from bomer.engines.optimizer import optimize_bom
from bomer.engines.risk import analyze_risk

def run_analysis(
    bom_path: Path,
    suppliers_path: Path,
    config_path: Path | None = None,
) -> Dict[str, Any]:
    config = load_config(str(config_path) if config_path else None)
    bom_df = load_bom(bom_path)
    norm_df = normalize_bom_columns(bom_df)
    issues = validate_bom(norm_df)

    optimized = optimize_bom(norm_df)
    suppliers = load_suppliers(suppliers_path)
    cost_summary = analyze_costs(optimized, suppliers, config)
    risk_summary = analyze_risk(optimized, suppliers, config)

    return {
        "normalized_bom": norm_df,
        "optimized_bom": optimized,
        "issues": issues,
        "cost_summary": cost_summary,
        "risk_summary": risk_summary,
    }
