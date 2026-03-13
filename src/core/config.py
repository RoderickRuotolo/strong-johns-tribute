WIDTH = 1100
HEIGHT = 600
FPS = 60

WINDOW_TITLE = "Jooes Fortões"
FONT_NAME = "arial"
FONT_SIZE = 24

BAR_BG = (90, 55, 30)
FLOOR = (60, 35, 20)
WOOD = (110, 70, 40)

SKIN = (230, 200, 170)
BEARD = (60, 40, 20)
BOSS_SKIN = (70, 40, 30)

BLUE = (40, 100, 220)
GRAY = (170, 170, 170)
RED = (160, 60, 60)
ORANGE = (220, 130, 40)
PURPLE = (150, 90, 190)

MUSCLE_LIGHT = (240, 210, 180)
MUSCLE_SHADOW = (200, 170, 140)
OUTLINE = (0, 0, 0)

PLAYER_Y = 420
PLAYER_WIDTH = 70
PLAYER_HEIGHT = 70

ENEMY_Y = 420
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 70

BOSS_Y = 400
BOSS_WIDTH = 110
BOSS_HEIGHT = 90

KNOCKBACK_FRICTION = 0.8
GRAVITY = 0.9
JUMP_VELOCITY = -14.5
MAX_FALL_SPEED = 18.0

ATTACK_CHAIN = [
    {
        "name": "light_1",
        "damage": 8,
        "hitbox_width": 82,
        "hitbox_height": 32,
        "hitbox_offset_x": 16,
        "hitbox_offset_y": 20,
        "total_frames": 12,
        "active_start": 3,
        "active_end": 6,
        "combo_link_window": 14,
        "hit_stun": 9,
        "knockback": 6.0,
    },
    {
        "name": "light_2",
        "damage": 10,
        "hitbox_width": 94,
        "hitbox_height": 34,
        "hitbox_offset_x": 18,
        "hitbox_offset_y": 18,
        "total_frames": 14,
        "active_start": 4,
        "active_end": 7,
        "combo_link_window": 12,
        "hit_stun": 11,
        "knockback": 8.0,
    },
    {
        "name": "light_3",
        "damage": 14,
        "hitbox_width": 108,
        "hitbox_height": 36,
        "hitbox_offset_x": 20,
        "hitbox_offset_y": 16,
        "total_frames": 18,
        "active_start": 5,
        "active_end": 10,
        "combo_link_window": 0,
        "hit_stun": 14,
        "knockback": 11.0,
    },
]

HEAVY_ATTACK = {
    "name": "heavy",
    "damage": 22,
    "hitbox_width": 120,
    "hitbox_height": 40,
    "hitbox_offset_x": 24,
    "hitbox_offset_y": 14,
    "total_frames": 26,
    "active_start": 8,
    "active_end": 12,
    "combo_link_window": 0,
    "hit_stun": 18,
    "knockback": 14.0,
}

AIR_ATTACK = {
    "name": "air_light",
    "damage": 11,
    "hitbox_width": 90,
    "hitbox_height": 28,
    "hitbox_offset_x": 16,
    "hitbox_offset_y": 26,
    "total_frames": 14,
    "active_start": 4,
    "active_end": 8,
    "combo_link_window": 0,
    "hit_stun": 10,
    "knockback": 7.0,
}

ENEMY_ARCHETYPES = {
    "rush": {
        "health": 16,
        "speed_min": 3,
        "speed_max": 5,
        "damage": 4,
        "attack_cooldown": 30,
        "contact_range": 0,
        "stun_resistance": 0.8,
        "color": RED,
    },
    "tank": {
        "health": 34,
        "speed_min": 1,
        "speed_max": 2,
        "damage": 8,
        "attack_cooldown": 48,
        "contact_range": 0,
        "stun_resistance": 1.5,
        "color": ORANGE,
    },
    "ranged": {
        "health": 20,
        "speed_min": 2,
        "speed_max": 3,
        "damage": 5,
        "attack_cooldown": 44,
        "contact_range": 170,
        "stun_resistance": 1.0,
        "color": PURPLE,
    },
}

WAVE_RULES = {
    "max_wave": 8,
    "base_spawn_interval": 110,
    "min_spawn_interval": 45,
    "base_enemy_cap": 5,
    "max_enemy_cap": 12,
    "wave_duration_frames": 900,
}
