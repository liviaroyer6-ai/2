"""Utility functions for the game.

This module provides helper functions for common operations like
loading images, calculating distances, and other utilities.
"""

import math
import os
from typing import Any

import pygame

from constants import BLACK


def load_image(path: str, colorkey: tuple[int, int, int] | None = None) -> pygame.Surface:
    """Load an image from file with optional transparency.
    
    Args:
        path: Path to the image file.
        colorkey: Color to use as transparency key. If None, uses alpha channel.
    
    Returns:
        Loaded pygame.Surface with optimized format.
    
    Raises:
        FileNotFoundError: If the image file doesn't exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    
    image = pygame.image.load(path)
    
    if colorkey is not None:
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    
    return image


def load_images(paths: list[str]) -> list[pygame.Surface]:
    """Load multiple images from file paths.
    
    Args:
        paths: List of image file paths.
    
    Returns:
        List of loaded pygame.Surface objects.
    """
    return [load_image(path) for path in paths]


def distance(point1: tuple[float, float], point2: tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points.
    
    Args:
        point1: First point as (x, y) tuple.
        point2: Second point as (x, y) tuple.
    
    Returns:
        Distance between the two points.
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx * dx + dy * dy)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp a value between minimum and maximum bounds.
    
    Args:
        value: Value to clamp.
        min_value: Minimum allowed value.
        max_value: Maximum allowed value.
    
    Returns:
        Clamped value between min_value and max_value.
    """
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """Linear interpolation between two values.
    
    Args:
        start: Starting value.
        end: Ending value.
        t: Interpolation factor (0.0 to 1.0).
    
    Returns:
        Interpolated value.
    """
    return start + (end - start) * clamp(t, 0.0, 1.0)


def rect_collide_circle(rect: pygame.Rect, center: tuple[float, float], radius: float) -> bool:
    """Check if a rectangle collides with a circle.
    
    Args:
        rect: pygame.Rect to check.
        center: Center of circle as (x, y) tuple.
        radius: Radius of circle.
    
    Returns:
        True if collision detected, False otherwise.
    """
    # Find closest point on rectangle to circle center
    closest_x = clamp(center[0], rect.left, rect.right)
    closest_y = clamp(center[1], rect.top, rect.bottom)
    
    # Calculate distance from closest point to circle center
    distance_x = center[0] - closest_x
    distance_y = center[1] - closest_y
    
    return (distance_x * distance_x + distance_y * distance_y) <= (radius * radius)


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int] = BLACK,
    pos: tuple[float, float] = (0, 0),
    center: bool = False,
) -> pygame.Rect:
    """Draw text on a surface.
    
    Args:
        surface: Surface to draw on.
        text: Text string to render.
        font: pygame.font.Font object.
        color: RGB color tuple.
        pos: Position as (x, y) tuple.
        center: If True, center the text at pos.
    
    Returns:
        Rect of the rendered text.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = pos
    else:
        text_rect.topleft = pos
    
    surface.blit(text_surface, text_rect)
    return text_rect
