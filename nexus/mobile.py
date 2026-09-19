from __future__ import annotations
import re, zipfile
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from .utils import redact_secret, now, save_json

console=Console()
URL_RE=re.compile(rb'https?://[^\s"\'<>]+')
SECRET_RE=re.compile(rb'(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*[A-Za-z0-9_\-./+=]{8,}')

def analyze_apk(path):
    p=Path(path)
    if not p.is_file() or p.suffix.lower()!=".apk": raise ValueError("Select a valid .apk file.")
    findings=[]; urls=set(); entries=[]
    with zipfile.ZipFile(p) as z:
        entries=z.namelist()
        for name in entries:
            if name.endswith((".xml",".json",".properties",".txt",".smali")):
                try: data=z.read(name)
                except KeyError: continue
                urls.update(x.decode("utf-8","ignore") for x in URL_RE.findall(data))
                for m in SECRET_RE.findall(data):
                    findings.append({"id":"APK-SECRET","severity":"HIGH","evidence":f"{name}: {redact_secret(m.decode('utf-8','ignore'))}"})
    manifest="AndroidManifest.xml" in entries
    return {"timestamp":now(),"apk":str(p),"valid_zip":True,"manifest_present":manifest,
            "entry_count":len(entries),"urls":sorted(urls),"findings":findings}

def menu(cfg):
    console.print("[bold cyan]APK SECURITY LAB[/bold cyan]")
    path=Prompt.ask("APK path (0 to back)")
    if path=="0": return
    try: data=analyze_apk(path)
    except Exception as e: console.print(f"[red]Error:[/red] {e}"); return
    while True:
        console.print("[1] File Inventory\n[2] Manifest Analysis\n[3] Permission Analysis\n[4] DEX / Resource Inventory\n[5] URL & Domain Extraction\n[6] Secret Pattern Detection\n[7] Security Findings\n[8] Generate Report\n[0] Back")
        c=Prompt.ask("APK", choices=list("123456780"), default="7")
        if c=="0": return
        if c=="1": console.print(f"Entries: {data['entry_count']}")
        elif c=="2": console.print(f"Manifest present: {data['manifest_present']}")
        elif c=="3": console.print("[yellow]Static ZIP-level analysis does not decode Android permissions without external APK tooling.[/yellow]")
        elif c=="4": console.print(f"DEX/resources: {data['entry_count']} archive entries")
        elif c=="5": console.print("\n".join(data["urls"]) or "No URLs found")
        elif c=="6": console.print(f"Potential secret-pattern findings: {len(data['findings'])}")
        elif c=="7":
            t=Table(title="SECURITY FINDINGS"); [t.add_column(x) for x in ("ID","Severity","Evidence")]
            for f in data["findings"]: t.add_row(f["id"],f["severity"],f["evidence"])
            console.print(t)
        elif c=="8": save_json("reports/apk/apk_report.json",data); console.print("[green]Report saved.[/green]")
