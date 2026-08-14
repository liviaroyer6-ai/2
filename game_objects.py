import pygame
import random
import math  # Added math import
from constants import GAME_W, GAME_H, GREEN, YELLOW, RED, WHITE

class Player:
    def __init__(self, img):
        self.img = img
        self.w, self.h = img.get_size()
        self.x = GAME_W // 2 - self.w // 2
        self.y = GAME_H - self.h - 10
        self.speed = 5
        self.original_speed = self.speed
        self.power_up_end = 0
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
        if self.shield_active:
            pygame.draw.circle(surface, (0, 255, 255), (self.x + self.w // 2, self.y + self.h // 2), max(self.w, self.h) // 2 + 5, 3)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Enemy:
    def __init__(self, img, speed):
        self.img = img
        self.w, self.h = img.get_size()
        self.speed = speed
        self.reset()

    def reset(self):
        self.x = random.randint(0, GAME_W - self.w)
        self.y = -self.h

    def move(self):
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()

    def draw(self, s):
        s.blit(self.img, (self.x, self.y))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class FastEnemy(Enemy):
    def move(self):
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
            self.invincible_end = pygame.time.get_ticks() + 1000
        if self.invincible and pygame.time.get_ticks() > self.invincible_end:
            self.invincible = False
        self.y += self.speed
        if self.y > GAME_H:
            self.reset()

    def draw(self, s):
        if self.invincible:
            blurred = pygame.transform.smoothscale(self.img, (self.w // 2, self.h // 2))
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
        pygame.draw.circle(s, (0, 255, 0), (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class PowerUp:
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
        pts = [(self.x + self.size // 2, self.y), (self.x, self.y + self.size // 2),
               (self.x + self.size // 2, self.y + self.size), (self.x + self.size, self.y + self.size // 2)]
        pygame.draw.polygon(s, YELLOW, pts)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

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
        pygame.draw.circle(s, (0, 255, 255), (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

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
        pygame.draw.circle(s, (255, 0, 255), (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

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
        pygame.draw.circle(s, (255, 255, 0), (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

class BossEnemy:
    def __init__(self):
        self.w, self.h = 200, 200
        self.x, self.y = GAME_W // 2 - self.w // 2, -self.h
        self.speed = 2
        self.dir = 1
        self.health = 20

    def move(self):
        if self.y < 50:
            self.y += 2
        else:
            self.x += self.speed * self.dir
            if self.x <= 0 or self.x >= GAME_W - self.w:
                self.dir *= -1

    def draw(self, s):
        pygame.draw.rect(s, (0, 0, 255), (self.x, self.y, self.w, self.h))
        pygame.draw.rect(s, RED, (GAME_W - 210, 10, self.health * 10, 20))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class BaseBoss:
    def __init__(self, health, speed):
        self.health = health
        self.max_health = health
        self.speed = speed
        self.w, self.h = 200, 200
        self.x = GAME_W // 2 - self.w // 2
        self.y = -self.h
        self.start_time = pygame.time.get_ticks()

    def move(self):
        if self.y < 50:
            self.y += self.speed
        else:
            t = (pygame.time.get_ticks() - self.start_time) / 1000.0
            self.x = (GAME_W // 2 - self.w // 2) + int(200 * math.sin(t * 2))

    def draw(self, s):
        pygame.draw.rect(s, (0, 0, 255), (self.x, self.y, self.w, self.h))
        bar_width = 300
        bar_height = 20
        bar_x = (GAME_W - bar_width) // 2
        bar_y = 10
        health_ratio = max(self.health / self.max_health, 0)
        filled_width = int(bar_width * health_ratio)
        pygame.draw.rect(s, RED, (bar_x, bar_y, filled_width, bar_height))
        pygame.draw.rect(s, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class BossType1(BaseBoss):
    def __init__(self):
        super().__init__(health=20, speed=2)

class BossType2(BaseBoss):
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
    def __init__(self):
        super().__init__(health=40, speed=3)

    def move(self):
        if self.y < 100:
            self.y += self.speed * 2
        else:
            t = (pygame.time.get_ticks() - self.start_time) / 1000.0
            self.x = (GAME_W // 2 - self.w // 2) + int(250 * math.sin(t * 3))

class UnbreakableEnemy:
    def __init__(self, x, y, w, h, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.speed = 3

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > GAME_H:
            self.rect.y = -self.rect.h
            self.rect.x = random.randint(0, GAME_W - self.rect.w)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def check(self, player_rect):
        return player_rect.colliderect(self.rect)