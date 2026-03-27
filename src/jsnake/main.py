import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from .tui import SnakeApp

def boot_sequence():
    """A cinematic arcade-style boot sequence for the JSNAKE engine."""
    console = Console()
    console.clear()
    
    console.print(Panel.fit(
        "[bold green]JSNAKE NEURAL ENGINE[/bold green]\n"
        "[dim]Initializing Core Subsystems v0.1.5[/dim]",
        border_style="bright_blue"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        t1 = progress.add_task("[cyan]Syncing Grid Logic...", total=100)
        while not progress.tasks[t1].finished:
            progress.update(t1, advance=5)
            time.sleep(0.03)
        
        t2 = progress.add_task("[yellow]Calibrating Neon TUI...", total=100)
        while not progress.tasks[t2].finished:
            progress.update(t2, advance=3)
            time.sleep(0.03)

        t3 = progress.add_task("[magenta]Optimizing Game State...", total=100)
        while not progress.tasks[t3].finished:
            progress.update(t3, advance=10)
            time.sleep(0.04)
            
    time.sleep(0.5)

def main() -> int:
    """The main entry point for the CLI snake game."""
    try:
        # Check if we should skip boot (optional)
        if "--skip-boot" not in sys.argv:
            boot_sequence()
            
        app = SnakeApp()
        app.run()
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"Error running CLI Snake: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
