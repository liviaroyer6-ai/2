import pygame
import sys
import math  # Added math import
import traceback  # Added traceback import
import json  # Added json import
import os
from constants import (
    screen_width, screen_height, GREEN, GRAY, DARK_GRAY, WHITE, YELLOW, CHAR_SPRITES, LEVELS
)
from game_loop import selection_screen
from constants import ASSET_DIR
from ui import ui_button, ui_text
from utils import load_image
from game_state import get_selected_char, set_selected_char  # Add this import

def load_settings():
    """Load game settings from file, create default if not exists"""
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        default_settings = {
            "fullscreen": True,
            "sound_volume": 0.7,
            "music_volume": 0.5,
            "show_fps": False,
            "difficulty": "normal"
        }
        # Save default settings
        with open("settings.json", "w") as f:
            json.dump(default_settings, f)
        return default_settings

# Add global declarations for current_user and current_progress
current_user = None
current_progress = None
show_fps = False  # Added global variable for FPS display
current_settings = load_settings()  # Load settings at the start

def toggle_fullscreen():
    pygame.display.toggle_fullscreen()

def toggle_fps():
    global show_fps
    show_fps = not show_fps

def adjust_volume(amount):
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(0.0, min(1.0, current_volume + amount))
    pygame.mixer.music.set_volume(new_volume)
    return new_volume

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f)

def set_difficulty(level):
    global current_settings
    current_settings["difficulty"] = level
    save_settings(current_settings)

def show_tutorial():
    screen = pygame.display.get_surface()
    tutorial_active = True
    while tutorial_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Tutorial", screen_width//2, screen_height//2 - 200, WHITE)
        ui_text("Use arrow keys to move", screen_width//2, screen_height//2 - 100, WHITE)
        ui_text("Press SPACE to shoot", screen_width//2, screen_height//2, WHITE)
        ui_text("Collect power-ups to get stronger", screen_width//2, screen_height//2 + 100, WHITE)
        ui_text("Click anywhere to close", screen_width//2, screen_height//2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                tutorial_active = False

def show_controls():
    screen = pygame.display.get_surface()
    controls_active = True
    while controls_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Controls", screen_width//2, screen_height//2 - 200, WHITE)
        ui_text("← → : Move left/right", screen_width//2, screen_height//2 - 100, WHITE)
        ui_text("↑ ↓ : Move up/down", screen_width//2, screen_height//2, WHITE)
        ui_text("SPACE : Shoot", screen_width//2, screen_height//2 + 100, WHITE)
        ui_text("ESC : Pause", screen_width//2, screen_height//2 + 150, WHITE)
        ui_text("Click anywhere to close", screen_width//2, screen_height//2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                controls_active = False

def show_credits():
    screen = pygame.display.get_surface()
    credits_active = True
    while credits_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Credits", screen_width//2, screen_height//2 - 200, WHITE)
        ui_text("Game Design: Team", screen_width//2, screen_height//2 - 100, WHITE)
        ui_text("Programming: Team", screen_width//2, screen_height//2, WHITE)
        ui_text("Graphics: Team", screen_width//2, screen_height//2 + 100, WHITE)
        ui_text("Click anywhere to close", screen_width//2, screen_height//2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_active = False

def show_stats(progress):
    screen = pygame.display.get_surface()
    stats_active = True
    while stats_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Statistics", screen_width//2, screen_height//2 - 200, WHITE)
        ui_text(f"Levels Completed: {len(progress['completed'])}",
                screen_width//2, screen_height//2 - 100, WHITE)
        ui_text(f"Current Level: {progress['last']}",
                screen_width//2, screen_height//2, WHITE)
        ...
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                stats_active = False

def show_achievements():
    screen = pygame.display.get_surface()
    achievements_active = True
    while achievements_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Achievements", screen_width//2, screen_height//2 - 200, WHITE)
        if len(current_progress['completed']) >= 5:
            ui_text("🏆 Rookie - Complete 5 levels", screen_width//2, screen_height//2 - 100, GREEN)
        if len(current_progress['completed']) >= 10:
            ui_text("🏆 Veteran - Complete 10 levels", screen_width//2, screen_height//2, GREEN)
        if len(current_progress['completed']) >= 15:
            ui_text("🏆 Master - Complete 15 levels", screen_width//2, screen_height//2 + 100, GREEN)
        ui_text("Click anywhere to close", screen_width//2, screen_height//2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                achievements_active = False

def level_select(progress):
    from screen import main_menu  # Lazy import to define main_menu
    global current_user, current_progress
    print("[DEBUG] Entered level_select() with progress:", progress)
    completed = progress.get("completed", [])
    last = progress.get("last", 1)
    print("[DEBUG] Completed levels:", completed, "Last available level:", last)
    
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    scroll_offset = 0
    pulse_timer = 0
    selected_level = None
    menu_open = False

    # Globale Variablen für Einstellungen
    sound_enabled = True
    music_enabled = True

    def toggle_sound():
        nonlocal sound_enabled
        sound_enabled = not sound_enabled
        print(f"[DEBUG] Sound {'enabled' if sound_enabled else 'disabled'}")

    def toggle_music():
        nonlocal music_enabled
        music_enabled = not music_enabled
        if music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        print(f"[DEBUG] Music {'enabled' if music_enabled else 'disabled'}")

    def show_help():
        help_active = True
        while help_active:
            # Hilfe-Overlay anzeigen
            help_surface = pygame.Surface((600, 400), pygame.SRCALPHA)
            help_surface.fill((30, 30, 30, 240))
            screen.blit(help_surface, (screen_width//2 - 300, screen_height//2 - 200))
            
            # Hilfetext anzeigen
            help_texts = [
                "Steuerung:",
                "- Pfeiltasten zum Bewegen",
                "- Leertaste zum Schießen",
                "- ESC zum Pausieren",
                "",
                "Power-Ups:",
                "- 🛡️ Schild",
                "- 🔫 Doppelschuss",
                "- ⏱️ Zeitverlangsamung",
                "",
                "Klicke zum Schließen"
            ]
            
            for i, text in enumerate(help_texts):
                ui_text(text, screen_width//2 - 250, screen_height//2 - 150 + i*30, WHITE)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    help_active = False
                    break

    # Menu buttons aktualisieren
    menu_buttons = [
        ("⚙️ Einstellungen", [
            ("🎮 Vollbild", toggle_fullscreen),
            ("🎵 Musik +", lambda: adjust_volume(0.1)),
            ("🎵 Musik -", lambda: adjust_volume(-0.1)),
            ("🔢 FPS anzeigen", toggle_fps),
            ("💾 Speichern", lambda: save_settings(current_settings))
        ]),
        ("🎮 Schwierigkeit", [
            ("😊 Leicht", lambda: set_difficulty("easy")),
            ("😐 Normal", lambda: set_difficulty("normal")),
            ("😈 Schwer", lambda: set_difficulty("hard"))
        ]),
        ("❔ Hilfe", [
            ("📖 Tutorial", show_tutorial),
            ("🎮 Steuerung", show_controls),
            ("ℹ️ Credits", show_credits)
        ]),
        ("👤 Profil", [
            ("👤 Anmelden", lambda: show_login_screen()),
           ("📊 Statistiken", lambda: show_stats(progress)),
           ("🏆 Erfolge", lambda: show_achievements(progress)),
        ]),
        ("☰ Hauptmenü", lambda: back_button())
    ]

    print("[DEBUG] level_select variables initialized")
    
    try:
        bg_path = os.path.join(ASSET_DIR, "ui_background_levels.jpg")
        print("[DEBUG] Loading level background from:", bg_path)
        background = pygame.image.load(bg_path)
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print("[DEBUG] Error loading level_select background:", e)
        background = None

    def start_level(level_num, prog):
        print(f"[DEBUG] Starting level {level_num}")
        selected_char = get_selected_char()
        
        if not selected_char:
            print("[DEBUG] No character selected, redirecting to selection screen")
            selection_screen(prog)
            return False
            
        from game_loop import game_loop
        try:
            print(f"[DEBUG] Starting game loop with character")
            result = game_loop(level_num, prog)
            if not result:
                print("[DEBUG] Game loop failed, returning to selection")
                selection_screen(prog)
                return False
            return True
        except Exception as e:
            print(f"[DEBUG] Error in game loop: {e}")
            return False

    def back_button():
        print("[DEBUG] Back to game menu")
        from game_menu import GameMenu
        menu = GameMenu()
        menu.show(progress)
        return True

    def show_login_screen():
        from screen import login_screen
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        login_screen()
        return True

    def draw_menu_button():
        nonlocal menu_open
        # Menu button in top right corner
        menu_btn = pygame.Rect(screen_width - 60, 10, 50, 50)
        
        # Draw main menu button
        pygame.draw.rect(screen, (30, 30, 30, 200), menu_btn, border_radius=10)
        ui_text("☰", menu_btn.centerx - 10, menu_btn.centery - 10, WHITE)
        
        # Handle menu button click
        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and menu_btn.collidepoint(mx, my):
            pygame.time.delay(100)  # Prevent double clicks
            menu_open = not menu_open
            
        # Draw dropdown menu if open
        if menu_open:
            current_y = 70
            for i, (text, action) in enumerate(menu_buttons):
                if isinstance(action, list):  # Untermenü
                    # Zeichne Hauptmenüpunkt
                    btn_rect = pygame.Rect(screen_width - 200, current_y, 190, 50)
                    hover = btn_rect.collidepoint(mx, my)
                    color = (60, 60, 60) if hover else (40, 40, 40)
                    pygame.draw.rect(screen, color, btn_rect, border_radius=10)
                    pygame.draw.rect(screen, WHITE, btn_rect, 1, border_radius=10)
                    ui_text(text, btn_rect.x + 10, btn_rect.centery - 10, WHITE)
                    
                    # Wenn hover, zeige Untermenü
                    if hover:
                        sub_x = btn_rect.x - 200
                        sub_y = btn_rect.y
                        for sub_text, sub_action in action:
                            sub_btn = pygame.Rect(sub_x, sub_y, 190, 50)
                            sub_hover = sub_btn.collidepoint(mx, my)
                            sub_color = (70, 70, 70) if sub_hover else (50, 50, 50)
                            pygame.draw.rect(screen, sub_color, sub_btn, border_radius=10)
                            pygame.draw.rect(screen, WHITE, sub_btn, 1, border_radius=10)
                            ui_text(sub_text, sub_btn.x + 10, sub_btn.centery - 10, WHITE)
                            
                            if sub_hover and pygame.mouse.get_pressed()[0]:
                                pygame.time.delay(100)
                                sub_action()
                            
                            sub_y += 60
                else:  # Normaler Menüpunkt
                    btn_rect = pygame.Rect(screen_width - 200, current_y, 190, 50)
                    hover = btn_rect.collidepoint(mx, my)
                    color = (60, 60, 60) if hover else (40, 40, 40)
                    pygame.draw.rect(screen, color, btn_rect, border_radius=10)
                    pygame.draw.rect(screen, WHITE, btn_rect, 1, border_radius=10)
                    ui_text(text, btn_rect.x + 10, btn_rect.centery - 10, WHITE)
                    
                    if hover and pygame.mouse.get_pressed()[0]:
                        pygame.time.delay(100)
                        action()
                current_y += 60

    while True:
        print("[DEBUG] level_select loop start; selected_level =", selected_level)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10,10,10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # Verschiebe das Panel nach oben
        panel = pygame.Surface((800, 500), pygame.SRCALPHA)  # Reduzierte Höhe
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (0, 255, 255, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 400, screen_height // 2 - 400))  # Höhere Position

        # Verschiebe den Titel nach oben
        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (0, pulse, 255)
        ui_text("🌟 LEVEL AUSWÄHLEN", screen_width // 2 - 150, screen_height // 2 - 450, WHITE)

        # Verschiebe die Level-Buttons nach oben
        for i in range(len(LEVELS)):
            x = screen_width // 2 - 300 + (i % 3) * 250
            y = screen_height // 2 - 300 + (i // 3) * 100 + scroll_offset  # Höhere Position
            lvl = i + 1
            if lvl in completed:
                col = GREEN
            elif lvl <= last:
                col = GRAY
            else:
                col = DARK_GRAY
            pygame.draw.rect(screen, col, (x, y, 200, 80), border_radius=8)
            ui_text(f"Level {lvl}", x + 50, y + 25, WHITE)

            mx, my = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]
            if lvl <= last and x < mx < x + 200 and y < my < y + 80 and click:
                selected_level = lvl
                print(f"[DEBUG] Level {selected_level} selected")

        if selected_level is not None:
            print(f"[DEBUG] Highlighting selected level {selected_level}")
            x = screen_width // 2 - 300 + ((selected_level - 1) % 3) * 250
            y = screen_height // 2 - 300 + ((selected_level - 1) // 3) * 100 + scroll_offset  # Höhere Position
            pygame.draw.rect(screen, YELLOW, (x - 5, y - 5, 210, 90), 3)

        # Verschiebe den Start-Button nach oben
        if selected_level is not None:
            # Create and draw button
            start_btn = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 150, 200, 50)  # Höhere Position
            
            # Check hover
            mouse_pos = pygame.mouse.get_pos()
            hover = start_btn.collidepoint(mouse_pos)
            
            # Draw button
            pygame.draw.rect(screen, (0, 255, 0) if hover else (0, 200, 0), start_btn, border_radius=10)
            pygame.draw.rect(screen, WHITE, start_btn, 2, border_radius=10)
            
            # Add text
            text = "▶️ Start Level"
            font = pygame.font.SysFont('arial', 24)
            text_surf = font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=start_btn.center)
            screen.blit(text_surf, text_rect)
            
            # Handle click
            if pygame.mouse.get_pressed()[0] and hover:
                pygame.time.delay(200)
                start_level(selected_level, progress)

        ui_button("🔙 Back", 30, 30, 100, 40, back_button, hover_color=(200, 50, 50))

        # Draw menu button last (on top of everything)
        draw_menu_button()

        # Add click detection for menu area
        mx, my = pygame.mouse.get_pos()
        menu_area = pygame.Rect(screen_width - 210, 0, 210, 320)
        if menu_open and not menu_area.collidepoint(mx, my) and pygame.mouse.get_pressed()[0]:
            menu_open = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("[DEBUG] Quit event in level_select")
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEWHEEL:
                scroll_offset += e.y * 20
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    scroll_offset -= 20
                elif e.key == pygame.K_DOWN:
                    scroll_offset += 20
                elif e.key == pygame.K_ESCAPE:  # ESC key now returns to game menu
                    back_button()
                    return

        scroll_offset = max(min(scroll_offset, 0), -300)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

#def selection_screen(progress=None):
 ##   """Charakter-Auswahl vor jedem Level."""
   # from game_loop import game_loop
    #from screen import main_menu
   # global selected_char_img, current_progress
    #
    ## Store the progress
  #  current_progress = progress
  #  print(f"[DEBUG] selection_screen received progress: {progress}")
#
  #  # Richtige Initialisierung des Screens
  #  screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
  #  pygame.display.flip()  # Bildschirm aktualisieren
  #  
   # chars = [load_image(fn, (120, 120)) for fn in CHAR_SPRITES]
   ## idx_c = 0
  #  pulse_timer = 0
#
 #   try:
 #       bg_path = os.path.join(ASSET_DIR, "ui_background_characters.jpg")
 #       print("[DEBUG] Loading character background from:", bg_path)
  #      background = pygame.image.load(bg_path)
  #      background = pygame.transform.scale(background, (screen_width, screen_height))
 #   except Exception as e:
 #       print(f"[DEBUG] Failed to load character selection background: {e}")
 #       background = None

 #   def confirm_selection():
 #       print("[DEBUG] confirm_selection called, idx_c =", idx_c)
#        selected = load_image(CHAR_SPRITES[idx_c], (80, 80))
 #       if selected:
#            set_selected_char(selected)
 #           print("[DEBUG] Character selected and saved to state")
#            return selected
#       return None

 #   while True:
        # Hintergrund zeichnen
 #       if background:
  #         screen.blit(background, (0, 0))
  #      else:
  #          screen.fill((10, 10, 10))
#
 #       # Overlay
  #      overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
 #       overlay.fill((0, 0, 0, 120))
  #      screen.blit(overlay, (0, 0))

 #       # ...rest of existing code...

  #      pygame.display.flip()
  #      pygame.time.Clock().tick(60)

   # return selected_char_img