# Testing Guide For Generated AstrBot Plugins

## Goal
Provide baseline confidence that plugin can be imported and key behavior works.

## Recommended Test Layers
1. Smoke test:
   - plugin module import succeeds
   - core class/function exists
2. Behavior test:
   - key function returns expected output
   - handles invalid input gracefully
3. Optional integration test:
   - run under AstrBot runtime when environment is available

## Suggested Layout
- tests/test_plugin_smoke.py
- tests/test_plugin_behavior.py

## Run Commands
```bash
pytest -q
```

## Notes
- Keep tests deterministic and offline.
- For async code, use `pytest.mark.asyncio` when required.
