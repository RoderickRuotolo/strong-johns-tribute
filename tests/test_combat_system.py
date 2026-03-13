import unittest

import pygame

from src.systems.combat_system import player_attack


class DummyPlayer:
    def __init__(self):
        self.attack = True
        self.attack_rect = pygame.Rect(100, 100, 80, 40)
        self.rect = pygame.Rect(80, 100, 20, 40)
        self.current_attack_hits = set()
        self.attack_profile = {
            "name": "light_1",
            "damage": 8,
            "hit_stun": 10,
            "knockback": 7.0,
        }


class DummyEnemy:
    def __init__(self):
        self.rect = pygame.Rect(110, 110, 40, 40)
        self.alive = True
        self.last_damage = 0

    def take_hit(self, damage, attacker_x, hit_stun, knockback):
        self.last_damage = damage
        self.alive = False
        return True


class DummyBoss:
    def __init__(self):
        self.rect = pygame.Rect(400, 400, 80, 80)
        self.last_damage = 0

    def take_hit(self, damage, attacker_x, hit_stun, knockback):
        self.last_damage = damage
        return True


class TestCombatSystem(unittest.TestCase):
    def test_player_attack_hits_enemy_and_removes_dead(self):
        player = DummyPlayer()
        enemy = DummyEnemy()
        enemies = [enemy]
        boss = None

        events = player_attack([player], enemies, boss)
        self.assertEqual(enemy.last_damage, 8)
        self.assertEqual(len(enemies), 0)
        self.assertEqual(len(events), 1)
        self.assertFalse(events[0]["heavy"])

    def test_heavy_attack_flags_event(self):
        player = DummyPlayer()
        player.attack_profile["name"] = "heavy"
        enemy = DummyEnemy()

        events = player_attack([player], [enemy], None)
        self.assertEqual(len(events), 1)
        self.assertTrue(events[0]["heavy"])


if __name__ == "__main__":
    unittest.main()
