import random

from .models import Direction, GameState, Point


class GameEngine:
    """Manages the evolution of the snake game's state over time."""

    def __init__(self, width: int = 40, height: int = 20):
        """Build the engine with a specified grid size."""
        self.state = GameState(width, height)

    def change_direction(self, new_dir: Direction) -> None:
        """Update the snake's direction, preventing 180-degree turns."""
        if self.state.direction != new_dir.opposite:
            self.state.direction = new_dir

    @property
    def speed(self) -> float:
        """Calculate the current game speed (interval in seconds) based on level."""
        # Level 1: 0.15s, Level 10: 0.05s
        return max(0.04, 0.16 - (self.state.level * 0.01))

    def step(self) -> bool:
        """Process one tick of the game. Returns True if the game is still active."""
        if self.state.is_over:
            return False

        # Calculate new head position
        new_head = self.state.head + self.state.direction

        # Check for collisions with walls
        if (new_head.x < 0 or new_head.x >= self.state.width or 
            new_head.y < 0 or new_head.y >= self.state.height):
            self.state.is_over = True
            return False

        # Check for collisions with self
        if new_head in self.state.body_set:
            self.state.is_over = True
            return False

        # Check for food
        if new_head == self.state.food:
            # Eat food
            self.state.snake.insert(0, new_head)
            self.state.score += 10
            
            # Level Up logic (every 50 points = 5 foods)
            if self.state.score % 50 == 0:
                self.state.level += 1
            
            self._spawn_food()
            return True # Signal that food was eaten
        else:
            # Move snake
            self.state.snake.insert(0, new_head)
            self.state.snake.pop()

        return True

    def _spawn_food(self) -> None:
        """Randomly position food on an unoccupied grid square."""
        # Using a set for faster collision check
        body_set = self.state.body_set
        potential_spots = [
            Point(x, y) 
            for x in range(self.state.width) 
            for y in range(self.state.height)
            if Point(x, y) not in body_set
        ]
        if potential_spots:
            self.state.food = random.choice(potential_spots)  # noqa: S311
        else:
            # Game won (no more space)
            self.state.is_over = True
