#!/usr/bin/env python3
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.entities.player import Player
from src.systems.ai_system import select_target_by_threat
from src.systems.combat_system import player_attack
from src.systems.spawn_system import init_wave_state, update_spawning


def main():
    random.seed(42)

    players = [Player(150, (255, 255, 255)), Player(260, (40, 100, 220))]
    enemies = []
    boss = None
    spawn_timer = 0
    wave_state = init_wave_state()

    frames = 3000
    start = time.perf_counter()

    for i in range(frames):
        for player in players:
            player.update()

        spawn_timer, boss, wave_state = update_spawning(spawn_timer, enemies, boss, wave_state)

        for enemy in enemies:
            target = select_target_by_threat(players, enemy.rect.centerx)
            enemy.move(target)
            for player in players:
                enemy.attack(player)
            enemy.update()

        if boss:
            target = select_target_by_threat(players, boss.rect.centerx)
            boss.move(target)
            for player in players:
                boss.attack(player)
            boss.update()

        for player in players:
            # deterministic periodic attacks
            if i % 40 == 0:
                player.queue_light_attack()
            if i % 125 == 0:
                player.queue_heavy_attack()

        hit_events = player_attack(players, enemies, boss)
        _ = len(hit_events)

    elapsed = time.perf_counter() - start
    fps = frames / elapsed if elapsed > 0 else 0.0
    print(f"frames={frames}")
    print(f"elapsed_seconds={elapsed:.4f}")
    print(f"sim_fps={fps:.2f}")


if __name__ == "__main__":
    main()
