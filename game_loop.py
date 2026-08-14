import pygame
import os
import sys
import traceback

from constants import (
    GAME_W, GAME_H, pause_button, try_again_button, quit_button, resume_button, menu_button,
    CHAR_SPRITES, LEVELS, BLACK, WHITE, YELLOW, GREEN, RED, BLUE, ASSET_DIR, screen_width, screen_height
)
from game_objects import (
    Player, Enemy, FastEnemy, TeleportingEnemy, PowerUp, ShieldPowerUp, DoubleShootingPowerUp, TimeSlowPowerUp,
    BossType1, BossType2, BossType3, UnbreakableEnemy, SpeedBoost
)
from persistence import save_progress
from ui import draw_text, ui_button
from utils import load_image
from game_state import current_user, current_progress, get_selected_char, set_selected_char

from constants import ASSET_DIR
from game_state import set_selected_char, get_selected_char


def collision_overlay(scr, bg, level, progress):
    """Handle collision overlay and user choices."""
    while True:
        scr.blit(bg, (0, 0))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if try_again_button.collidepoint(mx, my):
                    return "restart"
                if resume_button.collidepoint(mx, my):
                    return "resume"
                if menu_button.collidepoint(mx, my):
                    return "menu"

        overlay = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        scr.blit(overlay, (0, 0))
        
        # Draw buttons
        pygame.draw.rect(scr, GREEN, try_again_button)
        pygame.draw.rect(scr, YELLOW, resume_button)
        pygame.draw.rect(scr, BLUE, menu_button)  # Now BLUE is properly imported
        
        # Draw texts
        draw_text(scr, "Try Again", 30, BLACK, try_again_button.centerx, try_again_button.centery)
        draw_text(scr, "Resume", 30, BLACK, resume_button.centerx, resume_button.centery)
        draw_text(scr, "Game Menu", 30, BLACK, menu_button.centerx, menu_button.centery)
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)

def fire_bullet(bullets, player, shoot_sound, last, interval):
    now = pygame.time.get_ticks()
    if now - last >= interval:
        bx = player.x + player.w // 2 - 2
        by = player.y
        bullets.append(pygame.Rect(bx, by, 4, 10))
        # If double shooting is active, fire a second bullet slightly offset
        if player.double_shoot:
            bullets.append(pygame.Rect(bx + 10, by, 4, 10))
        # Use a channel instead of shoot_sound.get_busy()
        channel = pygame.mixer.find_channel()
        if channel and not channel.get_busy():
            channel.play(shoot_sound)
        return now
    return last

def move_bullets(bullets):
    for bullet in bullets[:]:
        bullet.y -= 5  # Move the bullet upward
        if bullet.y < 0:  # Remove bullets that go off-screen
            bullets.remove(bullet)

def draw_bullets(screen, bullets):
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 0, 0), bullet)  # Draw bullets in red

print("[DEBUG] Entered game_loop.py")

def game_loop(level, progress):
    print(f"[DEBUG] Entered game_loop for level {level}")
    print(f"[DEBUG] Checking for selected character")

    selected_char = get_selected_char()

    if selected_char is None:
        print("[DEBUG] No character selected, opening selection_screen")
        # Charakter-Auswahl öffnen
        selection_screen(progress)
        # danach nochmal prüfen
        selected_char = get_selected_char()
        if selected_char is None:
            print("[DEBUG] Still no character selected, aborting level")
            return False

    ply = Player(selected_char)
    print(f"[DEBUG] Player created with character")

    try:
        scr = pygame.display.set_mode((GAME_W, GAME_H), pygame.FULLSCREEN)
        pygame.display.set_caption(f"Level {level}")
        cfg = LEVELS[level-1]
        bg = load_image(cfg["bg"], (GAME_W, GAME_H))
        speed = cfg["speed"]
        count = cfg["count"]
        thresh = cfg["threshold"]
        # Level‑Daten
        print("[DEBUG] Level data loaded, starting Ready phase")
        loading_time = 1500  # in Millisekunden
        start_ticks = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_ticks < loading_time:
            scr.blit(bg, (0, 0))
            draw_text(scr, "Ready...", 50, BLACK, GAME_W//2, GAME_H//2)
            pygame.display.flip()
            pygame.time.Clock().tick(60)
        print("[DEBUG] Ready phase complete, entering game loop")
        
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

        while True:
            dt = clock.tick(60)
            scr.blit(bg, (0, 0))
            mx, my = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            # Cheat key: If "C" is pressed, set score to threshold (full level)
            if keys[pygame.K_c]:
                score = thresh
                print("[DEBUG] Cheat key pressed: score set to threshold")

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
                if not boss_active and score >= thresh:
                    boss_active = True
                    boss_entry_delay = pygame.time.get_ticks() + 1000  # 1 Sekunde Grace Period
                    print("[DEBUG] Boss activated, delay until:", boss_entry_delay)
                    enemies = []          # Normale Gegner entfernen
                    pygame.time.delay(500)  # Kurze Pause
                    if level < 5:
                        boss = BossType1()
                    elif level < 10:
                        boss = BossType2()
                    else:
                        boss = BossType3()
            else:
                if boss is None:
                    if level < 5:
                        boss = BossType1()
                    elif level < 10:
                        boss = BossType2()
                    else:
                        boss = BossType3()
                boss.move()
                if pygame.time.get_ticks() > boss_entry_delay:
                    if ply.rect().colliderect(boss.rect()):
                        collision = True
                hit_bullets = []
                for b in bullets:
                    if boss.rect().colliderect(b):
                        boss.health -= 1
                        hit_bullets.append(b)
                for b in hit_bullets:
                    bullets.remove(b)
                if boss.health <= 0:
                    print(f"[DEBUG] Boss defeated! Current user: {current_user}")
                    if not current_user:
                        print("[DEBUG] Warning: No current user!")
                        from level_management import level_select   # lokaler Import
                        return level_select(progress)
                    
                    print(f"[DEBUG] Saving progress for {current_user}")
                    print(f"[DEBUG] Before save - Progress: {progress}")
                    
                    # Update progress before saving
                    if level not in progress['completed']:
                        progress['completed'].append(level)
                    progress['last'] = max(progress['last'], level + 1)
                    
                    # Save progress
                    success = save_progress(current_user, level, progress)
                    print(f"[DEBUG] Save success: {success}")
                    print(f"[DEBUG] After save - Progress: {progress}")
                    
                    # Show success message
                    draw_text(scr, "Level Complete!", 50, GREEN, GAME_W//2, GAME_H//2)
                    pygame.display.flip()
                    # ...
                    pygame.time.delay(1000)
                    from level_management import level_select       # lokaler Import
                    return level_select(progress)

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
                print("[DEBUG] Collision detected")
                choice = collision_overlay(scr, bg, level, progress)
                print("[DEBUG] Collision overlay returned:", choice)
                if choice == "restart":
                    print("[DEBUG] Restarting level")
                    return game_loop(level, progress)
                elif choice == "resume":
                    print("[DEBUG] Resuming game")
                    collision = False
                elif choice == "menu":
                    print("[DEBUG] Returning to game menu")
                    from game_menu import GameMenu
                    menu = GameMenu()
                    menu.show(progress)
                    return True
            
            pygame.display.flip()
    except Exception as e:
        print("[DEBUG] Exception in game_loop:", e)
        traceback.print_exc()  # Log the full traceback for debugging
        pygame.quit()
        sys.exit()

def selection_screen(progress=None):
    """Charakter-Auswahl vor jedem Level."""
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    chars = [load_image(fn, (120, 120)) for fn in CHAR_SPRITES]
    idx_c = 0
    pulse_timer = 0
    done = False  # flag to indicate selection completion

    try:
        bg_path = os.path.join(ASSET_DIR, "ui_background_characters.jpg")
        print("[DEBUG] Loading character background from:", bg_path)
        background = pygame.image.load(bg_path)
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except Exception as e:
        print(f"[DEBUG] Failed to load character selection background: {e}")
        background = None

    def confirm_selection():
        print("[DEBUG] confirm_selection called, idx_c =", idx_c)
        selected = load_image(CHAR_SPRITES[idx_c], (80, 80))
        if selected:
            set_selected_char(selected)  # im globalen game_state speichern
            print("[DEBUG] Character selected and saved to state")
            return True
        return False

    while not done:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((10, 10, 10))

        pulse_timer += 1
        for i, img in enumerate(chars):
            x = screen_width // 2 - (len(chars) * 150) // 2 + i * 150
            y = screen_height // 2 - 100
            screen.blit(img, (x, y))
            if i == idx_c:
                pygame.draw.rect(screen, GREEN, (x - 5, y - 5, 130, 130), 3)

        ui_button("✅ OK", screen_width // 2 - 75, screen_height // 2 + 150, 150, 50,
                  lambda: None, hover_color=(50, 200, 50))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    idx_c = (idx_c - 1) % len(chars)
                elif e.key == pygame.K_RIGHT:
                    idx_c = (idx_c + 1) % len(chars)
                elif e.key == pygame.K_RETURN:
                    if confirm_selection():
                        done = True
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                ok_btn_rect = pygame.Rect(screen_width // 2 - 75, screen_height // 2 + 150, 150, 50)
                if ok_btn_rect.collidepoint(mx, my):
                    if confirm_selection():
                        done = True
                else:
                    for i, img in enumerate(chars):
                        x = screen_width // 2 - (len(chars) * 150) // 2 + i * 150
                        y = screen_height // 2 - 100
                        if pygame.Rect(x, y, 120, 120).collidepoint(mx, my):
                            idx_c = i

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return get_selected_char()