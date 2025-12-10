from pathlib import Path
from typing import Any, Dict, Optional

import yaml


def load_config(config_path: Optional[str]) -> Dict[str, Any]:
    """
    Load configuration from YAML file.

    Priority:
    1) Explicit path passed via CLI.
    2) ./bomer.yaml in current directory, if present.
    3) Empty dict as fallback.
    """
    if config_path:
        path = Path(config_path)
    else:
        path = Path("bomer.yaml")

    if path.is_file():
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    return {}
