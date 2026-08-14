import os
import pygame

# Paths
# Updated constants.py for new local folders
ASSET_ROOT = r"D:\programing\oldgametonewwithperpel\sachenthaitneeds"
IMAGE_DIR = os.path.join(ASSET_ROOT, "bilder")
SOUND_DIR = os.path.join(ASSET_ROOT, "sound")

USER_FILE = os.path.join(ASSET_ROOT, "users.json")

# Screen dimensions
UI_WIDTH, UI_HEIGHT = 800, 600
GAME_W, GAME_H = 1600, 1000

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Font
FONT = pygame.font.SysFont(None, 40)

# Level definitions (image filenames live in IMAGE_DIR)
LEVELS = [
    {"bg": "ahabild1.png", "speed": 3, "count": 3, "threshold": 10},
    {"bg": "ahabild2.png", "speed": 5, "count": 5, "threshold": 30},
    {"bg": "ahabild3.png", "speed": 7, "count": 7, "threshold": 45},
    {"bg": "ahabild4.png", "speed": 4, "count": 4, "threshold": 20},
    {"bg": "ahabild5.png", "speed": 4, "count": 6, "threshold": 25},
    {"bg": "ahabild6.png", "speed": 5, "count": 5, "threshold": 35},
    {"bg": "ahabild7.png", "speed": 6, "count": 6, "threshold": 40},
    {"bg": "ahabild8.png", "speed": 6, "count": 7, "threshold": 45},
    {"bg": "ahabild9.png", "speed": 7, "count": 7, "threshold": 50},
    {"bg": "ahabild10.png", "speed": 7, "count": 8, "threshold": 55},
    {"bg": "ahabild11.png", "speed": 8, "count": 8, "threshold": 60},
    {"bg": "ahabild12.png", "speed": 8, "count": 9, "threshold": 65},
    {"bg": "ahabild13.png", "speed": 9, "count": 9, "threshold": 70},
    {"bg": "ahabild14.png", "speed": 9, "count": 10, "threshold": 75},
    {"bg": "ahabild15.png", "speed": 10, "count": 10, "threshold": 80},
    {"bg": "ahabild16.png", "speed": 10, "count": 11, "threshold": 85},
    {"bg": "ahabild17.png", "speed": 11, "count": 11, "threshold": 90},
    {"bg": "ahabild18.png", "speed": 11, "count": 12, "threshold": 95},
    {"bg": "ahabild19.png", "speed": 12, "count": 12, "threshold": 100},
    {"bg": "ahabild20.png", "speed": 12, "count": 13, "threshold": 105},
    {"bg": "ahabild21.png", "speed": 13, "count": 13, "threshold": 110},
    {"bg": "ahabild22.png", "speed": 13, "count": 14, "threshold": 115},
    {"bg": "ahabild23.png", "speed": 14, "count": 14, "threshold": 120},
]

# Character sprites (image filenames live in IMAGE_DIR)
CHAR_SPRITES = [
    "butterfly.png",
    "dino.png",
    "demon.png",
]

# Buttons
pause_button = pygame.Rect(GAME_W - 110, 10, 100, 40)
resume_button = pygame.Rect(GAME_W // 2 - 100, GAME_H // 2, 200, 50)
restart_button = pygame.Rect(GAME_W // 2 - 100, GAME_H // 2 + 10, 200, 50)
quit_button = pygame.Rect(GAME_W // 2 - 100, GAME_H // 2 + 80, 200, 50)
try_again_button = pygame.Rect(GAME_W // 2 - 100, GAME_H // 2 - 80, 200, 50)
menu_button = pygame.Rect(GAME_W // 2 - 100, GAME_H // 2 + 150, 200, 50)
