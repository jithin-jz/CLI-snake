from jsnake.engine import Direction, GameEngine


def test_engine_initialization():
    """Verify the snake engine starts with correct default values."""
    engine = GameEngine(width=20, height=10)
    assert engine.state.width == 20
    assert engine.state.height == 10
    assert len(engine.state.snake) == 3
    assert engine.state.score == 0
    assert not engine.state.is_over

def test_movement_logic():
    """Ensure the snake moves in the intended direction."""
    engine = GameEngine(width=20, height=10)
    initial_head = engine.state.head
    engine.change_direction(Direction.RIGHT)
    engine.step()
    assert engine.state.head.x == initial_head.x + 1
    assert engine.state.head.y == initial_head.y

def test_collision_with_wall():
    """Verify that hitting a wall ends the game."""
    engine = GameEngine(width=10, height=10)
    # Head is at (5, 5) by default. Move it right until it hits edge.
    for _ in range(5):
        engine.step()
    assert engine.state.is_over

def test_food_consumption():
    """Confirm the snake grows and its score increases when it eats food."""
    engine = GameEngine(width=10, height=10)
    # Force food to be directly in front of snake
    target_food = engine.state.head + Direction.RIGHT
    engine.state.food = target_food
    
    initial_length = len(engine.state.snake)
    engine.step()
    
    # Growth check
    assert len(engine.state.snake) == initial_length + 1
    # Score check
    assert engine.state.score == 10
    # Food spawn check (should have moved)
    assert engine.state.food != target_food
