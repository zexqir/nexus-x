from __future__ import annotations
from pathlib import Path
import json

DEFAULT = {
    "report_dir": "reports",
    "scan_timeout": 10,
    "max_file_size": 5_000_000,
    "ignore_paths": [".git", ".venv", "__pycache__"],
    "output_format": "json",
    "logging_level": "INFO",
    "ui": {"compact": False}
}

def load_config(reset=False):
    p = Path("config/config.json")
    p.parent.mkdir(exist_ok=True)
    if reset or not p.exists():
        p.write_text(json.dumps(DEFAULT, indent=2), encoding="utf-8")
        return DEFAULT.copy()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        merged = DEFAULT.copy()
        merged.update(data)
        return merged
    except (OSError, json.JSONDecodeError):
        return DEFAULT.copy()
