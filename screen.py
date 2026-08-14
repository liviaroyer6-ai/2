"""Screen rendering and display management.

This module handles all rendering operations for different game states.
"""

import pygame
from typing import Final

from constants import (
    BLACK,
    BUTTON_HEIGHT,
    BUTTON_WIDTH,
    FONT_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    WHITE,
)
from game_state import GameState, StateManager


class Screen:
    """Manages screen rendering for all game states.
    
    This class handles:
    - Menu rendering
    - Game rendering
    - Pause screen
    - Game over screen
    - UI elements
    """
    
    def __init__(self, display: pygame.Surface, state_manager: StateManager) -> None:
        """Initialize the screen renderer.
        
        Args:
            display: pygame.Surface to render on.
            state_manager: StateManager for tracking game state.
        """
        self.display: Final[pygame.Surface] = display
        self.state_manager: Final[StateManager] = state_manager
        
        # Initialize fonts
        pygame.font.init()
        self.font_large: Final[pygame.font.Font] = pygame.font.Font(None, FONT_SIZE * 2)
        self.font_medium: Final[pygame.font.Font] = pygame.font.Font(None, FONT_SIZE)
        self.font_small: Final[pygame.font.Font] = pygame.font.Font(None, FONT_SIZE // 2)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events for the current screen.
        
        Args:
            event: pygame event to process.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state_manager.is_playing():
                    self.state_manager.set(GameState.PAUSED)
                elif self.state_manager.is_paused():
                    self.state_manager.set(GameState.PLAYING)
    
    def update(self, dt: float) -> None:
        """Update game logic during playing state.
        
        Args:
            dt: Delta time in seconds.
        """
        # Update game objects here
        pass
    
    def update_menu(self, dt: float) -> None:
        """Update menu state.
        
        Args:
            dt: Delta time in seconds.
        """
        pass
    
    def update_paused(self, dt: float) -> None:
        """Update paused state.
        
        Args:
            dt: Delta time in seconds.
        """
        pass
    
    def update_game_over(self, dt: float) -> None:
        """Update game over state.
        
        Args:
            dt: Delta time in seconds.
        """
        pass
    
    def render(self) -> None:
        """Render the game during playing state."""
        # Render game objects here
        pass
    
    def render_menu(self) -> None:
        """Render the main menu screen."""
        # Title
        title_text: Final[pygame.Surface] = self.font_large.render(
            "Psychic Fortnight", True, WHITE
        )
        title_rect: Final[pygame.Rect] = title_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )
        self.display.blit(title_text, title_rect)
        
        # Start prompt
        start_text: Final[pygame.Surface] = self.font_medium.render(
            "Press ENTER to Start", True, WHITE
        )
        start_rect: Final[pygame.Rect] = start_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.display.blit(start_text, start_rect)
        
        # Instructions
        instructions: list[str] = [
            "Arrow Keys: Move",
            "SPACE: Action",
            "ESC: Pause"
        ]
        
        for i, instruction in enumerate(instructions):
            text: Final[pygame.Surface] = self.font_small.render(
                instruction, True, WHITE
            )
            text_rect: Final[pygame.Rect] = text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3 + i * 30)
            )
            self.display.blit(text, text_rect)
    
    def render_paused(self) -> None:
        """Render the pause screen."""
        # Semi-transparent overlay
        overlay: Final[pygame.Surface] = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.display.blit(overlay, (0, 0))
        
        # Paused text
        paused_text: Final[pygame.Surface] = self.font_large.render(
            "PAUSED", True, WHITE
        )
        paused_rect: Final[pygame.Rect] = paused_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.display.blit(paused_text, paused_rect)
        
        # Resume prompt
        resume_text: Final[pygame.Surface] = self.font_medium.render(
            "Press ESC to Resume", True, WHITE
        )
        resume_rect: Final[pygame.Rect] = resume_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        )
        self.display.blit(resume_text, resume_rect)
    
    def render_game_over(self) -> None:
        """Render the game over screen."""
        # Game Over text
        game_over_text: Final[pygame.Surface] = self.font_large.render(
            "GAME OVER", True, WHITE
        )
        game_over_rect: Final[pygame.Rect] = game_over_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        )
        self.display.blit(game_over_text, game_over_rect)
        
        # Restart prompt
        restart_text: Final[pygame.Surface] = self.font_medium.render(
            "Press ENTER to Restart", True, WHITE
        )
        restart_rect: Final[pygame.Rect] = restart_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.display.blit(restart_text, restart_rect)
