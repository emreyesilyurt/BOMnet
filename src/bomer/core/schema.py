from typing import Dict, List

import pandas as pd

# Canonical column names Bomer will use internally.
CANONICAL_COLUMNS = [
    "PartNumber",
    "Manufacturer",
    "Description",
    "Quantity",
    "LifecycleStatus",
    "RoHS",
]


# Common variations -> canonical name
_COLUMN_ALIASES = {
    "part": "PartNumber",
    "partnumber": "PartNumber",
    "mpn": "PartNumber",
    "mfr part #": "PartNumber",
    "mfr_part_number": "PartNumber",
    "manufacturer": "Manufacturer",
    "mfr": "Manufacturer",
    "desc": "Description",
    "description": "Description",
    "qty": "Quantity",
    "quantity": "Quantity",
    "life_cycle": "LifecycleStatus",
    "lifecycle": "LifecycleStatus",
    "lifecyclestatus": "LifecycleStatus",
    "rohs": "RoHS",
    "rohs_status": "RoHS",
}


def _normalize_header(name: str) -> str:
    return name.strip().lower().replace(" ", "").replace("-", "").replace("#", "")


def normalize_bom_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns to canonical names where possible, leaving others untouched.
    """
    new_columns: Dict[str, str] = {}

    for col in df.columns:
        key = _normalize_header(col)
        if key in _COLUMN_ALIASES:
            new_columns[col] = _COLUMN_ALIASES[key]
        else:
            new_columns[col] = col  # keep original

    return df.rename(columns=new_columns)


def validate_bom(df: pd.DataFrame) -> List[dict]:
    """
    Returns a list of issues.
    Each issue is a dict with 'row', 'type', 'message'.
    """
    issues: List[dict] = []

    # Basic checks
    has_part = "PartNumber" in df.columns
    has_qty = "Quantity" in df.columns

    if not has_part:
        issues.append(
            {
                "row": None,
                "type": "missing_column",
                "message": "Missing required column: PartNumber",
            }
        )
    if not has_qty:
        issues.append(
            {
                "row": None,
                "type": "missing_column",
                "message": "Missing required column: Quantity",
            }
        )

    if not has_part or not has_qty:
        return issues

    for idx, row in df.iterrows():
        part = str(row.get("PartNumber", "")).strip()
        qty = row.get("Quantity", 0)

        if not part:
            issues.append(
                {
                    "row": int(idx),
                    "type": "empty_part_number",
                    "message": "Empty PartNumber.",
                }
            )

        try:
            qty_value = float(qty)
        except (TypeError, ValueError):
            issues.append(
                {
                    "row": int(idx),
                    "type": "invalid_quantity",
                    "message": f"Quantity is not a number: {qty}",
                }
            )
            continue

        if qty_value <= 0:
            issues.append(
                {
                    "row": int(idx),
                    "type": "non_positive_quantity",
                    "message": f"Quantity must be > 0, got {qty_value}",
                }
            )

    return issues
