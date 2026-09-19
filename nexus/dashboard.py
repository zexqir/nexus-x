from pathlib import Path
import json
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console=Console()
def menu(cfg):
    root=Path(cfg["report_dir"])
    reports=list(root.rglob("*")) if root.exists() else []
    findings=0
    for p in reports:
        if p.suffix==".json":
            try:
                d=json.loads(p.read_text())
                if isinstance(d,list): findings+=len(d)
                elif isinstance(d,dict): findings+=len(d.get("findings",[]))
            except Exception: pass
    t=Table(title="SECURITY DASHBOARD")
    t.add_column("Metric"); t.add_column("Value")
    t.add_row("Reports",str(sum(p.suffix==".json" for p in reports)))
    t.add_row("Finding/record items",str(findings))
    t.add_row("Status","READY")
    console.print(t)
    Prompt.ask("Press Enter to return",default="")
