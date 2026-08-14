"""Game state management.

This module handles the game state machine and state transitions.
"""

from enum import Enum, auto
from typing import Any


class GameState(Enum):
    """Enumeration of possible game states."""
    
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    LEVEL_COMPLETE = auto()
    QUIT = auto()


class StateManager:
    """Manages game state transitions and state-specific data.
    
    This class provides a state machine for managing different game states
    and their associated data.
    """
    
    def __init__(self) -> None:
        """Initialize the state manager with default state."""
        self._current_state: GameState = GameState.MENU
        self._previous_state: GameState | None = None
        self._state_data: dict[GameState, dict[str, Any]] = {}
    
    @property
    def current(self) -> GameState:
        """Get the current game state."""
        return self._current_state
    
    @property
    def previous(self) -> GameState | None:
        """Get the previous game state."""
        return self._previous_state
    
    def set(self, state: GameState, data: dict[str, Any] | None = None) -> None:
        """Set the current game state.
        
        Args:
            state: New game state to transition to.
            data: Optional state-specific data to store.
        """
        if self._current_state != state:
            self._previous_state = self._current_state
            self._current_state = state
            
            if data is not None:
                self._state_data[state] = data
    
    def get_data(self, state: GameState | None = None) -> dict[str, Any]:
        """Get data associated with a game state.
        
        Args:
            state: Game state to get data for. If None, uses current state.
        
        Returns:
            Dictionary of state-specific data, or empty dict if none exists.
        """
        if state is None:
            state = self._current_state
        return self._state_data.get(state, {})
    
    def is_playing(self) -> bool:
        """Check if the game is in playing state."""
        return self._current_state == GameState.PLAYING
    
    def is_menu(self) -> bool:
        """Check if the game is in menu state."""
        return self._current_state == GameState.MENU
    
    def is_paused(self) -> bool:
        """Check if the game is paused."""
        return self._current_state == GameState.PAUSED
    
    def is_game_over(self) -> bool:
        """Check if the game is in game over state."""
        return self._current_state == GameState.GAME_OVER
    
    def reset(self) -> None:
        """Reset the state manager to initial state."""
        self._current_state = GameState.MENU
        self._previous_state = None
        self._state_data.clear()
