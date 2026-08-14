"""Global state management for the game"""

import pygame

# Global state variables
current_user = None
current_progress = None
selected_char_img = None

def set_current_user(username, progress):
    """Set the current user and their progress"""
    global current_user, current_progress
    current_user = username
    current_progress = progress

def set_selected_char(char_img):
    """Set the selected character image"""
    global selected_char_img
    selected_char_img = char_img
    print(f"[DEBUG] Character set: {selected_char_img is not None}")

def get_selected_char():
    """Get the currently selected character image"""
    global selected_char_img
    return selected_char_img
