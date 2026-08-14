import pygame
import sys
import os
import json
import random
import math

# -----------------------------------------------------------------------------
# 1) KONSTANTEN & GLOBALS
# -----------------------------------------------------------------------------
ASSET_DIR    = r"D:\progaming\selbst_visual_sudio_code\sachen_für_aha_game"
USER_FILE    = os.path.join(ASSET_DIR, "users.json")

UI_WIDTH, UI_HEIGHT = 800, 600
GAME_W, GAME_H     = 1600, 1000

WHITE     = (255,255,255)
BLACK     = (  0,  0,  0)
GRAY      = (200,200,200)
DARK_GRAY = (150,150,150)
GREEN     = (  0,200,  0)
RED       = (200,  0,  0)
PINK      = (255,192,203)
YELLOW    = (255,255,  0)

pygame.init()
pygame.mixer.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Level‑Definitionen: Hintergrund, Gegner-Speed, Gegner-Anzahl, Punkte zum Abschließen
LEVELS = [
    { "bg":"ahabild1.png", "speed":3,  "count":3,  "threshold":10  },
    { "bg":"ahabild2.png", "speed":5,  "count":5,  "threshold":30 },
    { "bg":"ahabild3.png", "speed":7,  "count":7,  "threshold":45 },
    { "bg":"ahabild4.png", "speed":4,  "count":4,  "threshold":20  },
    { "bg":"ahabild5.png", "speed":4,  "count":6,  "threshold":25  },
    { "bg":"ahabild6.png", "speed":5,  "count":5,  "threshold":35  },
    { "bg":"ahabild7.png", "speed":6,  "count":6,  "threshold":40  },
    { "bg":"ahabild8.png", "speed":6,  "count":7,  "threshold":45  },
    { "bg":"ahabild9.png", "speed":7,  "count":7,  "threshold":50  },
    { "bg":"ahabild10.png","speed":7,  "count":8,  "threshold":55  },
    { "bg":"ahabild11.png","speed":8,  "count":8,  "threshold":60  },
    { "bg":"ahabild12.png","speed":8,  "count":9,  "threshold":65  },
    { "bg":"ahabild13.png","speed":9,  "count":9,  "threshold":70  },
    { "bg":"ahabild14.png","speed":9,  "count":10, "threshold":75  },
    { "bg":"ahabild15.png","speed":10, "count":10, "threshold":80  },
    { "bg":"ahabild16.png","speed":10, "count":11, "threshold":85  },
    { "bg":"ahabild17.png","speed":11, "count":11, "threshold":90  },
    { "bg":"ahabild18.png","speed":11, "count":12, "threshold":95  },
    { "bg":"ahabild19.png","speed":12, "count":12, "threshold":100 },
    { "bg":"ahabild20.png","speed":12, "count":13, "threshold":105 },
    { "bg":"ahabild21.png","speed":13, "count":13, "threshold":110 },
    { "bg":"ahabild22.png","speed":13, "count":14, "threshold":115 },
    { "bg":"ahabild23.png","speed":14, "count":14, "threshold":120 },
]

CHAR_SPRITES = ["butterfly.png", "dino.png", "demon.png"]

# Buttons im Spiel
pause_button     = pygame.Rect(GAME_W-110, 10,    100, 40)
resume_button    = pygame.Rect(GAME_W//2-100, GAME_H//2-60, 200,50)
restart_button   = pygame.Rect(GAME_W//2-100, GAME_H//2+10, 200,50)
quit_button      = pygame.Rect(GAME_W//2-100, GAME_H//2+80, 200,50)
try_again_button = pygame.Rect(GAME_W//2-100, GAME_H//2-25, 200,50)

# Initialisiere die Kugeln, die letzte Schusszeit und das Intervall
bullets = []  # Liste für die Kugeln
last_shot = 0  # Der Zeitpunkt der letzten Schüsse
shoot_interval = 500  # Zeitintervall zwischen den Schüssen in Millisekunden

# -----------------------------------------------------------------------------
# 2) INITIALISIERUNG
# -----------------------------------------------------------------------------
shoot_channel = pygame.mixer.Channel(0)  # NEW: Dedicated channel for shooting sound
clock = pygame.time.Clock()

# UI-Fenster & Schrift
ui_screen = pygame.display.set_mode((UI_WIDTH, UI_HEIGHT))
pygame.display.set_caption("Login / Register")
FONT = pygame.font.SysFont(None, 40)

# Zustand nach Login
current_user = None
selected_char_img = None
selected_bg_img   = None
current_progress  = None  # NEW: Global persistent progress

# -----------------------------------------------------------------------------
# 3) PERSISTENCE
# -----------------------------------------------------------------------------
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE,"r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE,"w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(u, p):
    u = str(u)  # <--- Benutzername immer als String
    users = load_users()
    if u in users:
        return False, "❌ Benutzer existiert schon!"
    users[u] = { "password": p, "progress": {"last": 1, "completed": []} }
    save_users(users)
    return True, "✅ Registrierung erfolgreich!"

def login_user(u, p):
    u = str(u)  # <--- Benutzername immer als String
    users = load_users()
    if u in users and users[u]["password"] == p:
        return True, users[u]["progress"]
    return False, "❌ Login fehlgeschlagen!"


def save_progress(level, prog):
    users = load_users()
    pr = users[current_user]["progress"]
    if level not in pr["completed"]:
        pr["completed"].append(level)
    pr["last"] = min(level+1, len(LEVELS))
    save_users(users)
    # Aktualisiere das progress-Objekt, damit level_select() den neuen Stand sieht
    prog["completed"] = pr["completed"]
    prog["last"] = pr["last"]


# -----------------------------------------------------------------------------
# 4) UI-HILFSFUNKTIONEN
# -----------------------------------------------------------------------------
def ui_text(txt,x,y,color=BLACK,surf=None):
    s = surf or ui_screen
    r = FONT.render(txt,True,color)
    s.blit(r,(x,y))

def ui_button(text, x, y, w, h, callback, surf=None, hover_color=(180, 0, 0)):  # Added surf parameter
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    is_hover = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = hover_color if is_hover else (180, 0, 0)

    pygame.draw.rect(surf or screen, color, (x, y, w, h), border_radius=8)  # Use surf if provided
    ui_text(text, x + w // 2 - FONT.size(text)[0] // 2, y + h // 2 - FONT.get_height() // 2, WHITE, surf)

    if is_hover and click[0]:
        callback()

class InputBox:
    def __init__(self, x, y, w, h, password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.active = False
        self.password = password

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)  # Graue Hintergrundfarbe
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Schwarzer Rand
        display_text = "*" * len(self.text) if self.password else self.text
        surface.blit(FONT.render(display_text, True, BLACK), (self.rect.x + 5, self.rect.y + 5))

class Button:
    def __init__(self, x, y, w, h, text, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)  # Graue Hintergrundfarbe
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Schwarzer Rand
        surface.blit(FONT.render(self.text, True, BLACK), (self.rect.x + 10, self.rect.y + 10))

# -----------------------------------------------------------------------------
# 5) UI-SCREENS
# -----------------------------------------------------------------------------
def exit_game():
    pygame.quit()
    sys.exit()

def main_menu():
    global current_user, current_progress

    # Ensure the screen is set to fullscreen mode
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    pulse_timer = 0

    try:
        background = pygame.image.load("D:/progaming/selbst_visual_sudio_code/sachen_für_aha_game/ui_background_menu.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = None

    while True:
        # Hintergrund & Overlay
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # Panel
        panel = pygame.Surface((600, 400), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (255, 255, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 200))

        # Animierte Titel-Schrift (pulsierend)
        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (255, pulse, 0)
        draw_text_big("🎮 HAUPTMENÜ", screen_width // 2, screen_height // 2 - 250, pulse_color)

        # Buttons mit pulsierenden Farben
        login_color = (255, 50 + int(50 * math.sin(pulse_timer * 0.1)), 50)
        register_color = (50, 255, 50 + int(50 * math.sin(pulse_timer * 0.1)))
        exit_color = (255, 50, 50 + int(50 * math.sin(pulse_timer * 0.1)))

        ui_button("🔐 Login", screen_width // 2 - 150, screen_height // 2 - 100, 300, 60, login_screen, hover_color=login_color)
        ui_button("📝 Register", screen_width // 2 - 150, screen_height // 2, 300, 60, register_screen, hover_color=register_color)
        ui_button("❌ Exit", screen_width // 2 - 150, screen_height // 2 + 100, 300, 60, exit_game, hover_color=exit_color)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit_game()

        pygame.display.flip()
        clock.tick(60)

def draw_text_big(text, x, y, color):
    font = pygame.font.SysFont("arial", 64, bold=True)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(x, y))
    screen.blit(text_surf, text_rect)

def draw(self, screen, highlight=False):
    txt_surface = self.font.render(self.text, True, self.color)
    width = max(self.rect.w, txt_surface.get_width() + 10)
    self.rect.w = width
    screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
    if self.active and highlight:
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 3)
    else:
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Registrierungsbildschirm
def register_screen():
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
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
        background = pygame.image.load("D:/progaming/selbst_visual_sudio_code/sachen_für_aha_game/ui_background_register.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = None

    while True:
        # Hintergrund & Overlay
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # Panel
        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (0, 255, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 120))

        # Animierte Titel-Schrift (pulsierend)
        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (0, pulse, 255)
        draw_text_big("📝 REGISTRIEREN", screen_width // 2, screen_height // 2 - 160, pulse_color)

        # Eingabe-Labels & Felder
        ui_text("Benutzername:", ib_u.rect.x, ib_u.rect.y - 25, (0, 255, 0))
        ib_u.draw(screen)

        ui_text("Passwort:", ib_p.rect.x, ib_p.rect.y - 25, (0, 255, 0))
        ib_p.draw(screen)

        # Buttons mit Hover
        ui_button("🔙 Back", 30, 30, 100, 40, main_menu, hover_color=(200, 50, 50))
        ui_button("✅ Registrieren", center_x, screen_height // 2 + 110, input_width, 50, do_reg, hover_color=(50, 200, 50))

        # Feedback
        if msg:
            color = GREEN if msg.startswith("✅") else RED
            ui_text(msg, screen_width // 2 - FONT.size(msg)[0] // 2, screen_height // 2 + 170, color)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.display.set_mode((UI_WIDTH, UI_HEIGHT))
                main_menu()
                return
            ib_u.handle(e)
            ib_p.handle(e)

        pygame.display.flip()
        clock.tick(60)


def login_screen():
    global current_user, current_progress

    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
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
        global current_user, current_progress
        ok, res = login_user(ib_u.text, ib_p.text)
        if ok:
            current_user = ib_u.text
            progress = res
            current_progress = res
        else:
            msg = res

    try:
        background = pygame.image.load("D:/progaming/selbst_visual_sudio_code/sachen_für_aha_game/ui_background_login.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = None

    while True:
        # Hintergrund & Overlay
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # Panel
        panel = pygame.Surface((600, 300), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (255, 0, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 300, screen_height // 2 - 120))

        # Animierte Titel-Schrift (pulsierend)
        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (255, pulse, pulse)
        draw_text_big("🔐 LOGIN", screen_width // 2, screen_height // 2 - 160, pulse_color)

        # Eingabe-Labels & Felder
        ui_text("Username:", ib_u.rect.x, ib_u.rect.y - 25, (255, 0, 0))
        ib_u.draw(screen)  # Removed highlight argument

        ui_text("Password:", ib_p.rect.x, ib_p.rect.y - 25, (255, 0, 0))
        ib_p.draw(screen)  # Removed highlight argument

        # Buttons mit Hover
        ui_button("🔙 Back", 30, 30, 100, 40, main_menu, hover_color=(200, 50, 50))
        ui_button("🚀 Login", center_x, screen_height // 2 + 110, input_width, 50, do_log, hover_color=(200, 50, 50))

        # Feedback
        if msg:
            color = GREEN if msg.startswith("✅") else RED
            ui_text(msg, screen_width // 2 - FONT.size(msg)[0] // 2, screen_height // 2 + 170, color)

        if progress is not None:
            pygame.time.delay(300)
            level_select(progress)
            return

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                pygame.display.set_mode((UI_WIDTH, UI_HEIGHT))
                main_menu()
                return
            ib_u.handle(e)
            ib_p.handle(e)

        pygame.display.flip()
        clock.tick(60)

ui_button("Login", 250, 250, 300, 60, login_screen, hover_color=(200, 50, 50))

def level_select(progress):
    global current_user, current_progress

    # Ensure the screen is set to fullscreen mode
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    completed = progress["completed"]
    last = progress["last"]
    scroll_offset = 0
    pulse_timer = 0
    selected_level = None  # Track the selected level

    try:
        background = pygame.image.load("D:/progaming/selbst_visual_sudio_code/sachen_für_aha_game/ui_background_levels.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = None

    try:
        while True:
            # Hintergrund & Overlay
            if background:
                screen.blit(background, (0, 0))
            else:
                screen.fill((10, 10, 10))
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))

            # Panel
            panel = pygame.Surface((800, 600), pygame.SRCALPHA)
            panel.fill((30, 30, 30, 200))
            pygame.draw.rect(panel, (0, 255, 255, 100), panel.get_rect(), 2)
            screen.blit(panel, (screen_width // 2 - 400, screen_height // 2 - 300))

            # Animierte Titel-Schrift (pulsierend)
            pulse_timer += 1
            pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
            pulse_color = (0, pulse, 255)
            draw_text_big("🌟 LEVEL AUSWÄHLEN", screen_width // 2, screen_height // 2 - 350, pulse_color)

            # Level-Buttons mit Scroll-Offset
            for i in range(len(LEVELS)):
                x = screen_width // 2 - 300 + (i % 3) * 250
                y = screen_height // 2 - 200 + (i // 3) * 100 + scroll_offset
                lvl = i + 1
                if lvl in completed:
                    col = GREEN
                elif lvl <= last:
                    col = GRAY
                else:
                    col = DARK_GRAY
                pygame.draw.rect(screen, col, (x, y, 200, 80), border_radius=8)
                ui_text(f"Level {lvl}", x + 50, y + 25, WHITE)

                # Check for hover and click
                mx, my = pygame.mouse.get_pos()
                click = pygame.mouse.get_pressed()[0]
                if lvl <= last and x < mx < x + 200 and y < my < 80 and click:
                    selected_level = lvl  # Set the selected level

            # Highlight the selected level
            if selected_level is not None:
                x = screen_width // 2 - 300 + ((selected_level - 1) % 3) * 250
                y = screen_height // 2 - 200 + ((selected_level - 1) // 3) * 100 + scroll_offset
                pygame.draw.rect(screen, YELLOW, (x - 5, y - 5, 210, 90), 3)

            # OK Button
            ui_button("✅ OK", screen_width // 2 - 75, screen_height // 2 + 250, 150, 50, 
                      lambda: game_loop(selected_level if selected_level is not None else last, progress), 
                      hover_color=(50, 200, 50))

            # Back Button
            ui_button("🔙 Back", 30, 30, 100, 40, main_menu, hover_color=(200, 50, 50))

            # Scroll-Handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.MOUSEWHEEL:
                    scroll_offset += e.y * 20
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_UP:
                        scroll_offset -= 20
                    elif e.key == pygame.K_DOWN:
                        scroll_offset += 20

            # Begrenze den Scroll-Offset
            scroll_offset = max(min(scroll_offset, 0), -300)

            pygame.display.flip()
            clock.tick(60)
    except Exception as e:
        print("[DEBUG] Exception in level_select loop:", e)
        main_menu()

def logout_user():
    global current_user, current_progress
    current_user = None
    current_progress = None
    main_menu()

def selection_screen():
    """Charakter-Auswahl vor jedem Level."""
    global selected_char_img

    # Ensure the screen is set to fullscreen mode
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

    chars = [load_image(fn, (120, 120)) for fn in CHAR_SPRITES]
    idx_c = 0
    pulse_timer = 0

    try:
        background = pygame.image.load("D:/progaming/selbst_visual_sudio_code/sachen_für_aha_game/ui_background_characters.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except:
        background = None

    def confirm_selection():
        global selected_char_img
        selected_char_img = load_image(CHAR_SPRITES[idx_c], (80, 80))  # Load the selected character image
        pygame.time.delay(200)  # Add a small delay for better UX
        game_loop(current_progress["last"], current_progress)  # Proceed to the game loop

    while True:
        # Hintergrund & Overlay
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # Panel
        panel = pygame.Surface((800, 400), pygame.SRCALPHA)
        panel.fill((30, 30, 30, 200))
        pygame.draw.rect(panel, (255, 255, 0, 100), panel.get_rect(), 2)
        screen.blit(panel, (screen_width // 2 - 400, screen_height // 2 - 200))

        # Animierte Titel-Schrift (pulsierend)
        pulse_timer += 1
        pulse = 128 + int(127 * math.sin(pulse_timer * 0.05))
        pulse_color = (255, pulse, 0)
        draw_text_big("🦸 CHARAKTER WÄHLEN", screen_width // 2, screen_height // 2 - 250, pulse_color)

        # Charaktere anzeigen
        for i, img in enumerate(chars):
            x = screen_width // 2 - (len(chars) * 150) // 2 + i * 150
            y = screen_height // 2 - 100
            screen.blit(img, (x, y))
            if i == idx_c:
                pygame.draw.rect(screen, GREEN, (x - 5, y - 5, 130, 130), 3)  # Highlight selected character

        # OK-Button
        ui_button("✅ OK", screen_width // 2 - 75, screen_height // 2 + 150, 150, 50, confirm_selection, hover_color=(50, 200, 50))

        # Navigation
        mx, my = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    idx_c = (idx_c - 1) % len(chars)
                elif e.key == pygame.K_RIGHT:
                    idx_c = (idx_c + 1) % len(chars)
                elif e.key == pygame.K_RETURN:
                    confirm_selection()
                    return
            if e.type == pygame.MOUSEBUTTONDOWN:
                for i, img in enumerate(chars):
                    x = screen_width // 2 - (len(chars) * 150) // 2 + i * 150
                    y = screen_height // 2 - 100
                    if pygame.Rect(x, y, 120, 120).collidepoint(mx, my):
                        idx_c = i

        pygame.display.flip()
        clock.tick(60)

# -----------------------------------------------------------------------------
# 6) KLASSEN & SPIEL-FUNKTIONEN
# -----------------------------------------------------------------------------
def load_image(fn, size=None):
    path = os.path.join(ASSET_DIR, fn)
    img  = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size) if size else img

class Player:
    def __init__(self, img):
        self.img = img
        self.w, self.h = img.get_size()
        self.x = GAME_W//2 - self.w//2
        self.y = GAME_H - self.h - 10
        self.speed = 5
        self.original_speed = self.speed
        self.power_up_end = 0  # Für Temp.-Speed-Boost
        # Neue Attribute:
        self.shield_active = False
        self.shield_end = 0
        self.double_shoot = False
        self.double_shoot_end = 0

    def move(self, keys):
        if pygame.time.get_ticks() > self.power_up_end:
            self.speed = self.original_speed
        if pygame.time.get_ticks() > self.shield_end:
            self.shield_active = False
        if pygame.time.get_ticks() > self.double_shoot_end:
            self.double_shoot = False
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < GAME_W - self.w:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < GAME_H - self.h:
            self.y += self.speed

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        # Zeichne Schild als Kreis um den Spieler, wenn aktiv
        if self.shield_active:
            pygame.draw.circle(surface, (0,255,255), (self.x + self.w//2, self.y + self.h//2), max(self.w, self.h)//2 + 5, 3)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Enemy:
    def __init__(self, img, speed):
        self.img = img; self.w,self.h=img.get_size()
        self.speed = speed; self.reset()
    def reset(self):
        self.x = random.randint(0,GAME_W-self.w); self.y = -self.h
    def move(self):
        self.y += self.speed
        if self.y > GAME_H: self.reset()
    def draw(self,s): s.blit(self.img,(self.x,self.y))
    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)

class FastEnemy(Enemy):
    def move(self):
        # Schneller als der Standard-Gegner
        self.y += self.speed * 1.5
        if self.y > GAME_H:
            self.reset()

class TeleportingEnemy(Enemy):
    def __init__(self, img, speed):
        super().__init__(img, speed)
        self.invincible = False
        self.invincible_end = 0

    def move(self):
        if random.random() < 0.01:
            self.x = random.randint(0, GAME_W - self.w)
            self.invincible = True
            self.invincible_end = pygame.time.get_ticks() + 1000  # 1 Sekunde invincible
        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.invincible = False
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()

    def draw(self, s):
        if self.invincible:
            # Erzeuge einen verschwommenen Effekt, indem das Bild verkleinert und wieder hochskaliert wird.
            blurred = pygame.transform.smoothscale(self.img, (self.w//2, self.h//2))
            blurred = pygame.transform.smoothscale(blurred, (self.w, self.h))
            s.blit(blurred, (self.x, self.y))
        else:
            s.blit(self.img, (self.x, self.y))

class SpeedBoost:
    def __init__(self):
        self.size = 25
        self.reset()
    def reset(self):
        self.x = random.randint(0, GAME_W - self.size)
        self.y = -self.size
        self.speed = 3
    def move(self):
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()
    def draw(self, s):
        pygame.draw.circle(s, (0,255,0), (self.x + self.size//2, self.y + self.size//2), self.size//2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class UnbreakableEnemy:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x,y,w,h); self.color=color; self.speed=3
    def move(self):
        self.rect.y += self.speed
        if self.rect.y > GAME_H: self.rect.y = -self.rect.h; self.rect.x = random.randint(0,GAME_W-self.rect.w)
    def draw(self,s): pygame.draw.rect(s,self.color,self.rect)
    def check(self, pr): return pr.colliderect(self.rect)

class PowerUp:
    def __init__(self):
        self.size = 30; self.reset()
    def reset(self):
        self.x = random.randint(0,GAME_W-self.size); self.y = -self.size; self.speed=4
    def move(self):
        self.y += self.speed
        if self.y>GAME_H: self.reset()
    def draw(self,s):
        pts = [(self.x+self.size//2,self.y),(self.x,self.y+self.size//2),
               (self.x+self.size//2,self.y+self.size),(self.x+self.size,self.y+self.size//2)]
        pygame.draw.polygon(s,YELLOW,pts)
    def rect(self): return pygame.Rect(self.x,self.y,self.size,self.size)

class ShieldPowerUp:
    def __init__(self):
        self.size = 30
        self.reset()
    def reset(self):
        self.x = random.randint(0, GAME_W - self.size)
        self.y = -self.size
        self.speed = 4
    def move(self):
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()
    def draw(self, s):
        # Zyan-Farbe für den Schild
        pygame.draw.circle(s, (0,255,255), (self.x + self.size//2, self.y + self.size//2), self.size//2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class DoubleShootingPowerUp:
    def __init__(self):
        self.size = 30
        self.reset()
    def reset(self):
        self.x = random.randint(0, GAME_W - self.size)
        self.y = -self.size
        self.speed = 4
    def move(self):
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()
    def draw(self, s):
        # Lila Farbe
        pygame.draw.circle(s, (255,0,255), (self.x + self.size//2, self.y + self.size//2), self.size//2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class TimeSlowPowerUp:
    def __init__(self):
        self.size = 30
        self.reset()
    def reset(self):
        self.x = random.randint(0, GAME_W - self.size)
        self.y = -self.size
        self.speed = 4
    def move(self):
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()
    def draw(self, s):
        # Gelb für Zeitverlangsamung
        pygame.draw.circle(s, (255,255,0), (self.x + self.size//2, self.y + self.size//2), self.size//2)
    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class BossEnemy:
    def __init__(self):
        self.w,self.h = 200,200
        self.x,self.y = GAME_W//2-self.w//2, -self.h
        self.speed=2; self.dir=1; self.health=20
    def move(self):
        if self.y < 50: self.y += 2
        else:
            self.x += self.speed*self.dir
            if self.x<=0 or self.x>=GAME_W-self.w: self.dir *= -1
    def draw(self,s):
        pygame.draw.rect(s,(0,0,255),(self.x,self.y,self.w,self.h))
        pygame.draw.rect(s,RED,(GAME_W-210,10,self.health*10,20))
    def rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)

import math

class BaseBoss:
    def __init__(self, health, speed):
        self.health = health
        self.max_health = health
        self.speed  = speed
        self.w, self.h = 200, 200
        self.x = GAME_W//2 - self.w//2
        self.y = -self.h
        self.start_time = pygame.time.get_ticks()
        
    def move(self):
        if self.y < 50:
            self.y += self.speed
        else:
            t = (pygame.time.get_ticks() - self.start_time) / 1000.0
            self.x = (GAME_W//2 - self.w//2) + int(200 * math.sin(t * 2))
            
    def draw(self, s):
        pygame.draw.rect(s, (0, 0, 255), (self.x, self.y, self.w, self.h))
        bar_width = 300; bar_height = 20
        bar_x = (GAME_W - bar_width)//2; bar_y = 10
        health_ratio = max(self.health / self.max_health, 0)
        filled_width = int(bar_width * health_ratio)
        pygame.draw.rect(s, RED,   (bar_x, bar_y, filled_width, bar_height))
        pygame.draw.rect(s, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class BossType1(BaseBoss):
    # Einfacher Boss für niedrigere Levels
    def __init__(self):
        super().__init__(health=20, speed=2)

class BossType2(BaseBoss):
    # Boss mit leicht diagonaler Bewegung
    def __init__(self):
        super().__init__(health=30, speed=3)
        self.dir = 1
    def move(self):
        if self.y < 50:
            self.y += self.speed
        else:
            self.x += self.speed * self.dir
            if self.x <= 0 or self.x >= GAME_W - self.w:
                self.dir *= -1

class BossType3(BaseBoss):
    # Boss bewegt sich schnell nach unten und dann in einer komplexeren Sinusbewegung
    def __init__(self):
        super().__init__(health=40, speed=3)
    def move(self):
        if self.y < 100:
            self.y += self.speed * 2
        else:
            t = (pygame.time.get_ticks() - self.start_time) / 1000.0
            self.x = (GAME_W//2 - self.w//2) + int(250 * math.sin(t * 3))

# In fire_bullet:
# Diese Funktion feuert eine Kugel, wenn der Spieler die Leertaste drückt und das Intervall abgelaufen ist.
def fire_bullet(bullets, player, shoot_sound, last, interval):
    now = pygame.time.get_ticks()
    if now - last >= interval:
        bx = player.x + player.w//2 - 2
        by = player.y
        bullets.append(pygame.Rect(bx, by, 4, 10))
        # Wenn doppeltes Schießen aktiv ist, feuere eine zweite Kugel leicht seitlich
        if player.double_shoot:
            bullets.append(pygame.Rect(bx + 10, by, 4, 10))
        try:
            if not shoot_channel.get_busy():
                shoot_channel.play(shoot_sound)
        except Exception as e:
            print("Fehler beim Abspielen des Schusssounds:", e)
        return now
    return last

def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= 5  # Bewege die Kugel nach oben (y-Wert verringern)
        
        # Entferne die Kugel, wenn sie den Bildschirm verlässt
        if bullet.y < 0:
            bullets.remove(bullet)
def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)  # Zeichne die Kugeln (rote Farbe)

def draw_text(s, txt, size, color, x, y, outline_color=WHITE):
    f = pygame.font.Font(None, size)
    # Zeichne Outline in 8 Richtungen
    text = f.render(txt, True, color)
    rect = text.get_rect(center=(x, y))
    for dx in (-1,0,1):
        for dy in (-1,0,1):
            outline = f.render(txt, True, outline_color)
            s.blit(outline, (rect.x+dx, rect.y+dy))
    s.blit(text, rect)

# Neue Funktion zur Kollisionsbehandlung (Overlay)
def collision_overlay(scr, bg, level, progress):
    while True:
        scr.blit(bg, (0, 0))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                return "restart"
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if try_again_button.collidepoint(mx, my):
                    return "restart"
                if quit_button.collidepoint(mx, my):
                    return "quit"
        overlay = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        scr.blit(overlay, (0, 0))
        pygame.draw.rect(scr, GREEN, try_again_button)
        pygame.draw.rect(scr, RED, quit_button)
        draw_text(scr, "Try Again", 30, BLACK, try_again_button.centerx, try_again_button.centery)
        draw_text(scr, "Quit", 30, BLACK, quit_button.centerx, quit_button.centery)
        pygame.display.flip()
        clock.tick(30)

def game_loop(level, progress):
    if selected_char_img is None:
        print("Fehler: Kein Charakter ausgewählt!")
        selection_screen()  # Sicherstellen, dass ein Bild gesetzt wird

    ply = Player(selected_char_img)
    scr = pygame.display.set_mode((GAME_W, GAME_H), pygame.FULLSCREEN)
    pygame.display.set_caption(f"Level {level}")
    
    # Level‑Daten
    cfg = LEVELS[level-1]
    bg = load_image(cfg["bg"], (GAME_W, GAME_H))
    speed = cfg["speed"]
    count = cfg["count"]
    thresh = cfg["threshold"]
    
    # Gegnertyp (normaler Modus)
    enemy_cls = Enemy
    if 4 <= level <= 10:
        enemy_cls = FastEnemy
    elif 11 <= level <= 15:
        enemy_cls = TeleportingEnemy
    enemies = [enemy_cls(load_image(CHAR_SPRITES[1], (60,60)), speed) for _ in range(count)]
    
    unb = UnbreakableEnemy(400, 100, 40, 40, YELLOW)
    pu = PowerUp()
    boss = None
    shoot_sound = pygame.mixer.Sound(os.path.join(ASSET_DIR, "laser.mp3"))
    speed_boost = SpeedBoost() if level >= 17 else None

    bullets = []
    last_shot = 0
    interval = 200
    score = 0
    boss_active = False
    collision = False
    clock = pygame.time.Clock()
    
    # Power‑Ups
    shield_powerup = ShieldPowerUp()
    double_shoot_powerup = DoubleShootingPowerUp() if level >= 10 else None
    timeslow_powerup = TimeSlowPowerUp() if level >= 15 else None
    slow_factor = 1.0
    slow_end = 0

    # Kurze "Ready"-Phase
    loading_time = 1500  # in Millisekunden
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < loading_time:
        scr.blit(bg, (0, 0))
        draw_text(scr, "Ready...", 50, BLACK, GAME_W//2, GAME_H//2)
        pygame.display.flip()
        clock.tick(60)
    
    while True:
        dt = clock.tick(60)
        scr.blit(bg, (0, 0))
        mx, my = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        # Cheat key: If "C" is pressed, set score to threshold (full level)
        if keys[pygame.K_c]:
            score = thresh

        # Bullets aktualisieren
        move_bullets(bullets)
        draw_bullets(scr, bullets)
        
        # Normale Gegnerphase, sofern kein Boss aktiv
        if not boss_active:
            for bullet in bullets[:]:
                for enemy in enemies:
                    if bullet.colliderect(enemy.rect()):
                        bullets.remove(bullet)
                        enemy.reset()
                        score += 1
                        break
            for en in enemies:
                en.move()
                if ply.rect().colliderect(en.rect()):
                    if isinstance(en, TeleportingEnemy) and en.invincible:
                        continue
                    collision = True
           # Falls der Score den Threshold erreicht und noch kein Boss aktiv ist
            if not boss_active and score >= thresh:
                boss_active = True
                boss_entry_delay = pygame.time.get_ticks() + 1000  # 1 Sekunde Grace Period
                print("Boss aktiviert, Delay bis:", boss_entry_delay)
                enemies = []          # Normale Gegner entfernen
                      # Kugeln löschen
                pygame.time.delay(500)  # Kurze Pause
                if level < 5:
                    boss = BossType1()
                elif level < 10:
                    boss = BossType2()
                else:
                    boss = BossType3()
        else:
            # Bossphase: Stelle sicher, dass boss existiert
            if boss is None:
                if level < 5:
                    boss = BossType1()
                elif level < 10:
                    boss = BossType2()
                else:
                    boss = BossType3()
            boss.move()

# Prüfe die Kollision erst, wenn die Grace Period vorbei ist
            if pygame.time.get_ticks() > boss_entry_delay:
                if ply.rect().colliderect(boss.rect()):
                    collision = True

            # NEW: Safely handle bullet–boss collisions
            hit_bullets = []
            for b in bullets:
                if boss.rect().colliderect(b):
                    boss.health -= 1
                    hit_bullets.append(b)
            for b in hit_bullets:
                bullets.remove(b)

            if boss.health <= 0:
                save_progress(level, progress)
                level_select(progress)
                return

        # Unzerstörbarer Gegner und PowerUp von PU
        unb.move()
        if unb.check(ply.rect()):
            collision = True
        pu.move()
        if pu.rect().colliderect(ply.rect()):
            bullets.clear()
            pu.reset()
            ply.speed += 3
            ply.power_up_end = pygame.time.get_ticks() + 5000

        if speed_boost:
            speed_boost.move()
            speed_boost.draw(scr)
            if ply.rect().colliderect(speed_boost.rect()):
                ply.speed += 2
                speed_boost.reset()
        
        # Integration der Power‑Ups
        shield_powerup.move()
        shield_powerup.draw(scr)
        if shield_powerup.rect().colliderect(ply.rect()):
            shield_powerup.reset()
            ply.shield_active = True
            ply.shield_end = pygame.time.get_ticks() + 5000
        
        if double_shoot_powerup:
            double_shoot_powerup.move()
            double_shoot_powerup.draw(scr)
            if double_shoot_powerup.rect().colliderect(ply.rect()):
                double_shoot_powerup.reset()
                ply.double_shoot = True
                ply.double_shoot_end = pygame.time.get_ticks() + 5000
        
        if timeslow_powerup:
            timeslow_powerup.move()
            timeslow_powerup.draw(scr)
            if timeslow_powerup.rect().colliderect(ply.rect()):
                timeslow_powerup.reset()
                slow_factor = 0.5
                slow_end = pygame.time.get_ticks() + 5000

        # Zeitverlangsamung auf Gegner anwenden (nur im normalen Modus)
        if not boss_active:
            for en in enemies:
                original_speed = en.speed
                if pygame.time.get_ticks() < slow_end:
                    en.speed = original_speed * slow_factor
                else:
                    en.speed = original_speed
                en.move()  # Nochmal aufrufen, um die Änderung zu übernehmen
                if ply.rect().colliderect(en.rect()):
                    if isinstance(en, TeleportingEnemy) and en.invincible:
                        continue
                    collision = True

        # Ereignis‑Verarbeitung
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(mx, my):
                    collision = True
                if collision and resume_button.collidepoint(mx, my):
                    collision = False
                if collision and quit_button.collidepoint(mx, my):
                    save_progress(level, progress)
                    level_select(progress)
                    return
        
        # Spieler und Schießen, sofern keine Kollision vorliegt
        if not collision:
            ply.move(keys)
            if keys[pygame.K_SPACE]:
                last_shot = fire_bullet(bullets, ply, shoot_sound, last_shot, interval)

        # Zeichne alle Objekte
        ply.draw(scr)
        if not boss_active:
            for en in enemies:
                en.draw(scr)
        else:
            if boss:
                boss.draw(scr)
        unb.draw(scr)
        pu.draw(scr)
        for b in bullets:
            pygame.draw.rect(scr, BLACK, b)
        draw_text(scr, f"{score}/{thresh}", 30, BLACK, 70, 30)
        pygame.draw.rect(scr, WHITE, pause_button)
        draw_text(scr, "Pause", 20, BLACK, pause_button.centerx, pause_button.centery)
        
        # Bei Kollision: Overlay anzeigen und Aktion abfragen
        if collision:
            choice = collision_overlay(scr, bg, level, progress)
            if choice == "restart":
                return game_loop(level, progress)
            elif choice == "quit":
                save_progress(level, progress)
                return level_select(progress)
        
        pygame.display.flip()

# -----------------------------------------------------------------------------
# 7) ENTRYPOINT
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main_menu()
