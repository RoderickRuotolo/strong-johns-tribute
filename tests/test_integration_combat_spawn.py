import random
import unittest

import pygame

from src.entities.player import Player
from src.systems.combat_system import player_attack
from src.systems.spawn_system import init_wave_state, update_spawning


class TestIntegrationCombatSpawn(unittest.TestCase):
    def setUp(self):
        random.seed(7)

    def test_spawn_then_player_can_hit_enemy(self):
        players = [Player(150, (255, 255, 255))]
        enemies = []
        boss = None
        wave_state = init_wave_state()
        spawn_timer = 200

        spawn_timer, boss, wave_state = update_spawning(spawn_timer, enemies, boss, wave_state)
        self.assertGreaterEqual(len(enemies), 1)
        self.assertIsNone(boss)

        enemy = enemies[0]
        players[0].attack = True
        players[0].current_attack = {
            "name": "light_1",
            "damage": 50,
            "hit_stun": 8,
            "knockback": 10.0,
        }
        players[0].attack_rect = pygame.Rect(enemy.rect.x - 5, enemy.rect.y - 5, 120, 120)

        events = player_attack(players, enemies, boss)
        self.assertGreaterEqual(len(events), 1)
        self.assertEqual(len(enemies), 0)


if __name__ == "__main__":
    unittest.main()
