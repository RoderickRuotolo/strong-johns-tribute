# Development Roadmap

This roadmap is organized for incremental implementation.  
Each phase should result in a playable build.

## Phase 0 - Foundation (current step)

- [x] Create project-level documentation.
- [x] Create `.codex/` with `manifest.md`, `instructions.md`, and `architecture.md`.
- [x] Add `.gitignore` tuned for Python/Pygame.
- [x] Freeze minimum Python and dependency versions.
- [x] Add a basic run script (`run.sh` or `Makefile` target).

## Phase 1 - Codebase Restructure (no feature changes)

- [x] Create `src/` package layout (`core`, `entities`, `systems`, `ui`).
- [x] Move constants/colors into `src/core/config.py`.
- [x] Move `Player`, `Enemy`, and `Boss` into `src/entities/`.
- [x] Move spawn/combat logic into `src/systems/`.
- [x] Keep `game.py` as a thin entry point only.
- [ ] Confirm behavior parity with current prototype.

## Phase 2 - Core Beat'em Up Loop (MVP gameplay)

- [x] Add left/right facing direction for players and enemies.
- [x] Make attack hitboxes direction-aware.
- [x] Add enemy knockback and short hit-stun on hit.
- [x] Add player hurt feedback (flash or brief stun).
- [x] Add basic victory and defeat states.
- [x] Add game restart flow from end state.

## Phase 3 - Combat Depth

- [x] Add combo chain (light x3 or similar).
- [x] Add per-attack damage, range, and recovery tuning table.
- [x] Add jump and optional air attack.
- [x] Add grab or heavy attack prototype.
- [x] Add invulnerability windows where needed for fairness.

## Phase 4 - Enemy and Encounter Design

- [x] Define at least 3 enemy archetypes (rush, tank, ranged or gimmick).
- [x] Add wave progression with pacing rules.
- [x] Rework target selection (closest player / threat scoring).
- [x] Add boss state machine (intro, phases, enraged pattern).
- [x] Add boss defeat transition to clear/win screen.

## Phase 5 - Visual and Audio Pass

- [x] Replace placeholder primitives with sprite pipeline.
- [x] Add background layers and parallax.
- [x] Add hit effects (impact sparks, shake, freeze-frame-lite).
- [x] Add SFX for punches, damage, KO, and UI.
- [x] Add music loop and volume settings.

## Phase 6 - UX, Settings, and Game Feel

- [x] Add key rebinding support.
- [x] Add pause menu with resume/restart/quit.
- [x] Add options menu (audio, controls, display).
- [x] Add polish pass for timings and input buffering.
- [x] Improve HUD readability and feedback.

## Phase 7 - Stability and Packaging

- [x] Add unit tests for pure logic modules.
- [x] Add lightweight integration tests for combat/spawn behavior.
- [x] Run performance pass on low-end hardware target.
- [x] Package executable build (e.g., PyInstaller).
- [x] Create release checklist and version tag process.

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

## Version 0.2 Roadmap (2P Split Controls + Beat'em Up Plane)

### V2 Phase 1 - Mode Select and Session Setup

- [ ] Add start menu with mode selection: `1 Player` or `2 Players`.
- [ ] In `1 Player` mode, instantiate only Player 1 systems and HUD.
- [ ] In `2 Players` mode, instantiate both players and shared encounter flow.
- [ ] Ensure restart flow preserves selected mode until returning to title.

### V2 Phase 2 - Fixed Per-Player Control Schemes

- [ ] Disable shared attack triggers; route attacks per player.
- [ ] Set Player 1 movement to `A` (left), `W` (up), `S` (down), `D` (right).
- [ ] Set Player 2 movement to `Left`, `Up`, `Down`, `Right`.
- [ ] Set Player 1 actions: `2` (light attack), `1` (jump), `3` (heavy attack).
- [ ] Set Player 2 actions: `.` (light attack), `,` (jump), `;` (heavy attack).
- [ ] Keep pause/menu controls globally accessible and conflict-free.
- [ ] Update controls menu to show default split layout clearly.

### V2 Phase 3 - Beat'em Up Movement Plane (Horizontal + Depth)

- [ ] Add movement on depth axis (`up/down`) with bounded walkable lane.
- [ ] Convert world positioning to side-scrolling beat'em up plane (`x` + `depth`).
- [ ] Update collision and hit checks to consider depth distance tolerance.
- [ ] Restrict attacks to targets inside horizontal range and depth range.
- [ ] Update enemy navigation to chase player on both `x` and `depth`.
- [ ] Update boss navigation/attacks for depth-aware engagement.

### V2 Phase 4 - Camera, Rendering, and UX for Side-Scrolling Lane

- [ ] Add camera follow behavior prioritizing active player centroid.
- [ ] Keep side-scrolling flow while preserving readable vertical depth.
- [ ] Add player/enemy shadow or grounding cue for depth readability.
- [ ] Update HUD labels to indicate active mode (`1P` / `2P`) and control hints.

### V2 Phase 5 - Validation and Balancing

- [ ] Add unit tests for split input mapping and per-player action dispatch.
- [ ] Add integration test for `1P` mode (no Player 2 dependency paths).
- [ ] Add integration test for `2P` mode simultaneous combat.
- [ ] Add integration test for depth-aware hit validation.
- [ ] Run performance pass with depth movement and updated camera logic.

### V2 Milestones

- **V2-M1:** Title menu + mode selection stable.
- **V2-M2:** Split controls fully independent for both players.
- **V2-M3:** Depth movement and depth-aware combat stable.
- **V2-M4:** Release candidate for `v0.2.0`.
