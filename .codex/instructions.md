# General Coding Instructions

## Principles

- Prioritize readability and simplicity.
- Keep module coupling low.
- Prefer small functions with single responsibility.
- Do not break existing behavior without explicit intent.

## Language and Stack

- Main language: Python 3.
- Current framework: Pygame.

## Organization Standards

- Split gameplay logic, rendering, and input into separate modules.
- Avoid global state for critical gameplay data when possible.
- Centralize gameplay constants and balancing values.

## Quality Expectations

- Add tests as modules become decoupled and testable.
- Validate changes by running the game locally.
- Fix warnings and errors before moving to the next feature step.

## Style Conventions

- Use PEP 8 as the baseline.
- Use clear names for classes, functions, and variables.
- Add short comments only for non-trivial logic blocks.

## Performance and Game Loop

- Prefer `delta time` updates when systems become time-sensitive.
- Avoid unnecessary allocations inside the main loop.
- Keep rendering concerns separate from gameplay rules.

## Evolution Guidelines

- Refactor from single-file prototype to modular architecture.
- Build systems by layers: input, simulation, combat, UI, audio.
- Record major architecture decisions in `.codex/architecture.md`.
