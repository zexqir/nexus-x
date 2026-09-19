from __future__ import annotations
import os, stat
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from .utils import now, save_json

console=Console()

def local_audit():
    findings=[]
    if os.geteuid()==0:
        findings.append({"id":"AUDIT-001","title":"Process is running as root","severity":"INFO",
                         "description":"NEXUS-X does not require root for most modules.",
                         "recommendation":"Prefer least privilege where practical."})
    ssh=Path("/etc/ssh/sshd_config")
    if ssh.exists():
        try:
            text=ssh.read_text(errors="ignore")
            if "PermitRootLogin yes" in text:
                findings.append({"id":"AUDIT-002","title":"SSH root login explicitly enabled","severity":"HIGH",
                                 "description":"The local SSH configuration contains an explicit PermitRootLogin yes.",
                                 "recommendation":"Review whether root SSH login is necessary."})
        except OSError: pass
    return [{"timestamp":now(),**f} for f in findings]

def menu(cfg):
    console.print("[bold cyan]SECURITY AUDIT[/bold cyan]")
    console.print("[1] Local Linux Posture\n[2] File Permission Review\n[3] Configuration Review\n[4] Generate Report\n[0] Back")
    c=Prompt.ask("Audit",choices=list("12340"),default="1")
    if c=="0": return
    findings=local_audit()
    for f in findings: console.print(f"[bold]{f['severity']}[/bold] {f['title']} — {f['recommendation']}")
    save_json("reports/audits/audit_report.json",findings)
