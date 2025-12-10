import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from bomer.engines.models import CostSummary, RiskSummary


def write_normalized_bom(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def write_optimized_bom(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def write_analysis_json(
    optimized_bom: pd.DataFrame,
    cost_summary: CostSummary,
    risk_summary: RiskSummary,
    bom_path: Path,
    suppliers_path: Path,
    path: Path,
) -> None:
    analysis: Dict[str, Any] = {
        "metadata": {
            "bom_path": str(bom_path),
            "suppliers_path": str(suppliers_path),
            "part_count": int(len(optimized_bom)),
        },
        "cost": asdict(cost_summary),
        "risk": asdict(risk_summary),
    }

    with path.open("w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)


def write_issues_json(issues: List[Dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)


def write_summary_text(
    optimized_bom: pd.DataFrame,
    cost_summary: CostSummary,
    risk_summary: RiskSummary,
    issues: List[Dict[str, Any]],
    path: Path,
) -> None:
    lines: List[str] = []

    lines.append("Bomer Analysis Summary")
    lines.append("======================")
    lines.append("")
    lines.append(f"Total parts (optimized): {len(optimized_bom)}")
    lines.append(
        f"Total cost: {cost_summary.total_cost:.4f} {cost_summary.currency}"
    )
    lines.append("")
    lines.append("Risk:")
    lines.append(f"- risk_score: {risk_summary.risk_score}")
    lines.append(
        f"- single_source_ratio: {risk_summary.single_source_ratio:.3f}"
    )
    lines.append(
        f"- missing_price_ratio: {risk_summary.missing_price_ratio:.3f}"
    )
    lines.append(f"- obsolete_ratio: {risk_summary.obsolete_ratio:.3f}")
    lines.append("")
    lines.append(f"Issues detected: {len(issues)}")

    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
