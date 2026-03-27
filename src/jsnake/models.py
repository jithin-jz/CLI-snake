from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Direction(Enum):
    """Represents the possible movement directions for the snake."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def opposite(self) -> Direction:
        """Helper to prevent the snake from moving directly backward into itself."""
        match self:
            case Direction.UP: return Direction.DOWN
            case Direction.DOWN: return Direction.UP
            case Direction.LEFT: return Direction.RIGHT
            case Direction.RIGHT: return Direction.LEFT


@dataclass(frozen=True, order=True)
class Point:
    """A single coordinate on the coordinate plane."""
    x: int
    y: int

    def __add__(self, other: Direction) -> Point:
        dx, dy = other.value
        return Point(self.x + dx, self.y + dy)


@dataclass
class GameState:
    """Encapsulates the entire state of the Snake game."""
    width: int
    height: int
    snake: list[Point] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    food: Point = field(default_factory=lambda: Point(5, 5))
    score: int = 0
    high_score: int = 0
    level: int = 1
    is_over: bool = False
    is_paused: bool = False

    def __post_init__(self) -> None:
        """Initialize the snake if not provided."""
        if not self.snake:
            center_x, center_y = self.width // 2, self.height // 2
            self.snake = [
                Point(center_x, center_y),
                Point(center_x - 1, center_y),
                Point(center_x - 2, center_y),
            ]

    @property
    def head(self) -> Point:
        """Get the point representing the snake's head."""
        return self.snake[0]

    @property
    def body_set(self) -> set[Point]:
        """Get a set of all body points for fast collision checking."""
        return set(self.snake)
