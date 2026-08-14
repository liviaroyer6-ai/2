import pygame
from constants import FONT, GRAY, BLACK, WHITE

def draw_text(surf, txt, size, color, x, y):
    font = pygame.font.Font(None, size)
    text = font.render(txt, True, color)
    rect = text.get_rect(center=(x, y))
    surf.blit(text, rect)

def ui_text(txt, x, y, color=BLACK, surf=None):
    s = surf or pygame.display.get_surface()
    r = FONT.render(txt, True, color)
    s.blit(r, (x, y))

_last_click = 0  # global oder in einer Klasse kapseln

def ui_button(text, x, y, w, h, callback, surf=None, hover_color=(180, 0, 0)):
    global _last_click
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    is_hover = x < mouse[0] < x + w and y < mouse[1] < y + h
    color = hover_color if is_hover else (180, 0, 0)

    target = surf or pygame.display.get_surface()
    pygame.draw.rect(target, color, (x, y, w, h), border_radius=8)
    ui_text(text, x + w // 2 - FONT.size(text)[0] // 2,
            y + h // 2 - FONT.get_height() // 2, WHITE, target)

    if is_hover and click[0]:
        now = pygame.time.get_ticks()
        if now - _last_click > 200:  # 200 ms Delay
            _last_click = now
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
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
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
        pygame.draw.rect(surface, GRAY, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        surface.blit(FONT.render(self.text, True, BLACK), (self.rect.x + 10, self.rect.y + 10))