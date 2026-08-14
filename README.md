# Psychic Fortnight 🎮

A Pygame-based platformer game with clean architecture and modern Python practices.

## Features ✨

- **Clean Code Structure** - Modular design with separate concerns
- **Type Hints** - Full type annotations for better IDE support
- **Delta-Time Movement** - Frame-independent physics
- **State Machine** - Robust game state management
- **Object-Oriented** - Base classes for game entities
- **Error Handling** - Graceful error handling throughout

## Installation 🚀

### Requirements

- Python 3.10+
- pygame 2.0+

### Setup

```bash
# Clone the repository
git clone https://github.com/liviaroyer6-ai/2.git
cd 2

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install pygame
```

## Usage 🎯

```bash
# Run the game
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move |
| SPACE | Action / Jump |
| ESC | Pause / Menu |
| ENTER | Start / Restart |

## Project Structure 📁

```
.
├── main.py              # Entry point
├── game_loop.py         # Main game loop
├── game_state.py        # State machine
├── screen.py            # Rendering
├── game_objects.py      # Game entities
├── constants.py         # Configuration
├── utils.py             # Helper functions
├── levels.py            # Level definitions
├── level_management.py  # Level system
├── ui.py                # UI components
└── README.md            # This file
```

## Architecture 🏗️

### Game Loop

The game uses a classic game loop pattern with delta-time:

```python
while running:
    delta_time = clock.tick(FPS) / 1000.0
    
    process_events()
    update(delta_time)
    render()
```

### State Machine

Game states are managed by `StateManager`:

- `MENU` - Main menu screen
- `PLAYING` - Active gameplay
- `PAUSED` - Game paused
- `GAME_OVER` - Game over screen

### Game Objects

All game entities inherit from `GameObject`:

- `Player` - Player character with physics
- `Enemy` - AI-controlled enemies
- `Platform` - Static platforms

## Code Quality ✅

### Type Hints

All functions and methods use type annotations:

```python
def update(self, dt: float) -> None:
    """Update game object state."""
    pass
```

### Docstrings

Comprehensive documentation using Google-style docstrings:

```python
def load_image(path: str, colorkey: tuple | None = None) -> pygame.Surface:
    """Load an image from file with optional transparency.
    
    Args:
        path: Path to the image file.
        colorkey: Color to use as transparency key.
    
    Returns:
        Loaded pygame.Surface with optimized format.
    """
```

## Development 🛠️

### Running Tests

```bash
python -m pytest
```

### Code Formatting

```bash
# Format code
black .

# Type checking
mypy .

# Linting
flake8 .
```

## Performance Tips ⚡

1. **Use `convert()` or `convert_alpha()`** for images after loading
2. **Batch sprite rendering** using `pygame.sprite.Group`
3. **Limit collision checks** with spatial partitioning
4. **Cache frequently used surfaces**

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic platformer games
