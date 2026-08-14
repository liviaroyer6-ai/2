"""Main game loop implementation.

This module contains the core game loop that handles:
- Event processing
- Game state updates
- Rendering
- Frame rate control
"""

import pygame
from typing import Final

from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from game_state import GameState, StateManager
from screen import Screen


class GameLoop:
    """Main game loop that manages the game lifecycle.
    
    This class handles the core game loop including:
    - Initialization and cleanup of pygame
    - Event processing
    - Delta-time calculation for frame-independent updates
    - State management
    - Rendering
    """
    
    def __init__(self) -> None:
        """Initialize the game loop and pygame."""
        pygame.init()
        pygame.mixer.init()
        
        self.screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.state_manager: StateManager = StateManager()
        
        self._running: bool = True
        self._delta_time: float = 0.0
        
        # Initialize game systems
        self.game_screen: Screen = Screen(self.screen, self.state_manager)
    
    def run(self) -> None:
        """Run the main game loop.
        
        This is the primary entry point for the game execution.
        The loop continues until the game state is set to QUIT.
        """
        while self._running:
            self._delta_time = self.clock.tick(FPS) / 1000.0  # Convert to seconds
            
            self._process_events()
            self._update()
            self._render()
        
        self._cleanup()
    
    def _process_events(self) -> None:
        """Process pygame events.
        
        Handles:
        - Window close events
        - Keyboard input
        - Mouse input
        - Custom game events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                self.state_manager.set(GameState.QUIT)
            
            # Delegate event handling to current state
            self.game_screen.handle_event(event)
    
    def _update(self) -> None:
        """Update game state.
        
        Uses delta-time for frame-independent updates.
        """
        dt: Final[float] = self._delta_time
        
        # Update game systems based on current state
        if self.state_manager.is_playing():
            self.game_screen.update(dt)
        elif self.state_manager.is_menu():
            self.game_screen.update_menu(dt)
        elif self.state_manager.is_paused():
            self.game_screen.update_paused(dt)
        elif self.state_manager.is_game_over():
            self.game_screen.update_game_over(dt)
        
        # Check for quit state
        if self.state_manager.current == GameState.QUIT:
            self._running = False
    
    def _render(self) -> None:
        """Render the game.
        
        Clears the screen and renders all game objects.
        """
        self.screen.fill((0, 0, 0))  # Clear screen with black
        
        # Render based on current state
        if self.state_manager.is_playing():
            self.game_screen.render()
        elif self.state_manager.is_menu():
            self.game_screen.render_menu()
        elif self.state_manager.is_paused():
            self.game_screen.render_paused()
        elif self.state_manager.is_game_over():
            self.game_screen.render_game_over()
        
        pygame.display.flip()
    
    def _cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()
