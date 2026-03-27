from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.timer import Timer
from textual.widgets import Digits, Footer, Header, Label, ProgressBar, Static

from .engine import Direction, GameEngine


class SnakeGrid(Static):
    """A high-fidelity rendering of the snake's environment with 1:1 aspect ratio emulation."""

    def __init__(self, engine: GameEngine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def render(self) -> str:
        state = self.engine.state
        # Use wider characters to fix the "up/down is faster than left/right" illusion
        # Height is 1 unit, Width is 2 characters (~1 unit in most terminals)
        grid = [['  ' for _ in range(state.width)] for _ in range(state.height)]

        # Render Food (2-char wide)
        grid[state.food.y][state.food.x] = '[bold red]◍ [/bold red]'

        # Render Snake
        for i, point in enumerate(state.snake):
            if i == 0:
                # Snake Head
                char = '██' if not state.is_over else 'XX'
                color = 'bright_yellow' if state.is_over else 'bright_green'
            else:
                # Snake Body
                char = '▓▓'
                color = 'green'
            
            grid[point.y][point.x] = f'[bold {color}]{char}[/bold {color}]'

        return "\n".join("".join(row) for row in grid)


class StatsPanel(Vertical):
    """A side panel for game information and progress."""
    
    def __init__(self, engine: GameEngine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def compose(self) -> ComposeResult:
        with Vertical(id="stats-content"):
            yield Label("SCORE", classes="stat-label")
            yield Digits(str(self.engine.state.score), id="current-score")
            
            yield Label("LEVEL", classes="stat-label m-top")
            yield Digits(str(self.engine.state.level), id="current-level")
            
            yield Label("PROGRESS", classes="stat-label m-top")
            yield ProgressBar(total=50, show_percentage=False, id="level-progress")
            
            yield Label("BEST", classes="stat-label m-top")
            yield Digits(str(self.engine.state.high_score), id="high-score")
            
            yield Label("SYSTEM STATUS", classes="stat-label m-top")
            yield Label("OPTIMAL", id="status-tag")
            
            yield Label("COMMANDS", classes="stat-label m-top")
            yield Label("[W][A][S][D] Move", classes="hint")
            yield Label("[P] Pause", classes="hint")
            yield Label("[R] Restart", classes="hint")

    def update_stats(self):
        state = self.engine.state
        self.query_one("#current-score", Digits).update(str(state.score))
        self.query_one("#current-level", Digits).update(str(state.level))
        self.query_one("#high-score", Digits).update(str(state.high_score))
        
        # Level progress calculation (score % 50 represents progress towards next level)
        progress = state.score % 50
        self.query_one("#level-progress", ProgressBar).update(progress=progress)
        
        if state.score > state.high_score and state.score > 0:
            self.query_one("#current-score").styles.color = "yellow"
        else:
            self.query_one("#current-score").styles.color = "white"


class SnakeApp(App):
    """A premium, feature-rich Snake implementation for the modern terminal."""

    TITLE = "🐍 JSNAKE"
    SUB_TITLE = "Reactive Terminal Arcade"
    
    LAYERS = ["base", "top"]
    
    CSS = """
    Screen {
        background: #0a0a0c;
        color: #e0e0e0;
    }

    #app-container {
        layout: horizontal;
        padding: 1 2;
        align: center middle;
    }

    #game-view {
        width: 78;  /* 38 * 2 (units) + 2 (borders) */
        height: 20; /* 18 * 1 (units) + 2 (borders) */
        background: #141416;
        border: heavy #3b3b3f;
        padding: 0;
        margin: 0;
    }

    SnakeGrid {
        width: 76;
        height: 18;
    }

    #stats-panel {
        width: 30;
        height: 22;
        margin-left: 2;
        padding: 1;
        background: #1c1c1e;
        border: solid #3b3b3f;
    }

    .stat-label {
        color: #6e6e73;
        text-style: bold;
        margin-bottom: 0;
    }

    .m-top {
        margin-top: 1;
    }

    Digits {
        margin-bottom: 0;
    }

    #level-progress {
        margin: 1 0;
        height: 1;
        background: #2c2c2e;
    }

    #level-progress > .bar--complete {
        background: #30d158;
    }

    #status-tag {
        background: #2c2c2e;
        color: #30d158;
        padding: 0 1;
        width: auto;
        text-style: bold;
    }

    .hint {
        color: #8e8e93;
    }

    #overlay {
        display: none;
        width: 100%; height: 100%;
        background: #000000B3; 
        content-align: center middle;
        layer: top;
    }

    .finished #overlay {
        display: block;
    }

    #game-over-text {
        text-style: bold underline;
        color: #ff453a;
        margin-bottom: 1;
    }

    .paused #status-tag {
        color: #ff9f0a;
        background: transparent;
    }

    .lvl-up #game-view {
        border: double #30d158;
    }
    """

    BINDINGS = [
        Binding("up,w", "change_direction('UP')", "Move Up", show=False),
        Binding("down,s", "change_direction('DOWN')", "Move Down", show=False),
        Binding("left,a", "change_direction('LEFT')", "Move Left", show=False),
        Binding("right,d", "change_direction('RIGHT')", "Move Right", show=False),
        Binding("p", "toggle_pause", "Pause/Resume"),
        Binding("r", "reset_game", "Restart"),
        Binding("q", "quit", "Exit"),
    ]

    def __init__(self):
        super().__init__()
        self.engine = GameEngine(width=38, height=18)
        self.high_score = 0
        self.game_timer: Timer | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="app-container"):
            with Container(id="game-view"):
                yield SnakeGrid(self.engine, id="grid")
                with Vertical(id="overlay"):
                    yield Label("CORE FAILURE", id="game-over-text")
                    yield Label("SNAKE SYSTEM COMPROMISED")
                    yield Label("Press [R] to Reboot", classes="hint m-top")
            yield StatsPanel(self.engine, id="stats-panel")
        yield Footer()

    def on_mount(self) -> None:
        self._start_timer()

    def _start_timer(self) -> None:
        if self.game_timer:
            self.game_timer.stop()
        self.game_timer = self.set_interval(self.engine.speed, self.tick)

    def tick(self) -> None:
        if self.engine.state.is_over or self.engine.state.is_paused:
            return

        old_score = self.engine.state.score
        old_level = self.engine.state.level
        
        if self.engine.step():
            # Handle Level Up Visuals
            if self.engine.state.level > old_level:
                self.add_class("lvl-up")
                self.set_timer(0.5, lambda: self.remove_class("lvl-up"))
                self._start_timer() # Update interval for new level

            # Update High Score
            if self.engine.state.score > self.high_score:
                self.high_score = self.engine.state.score
                self.engine.state.high_score = self.high_score

            self.query_one("#grid").refresh()
            self.query_one("#stats-panel", StatsPanel).update_stats()
        else:
            self.add_class("finished")
            self.query_one("#status-tag").update("CRITICAL")

    def action_change_direction(self, direction_name: str) -> None:
        if not self.engine.state.is_paused:
            new_dir = getattr(Direction, direction_name)
            self.engine.change_direction(new_dir)

    def action_toggle_pause(self) -> None:
        if not self.engine.state.is_over:
            self.engine.state.is_paused = not self.engine.state.is_paused
            if self.engine.state.is_paused:
                self.add_class("paused")
                self.query_one("#status-tag").update("PAUSED")
            else:
                self.remove_class("paused")
                self.query_one("#status-tag").update("OPTIMAL")

    def action_reset_game(self) -> None:
        self.remove_class("finished")
        self.remove_class("paused")
        self.engine = GameEngine(width=38, height=18)
        self.engine.state.high_score = self.high_score
        self.query_one("#grid").engine = self.engine
        self.query_one("#stats-panel", StatsPanel).engine = self.engine
        self.query_one("#grid").refresh()
        self.query_one("#stats-panel", StatsPanel).update_stats()
        self.query_one("#status-tag").update("OPTIMAL")
        self._start_timer()
