import unittest

from src.entities.player import Player
from src.systems.ai_system import select_target_by_threat


class TestAISystem(unittest.TestCase):
    def test_selects_alive_player_only(self):
        p1 = Player(100, (255, 255, 255))
        p2 = Player(200, (40, 100, 220))
        p1.health = 0
        target = select_target_by_threat([p1, p2], attacker_x=120)
        self.assertIs(target, p2)

    def test_prefers_higher_threat_over_distance(self):
        p1 = Player(200, (255, 255, 255))
        p2 = Player(100, (40, 100, 220))

        # p1 farther, but actively attacking and in combo.
        p1.current_attack = {"name": "light_2"}
        p1.combo_index = 2
        p2.current_attack = None
        p2.combo_index = -1

        target = select_target_by_threat([p1, p2], attacker_x=120)
        self.assertIs(target, p1)


if __name__ == "__main__":
    unittest.main()
