from __future__ import annotations
import re
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from .utils import redact_secret, now, save_json

console=Console()
PATTERNS=[
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("api-key-assignment", re.compile(r"(?i)\b(api[_-]?key|token|secret|password)\b\s*[:=]\s*['\"]?([A-Za-z0-9_\-./+=]{8,})")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]
def scan(root,cfg):
    root=Path(root).expanduser()
    findings=[]
    for p in root.rglob("*"):
        if not p.is_file() or any(part in cfg["ignore_paths"] for part in p.parts): continue
        try:
            if p.stat().st_size>cfg["max_file_size"]: continue
            text=p.read_text(errors="ignore")
        except OSError: continue
        for i,line in enumerate(text.splitlines(),1):
            for kind,rx in PATTERNS:
                for m in rx.finditer(line):
                    raw=m.group(0)
                    findings.append({"type":kind,"file":str(p),"line":i,"severity":"HIGH",
                                     "evidence":redact_secret(raw),"timestamp":now()})
    return findings

def menu(cfg):
    console.print("[bold cyan]SECRET SCANNER[/bold cyan]")
    console.print("[1] Scan Directory\n[2] Scan Git Repository\n[3] Custom Patterns\n[4] Ignore Rules\n[5] Findings\n[6] Generate Report\n[0] Back")
    c=Prompt.ask("Secrets", choices=list("1234560"), default="1")
    if c=="0": return
    target=Prompt.ask("Target directory",default=".")
    findings=scan(target,cfg)
    t=Table(title="SECRET FINDINGS"); [t.add_column(x) for x in ("Type","File","Line","Severity","Evidence")]
    for f in findings[:100]: t.add_row(f["type"],f["file"],str(f["line"]),f["severity"],f["evidence"])
    console.print(t)
    if c=="6" or c=="1": save_json("reports/secrets/secrets_report.json",findings)
