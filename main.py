"""Main entry point for the game.

This module initializes and runs the game loop.
"""

import sys
import traceback
from game_loop import GameLoop


def main() -> None:
    """Initialize and run the game.
    
    Catches and logs any exceptions that occur during game execution.
    """
    try:
        game = GameLoop()
        game.run()
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
