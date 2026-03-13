# Performance Baseline

Date: 2026-03-13  
Environment: local dev machine, Python 3.12.3, pygame 2.5.2

Command:

```bash
./scripts/perf_pass.py
```

Result:

- frames: `3000`
- elapsed_seconds: `0.0586`
- sim_fps: `51164.87`

Notes:

- This is a logic-heavy simulation pass, not full render FPS.
- Use it comparatively across commits to catch major regressions.
