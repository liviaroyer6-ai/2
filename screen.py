import pygame
import math
import sys
from constants import (
    screen_width, screen_height, GREEN, RED, GRAY, DARK_GRAY, WHITE, YELLOW,
    FONT, UI_WIDTH, UI_HEIGHT, LEVELS, CHAR_SPRITES
)
from ui import ui_button, ui_text, InputBox
from persistence import register_user, login_user
from utils import load_image
from level_management import level_select
from game_state import set_current_user
from session import save_session, load_session, clear_session
from game_menu import GameMenu  # Add this import

# screen.py
import os

from constants import screen_width, screen_height, WHITE, BLACK, pause_button, menu_button
from ui import ui_button, ui_text  # wenn du das nutzt
from ui import draw_texst           # oder deine Textfunktion

# Global state
current_user = None
current_progress = None

# Initialize clockss
clock = pygame.time.Clock()

def exit_game():
    print("[DEBUG] exit_game() called")
    pygame.quit()
    sys.exit()

def draw_text_big(text, x, y, color):
    font = pygame.font.SysFont("arial", 64, bold=True)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    pygame.display.get_surface().blit(text_surf, text_rect)

def main_menu():
    global current_user, current_progress
    print("[DEBUG] Entered main_menu()")

    # Session laden: Wenn schon jemand eingeloggt war, direkt ins GameMenu
    session = load_session()
    if session and not hasattr(main_menu, 'initial_load'):
        print("[DEBUG] Found existing session")
        username = session["username"]
        progress = session["progress"]
        set_current_user(username, progress)
        main_menu.initial_load = True  # Nur einmal automatischss
        game_menu = GameMenu()
        game_menu.show(progress)
        return

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pulse_timer = 0

    try:
        background = pygame.image.load(
            "Y:\alles bevor löschen\progaming\selbst_visual_sudio_code\sachen_für_aha_gamee/ui_background_menu.jpg"
        )
        background = pygame.transform.scale(background, (screen_width, screen_height))
        print("[DEBUG] main_menu background loaded")
    except:
        print("[DEBUG] Failed to load main_menu background")
        background = None

    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        panel = pygame.Surface((600, 400), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (255, 255, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 200))

        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (255, pulse, 0)
        draw_text_big("🚀 Willkommen im Spiel", screen_width // 2, screen_height // 2 - 250, pulse_color)

        # Buttons
        # Registrieren
        ui_button(
            "📝 Registrieren",
            screen_width // 2 - 150, screen_height // 2 - 40,
            300, 60,
            register_screen,
            hover_color=(50, 200, 50),
        )

        # Login
        ui_button(
            "🔐 Login",
            screen_width // 2 - 150, screen_height // 2 + 40,
            300, 60,
            login_screen,
            hover_color=(200, 50, 50),
        )

        # Exit
        exit_color = (255, 50, 50 + int(50 * math.sin(pulse_timer * 0.1)))
        ui_button(
            "❌ Exit",
            screen_width // 2 - 150, screen_height // 2 + 120,
            300, 60,
            exit_game,
            hover_color=exit_color,
        )

        # Logout nur anzeigen, wenn jemand eingeloggt ist
        if current_user:
            ui_button(
                "🔓 Logout",
                30, screen_height - 80,
                200, 50,
                logout,
                hover_color=(200, 50, 50),
            )

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("[DEBUG] Quit event in main_menu")
                exit_game()

        pygame.display.flip()
        clock.tick(60)

def logout():
    global current_user, current_progress
    print("[DEBUG] Logging out user")
    current_user = None
    current_progress = None
    clear_session()
    main_menu()

def register_screen():
    print("[DEBUG] Entered register_screen()")
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    input_width, input_height = 300, 40
    center_x = screen_width // 2 - input_width // 2

    ib_u = InputBox(center_x, screen_height // 2 - 50, input_width, input_height)
    ib_p = InputBox(center_x, screen_height // 2 + 30, input_width, input_height, password=True)

    msg = ""
    pulse_timer = 0

    def do_reg():
        nonlocal msg
        if ib_u.text and ib_p.text:
            ok, m = register_user(ib_u.text, ib_p.text)
            msg = m
        else:
            msg = "❌ Bitte alle Felder ausfüllen!"

    try:
        background = pygame.image.load("Y:\alles bevor löschen\progaming\selbst_visual_sudio_code\sachen_für_aha_game/ui_background_register.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        print("[DEBUG] Failed to load register_screen background")
        background = None

    while True:
        print("[DEBUG] register_screen loop start")
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (0, 255, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 120))

        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (0, pulse, 255)
        draw_text_big("📝 REGISTRIEREN", screen_width // 2, screen_height // 2 - 160, pulse_color)

        ui_text("Benutzername:", ib_u.rect.x, ib_u.rect.y - 25, (0, 255, 0))
        ib_u.draw(screen)

        ui_text("Passwort:", ib_p.rect.x, ib_p.rect.y - 25, (0, 255, 0))
        ib_p.draw(screen)

        ui_button("🔙 Back", 30, 30, 100, 40, main_menu, hover_color=(200, 50, 50))
        ui_button("✅ Registrieren", center_x, screen_height // 2 + 110, input_width, 50, do_reg, hover_color=(50, 200, 50))

        if msg:
            color = GREEN if msg.startswith("✅") else RED
            ui_text(msg, screen_width // 2 - FONT.size(msg)[0] // 2, screen_height // 2 + 170, color)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("[DEBUG] Quit event in register_screen")
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                print("[DEBUG] ESC pressed in register_screen")
                pygame.display.set_mode((UI_WIDTH, UI_HEIGHT))
                main_menu()
                return
            ib_u.handle(e)
            ib_p.handle(e)

        pygame.display.flip()
        clock.tick(60)

def login_screen():
    print("[DEBUG] Entered login_screen()")
    global current_user, current_progress

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    input_width, input_height = 300, 40
    center_x = screen_width // 2 - input_width // 2

    ib_u = InputBox(center_x, screen_height // 2 - 50, input_width, input_height)
    ib_p = InputBox(center_x, screen_height // 2 + 30, input_width, input_height, password=True)

    msg = ""
    progress = None
    pulse_timer = 0

    def do_log():
        nonlocal msg, progress
        print("[DEBUG] do_log called")
        ok, res = login_user(ib_u.text, ib_p.text)
        if ok:
            username = ib_u.text.strip()
            set_current_user(username, res)
            progress = res
            # Save session after successful login
            save_session(username, res)
            print(f"[DEBUG] Login successful. User:{username}, Progress:{progress}")
        else:
            msg = res
            print(f"[DEBUG] Login failed: {msg}")

    try:
        background = pygame.image.load("Y:\alles bevor löschen\progaming\selbst_visual_sudio_code\sachen_für_aha_game/ui_background_login.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        print("[DEBUG] Failed to load login_screen background")
        background = None

    while True:
        print("[DEBUG] login_screen loop start")
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (255, 0, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 120))

        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (255, pulse, pulse)
        draw_text_big("🔐 LOGIN", screen_width // 2, screen_height // 2 - 160, pulse_color)

        ui_text("Username:", ib_u.rect.x, ib_u.rect.y - 25, (255, 0, 0))
        ib_u.draw(screen)

        ui_text("Password:", ib_p.rect.x, ib_p.rect.y - 25, (255, 0, 0))
        ib_p.draw(screen)

        ui_button("🔙 Back", 30, 30, 100, 40, main_menu, hover_color=(200, 50, 50))
        ui_button("🚀 Login", center_x, screen_height // 2 + 110, input_width, 50, do_log, hover_color=(200, 50, 50))

        if msg:
            color = GREEN if msg.startswith("✅") else RED
            ui_text(msg, screen_width // 2 - FONT.size(msg)[0] // 2, screen_height // 2 + 170, color)

        if progress is not None:
            pygame.time.delay(300)
            print("[DEBUG] Moving to game menu")
            try:
                game_menu = GameMenu()
                game_menu.show(progress)
            except Exception as e:
                print("[DEBUG] Exception:", e)
                exit_game()
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print("[DEBUG] Quit event in login_screen")
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                print("[DEBUG] ESC pressed in login_screen")
                pygame.display.set_mode((UI_WIDTH, UI_HEIGHT))
                main_menu()
                return
            ib_u.handle(e)
            ib_p.handle(e)

        pygame.display.flip()
        clock.tick(60)
