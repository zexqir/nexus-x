from __future__ import annotations
import json, re, subprocess
from pathlib import Path
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat()

def run_command(cmd, timeout=10):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return {"returncode": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
    except (OSError, subprocess.TimeoutExpired) as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e)}

def save_json(path, data):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return p

def redact_secret(value):
    if not value: return ""
    s = str(value)
    if len(s) <= 8: return "*" * len(s)
    return s[:4] + "*" * max(4, len(s)-8) + s[-4:]

def severity_from_keyword(s):
    s = str(s).lower()
    if any(x in s for x in ("private key","password","token","secret","credential")): return "HIGH"
    return "MEDIUM"
