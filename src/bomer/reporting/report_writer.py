from pathlib import Path
from typing import Any, Dict, List

import json
import pandas as pd


def write_normalized_bom(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def write_optimized_bom(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def write_analysis_json(
    optimized_bom: pd.DataFrame,
    cost_summary: Dict[str, Any],
    risk_summary: Dict[str, Any],
    bom_path: Path,
    suppliers_path: Path,
    path: Path,
) -> None:
    payload = {
        "meta": {
            "bom_path": str(bom_path),
            "suppliers_path": str(suppliers_path),
            "part_count": int(len(optimized_bom)),
        },
        "cost": cost_summary,
        "risk": risk_summary,
    }
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def write_issues_json(issues: List[Dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(issues, f, indent=2)


def write_summary_text(
    optimized_bom: pd.DataFrame,
    cost_summary: Dict[str, Any],
    risk_summary: Dict[str, Any],
    issues: List[Dict[str, Any]],
    path: Path,
) -> None:
    currency = cost_summary.get("currency", "USD")
    total_cost = cost_summary.get("total_cost", "N/A")
    missing_prices = cost_summary.get("missing_prices", [])

    risk_score = risk_summary.get("risk_score", "N/A")
    single_ratio = risk_summary.get("single_source_ratio", 0)
    missing_ratio = risk_summary.get("missing_price_ratio", 0)
    obsolete_ratio = risk_summary.get("obsolete_ratio", 0)

    with path.open("w", encoding="utf-8") as f:
        f.write("=== BOMER Summary ===\n\n")
        f.write(f"Parts after optimization: {len(optimized_bom)}\n")
        f.write(f"Total cost: {total_cost} {currency}\n")
        f.write(f"Estimated risk score (0-100): {risk_score}\n\n")

        f.write("Risk breakdown:\n")
        f.write(f"  Single-source parts ratio: {single_ratio:.2%}\n")
        f.write(f"  Missing-price parts ratio: {missing_ratio:.2%}\n")
        f.write(f"  Obsolete parts ratio:      {obsolete_ratio:.2%}\n\n")

        if missing_prices:
            f.write("Parts with no price in supplier data:\n")
            for p in missing_prices:
                f.write(f"  - {p}\n")
            f.write("\n")

        if issues:
            f.write("Validation issues:\n")
            for issue in issues:
                row = issue.get("row")
                msg = issue.get("message")
                f.write(f"  - row={row}: {msg}\n")
        else:
            f.write("Validation issues: none.\n")
