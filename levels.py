from constants import LEVELS

def get_level_config(level):
    if level < 1 or level > len(LEVELS):
        raise ValueError(f"Invalid level {level}, must be between 1 and {len(LEVELS)}")
    return LEVELS[level - 1]