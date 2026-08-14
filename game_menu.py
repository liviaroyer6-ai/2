import pygame
import os

from constants import screen_width, screen_height, WHITE, GREEN, YELLOW, RED, ASSET_DIR
from ui import ui_button, ui_text
from utils import load_image
from game_state import get_selected_char, set_selected_char
from level_management import level_select
from game_loop import selection_screen
class GameMenu:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.FULLSCREEN
        )
        try:
            bg_path = os.path.join(ASSET_DIR, "ui_background_menu.jpg")
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(
                self.background, (screen_width, screen_height)
            )
        except Exception as e:
            print("[DEBUG] Failed to load game_menu background:", e)
            self.background = None

    def show(self, progress):
        self.current_progress = progress
        clock = pygame.time.Clock()

        while True:
            if self.background:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.fill((10, 10, 10))

            # Charakterbild anzeigen, falls vorhanden
            char_img = get_selected_char()
            if char_img:
                char_rect = char_img.get_rect(
                    center=(screen_width // 2, screen_height // 2 - 100)
                )
                self.screen.blit(char_img, char_rect)

            # Button: Charakter wählen
            ui_button(
                "🦸 Charakter Wählen",
                screen_width // 2 - 150, screen_height // 2 + 150, 300, 60,
                lambda: self.to_selection_screen(progress),
                hover_color=(50, 200, 50),
            )

            # Button: Level wählen
            ui_button(
                "🎮 Level Wählen",
                screen_width // 2 - 150, screen_height // 2 + 250, 300, 60,
                lambda: self.show_level_select(progress),
                hover_color=(50, 200, 50),
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    from screen import main_menu
                    main_menu()
                    return

            pygame.display.flip()
            clock.tick(60)

    def to_selection_screen(self, progress):
        print("[DEBUG] GameMenu: to_selection_screen called")
        try:
            selection_screen(progress)
        except Exception as e:
            print("[DEBUG] Error in selection_screen:", e)
            return
    # NICHT erneut self.show(progress) aufrufes
    def show_level_select(self, progress):
        """Öffnet die Level-Auswahl."""
        print("[DEBUG] GameMenu: show_level_select called")
        try:
            level_select(progress)
        except Exception as e:
            print("[DEBUG] Error in level_select:", e)
            return