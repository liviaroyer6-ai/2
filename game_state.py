"""Simple global game state for user, progress and selected character.

This restores the original expectations of other modules like game_loop.py
and level_management.py, which import `current_user`, `current_progress`,
`get_selected_char` and `set_selected_char`.
"""

from __future__ import annotations

from typing import Any

# Currently logged-in user name (or None if not logged in)
current_user: str | None = None

# Progress of the current user. Other modules treat this as a dict with
# keys like "completed" (list of finished levels) and "last" (highest unlocked).
current_progress: dict[str, Any] = {
    "completed": [],
    "last": 1,
}

# Selected character sprite (e.g. a pygame.Surface). We keep type loose here
# to avoid importing pygame in this module.
_selected_char: Any = None


def set_current_user(username: str | None, progress: dict[str, Any] | None = None) -> None:
    """Set the current user and optionally their progress.

    Args:
        username: New username or None to clear.
        progress: Optional progress dict to replace current_progress.
    """
    global current_user, current_progress
    current_user = username
    if progress is not None:
        current_progress = progress


def get_current_user() -> str | None:
    """Get the name of the current user."""
    return current_user


def get_current_progress() -> dict[str, Any]:
    """Get the current user's progress dict."""
    return current_progress


def set_selected_char(char: Any) -> None:
    """Store the currently selected character sprite/object."""
    global _selected_char
    _selected_char = char


def get_selected_char() -> Any:
    """Return the currently selected character sprite/object."""
    return _selected_char
