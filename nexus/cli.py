from __future__ import annotations
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from .config import load_config
from .logger import setup_logging
from . import network, wireless, mobile, secrets, assets, audit, dashboard, report, plugins, correlation

console = Console()

BANNER = """[bold cyan]
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                     N E X U S - X                            ║
║              SECURITY ASSESSMENT FRAMEWORK                   ║
║                                                              ║
║                         by ZEXQIR                            ║
║                 github.com/zexqir/nexus-x                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]"""

def startup():
    console.print("[yellow][*][/yellow] Initializing NEXUS-X...")
    cfg = load_config()
    setup_logging(cfg)
    for msg in ["Configuration loaded", "Modules loaded", "Report engine ready",
                "Logging initialized", "Environment detected"]:
        console.print(f"[green][✓][/green] {msg}")
    console.print("[bold green]NEXUS-X ready.[/bold green]\n")
    return cfg

def main_menu():
    while True:
        console.clear()
        console.print(BANNER)
        table = Table(title="MAIN MENU", show_header=False, box=None)
        for k, v in [
            ("1","🌐 Network Intelligence"),("2","📡 Wireless Analyzer"),
            ("3","📱 APK Security Lab"),("4","🔐 Secret Scanner"),
            ("5","🔎 Asset Discovery"),("6","🛡️ Security Audit"),
            ("7","🧠 Correlation Engine"),("8","📊 Security Dashboard"),
            ("9","📄 Report Center"),("A","⚙️ Configuration"),
            ("B","🧩 Plugin Manager"),("C","ℹ️ About / Credits"),("0","🚪 Exit")]:
            table.add_row(f"[bold]{k}[/bold]", v)
        console.print(Panel(table, border_style="cyan"))
        choice = Prompt.ask("NEXUS-X", choices=list("123456789ABC0abc"), default="8").upper()
        if choice == "0": break
        dispatch(choice)

def dispatch(choice):
    cfg = load_config()
    if choice == "1": network.menu(cfg)
    elif choice == "2": wireless.menu(cfg)
    elif choice == "3": mobile.menu(cfg)
    elif choice == "4": secrets.menu(cfg)
    elif choice == "5": assets.menu(cfg)
    elif choice == "6": audit.menu(cfg)
    elif choice == "7": correlation.menu(cfg)
    elif choice == "8": dashboard.menu(cfg)
    elif choice == "9": report.menu(cfg)
    elif choice == "A": config_menu(cfg)
    elif choice == "B": plugins.menu(cfg)
    elif choice == "C": console.print(Panel(
        "NEXUS-X\nSecurity Assessment Framework\n\nby ZEXQIR\n"
        "github.com/zexqir/nexus-x\n\nAuthorized defensive assessment only.",
        title="About / Credits", border_style="cyan"))
    Prompt.ask("Press Enter to continue", default="")

def config_menu(cfg):
    while True:
        console.print(Panel(
            "[1] Report Directory\n[2] Scan Timeout\n[3] Maximum File Size\n"
            "[4] Ignore Paths\n[5] Output Format\n[6] Logging Level\n"
            "[7] UI Settings\n[8] Reset Configuration\n[0] Back",
            title="CONFIGURATION"))
        c = Prompt.ask("Configuration", choices=list("123456780"), default="0")
        if c == "0": return
        if c == "1":
            cfg["report_dir"] = Prompt.ask("Report directory", default=cfg["report_dir"])
        elif c == "2":
            cfg["scan_timeout"] = int(Prompt.ask("Timeout seconds", default=str(cfg["scan_timeout"])))
        elif c == "3":
            cfg["max_file_size"] = int(Prompt.ask("Maximum file size (bytes)", default=str(cfg["max_file_size"])))
        elif c == "4":
            raw = Prompt.ask("Ignore paths (comma-separated)", default=",".join(cfg["ignore_paths"]))
            cfg["ignore_paths"] = [x.strip() for x in raw.split(",") if x.strip()]
        elif c == "5": cfg["output_format"] = Prompt.ask("Format", default=cfg["output_format"])
        elif c == "6": cfg["logging_level"] = Prompt.ask("Level", default=cfg["logging_level"])
        elif c == "8": cfg = load_config(reset=True)
        Path("config").mkdir(exist_ok=True)
        Path("config/config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="NEXUS-X Security Assessment Framework")
    parser.add_argument("--version", action="version", version="NEXUS-X 1.0.0 by ZEXQIR")
    args = parser.parse_args()
    startup()
    main_menu()

if __name__ == "__main__":
    main()
