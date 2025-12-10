from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file {path} must contain a YAML mapping at top level.")
    return data


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate basic structure and ranges of the config.

    - risk weights should be in [0, 1]
    - suppliers.path should be a string if present
    - cost.default_volume should be positive if present
    """
    risk_cfg = config.get("risk", {})
    for key in ("single_source_weight", "missing_price_weight", "lifecycle_weight"):
        if key in risk_cfg:
            try:
                val = float(risk_cfg[key])
            except (TypeError, ValueError):
                raise ValueError(f"risk.{key} must be a number.")
            if not (0.0 <= val <= 1.0):
                raise ValueError(f"risk.{key} must be between 0 and 1, got {val}.")

    suppliers_cfg = config.get("suppliers", {})
    if "path" in suppliers_cfg and not isinstance(suppliers_cfg["path"], str):
        raise ValueError("suppliers.path must be a string if provided.")

    cost_cfg = config.get("cost", {})
    if "default_volume" in cost_cfg:
        try:
            vol = float(cost_cfg["default_volume"])
        except (TypeError, ValueError):
            raise ValueError("cost.default_volume must be numeric if provided.")
        if vol <= 0:
            raise ValueError("cost.default_volume must be positive if provided.")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load config from YAML file.

    Resolution order:
    - if config_path is given and exists, use it
    - else if ./bomer.yaml exists, use that
    - else return an empty dict

    Always performs basic validation.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path("bomer.yaml")

    if path.exists():
        config = _load_yaml(path)
    else:
        config = {}

    validate_config(config)
    return config
