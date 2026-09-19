from pathlib import Path
import json
from rich.console import Console
from rich.prompt import Prompt

console=Console()

def menu(cfg):
    console.print("[bold cyan]CORRELATION ENGINE[/bold cyan]")
    console.print("This module links existing local reports without exploitation.")
    root=Path(cfg["report_dir"])
    reports=list(root.rglob("*.json")) if root.exists() else []
    for p in reports:
        try:
            d=json.loads(p.read_text())
            count=len(d) if isinstance(d,list) else len(d.get("findings",[])) if isinstance(d,dict) else 0
            console.print(f"[cyan]{p}[/cyan] → {count} finding/record items")
        except Exception: pass
    Prompt.ask("Press Enter to return",default="")
