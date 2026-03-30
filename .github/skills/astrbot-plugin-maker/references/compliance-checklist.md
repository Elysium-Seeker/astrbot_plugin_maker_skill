# Compliance Checklist For AstrBot Plugin Generation

## Metadata Compliance
- `metadata.yaml` exists.
- Required keys: `name`, `desc`, `version`, `author`.
- Optional keys are valid and documented (`display_name`, `support_platforms`, `astrbot_version`).
- `astrbot_version` follows PEP 440 and has no `v` prefix.

## Adapter Compliance
- `support_platforms` only contains supported keys:
  - aiocqhttp
  - qq_official
  - telegram
  - wecom
  - lark
  - dingtalk
  - discord
  - slack
  - kook
  - vocechat
  - weixin_official_account
  - satori
  - misskey
  - line

## Code Compliance
- No persistent data written in plugin source directory.
- Persistent data paths use AstrBot `data` directory.
- Network calls avoid `requests`; prefer async `aiohttp` or `httpx`.
- Error handling prevents single-failure crash.

## Test Compliance
- At least one smoke test exists.
- Behavior tests exist for non-trivial logic.
- Tests are runnable with `pytest`.

## Delivery Compliance
- Include debug and reload instructions.
- Include assumptions for ambiguous requirements.
- Keep generated code minimal and runnable.
