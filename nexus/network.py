from __future__ import annotations
import socket
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from .utils import run_command, now, save_json

console = Console()

def snapshot(cfg):
    host = socket.gethostname()
    interfaces = run_command(["ip","-brief","addr"], cfg["scan_timeout"])
    routes = run_command(["ip","route"], cfg["scan_timeout"])
    conns = run_command(["ss","-tunap"], cfg["scan_timeout"])
    dns = run_command(["resolvectl","status"], cfg["scan_timeout"])
    data = {
        "timestamp": now(), "hostname": host,
        "interfaces": interfaces["stdout"], "routes": routes["stdout"],
        "connections": conns["stdout"], "dns": dns["stdout"],
    }
    return data

def show(data):
    t=Table(title="NETWORK SUMMARY")
    t.add_column("Item"); t.add_column("Value")
    t.add_row("Hostname", data["hostname"])
    t.add_row("Interfaces", str(len([x for x in data["interfaces"].splitlines() if x.strip()])))
    t.add_row("Connections", str(max(0, len(data["connections"].splitlines())-1)))
    t.add_row("Routes", str(len([x for x in data["routes"].splitlines() if x.strip()])))
    console.print(t)

def menu(cfg):
    console.print("[bold cyan]NETWORK INTELLIGENCE[/bold cyan]")
    console.print("[1] Public IP\n[2] Local Interfaces\n[3] Network Connections\n[4] Listening Services\n[5] Routing Information\n[6] DNS Configuration\n[7] ARP / Neighbor Inventory\n[8] Full Network Snapshot\n[0] Back")
    c=Prompt.ask("Network", choices=list("123456780"), default="8")
    if c=="0": return
    data=snapshot(cfg)
    if c=="1":
        r=run_command(["curl","-fsS","https://api.ipify.org"],cfg["scan_timeout"])
        console.print(r["stdout"].strip() or "[yellow]Unavailable[/yellow]")
    elif c=="2": console.print(data["interfaces"] or "Unavailable")
    elif c=="3": console.print(data["connections"] or "Unavailable")
    elif c=="4": console.print(run_command(["ss","-lntup"],cfg["scan_timeout"])["stdout"] or "Unavailable")
    elif c=="5": console.print(data["routes"] or "Unavailable")
    elif c=="6": console.print(data["dns"] or "Unavailable")
    elif c=="7": console.print(run_command(["ip","neigh"],cfg["scan_timeout"])["stdout"] or "Unavailable")
    elif c=="8":
        show(data)
        save_json("reports/network/network_snapshot.json", data)
        console.print("[green]Saved reports/network/network_snapshot.json[/green]")
