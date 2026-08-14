"""Game objects and entities.

This module contains base classes for all game objects and entities.
"""

import pygame
from typing import Final
from abc import ABC, abstractmethod

from constants import GRAVITY, SCREEN_HEIGHT, SCREEN_WIDTH


class GameObject(ABC):
    """Abstract base class for all game objects.
    
    This class provides the common interface for all game objects:
    - Update logic
    - Rendering
    - Collision detection
    - Position and velocity tracking
    """
    
    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        color: tuple[int, int, int],
    ) -> None:
        """Initialize a game object.
        
        Args:
            x: Initial x position.
            y: Initial y position.
            width: Width of the object.
            height: Height of the object.
            color: RGB color tuple.
        """
        self.x: float = x
        self.y: float = y
        self.width: Final[int] = width
        self.height: Final[int] = height
        self.color: Final[tuple[int, int, int]] = color
        
        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0
        
        self._rect: pygame.Rect = pygame.Rect(x, y, width, height)
    
    @property
    def rect(self) -> pygame.Rect:
        """Get the bounding rectangle of this object."""
        self._rect.x = int(self.x)
        self._rect.y = int(self.y)
        return self._rect
    
    @property
    def center(self) -> tuple[float, float]:
        """Get the center position of this object."""
        return (self.x + self.width / 2, self.y + self.height / 2)
    
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update the game object state.
        
        Args:
            dt: Delta time in seconds.
        """
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        """Render the game object.
        
        Args:
            surface: pygame.Surface to render on.
        """
        pass
    
    def collides_with(self, other: 'GameObject') -> bool:
        """Check if this object collides with another.
        
        Args:
            other: Another GameObject to check collision with.
        
        Returns:
            True if collision detected, False otherwise.
        """
        return self.rect.colliderect(other.rect)
    
    def is_on_screen(self) -> bool:
        """Check if the object is within screen bounds."""
        return (
            0 <= self.x <= SCREEN_WIDTH - self.width
            and 0 <= self.y <= SCREEN_HEIGHT - self.height
        )


class Player(GameObject):
    """Player character class.
    
    Handles player movement, physics, and rendering.
    """
    
    def __init__(self, x: float, y: float) -> None:
        """Initialize the player.
        
        Args:
            x: Initial x position.
            y: Initial y position.
        """
        super().__init__(x, y, 32, 32, (0, 255, 0))  # Green player
        
        self.speed: Final[float] = 5.0
        self.jump_strength: Final[float] = -10.0
        self.is_jumping: bool = False
        self.is_grounded: bool = True
    
    def update(self, dt: float) -> None:
        """Update player position and physics.
        
        Args:
            dt: Delta time in seconds.
        """
        # Apply gravity
        if not self.is_grounded:
            self.velocity_y += GRAVITY * dt * 60  # Scale gravity for smoothness
        
        # Update position
        self.x += self.velocity_x * dt * 60
        self.y += self.velocity_y * dt * 60
        
        # Screen bounds
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        # Ground collision
        if self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
            self.is_grounded = True
            self.is_jumping = False
        else:
            self.is_grounded = False
        
        # Friction
        self.velocity_x *= 0.9
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the player.
        
        Args:
            surface: pygame.Surface to render on.
        """
        pygame.draw.rect(surface, self.color, self.rect)
    
    def move_left(self) -> None:
        """Move player left."""
        self.velocity_x = -self.speed
    
    def move_right(self) -> None:
        """Move player right."""
        self.velocity_x = self.speed
    
    def jump(self) -> None:
        """Make the player jump."""
        if self.is_grounded:
            self.velocity_y = self.jump_strength
            self.is_grounded = False
            self.is_jumping = True
    
    def stop(self) -> None:
        """Stop player horizontal movement."""
        self.velocity_x = 0


class Enemy(GameObject):
    """Enemy character class.
    
    Basic enemy that moves back and forth.
    """
    
    def __init__(self, x: float, y: float, move_range: float = 100.0) -> None:
        """Initialize the enemy.
        
        Args:
            x: Initial x position.
            y: Initial y position.
            move_range: How far the enemy moves back and forth.
        """
        super().__init__(x, y, 32, 32, (255, 0, 0))  # Red enemy
        
        self.start_x: Final[float] = x
        self.move_range: Final[float] = move_range
        self.direction: float = 1.0
        self.speed: Final[float] = 2.0
    
    def update(self, dt: float) -> None:
        """Update enemy position.
        
        Args:
            dt: Delta time in seconds.
        """
        self.x += self.direction * self.speed * dt * 60
        
        # Change direction at boundaries
        if self.x > self.start_x + self.move_range:
            self.direction = -1.0
        elif self.x < self.start_x - self.move_range:
            self.direction = 1.0
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the enemy.
        
        Args:
            surface: pygame.Surface to render on.
        """
        pygame.draw.rect(surface, self.color, self.rect)


class Platform(GameObject):
    """Static platform class.
    
    Platforms are stationary objects that players can stand on.
    """
    
    def __init__(self, x: float, y: float, width: int, height: int) -> None:
        """Initialize the platform.
        
        Args:
            x: x position.
            y: y position.
            width: Platform width.
            height: Platform height.
        """
        super().__init__(x, y, width, height, (128, 128, 128))  # Gray platform
    
    def update(self, dt: float) -> None:
        """Update platform (static, so does nothing).
        
        Args:
            dt: Delta time in seconds.
        """
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        """Render the platform.
        
        Args:
            surface: pygame.Surface to render on.
        """
        pygame.draw.rect(surface, self.color, self.rect)
