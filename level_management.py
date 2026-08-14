import pygame
import sys
import math
import traceback
import json
import os

from constants import (
    screen_width,
    screen_height,
    GREEN,
    GRAY,
    DARK_GRAY,
    WHITE,
    YELLOW,
    CHAR_SPRITES,
    LEVELS,
    IMAGE_DIR,
)
from game_loop import selection_screen
from ui import ui_button, ui_text
from utils import load_image
from game_state import get_selected_char, set_selected_char

from constants import SOUND_DIR


def load_settings():
    """Load game settings from file, create default if not exists."""
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        default_settings = {
            "fullscreen": True,
            "sound_volume": 0.7,
            "music_volume": 0.5,
            "show_fps": False,
            "difficulty": "normal",
        }
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(default_settings, f)
        return default_settings


current_user = None
current_progress = None
show_fps = False
current_settings = load_settings()


def toggle_fullscreen() -> None:
    pygame.display.toggle_fullscreen()


def toggle_fps() -> None:
    global show_fps
    show_fps = not show_fps


def adjust_volume(amount: float) -> float:
    current_volume = pygame.mixer.music.get_volume()
    new_volume = max(0.0, min(1.0, current_volume + amount))
    pygame.mixer.music.set_volume(new_volume)
    return new_volume


def save_settings(settings: dict) -> None:
    with open("settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f)


def set_difficulty(level: str) -> None:
    global current_settings
    current_settings["difficulty"] = level
    save_settings(current_settings)


def show_tutorial() -> None:
    screen = pygame.display.get_surface()
    tutorial_active = True
    while tutorial_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Tutorial", screen_width // 2, screen_height // 2 - 200, WHITE)
        ui_text("Use arrow keys to move", screen_width // 2, screen_height // 2 - 100, WHITE)
        ui_text("Press SPACE to shoot", screen_width // 2, screen_height // 2, WHITE)
        ui_text("Collect power-ups to get stronger", screen_width // 2, screen_height // 2 + 100, WHITE)
        ui_text("Click anywhere to close", screen_width // 2, screen_height // 2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                tutorial_active = False


def show_controls() -> None:
    screen = pygame.display.get_surface()
    controls_active = True
    while controls_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Controls", screen_width // 2, screen_height // 2 - 200, WHITE)
        ui_text("← → : Move left/right", screen_width // 2, screen_height // 2 - 100, WHITE)
        ui_text("↑ ↓ : Move up/down", screen_width // 2, screen_height // 2, WHITE)
        ui_text("SPACE : Shoot", screen_width // 2, screen_height // 2 + 100, WHITE)
        ui_text("ESC : Pause", screen_width // 2, screen_height // 2 + 150, WHITE)
        ui_text("Click anywhere to close", screen_width // 2, screen_height // 2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                controls_active = False


def show_credits() -> None:
    screen = pygame.display.get_surface()
    credits_active = True
    while credits_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Credits", screen_width // 2, screen_height // 2 - 200, WHITE)
        ui_text("Game Design: Team", screen_width // 2, screen_height // 2 - 100, WHITE)
        ui_text("Programming: Team", screen_width // 2, screen_height // 2, WHITE)
        ui_text("Graphics: Team", screen_width // 2, screen_height // 2 + 100, WHITE)
        ui_text("Click anywhere to close", screen_width // 2, screen_height // 2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                credits_active = False


def show_stats(progress: dict) -> None:
    screen = pygame.display.get_surface()
    stats_active = True
    while stats_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Statistics", screen_width // 2, screen_height // 2 - 200, WHITE)
        ui_text(
            f"Levels Completed: {len(progress['completed'])}",
            screen_width // 2,
            screen_height // 2 - 100,
            WHITE,
        )
        ui_text(
            f"Current Level: {progress['last']}",
            screen_width // 2,
            screen_height // 2,
            WHITE,
        )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                stats_active = False


def show_achievements(progress: dict) -> None:
    screen = pygame.display.get_surface()
    achievements_active = True
    while achievements_active:
        screen.fill((0, 0, 0, 180))
        ui_text("Achievements", screen_width // 2, screen_height // 2 - 200, WHITE)
        if len(progress["completed"]) >= 5:
            ui_text(
                "🏆 Rookie - Complete 5 levels",
                screen_width // 2,
                screen_height // 2 - 100,
                GREEN,
            )
        if len(progress["completed"]) >= 10:
            ui_text(
                "🏆 Veteran - Complete 10 levels",
                screen_width // 2,
                screen_height // 2,
                GREEN,
            )
        if len(progress["completed"]) >= 15:
            ui_text(
                "🏆 Master - Complete 15 levels",
                screen_width // 2,
                screen_height // 2 + 100,
                GREEN,
            )
        ui_text("Click anywhere to close", screen_width // 2, screen_height // 2 + 200, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                achievements_active = False


def level_select(progress: dict) -> None:
    from screen import main_menu

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

    sound_enabled = True
    music_enabled = True

    def toggle_sound() -> None:
        nonlocal sound_enabled
        sound_enabled = not sound_enabled
        print(f"[DEBUG] Sound {'enabled' if sound_enabled else 'disabled'}")

    def toggle_music() -> None:
        nonlocal music_enabled
        music_enabled = not music_enabled
        if music_enabled:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()
        print(f"[DEBUG] Music {'enabled' if music_enabled else 'disabled'}")

    def show_help() -> None:
        help_active = True
        while help_active:
            help_surface = pygame.Surface((600, 400), pygame.SRCALPHA)
            help_surface.fill((30, 30, 30, 240))
            screen.blit(help_surface, (screen_width // 2 - 300, screen_height // 2 - 200))

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
                "Klicke zum Schließen",
            ]

            for i, text in enumerate(help_texts):
                ui_text(text, screen_width // 2 - 250, screen_height // 2 - 150 + i * 30, WHITE)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                    help_active = False
                    break

    menu_buttons = [
        (
            "⚙️ Einstellungen",
            [
                ("🎮 Vollbild", toggle_fullscreen),
                ("🎵 Musik +", lambda: adjust_volume(0.1)),
                ("🎵 Musik -", lambda: adjust_volume(-0.1)),
                ("🔢 FPS anzeigen", toggle_fps),
                ("💾 Speichern", lambda: save_settings(current_settings)),
            ],
        ),
        (
            "🎮 Schwierigkeit",
            [
                ("😊 Leicht", lambda: set_difficulty("easy")),
                ("😐 Normal", lambda: set_difficulty("normal")),
                ("😈 Schwer", lambda: set_difficulty("hard")),
            ],
        ),
        (
            "❔ Hilfe",
            [
                ("📖 Tutorial", show_tutorial),
                ("🎮 Steuerung", show_controls),
                ("ℹ️ Credits", show_credits),
            ],
        ),
        (
            "👤 Profil",
            [
                ("👤 Anmelden", lambda: show_login_screen()),
                ("📊 Statistiken", lambda: show_stats(progress)),
                ("🏆 Erfolge", lambda: show_achievements(progress)),
            ],
        ),
        ("☰ Hauptmenü", lambda: back_button(progress)),
    ]

    print("[DEBUG] level_select variables initialized")

    try:
        bg_path = os.path.join(IMAGE_DIR, "ui_background_levels.jpg")
        print("[DEBUG] Loading level background from:", bg_path)
        background = pygame.image.load(bg_path)
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print("[DEBUG] Error loading level_select background:", e)
        background = None

    def start_level(level_num: int, prog: dict) -> bool:
        print(f"[DEBUG] Starting level {level_num}")
        selected_char = get_selected_char()

        if not selected_char:
            print("[DEBUG] No character selected, redirecting to selection screen")
            selection_screen(prog)
            return False

        from game_loop import game_loop
        try:
            print("[DEBUG] Starting game loop with character")
            result = game_loop(level_num, prog)
            if not result:
                print("[DEBUG] Game loop failed, returning to selection")
                selection_screen(prog)
                return False
            return True
        except Exception as e:
            print(f"[DEBUG] Error in game loop: {e}")
            traceback.print_exc()
            return False

    def back_button(prog: dict) -> bool:
        print("[DEBUG] Back to game menu")
        from game_menu import GameMenu
        menu = GameMenu()
        menu.show(prog)
        return True

    def show_login_screen() -> bool:
        from screen import login_screen
        pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        login_screen()
        return True

    def draw_menu_button() -> None:
        nonlocal menu_open

        menu_btn = pygame.Rect(screen_width - 60, 10, 50, 50)
        pygame.draw.rect(screen, (30, 30, 30, 200), menu_btn, border_radius=10)
        ui_text("☰", menu_btn.centerx - 10, menu_btn.centery - 10, WHITE)

        mx, my = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and menu_btn.collidepoint(mx, my):
            pygame.time.delay(100)
            menu_open = not menu_open

        if menu_open:
            current_y = 70
            for text, action in menu_buttons:
                if isinstance(action, list):
                    btn_rect = pygame.Rect(screen_width - 200, current_y, 190, 50)
                    hover = btn_rect.collidepoint(mx, my)
                    color = (60, 60, 60) if hover else (40, 40, 40)
                    pygame.draw.rect(screen, color, btn_rect, border_radius=10)
                    pygame.draw.rect(screen, WHITE, btn_rect, 1, border_radius=10)
                    ui_text(text, btn_rect.x + 10, btn_rect.centery - 10, WHITE)

                    if hover:
                        sub_x = btn_rect.x - 200
                        sub_y = btn_rect.y
                        for sub_text, sub_action in action:
                            sub_btn = pygame.Rect(sub_x, sub_y, 190, 50)
                            sub_hover = sub_btn.collidepoint(mx, my)
                            sub_color = (70, 70, 70) if sub_hover else (50, 50, 50)
                            pygame.draw.rect(
                                screen,
                                sub_color,
                                sub_btn,
                                border_radius=10,
                            )
                            pygame.draw.rect(screen, WHITE, sub_btn, 1, border_radius=10)
                            ui_text(
                                sub_text,
                                sub_btn.x + 10,
                                sub_btn.centery - 10,
                                WHITE,
                            )

                            if sub_hover and pygame.mouse.get_pressed()[0]:
                                pygame.time.delay(100)
                                sub_action()

                            sub_y += 60
                else:
                    btn_rect = pygame.Rect(screen_width - 200, current_y, 190, 50)
                    hover = btn_rect.collidepoint(mx, my)
                    color = (60, 60, 60) if hover else (40, 40, 40)
                    pygame.draw.rect(screen, color, btn_rect, border_radius=10)
                    pygame.draw.rect(screen, WHITE, btn_rect, 1, border_radius=10)
                    ui_text(text, btn_rect.x + 10, btn_rect.centery - 10, WHITE)

                    if hover and pygame.mouse.get_pressed()[0]:
                        pygame.time.delay(100)
                        action(progress)

                current_y += 60

    while True:
        print("[DEBUG] level_select loop start; selected_level =", selected_level)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))

        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        panel = pygame.Surface((800, 500), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (0, 255, 255, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 400, screen_height // 2 - 400))

        pulse_timer += 1
        ui_text(
            "🌟 LEVEL AUSWÄHLEN",
            screen_width // 2 - 150,
            screen_height // 2 - 450,
            WHITE,
        )

        for i, lvl_cfg in enumerate(LEVELS, start=1):
            x = screen_width // 2 - 300 + ((i - 1) % 3) * 250
            y = screen_height // 2 - 300 + ((i - 1) // 3) * 100 + scroll_offset
            if i in completed:
                col = GREEN
            elif i <= last:
                col = GRAY
            else:
                col = DARK_GRAY
            pygame.draw.rect(screen, col, (x, y, 200, 80), border_radius=8)
            ui_text(f"Level {i}", x + 50, y + 25, WHITE)

            mx, my = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()[0]
            if i <= last and x < mx < x + 200 and y < my < y + 80 and click:
                selected_level = i
                print(f"[DEBUG] Level {selected_level} selected")

        if selected_level is not None:
            x = screen_width // 2 - 300 + ((selected_level - 1) % 3) * 250
            y = screen_height // 2 - 300 + ((selected_level - 1) // 3) * 100 + scroll_offset
            pygame.draw.rect(screen, YELLOW, (x - 5, y - 5, 210, 90), 3)

            start_btn = pygame.Rect(
                screen_width // 2 - 100,
                screen_height // 2 + 150,
                200,
                50,
            )
            mouse_pos = pygame.mouse.get_pos()
            hover = start_btn.collidepoint(mouse_pos)
            pygame.draw.rect(
                screen,
                (0, 255, 0) if hover else (0, 200, 0),
                start_btn,
                border_radius=10,
            )
            pygame.draw.rect(screen, WHITE, start_btn, 2, border_radius=10)

            font = pygame.font.SysFont("arial", 24)
            text_surf = font.render("▶️ Start Level", True, WHITE)
            text_rect = text_surf.get_rect(center=start_btn.center)
            screen.blit(text_surf, text_rect)

            if pygame.mouse.get_pressed()[0] and hover:
                pygame.time.delay(200)
                start_level(selected_level, progress)

        ui_button("🔙 Back", 30, 30, 100, 40, lambda: back_button(progress), hover_color=(200, 50, 50))

        draw_menu_button()

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
                elif e.key == pygame.K_ESCAPE:
                    back_button(progress)
                    return

        scroll_offset = max(min(scroll_offset, 0), -300)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
