import random
import unittest

from src.systems.spawn_system import init_wave_state, update_spawning


class TestSpawnSystem(unittest.TestCase):
    def setUp(self):
        random.seed(1234)

    def test_spawning_increments_wave_timer(self):
        wave_state = init_wave_state()
        spawn_timer, boss, wave_state = update_spawning(0, [], None, wave_state)
        self.assertEqual(spawn_timer, 1)
        self.assertIsNone(boss)
        self.assertEqual(wave_state["wave_timer"], 1)

    def test_boss_spawns_in_final_wave_conditions(self):
        wave_state = init_wave_state()
        wave_state["wave"] = 8
        wave_state["wave_timer"] = 400
        enemies = [object() for _ in range(11)]
        spawn_timer, boss, wave_state = update_spawning(200, enemies, None, wave_state)
        self.assertIsNotNone(boss)
        self.assertTrue(wave_state["boss_spawned"])
        self.assertGreaterEqual(spawn_timer, 0)


if __name__ == "__main__":
    unittest.main()
