import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd


def load_bom(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"BOM file not found: {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"BOM file is empty: {path}")

    return df


def load_suppliers(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Suppliers file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
