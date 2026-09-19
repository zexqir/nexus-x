from __future__ import annotations
import socket
from rich.console import Console
from rich.prompt import Prompt
from .utils import now, save_json

console=Console()

def authorized(target):
    console.print(f"[yellow]Authorization required for active discovery target: {target}[/yellow]")
    return Prompt.ask("Confirm you are authorized", choices=["Y","N"], default="N").upper()=="Y"

def menu(cfg):
    console.print("[bold cyan]ASSET DISCOVERY[/bold cyan]")
    target=Prompt.ask("Target hostname/IP (0 to back)")
    if target=="0": return
    if not authorized(target): console.print("[red]Cancelled.[/red]"); return
    try:
        ip=socket.gethostbyname(target)
        data={"timestamp":now(),"target":target,"resolved_ip":ip,"connectivity":"resolved"}
    except socket.gaierror as e:
        data={"timestamp":now(),"target":target,"resolved_ip":None,"connectivity":"unresolved","error":str(e)}
    save_json("reports/assets/asset_report.json",data)
    console.print(data)
