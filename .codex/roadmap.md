# Development Roadmap

This roadmap is organized for incremental implementation.  
Each phase should result in a playable build.

## Phase 0 - Foundation (current step)

- [x] Create project-level documentation.
- [x] Create `.codex/` with `manifest.md`, `instructions.md`, and `architecture.md`.
- [ ] Add `.gitignore` tuned for Python/Pygame.
- [ ] Freeze minimum Python and dependency versions.
- [ ] Add a basic run script (`run.sh` or `Makefile` target).

## Phase 1 - Codebase Restructure (no feature changes)

- [ ] Create `src/` package layout (`core`, `entities`, `systems`, `ui`).
- [ ] Move constants/colors into `src/core/config.py`.
- [ ] Move `Player`, `Enemy`, and `Boss` into `src/entities/`.
- [ ] Move spawn/combat logic into `src/systems/`.
- [ ] Keep `game.py` as a thin entry point only.
- [ ] Confirm behavior parity with current prototype.

## Phase 2 - Core Beat'em Up Loop (MVP gameplay)

- [ ] Add left/right facing direction for players and enemies.
- [ ] Make attack hitboxes direction-aware.
- [ ] Add enemy knockback and short hit-stun on hit.
- [ ] Add player hurt feedback (flash or brief stun).
- [ ] Add basic victory and defeat states.
- [ ] Add game restart flow from end state.

## Phase 3 - Combat Depth

- [ ] Add combo chain (light x3 or similar).
- [ ] Add per-attack damage, range, and recovery tuning table.
- [ ] Add jump and optional air attack.
- [ ] Add grab or heavy attack prototype.
- [ ] Add invulnerability windows where needed for fairness.

## Phase 4 - Enemy and Encounter Design

- [ ] Define at least 3 enemy archetypes (rush, tank, ranged or gimmick).
- [ ] Add wave progression with pacing rules.
- [ ] Rework target selection (closest player / threat scoring).
- [ ] Add boss state machine (intro, phases, enraged pattern).
- [ ] Add boss defeat transition to clear/win screen.

## Phase 5 - Visual and Audio Pass

- [ ] Replace placeholder primitives with sprite pipeline.
- [ ] Add background layers and parallax.
- [ ] Add hit effects (impact sparks, shake, freeze-frame-lite).
- [ ] Add SFX for punches, damage, KO, and UI.
- [ ] Add music loop and volume settings.

## Phase 6 - UX, Settings, and Game Feel

- [ ] Add key rebinding support.
- [ ] Add pause menu with resume/restart/quit.
- [ ] Add options menu (audio, controls, display).
- [ ] Add polish pass for timings and input buffering.
- [ ] Improve HUD readability and feedback.

## Phase 7 - Stability and Packaging

- [ ] Add unit tests for pure logic modules.
- [ ] Add lightweight integration tests for combat/spawn behavior.
- [ ] Run performance pass on low-end hardware target.
- [ ] Package executable build (e.g., PyInstaller).
- [ ] Create release checklist and version tag process.

## Backlog (optional, after MVP)

- [ ] Local co-op drop-in/drop-out improvements.
- [ ] More stages and transitions.
- [ ] Character select and alternate move sets.
- [ ] Save system for progress and settings.
- [ ] Accessibility pass (high contrast, remap presets, screen shake toggle).

## Milestones

- **M1:** End of Phase 1 (clean modular architecture, same gameplay).
- **M2:** End of Phase 2 (solid playable MVP loop).
- **M3:** End of Phase 4 (full stage flow with proper boss encounter).
- **M4:** End of Phase 7 (stable packaged build).
