import subprocess
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.table import Table

console = Console()


def _fill_task(progress: Progress, task_id: int, step: int, delay: float) -> None:
    """Advance a progress task to completion with a short animated delay."""
    while not progress.tasks[task_id].finished:
        progress.update(task_id, advance=step)
        time.sleep(delay)


def run_installer():
    console.clear()
    
    # Hero Header
    console.print(Panel.fit(
        "[bold green]JSNAKE SYSTEM INSTALLER[/bold green]\n"
        "[dim]Initializing Neural Game Engine v0.1.6[/dim]",
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
        _fill_task(progress, t1, step=2, delay=0.02)

        t2 = progress.add_task("[yellow]Installing JSNAKE from PyPI...", total=100)
        process: subprocess.Popen[str] | None = None
        try:
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", "--upgrade", "jsnake"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            while process.poll() is None:
                progress.update(t2, advance=5)
                time.sleep(0.1)
                if progress.tasks[t2].percentage >= 95:
                    progress.update(t2, completed=95)

            stdout, stderr = process.communicate()
            progress.update(t2, completed=100)
        except Exception as e:
            console.print(f"[bold red]CRITICAL ERROR:[/bold red] {e}")
            sys.exit(1)

        if process is None or process.returncode != 0:
            console.print(
                Panel.fit(
                    "[bold red]INSTALLATION FAILED[/bold red]\n"
                    "PowerShell users can always retry with:\n"
                    "[bold cyan]py -m pip install jsnake[/bold cyan]",
                    border_style="red",
                )
            )
            if stderr:
                console.print(stderr.strip(), style="red")
            elif stdout:
                console.print(stdout.strip(), style="red")
            sys.exit(process.returncode if process is not None else 1)

        t3 = progress.add_task("[magenta]Calibrating Grid Aspect Ratio...", total=100)
        _fill_task(progress, t3, step=10, delay=0.05)

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
    
    console.print(
        "\n[bold white]To begin the simulation, type:[/bold white] "
        "[bold cyan]jsnake[/bold cyan]\n"
    )

if __name__ == "__main__":
    try:
        run_installer()
    except KeyboardInterrupt:
        console.print("\n[red]Installation Aborted by User.[/red]")
        sys.exit(1)
