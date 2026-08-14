import pygame
import os
from constants import ASSET_DIR

def load_image(name, size=None):
    try:
        # Vollständigen Pfad zum Bild erstellen
        fullpath = os.path.join(ASSET_DIR, name)
        print(f"[DEBUG] Loading image from: {fullpath}")
        
        # Bild laden
        img = pygame.image.load(fullpath).convert_alpha()
        
        # Wenn eine Größe angegeben wurde, Bild skalieren
        if size:
            img = pygame.transform.scale(img, size)
            
        print(f"[DEBUG] Successfully loaded image: {name}")
        return img
    except Exception as e:
        print(f"[DEBUG] Failed to load image {name}: {e}")
        return None
