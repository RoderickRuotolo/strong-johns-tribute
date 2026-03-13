# Beat'em Up Project (inspired by "Strong Johns")

This repository contains the foundation of a personal Beat'em Up game built with Python and Pygame.

## Current Goal

Set up a solid technical baseline for iterative development:

1. Organize project docs and AI directives.
2. Define an initial software architecture.
3. Establish an incremental development flow.

## Initial Structure

- `game.py`: current playable single-file prototype.
- `.codex/roadmap.md`: phased implementation plan with actionable checklists.
- `.codex/manifest.md`: AI directive inventory and loading policy.
- `.codex/instructions.md`: general coding and development rules.
- `.codex/architecture.md`: folder overview and data flow view.

## Run Locally

```bash
python3 -m pip install -r requirements.txt
./run.sh
```

## Quality and Build

```bash
python3 -m unittest discover -s tests -v
./scripts/perf_pass.py
./build.sh
```

Release process assets:

- `VERSION`
- `.codex/release-checklist.md`
- `.codex/performance-baseline.md`

## Project Status

Current version is an early prototype with:

- 2 local players.
- combo + heavy + air attack prototype.
- enemy archetypes (rush, tank, ranged).
- wave progression with pacing.
- boss phases (intro, phase 1, phase 2, enraged).
- sprite-based render pipeline with cached procedural sprites.
- parallax background layers.
- hit FX (sparks, screen shake, freeze-frame-lite).
- SFX and looping background music (with automatic fallback if audio init fails).
- health HUD.

## Current Controls

- `Player 1`: move `A/D`, jump `W`
- `Player 2`: move `Left/Right`, jump `Up`
- `Space`: light attack / combo (`x3`) for both players
- `Left Shift`: heavy attack for both players
- `Esc`: pause menu (resume/restart/options/quit)
- `R`: restart after victory/defeat

All controls can be rebound in-game:

- `Esc` -> `Options` -> `Controls`

## UX and Settings

- Pause menu with resume/restart/options/quit.
- Options for master volume, screen shake toggle, and fullscreen toggle.
- Input buffering for light/heavy attacks to improve responsiveness.
- HUD feedback for combo stage, invulnerability state, and air/ground state.

## AI Directive Policy

All AI directives (core and on-demand skills) must stay under `.codex/`.
