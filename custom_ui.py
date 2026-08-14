import pygame

def draw_rounded_button(surface, rect, color, text, font, text_color):
    pygame.draw.rect(surface, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_gradient(surface, rect, top_color, bottom_color):
    """Zeichnet einen vertikalen Farbverlauf im übergebenen Rect."""
    height = rect.height
    for y in range(height):
        ratio = y / height
        new_color = [int(top_color[i] * (1 - ratio) + bottom_color[i] * ratio) for i in range(3)]
        pygame.draw.line(surface, new_color, (rect.x, rect.y + y), (rect.x + rect.width, rect.y + y))