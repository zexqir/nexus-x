from pathlib import Path
import importlib.util
from rich.console import Console
from rich.prompt import Prompt

console=Console()
PLUGIN_DIR=Path("plugins")

def discover():
    PLUGIN_DIR.mkdir(exist_ok=True)
    return sorted(PLUGIN_DIR.glob("*.py"))

def menu(cfg):
    console.print("[bold cyan]PLUGIN MANAGER[/bold cyan]")
    for p in discover(): console.print(f"✓ {p.name}")
    console.print("[1] Plugin Information\n[2] Enable Plugin\n[3] Disable Plugin\n[4] Validate Plugin\n[5] Plugin Directory\n[0] Back")
    c=Prompt.ask("Plugin",choices=list("123450"),default="5")
    if c=="5": console.print(PLUGIN_DIR.resolve())
    elif c=="4":
        for p in discover():
            spec=importlib.util.spec_from_file_location(p.stem,p)
            try:
                mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
                console.print(f"[green]Valid[/green] {p.name}")
            except Exception as e: console.print(f"[red]Invalid[/red] {p.name}: {e}")
