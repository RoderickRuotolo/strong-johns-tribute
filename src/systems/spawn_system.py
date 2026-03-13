import random

from src.core.config import WAVE_RULES
from src.entities.boss import Boss
from src.entities.enemy import Enemy


def init_wave_state():
    return {
        "wave": 1,
        "wave_timer": 0,
        "boss_spawned": False,
    }


def _pick_archetype(wave):
    if wave <= 2:
        return random.choice(["rush", "rush", "tank"])
    if wave <= 4:
        return random.choice(["rush", "tank", "ranged", "rush"])
    if wave <= 6:
        return random.choice(["rush", "tank", "ranged", "ranged"])
    return random.choice(["tank", "ranged", "rush", "ranged"])


def _wave_spawn_interval(wave):
    interval = WAVE_RULES["base_spawn_interval"] - wave * 8
    return max(WAVE_RULES["min_spawn_interval"], interval)


def _wave_enemy_cap(wave):
    cap = WAVE_RULES["base_enemy_cap"] + wave
    return min(WAVE_RULES["max_enemy_cap"], cap)


def update_spawning(spawn_timer, enemies, boss, wave_state):
    spawn_timer += 1
    wave_state["wave_timer"] += 1

    if wave_state["wave_timer"] >= WAVE_RULES["wave_duration_frames"]:
        if wave_state["wave"] < WAVE_RULES["max_wave"]:
            wave_state["wave"] += 1
        wave_state["wave_timer"] = 0

    if boss is None:
        spawn_interval = _wave_spawn_interval(wave_state["wave"])
        enemy_cap = _wave_enemy_cap(wave_state["wave"])

        if spawn_timer > spawn_interval and len(enemies) < enemy_cap:
            enemies.append(Enemy(_pick_archetype(wave_state["wave"])))
            spawn_timer = 0

        if (
            wave_state["wave"] >= WAVE_RULES["max_wave"]
            and wave_state["wave_timer"] > WAVE_RULES["wave_duration_frames"] // 3
            and len(enemies) >= max(4, enemy_cap - 1)
            and not wave_state["boss_spawned"]
        ):
            boss = Boss()
            wave_state["boss_spawned"] = True

    return spawn_timer, boss, wave_state
