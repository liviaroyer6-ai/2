"""Main entry point for the game.

Starts the character selection screen and then the level selection
screen, which in turn starts the actual game_loop for the chosen level.

This matches the real API exposed by game_loop.py and
level_management.py (there is no GameLoop class in this project).
"""

import sys
import traceback

from game_state import set_current_user, get_current_progress
from game_loop import selection_screen
from level_management import level_select


def main() -> None:
    """Initialize game state and run the game.

    Sets a default user/progress, lets the player pick a character,
    then opens the level selection screen (which starts game_loop
    internally once a level is chosen).
    """
    try:
        # Default user/progress if you don't have a login system wired up yet.
        set_current_user("Player", {"completed": [], "last": 1})
        progress = get_current_progress()

        # Character selection first (stores selection in game_state).
        selection_screen(progress)

        # Then show the level selection screen. This will call game_loop()
        # internally when the player starts a level.
        level_select(progress)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
