from typing import Any, Dict, List, Optional

import pandas as pd

# Canonical columns we want in the BOM
CANONICAL_COLUMNS: List[str] = [
    "PartNumber",
    "Quantity",
    "Manufacturer",
    "Description",
    "LifecycleStatus",
    "RoHS",
]

# Default alias map: lowercased source column -> canonical column
_DEFAULT_ALIAS_MAP: Dict[str, str] = {
    "mpn": "PartNumber",
    "mfr part #": "PartNumber",
    "mfr part": "PartNumber",
    "part number": "PartNumber",
    "qty": "Quantity",
    "quantity": "Quantity",
    "manufacturer": "Manufacturer",
    "mfr": "Manufacturer",
    "description": "Description",
    "lifecycle": "LifecycleStatus",
    "lifecycle status": "LifecycleStatus",
    "rohs": "RoHS",
    "rohs status": "RoHS",
}


def _build_alias_map(config: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
    """
    Merge default alias map with optional overrides from config:

    schema:
      aliases:
        "manufacturer part": "PartNumber"
        "vendor": "Manufacturer"
    """
    alias_map = dict(_DEFAULT_ALIAS_MAP)
    if config is None:
        return alias_map

    schema_cfg = config.get("schema", {})
    user_aliases = schema_cfg.get("aliases", {})

    if isinstance(user_aliases, dict):
        for src, dest in user_aliases.items():
            if not isinstance(src, str) or not isinstance(dest, str):
                continue
            alias_map[src.strip().lower()] = dest.strip()

    return alias_map


def normalize_bom_columns(
    df: pd.DataFrame,
    config: Optional[Dict[str, Any]] = None,
) -> pd.DataFrame:
    """
    Rename BOM columns into canonical ones using alias mapping.

    - Uses default alias map plus optional overrides from config.
    - Ensures canonical columns exist via ensure_canonical_columns().
    """
    alias_map = _build_alias_map(config)

    # Build rename map based on current columns
    rename_map: Dict[str, str] = {}
    for col in df.columns:
        key = str(col).strip().lower()
        if key in alias_map:
            rename_map[col] = alias_map[key]

    result = df.rename(columns=rename_map).copy()
    result = ensure_canonical_columns(result)
    return result


def ensure_canonical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure that all canonical columns exist in the DataFrame.

    If a canonical column is missing, it is added with NA values.
    """
    for col in CANONICAL_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def validate_bom(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Perform simple BOM validation.

    Returns a list of issue dictionaries, e.g.:

    {
      "row_index": 0,
      "field": "Quantity",
      "message": "Quantity is missing or not numeric"
    }
    """
    issues: List[Dict[str, Any]] = []

    if "PartNumber" not in df.columns or "Quantity" not in df.columns:
        issues.append(
            {
                "row_index": None,
                "field": "schema",
                "message": "Required columns PartNumber and Quantity are missing.",
            }
        )
        return issues

    for idx, row in df.iterrows():
        part = str(row.get("PartNumber", "")).strip()
        qty = row.get("Quantity", None)

        if not part:
            issues.append(
                {
                    "row_index": int(idx),
                    "field": "PartNumber",
                    "message": "PartNumber is empty.",
                }
            )

        try:
            qty_val = float(qty)
        except (TypeError, ValueError):
            issues.append(
                {
                    "row_index": int(idx),
                    "field": "Quantity",
                    "message": "Quantity is missing or not numeric.",
                }
            )
            continue

        if qty_val <= 0:
            issues.append(
                {
                    "row_index": int(idx),
                    "field": "Quantity",
                    "message": "Quantity must be positive.",
                }
            )

    return issues
