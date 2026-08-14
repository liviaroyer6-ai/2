"""
Apple-Style Levelauswahl für ein Pygame-Spiel.

Datei ist eigenständig:
    - python level_select.py startet nur die Levelseite
    - später kannst du die Logik (ausgewähltes Level) in dein Spiel übernehmen
"""

import sys
import pygame

# ---------------------------------------------------------
# Grundkonfiguration
# ---------------------------------------------------------

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Levelauswahl")

CLOCK = pygame.time.Clock()
FPS = 60

# Farben (Apple-inspirierter, cleaner Look)
BG_COLOR = (245, 246, 250)       # sehr helles Grau
CARD_COLOR = (255, 255, 255)     # weiß für Levelkarten
CARD_BORDER_COLOR = (220, 220, 230)
PRIMARY_COLOR = (52, 152, 219)   # dezentes Blau für aktive Elemente
TEXT_COLOR = (30, 30, 40)        # dunkles Grau für Text
LOCKED_COLOR = (180, 180, 190)   # ausgegraut für gesperrte Levels
STAR_COLOR = (241, 196, 15)      # gelbes Star-Icon

# Fonts (systemnah, damit es überall funktioniert)
TITLE_FONT = pygame.font.SysFont("arial", 40, bold=True)
SUBTITLE_FONT = pygame.font.SysFont("arial", 22)
LEVEL_FONT = pygame.font.SysFont("arial", 24, bold=True)
INFO_FONT = pygame.font.SysFont("arial", 18)

# ---------------------------------------------------------
# Level-Definition (passt du später an dein Spiel an)
# ---------------------------------------------------------

LEVELS = [
    {"name": "Level 1", "stars": 3, "locked": False},
    {"name": "Level 2", "stars": 2, "locked": False},
    {"name": "Level 3", "stars": 1, "locked": False},
    {"name": "Level 4", "stars": 0, "locked": True},
    {"name": "Level 5", "stars": 0, "locked": True},
    {"name": "Level 6", "stars": 0, "locked": True},
]

# Layout: Kartenraster
CARD_WIDTH = 220
CARD_HEIGHT = 120
CARD_MARGIN_X = 40
CARD_MARGIN_Y = 30
GRID_COLUMNS = 2

START_X = (WIDTH - (GRID_COLUMNS * CARD_WIDTH + (GRID_COLUMNS - 1) * CARD_MARGIN_X)) // 2
START_Y = 160


# ---------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------

def draw_text(surface, text, font, color, center_pos):
    """Text mittig an einer Position zeichnen."""
    render = font.render(text, True, color)
    rect = render.get_rect(center=center_pos)
    surface.blit(render, rect)


def draw_star(surface, center_pos, size=10, color=STAR_COLOR):
    """Sehr simples Stern-Icon (Kreis als Platzhalter, damit es überall läuft)."""
    pygame.draw.circle(surface, color, center_pos, size)


# ---------------------------------------------------------
# Level-Karten (Buttons)
# ---------------------------------------------------------

class LevelCard:
    def __init__(self, index, name, stars, locked, rect):
        self.index = index
        self.name = name
        self.stars = stars
        self.locked = locked
        self.rect = pygame.Rect(rect)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, surface, mouse_pos):
        hovered = self.is_hovered(mouse_pos)

        # Hintergrund der Karte
        if self.locked:
            base_color = (CARD_COLOR[0], CARD_COLOR[1], CARD_COLOR[2])
            border_color = LOCKED_COLOR
        else:
            base_color = CARD_COLOR
            border_color = CARD_BORDER_COLOR

        # leichte Hover-Highlight
        if hovered and not self.locked:
            base_color = (
                min(base_color[0] + 10, 255),
                min(base_color[1] + 10, 255),
                min(base_color[2] + 10, 255),
            )

        pygame.draw.rect(surface, base_color, self.rect, border_radius=16)
        pygame.draw.rect(surface, border_color, self.rect, width=1, border_radius=16)

        # Level-Titel
        title_color = TEXT_COLOR if not self.locked else LOCKED_COLOR
        title_pos = (self.rect.centerx, self.rect.y + 30)
        draw_text(surface, self.name, LEVEL_FONT, title_color, title_pos)

        # Stars
        star_y = self.rect.y + 65
        if self.stars > 0:
            for i in range(self.stars):
                star_x = self.rect.centerx - (self.stars - 1) * 15 + i * 30
                draw_star(surface, (star_x, star_y), size=7)
        else:
            info_text = "Noch keine Sterne"
            info_pos = (self.rect.centerx, star_y)
            draw_text(surface, info_text, INFO_FONT, LOCKED_COLOR, info_pos)

        # Lock-Icon / Status
        status_y = self.rect.y + CARD_HEIGHT - 25
        if self.locked:
            status_text = "Gesperrt"
            status_color = LOCKED_COLOR
        else:
            status_text = "Tippen zum Spielen"
            status_color = PRIMARY_COLOR

        status_pos = (self.rect.centerx, status_y)
        draw_text(surface, status_text, INFO_FONT, status_color, status_pos)

    def handle_click(self):
        """Was passieren soll, wenn auf die Karte geklickt wird."""
        if self.locked:
            return None  # gesperrte Level ignorieren
        return self.index


# ---------------------------------------------------------
# Hauptloop für die Levelauswahl
# ---------------------------------------------------------


def create_level_cards():
    cards = []
    row = 0
    col = 0

    for i, level in enumerate(LEVELS):
        x = START_X + col * (CARD_WIDTH + CARD_MARGIN_X)
        y = START_Y + row * (CARD_HEIGHT + CARD_MARGIN_Y)
        rect = (x, y, CARD_WIDTH, CARD_HEIGHT)
        card = LevelCard(
            index=i,
            name=level["name"],
            stars=level["stars"],
            locked=level["locked"],
            rect=rect,
        )
        cards.append(card)

        col += 1
        if col >= GRID_COLUMNS:
            col = 0
            row += 1

    return cards



def level_select_loop():
    """Zeigt die Levelauswahl-Seite und gibt das gewählte Level zurück."""
    cards = create_level_cards()
    selected_level_index = None

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in cards:
                    if card.is_hovered(mouse_pos):
                        result = card.handle_click()
                        if result is not None:
                            selected_level_index = result
                            running = False
                            break

        # Hintergrund
        SCREEN.fill(BG_COLOR)

        # Header
        draw_text(
            SCREEN,
            "Levels",
            TITLE_FONT,
            TEXT_COLOR,
            (WIDTH // 2, 70),
        )
        draw_text(
            SCREEN,
            "Wähle ein Level aus, um zu spielen.",
            SUBTITLE_FONT,
            (120, 120, 140),
            (WIDTH // 2, 110),
        )

        # Level-Karten zeichnen
        for card in cards:
            card.draw(SCREEN, mouse_pos)

        pygame.display.flip()
        CLOCK.tick(FPS)

    return selected_level_index



def main():
    """Startet nur die Levelseite."""
    chosen = level_select_loop()
    # Hier nur Demo-Output – später ersetzt du das durch deine Spiel-Logik
    print(f"Gewähltes Level: {chosen}")


if __name__ == "__main__":
    main()
