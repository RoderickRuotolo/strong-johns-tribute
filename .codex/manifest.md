# AI Directives Manifest

This file defines where AI directives live in the project and how they are used.

## Scope

- `core` directives: permanent project-wide rules.
- `skill` directives: loaded on demand for specific tasks.

## Location Policy

All AI directive files must exist inside `.codex/`.

- Allowed: `.codex/*.md`, `.codex/skills/**`
- Not allowed: AI directives outside `.codex/`

## Recommended Read Order

1. `.codex/instructions.md` (general coding rules)
2. `.codex/architecture.md` (structure and data-flow view)
3. Task-specific skills (only when needed)

## Maintenance Conventions

- Update this manifest whenever a new directive or skill is added.
- Keep content concise, versionable, and auditable in Git.
- Avoid duplicating rules across files.
