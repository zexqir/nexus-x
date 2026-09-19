from rich.console import Console
from rich.prompt import Prompt
from .utils import run_command

console=Console()

def menu(cfg):
    console.print("[bold cyan]WIRELESS ANALYZER[/bold cyan]")
    console.print("[1] Wi-Fi Interfaces\n[2] Interface Status\n[3] Bluetooth Adapters\n[4] Bluetooth Device Inventory\n[5] Wireless Summary\n[0] Back")
    c=Prompt.ask("Wireless", choices=list("123450"), default="5")
    if c=="0": return
    if c in ("1","2","5"):
        console.print(run_command(["iw","dev"],cfg["scan_timeout"])["stdout"] or "iw unavailable")
    elif c in ("3","4"):
        cmd=["bluetoothctl","list"] if c=="3" else ["bluetoothctl","devices"]
        console.print(run_command(cmd,cfg["scan_timeout"])["stdout"] or "Bluetooth discovery unavailable")
    console.print("[dim]Jamming, deauthentication and denial-of-service functions are intentionally absent.[/dim]")
