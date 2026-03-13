import pygame

from src.core.config import (
    BAR_BG,
    BEARD,
    BLUE,
    FLOOR,
    FONT_NAME,
    FONT_SIZE,
    GRAY,
    MUSCLE_LIGHT,
    MUSCLE_SHADOW,
    OUTLINE,
    WOOD,
)
from src.systems.sprite_system import SpriteCache

SPRITES = SpriteCache()


def get_main_font():
    return pygame.font.SysFont(FONT_NAME, FONT_SIZE)


def outline_circle(surface, color, pos, radius):
    pygame.draw.circle(surface, OUTLINE, pos, radius + 2)
    pygame.draw.circle(surface, color, pos, radius)


def outline_rect(surface, color, rect):
    pygame.draw.rect(surface, OUTLINE, rect.inflate(4, 4))
    pygame.draw.rect(surface, color, rect)


def draw_head(surface, x, y):
    outline_circle(surface, MUSCLE_LIGHT, (x, y), 24)
    pygame.draw.circle(surface, (0, 0, 0), (x - 7, y - 6), 3)
    pygame.draw.circle(surface, (0, 0, 0), (x + 7, y - 6), 3)
    pygame.draw.circle(surface, BEARD, (x, y + 8), 16)


def draw_traps(surface, x, y):
    pygame.draw.polygon(
        surface,
        MUSCLE_SHADOW,
        [(x - 35, y + 5), (x, y - 10), (x + 35, y + 5), (x + 20, y + 20), (x - 20, y + 20)],
    )


def draw_chest(surface, x, y):
    outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x - 32, y + 10, 64, 55))
    pygame.draw.line(surface, MUSCLE_SHADOW, (x, y + 10), (x, y + 65), 2)
    pygame.draw.arc(surface, MUSCLE_SHADOW, (x - 32, y + 20, 64, 40), 0, 3.14, 2)


def draw_abs(surface, x, y):
    for i in range(3):
        pygame.draw.line(
            surface,
            MUSCLE_SHADOW,
            (x - 18, y + 25 + i * 12),
            (x + 18, y + 25 + i * 12),
            2,
        )


def draw_shoulders(surface, x, y):
    outline_circle(surface, MUSCLE_LIGHT, (x - 40, y + 20), 22)
    outline_circle(surface, MUSCLE_LIGHT, (x + 40, y + 20), 22)


def draw_biceps(surface, x, y):
    outline_circle(surface, MUSCLE_LIGHT, (x - 70, y + 40), 24)
    outline_circle(surface, MUSCLE_LIGHT, (x + 70, y + 40), 24)


def draw_forearms(surface, x, y, attack, facing):
    direction = 1 if facing >= 0 else -1

    if attack:
        if direction > 0:
            outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x + 70, y + 35, 70, 18))
        else:
            outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x - 140, y + 35, 70, 18))
    else:
        if direction > 0:
            outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x + 40, y + 35, 35, 18))
        else:
            outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x - 75, y + 35, 35, 18))

    if direction > 0:
        outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x - 100, y + 35, 45, 18))
    else:
        outline_rect(surface, MUSCLE_LIGHT, pygame.Rect(x + 55, y + 35, 45, 18))


def draw_hands(surface, x, y, attack, facing):
    direction = 1 if facing >= 0 else -1

    if direction > 0:
        outline_circle(surface, MUSCLE_LIGHT, (x - 110, y + 44), 12)
    else:
        outline_circle(surface, MUSCLE_LIGHT, (x + 110, y + 44), 12)

    if attack:
        if direction > 0:
            outline_circle(surface, MUSCLE_LIGHT, (x + 150, y + 44), 12)
        else:
            outline_circle(surface, MUSCLE_LIGHT, (x - 150, y + 44), 12)
    else:
        if direction > 0:
            outline_circle(surface, MUSCLE_LIGHT, (x + 80, y + 44), 12)
        else:
            outline_circle(surface, MUSCLE_LIGHT, (x - 80, y + 44), 12)


def draw_legs(surface, x, y):
    outline_rect(surface, (30, 30, 30), pygame.Rect(x - 20, y + 70, 18, 32))
    outline_rect(surface, (30, 30, 30), pygame.Rect(x + 2, y + 70, 18, 32))


def draw_fortao_shirtless(surface, x, y, attack, facing, hurt_flash_timer=0):
    cx = x + 35
    draw_head(surface, cx, y - 12)
    draw_traps(surface, cx, y)
    draw_shoulders(surface, cx, y)
    draw_chest(surface, cx, y)
    draw_abs(surface, cx, y)
    draw_biceps(surface, cx, y)
    draw_forearms(surface, cx, y, attack, facing)
    draw_hands(surface, cx, y, attack, facing)
    draw_legs(surface, cx, y)
    if hurt_flash_timer > 0 and hurt_flash_timer % 2 == 0:
        pygame.draw.rect(surface, (255, 90, 90), pygame.Rect(x - 5, y - 28, 80, 130), 3)


def draw_fortao_tank(surface, x, y, attack, color, facing, hurt_flash_timer=0):
    cx = x + 35
    draw_head(surface, cx, y - 12)
    draw_traps(surface, cx, y)
    draw_shoulders(surface, cx, y)
    outline_rect(surface, color, pygame.Rect(cx - 32, y + 10, 64, 55))
    draw_biceps(surface, cx, y)
    draw_forearms(surface, cx, y, attack, facing)
    draw_hands(surface, cx, y, attack, facing)
    draw_legs(surface, cx, y)
    if hurt_flash_timer > 0 and hurt_flash_timer % 2 == 0:
        pygame.draw.rect(surface, (255, 90, 90), pygame.Rect(x - 5, y - 28, 80, 130), 3)


def draw_players(surface, player1, player2):
    p1_sprite = SPRITES.get_player_sprite(
        outfit="shirtless",
        attack=player1.attack,
        facing=player1.facing,
        hurt=(player1.hurt_flash_timer > 0 and player1.hurt_flash_timer % 2 == 0),
    )
    p2_sprite = SPRITES.get_player_sprite(
        outfit="tank",
        attack=player2.attack,
        facing=player2.facing,
        hurt=(player2.hurt_flash_timer > 0 and player2.hurt_flash_timer % 2 == 0),
    )
    surface.blit(p1_sprite, (player1.rect.x - 55, player1.rect.y - 40))
    surface.blit(p2_sprite, (player2.rect.x - 55, player2.rect.y - 40))


def draw_enemy(surface, enemy):
    sprite = SPRITES.get_enemy_sprite(
        archetype=enemy.archetype,
        facing=enemy.facing,
        color=enemy.profile["color"],
    )
    surface.blit(sprite, (enemy.rect.x - 30, enemy.rect.y - 24))


def draw_boss(surface, boss):
    sprite = SPRITES.get_boss_sprite(state=boss.state, facing=boss.facing)
    surface.blit(sprite, (boss.rect.x - 35, boss.rect.y - 50))


def draw_bar(surface, frame_count=0):
    for y in range(0, 360):
        shade = max(12, 90 - y // 6)
        pygame.draw.line(surface, (shade, shade + 16, shade + 26), (0, y), (1100, y))

    far_offset = (frame_count // 6) % 1100
    mid_offset = (frame_count // 3) % 1100

    for base_x in range(-1100, 2200, 360):
        pygame.draw.rect(surface, (30, 30, 45), (base_x - far_offset, 230, 220, 150))
        pygame.draw.rect(surface, (36, 36, 54), (base_x + 80 - mid_offset, 200, 180, 180))

    pygame.draw.rect(surface, BAR_BG, (0, 300, 1100, 220))
    pygame.draw.rect(surface, FLOOR, (0, 480, 1100, 120))
    pygame.draw.rect(surface, WOOD, (400, 360, 300, 120))
    pygame.draw.rect(surface, WOOD, (200, 400, 120, 80))
    pygame.draw.rect(surface, WOOD, (750, 410, 120, 70))

    for x in range(420, 660, 40):
        pygame.draw.rect(surface, (30, 130, 50), (x, 340, 10, 20))


def draw_health(surface, player, x, y):
    pygame.draw.rect(surface, (255, 0, 0), (x, y, 200, 20))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, max(player.health * 2, 0), 20))


def draw_boss_text(surface, font, boss):
    boss_text = font.render(
        f"Black of Sausage Mouth HP: {boss.health} ({boss.state.upper()})",
        True,
        (255, 255, 255),
    )
    surface.blit(boss_text, (750, 40))


def draw_wave_info(surface, font, wave_state, enemies_count):
    wave_text = font.render(
        f"Wave {wave_state['wave']} | Enemies: {enemies_count}",
        True,
        (255, 255, 255),
    )
    surface.blit(wave_text, (40, 100))


def draw_game_over(surface, font):
    game_over = font.render(
        "OS JOOES FORTÕES FORAM DERROTADOS",
        True,
        (255, 0, 0),
    )
    surface.blit(game_over, (380, 200))


def draw_victory(surface, font):
    victory_text = font.render(
        "THE STRONG JOHNS WON!",
        True,
        (80, 255, 80),
    )
    surface.blit(victory_text, (420, 200))


def draw_restart_hint(surface, font, key_label="R"):
    restart_text = font.render(
        f"Press {key_label} to restart",
        True,
        (255, 255, 255),
    )
    surface.blit(restart_text, (470, 250))


def draw_stage_clear(surface, font):
    clear_text = font.render(
        "STAGE CLEAR!",
        True,
        (255, 230, 90),
    )
    surface.blit(clear_text, (470, 200))


def draw_player_feedback(surface, font, player, x, y, label):
    combo_text = "COMBO: -"
    if player.combo_index >= 0:
        combo_text = f"COMBO: {player.combo_index + 1}"

    invul_text = "INVUL: ON" if player.invulnerability_timer > 0 else "INVUL: OFF"
    jump_text = "AIR" if not player.on_ground else "GROUND"
    info = font.render(f"{label} {combo_text} | {invul_text} | {jump_text}", True, (235, 235, 235))
    surface.blit(info, (x, y))


def draw_pause_menu(surface, font, selected_index):
    panel = pygame.Rect(360, 150, 380, 300)
    pygame.draw.rect(surface, (20, 20, 20, 200), panel, border_radius=12)
    pygame.draw.rect(surface, (220, 220, 220), panel, width=2, border_radius=12)
    title = font.render("PAUSED", True, (255, 255, 255))
    surface.blit(title, (515, 175))

    entries = ["Resume", "Restart Match", "Options", "Quit"]
    for index, text in enumerate(entries):
        color = (255, 230, 90) if index == selected_index else (220, 220, 220)
        line = font.render(text, True, color)
        surface.blit(line, (470, 230 + index * 45))


def draw_options_menu(surface, font, selected_index, settings):
    panel = pygame.Rect(280, 110, 540, 380)
    pygame.draw.rect(surface, (18, 18, 24, 220), panel, border_radius=12)
    pygame.draw.rect(surface, (220, 220, 220), panel, width=2, border_radius=12)
    title = font.render("OPTIONS", True, (255, 255, 255))
    surface.blit(title, (520, 130))

    entries = [
        f"Master Volume: {int(settings['master_volume'] * 100)}%",
        f"Screen Shake: {'ON' if settings['screen_shake'] else 'OFF'}",
        f"Fullscreen: {'ON' if settings['fullscreen'] else 'OFF'}",
        "Controls",
        "Back",
    ]
    for index, text in enumerate(entries):
        color = (90, 220, 255) if index == selected_index else (220, 220, 220)
        line = font.render(text, True, color)
        surface.blit(line, (350, 195 + index * 50))


def draw_controls_menu(surface, font, selected_index, bindings, waiting_action):
    panel = pygame.Rect(220, 70, 660, 460)
    pygame.draw.rect(surface, (15, 15, 22, 230), panel, border_radius=12)
    pygame.draw.rect(surface, (220, 220, 220), panel, width=2, border_radius=12)
    title = font.render("CONTROLS", True, (255, 255, 255))
    surface.blit(title, (510, 88))

    entries = [
        ("P1 Left", "p1_left"),
        ("P1 Right", "p1_right"),
        ("P1 Jump", "p1_jump"),
        ("P2 Left", "p2_left"),
        ("P2 Right", "p2_right"),
        ("P2 Jump", "p2_jump"),
        ("Light Attack", "light_attack"),
        ("Heavy Attack", "heavy_attack"),
        ("Pause", "pause"),
        ("Restart", "restart"),
        ("Back", None),
    ]

    for index, (label, action) in enumerate(entries):
        color = (255, 230, 90) if index == selected_index else (220, 220, 220)
        if action is None:
            text = label
        else:
            text = f"{label}: {pygame.key.name(bindings[action]).upper()}"
        line = font.render(text, True, color)
        surface.blit(line, (280, 130 + index * 33))

    if waiting_action:
        hint = font.render(
            f"Press a key to bind: {waiting_action.replace('_', ' ').upper()}",
            True,
            (90, 220, 255),
        )
        surface.blit(hint, (250, 500))
