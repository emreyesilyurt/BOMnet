import json
from pathlib import Path
from typing import Any, Dict

import pandas as pd

from bomer.core.exceptions import BomLoadError, SupplierLoadError


def load_bom(path: Path) -> pd.DataFrame:
    """
    Load a BOM CSV from the given path.

    Raises BomLoadError with a clear message if loading fails.
    """
    if not path.exists():
        raise BomLoadError(f"BOM file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise BomLoadError(f"Unsupported BOM format for {path}. Expected .csv")

    try:
        df = pd.read_csv(path)
    except Exception as exc:  # pragma: no cover - generic safety net
        raise BomLoadError(f"Failed to read BOM CSV {path}: {exc}") from exc

    if df.empty:
        raise BomLoadError(f"BOM file {path} is empty.")

    return df


def load_suppliers(path: Path) -> Dict[str, Any]:
    """
    Load supplier pricing data from JSON.

    Structure is expected to be:
    {
      "currency": "USD",
      "suppliers": [
        {
          "name": "SupplierA",
          "prices": { "PART1": 0.1, ... }
        }
      ]
    }

    Raises SupplierLoadError if anything is invalid.
    """
    if not path.exists():
        raise SupplierLoadError(f"Suppliers file not found: {path}")

    if path.suffix.lower() != ".json":
        raise SupplierLoadError(f"Unsupported suppliers format for {path}. Expected .json")

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as exc:  # pragma: no cover
        raise SupplierLoadError(f"Failed to read suppliers JSON {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise SupplierLoadError(f"Suppliers file {path} must contain a JSON object at top level.")

    return data
