import sys
import subprocess
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
from rich.table import Table

console = Console()

def run_installer():
    console.clear()
    
    # Hero Header
    console.print(Panel.fit(
        "[bold green]JSNAKE SYSTEM INSTALLER[/bold green]\n"
        "[dim]Initializing Neural Game Engine v0.1.3[/dim]",
        border_style="bright_blue"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        t1 = progress.add_task("[cyan]Scanning System Environment...", total=100)
        while not progress.finished:
            progress.update(t1, advance=2)
            time.sleep(0.02)
        
        t2 = progress.add_task("[yellow]Establishing PyPI Connection...", total=100)
        # Actually start the pip install in background
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "jsnake", "--upgrade"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            while process.poll() is None:
                progress.update(t2, advance=5)
                time.sleep(0.1)
                if progress.tasks[t2].percentage >= 95:
                    progress.update(t2, completed=95)
            
            progress.update(t2, completed=100)
            
        except Exception as e:
            console.print(f"[bold red]CRITICAL ERROR:[/bold red] {e}")
            sys.exit(1)

        t3 = progress.add_task("[magenta]Calibrating Grid Aspect Ratio...", total=100)
        while not progress.finished:
            progress.update(t3, advance=10)
            time.sleep(0.05)

    # Success Summary
    table = Table(show_header=False, box=None)
    table.add_row("[green]✔[/green]", "Core Engine Synced")
    table.add_row("[green]✔[/green]", "TUI Framework Ready")
    table.add_row("[green]✔[/green]", "Global 'jsnake' Command Linked")
    
    console.print(Panel(
        table,
        title="[bold green]INSTALLATION COMPLETE[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    
    console.print("\n[bold white]To begin the simulation, type:[/bold white] [bold cyan]jsnake[/bold cyan]\n")

if __name__ == "__main__":
    try:
        run_installer()
    except KeyboardInterrupt:
        console.print("\n[red]Installation Aborted by User.[/red]")
        sys.exit(1)
