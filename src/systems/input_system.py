import pygame


def default_bindings():
    return {
        "p1_left": pygame.K_a,
        "p1_right": pygame.K_d,
        "p1_jump": pygame.K_w,
        "p2_left": pygame.K_LEFT,
        "p2_right": pygame.K_RIGHT,
        "p2_jump": pygame.K_UP,
        "light_attack": pygame.K_SPACE,
        "heavy_attack": pygame.K_LSHIFT,
        "pause": pygame.K_ESCAPE,
        "restart": pygame.K_r,
    }


def key_name(key):
    return pygame.key.name(key).upper()

