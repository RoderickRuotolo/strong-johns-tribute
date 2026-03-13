# Architecture Overview

## Current State

The project currently has a monolithic prototype in `game.py` containing:

- bootstrapping and main loop
- rendering routines
- input handling
- entity definitions (`Player`, `Enemy`, `Boss`)
- combat and collision logic
- spawning and progression rules

## Target Folder Structure (next iterations)

```text
.
├── game.py                     # temporary entry point (to be slimmed down)
├── README.md
├── .codex/
│   ├── manifest.md
│   ├── instructions.md
│   └── architecture.md
├── src/
│   ├── core/
│   │   ├── game_loop.py
│   │   ├── config.py
│   │   └── state.py
│   ├── entities/
│   │   ├── player.py
│   │   ├── enemy.py
│   │   └── boss.py
│   ├── systems/
│   │   ├── input_system.py
│   │   ├── combat_system.py
│   │   ├── spawn_system.py
│   │   └── render_system.py
│   ├── ui/
│   │   └── hud.py
│   └── assets/
│       ├── sprites/
│       ├── audio/
│       └── fonts/
└── tests/
```

## High-Level Data Flow

1. Input system reads keyboard state and emits player intents.
2. Simulation updates entities and timers based on intents and elapsed time.
3. Combat system resolves hitboxes, damage, cooldowns, and deaths.
4. Spawn/progression system creates waves and boss encounters.
5. Render system draws world, entities, effects, and UI.
6. Main loop presents frame and repeats at target FPS.

## Core Runtime Loop

```text
poll events -> collect input -> update gameplay state -> resolve combat
-> spawn/progression -> render frame -> tick clock
```

## Immediate Refactor Priorities

1. Extract constants and colors into `config.py`.
2. Move entity classes to `src/entities/`.
3. Isolate combat and spawning into `src/systems/`.
4. Keep `game.py` as a thin composition layer.
