import pygame


class SpriteCache:
    def __init__(self):
        self._player_cache = {}
        self._enemy_cache = {}
        self._boss_cache = {}

    def get_player_sprite(self, outfit, attack, facing, hurt):
        key = (outfit, attack, facing, hurt)
        if key not in self._player_cache:
            self._player_cache[key] = self._build_player_sprite(outfit, attack, facing, hurt)
        return self._player_cache[key]

    def get_enemy_sprite(self, archetype, facing, color):
        key = (archetype, facing, color)
        if key not in self._enemy_cache:
            self._enemy_cache[key] = self._build_enemy_sprite(archetype, facing, color)
        return self._enemy_cache[key]

    def get_boss_sprite(self, state, facing):
        key = (state, facing)
        if key not in self._boss_cache:
            self._boss_cache[key] = self._build_boss_sprite(state, facing)
        return self._boss_cache[key]

    def _build_player_sprite(self, outfit, attack, facing, hurt):
        surface = pygame.Surface((180, 150), pygame.SRCALPHA)
        skin = (235, 210, 180)
        torso = (240, 220, 185) if outfit == "shirtless" else (40, 100, 220)

        pygame.draw.ellipse(surface, skin, (70, 8, 40, 36))
        pygame.draw.rect(surface, torso, (62, 42, 56, 54), border_radius=8)
        pygame.draw.rect(surface, (35, 35, 35), (65, 94, 20, 34), border_radius=4)
        pygame.draw.rect(surface, (35, 35, 35), (95, 94, 20, 34), border_radius=4)

        # Back arm
        pygame.draw.rect(surface, skin, (36, 54, 26, 16), border_radius=8)
        # Front arm
        if attack:
            pygame.draw.rect(surface, skin, (120, 50, 48, 18), border_radius=8)
        else:
            pygame.draw.rect(surface, skin, (118, 56, 28, 16), border_radius=8)

        if hurt:
            pygame.draw.rect(surface, (255, 90, 90, 140), (50, 6, 78, 128), width=4, border_radius=8)

        if facing < 0:
            surface = pygame.transform.flip(surface, True, False)

        return surface

    def _build_enemy_sprite(self, archetype, facing, color):
        surface = pygame.Surface((120, 120), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (220, 190, 160), (45, 8, 28, 24))
        pygame.draw.rect(surface, color, (36, 30, 46, 56), border_radius=8)

        if archetype == "tank":
            pygame.draw.rect(surface, (80, 80, 80), (30, 40, 58, 12), border_radius=6)
        elif archetype == "ranged":
            pygame.draw.rect(surface, (20, 20, 20), (24, 50, 18, 10), border_radius=4)

        if facing < 0:
            surface = pygame.transform.flip(surface, True, False)
        return surface

    def _build_boss_sprite(self, state, facing):
        surface = pygame.Surface((180, 170), pygame.SRCALPHA)
        hair = (40, 100, 220)
        if state == "phase_2":
            hair = (220, 120, 40)
        elif state == "enraged":
            hair = (220, 40, 40)

        pygame.draw.ellipse(surface, (70, 40, 30), (70, 8, 40, 32))
        pygame.draw.rect(surface, hair, (60, 34, 60, 16), border_radius=6)
        pygame.draw.rect(surface, (170, 170, 170), (44, 52, 92, 68), border_radius=12)
        pygame.draw.rect(surface, hair, (44, 118, 92, 28), border_radius=8)

        if facing < 0:
            surface = pygame.transform.flip(surface, True, False)
        return surface
