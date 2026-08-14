"""Game constants and configuration.

This module contains all game-wide constants, settings, and configuration values.
"""

from typing import Final

# =============================================================================
# SCREEN SETTINGS
# =============================================================================

SCREEN_WIDTH: Final[int] = 800
SCREEN_HEIGHT: Final[int] = 600
FPS: Final[int] = 60
TITLE: Final[str] = "Psychic Fortnight"

# =============================================================================
# COLORS (RGB format)
# =============================================================================

WHITE: Final[tuple[int, int, int]] = (255, 255, 255)
BLACK: Final[tuple[int, int, int]] = (0, 0, 0)
RED: Final[tuple[int, int, int]] = (255, 0, 0)
GREEN: Final[tuple[int, int, int]] = (0, 255, 0)
BLUE: Final[tuple[int, int, int]] = (0, 0, 255)
GRAY: Final[tuple[int, int, int]] = (128, 128, 128)
DARK_GRAY: Final[tuple[int, int, int]] = (64, 64, 64)
YELLOW: Final[tuple[int, int, int]] = (255, 255, 0)

# =============================================================================
# GAME SETTINGS
# =============================================================================

PLAYER_SPEED: Final[float] = 5.0
PLAYER_SIZE: Final[int] = 32
GRAVITY: Final[float] = 0.5
JUMP_STRENGTH: Final[float] = -10.0

# =============================================================================
# UI SETTINGS
# =============================================================================

FONT_SIZE: Final[int] = 24
BUTTON_WIDTH: Final[int] = 200
BUTTON_HEIGHT: Final[int] = 50

# =============================================================================
# GAME STATES
# =============================================================================

STATE_MENU: Final[str] = "menu"
STATE_PLAYING: Final[str] = "playing"
STATE_PAUSED: Final[str] = "paused"
STATE_GAME_OVER: Final[str] = "game_over"

# =============================================================================
# DIRECTIONS
# =============================================================================

DIRECTION_UP: Final[tuple[int, int]] = (0, -1)
DIRECTION_DOWN: Final[tuple[int, int]] = (0, 1)
DIRECTION_LEFT: Final[tuple[int, int]] = (-1, 0)
DIRECTION_RIGHT: Final[tuple[int, int]] = (1, 0)
