from __future__ import annotations
import json, csv
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console=Console()
def menu(cfg):
    root=Path(cfg["report_dir"]); root.mkdir(parents=True,exist_ok=True)
    console.print("[bold cyan]REPORT CENTER[/bold cyan]")
    console.print("[1] View Reports\n[2] Open Latest Report\n[3] JSON Export\n[4] CSV Export\n[5] HTML Report\n[6] PDF Report\n[7] Compare Assessments\n[8] Delete Local Report\n[0] Back")
    c=Prompt.ask("Report",choices=list("123456780"),default="1")
    if c=="0": return
    reports=sorted(root.rglob("*.json"), key=lambda p:p.stat().st_mtime, reverse=True)
    if c=="1": console.print("\n".join(str(p) for p in reports) or "No reports.")
    elif c=="2" and reports:
        console.print(reports[0].read_text(errors="ignore")[:10000])
    elif c=="3": console.print("Reports are already JSON.")
    elif c=="4" and reports:
        data=json.loads(reports[0].read_text())
        out=root/"latest.csv"
        rows=data if isinstance(data,list) else [data]
        keys=sorted({k for r in rows if isinstance(r,dict) for k in r})
        with out.open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=keys); w.writeheader(); w.writerows(rows)
        console.print(f"Saved {out}")
    elif c=="5" and reports:
        body=reports[0].read_text().replace("&","&amp;").replace("<","&lt;")
        out=root/"latest.html"; out.write_text(f"<html><body><pre>{body}</pre></body></html>",encoding="utf-8")
        console.print(f"Saved {out}")
    elif c=="6": console.print("[yellow]PDF export is intentionally dependency-light; use HTML/JSON output or install an external PDF renderer.[/yellow]")
    elif c=="8" and reports:
        p=Path(Prompt.ask("Report path",default=str(reports[0])))
        if p.exists() and p.is_file(): p.unlink(); console.print("[green]Deleted local report.[/green]")
