# Release Checklist

Use this checklist before creating a tag/release.

## Pre-release

- [ ] Pull latest changes and resolve conflicts.
- [ ] Confirm `VERSION` is updated.
- [ ] Run tests: `python3 -m unittest discover -s tests -v`
- [ ] Run compile check: `python3 -m py_compile game.py $(rg --files -g '*.py' src | tr '\n' ' ')`
- [ ] Run perf pass: `./scripts/perf_pass.py`
- [ ] Validate game startup and core gameplay manually.

## Build

- [ ] Build executable: `./build.sh`
- [ ] Smoke test executable from `dist/`.

## Release Metadata

- [ ] Update changelog/release notes summary.
- [ ] Commit release prep changes.
- [ ] Create annotated tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Push branch and tags: `git push && git push --tags`

## Post-release

- [ ] Archive benchmark output in `.codex/performance-baseline.md`.
- [ ] Open next iteration milestone and update `.codex/roadmap.md`.
