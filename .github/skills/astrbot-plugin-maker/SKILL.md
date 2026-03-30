---
name: astrbot-plugin-maker
description: "Create AstrBot plugin scaffolds and compliant implementations from natural-language requirements based on official docs. Use when user asks to build, scaffold, implement, test, or publish an AstrBot plugin, including metadata.yaml, requirements.txt, compliance checks, and test generation."
argument-hint: "Describe plugin requirement in natural language: features, triggers, adapters, and constraints"
---

# AstrBot Plugin Maker

## When to Use
- User asks to create a new AstrBot plugin.
- User asks for a plugin scaffold in an existing plugin folder.
- User gives natural-language requirements and expects end-to-end compliant implementation.
- User needs plugin features that call AstrBot HTTP API endpoints.
- User asks for metadata.yaml fields, adapter support declaration, or AstrBot version constraints.
- User asks for debug/reload workflow, dependency setup, or automated tests for plugin packaging.

## Inputs To Collect
1. Plugin repository/folder name (recommended prefix: astrbot_plugin_).
2. Plugin purpose and main features.
3. Target adapters (optional): aiocqhttp, qq_official, telegram, wecom, lark, dingtalk, discord, slack, kook, vocechat, weixin_official_account, satori, misskey, line.
4. Minimal AstrBot version constraint (optional), e.g. >=4.17.0.
5. Required third-party dependencies.
6. Test preference: smoke tests only, or unit + smoke tests.
7. Whether plugin must call AstrBot OpenAPI endpoints.

## Procedure
1. Confirm scope: create only plugin files or also setup local AstrBot runtime.
2. Create or verify plugin directory naming:
   - lowercase
   - no spaces
   - prefer astrbot_plugin_<name>
3. Generate plugin metadata first, because AstrBot identifies plugin metadata through metadata.yaml.
4. Add optional fields when user provides them:
   - display_name
   - support_platforms
   - astrbot_version (PEP 440 style, no v prefix)
5. Convert natural-language requirement into a concrete implementation plan:
   - feature list
   - event/command triggers
   - input/output behavior
   - error paths and fallback behavior
6. Implement code and configuration files from that plan.
7. If OpenAPI access is required, apply API integration baseline:
   - base server default: http://localhost:6185
   - endpoint family: /api/v1/*
   - auth header: X-API-Key
   - handle 401/403 explicitly with clear error messages
8. Run compliance gate before finishing:
   - only documented metadata keys
   - supported adapter keys only
   - persistent data must go to data directory
   - avoid requests, prefer aiohttp/httpx
9. Add requirements.txt when dependencies are used.
10. Add tests:
   - create test files from templates
   - include at least one smoke test for import/basic wiring
   - include behavior tests when logic is present
   - if using OpenAPI, include auth-failure and response-shape tests
11. Add logo.png guidance (optional, 1:1, recommended 256x256).
12. Provide debug workflow:
   - run AstrBot runtime
   - use WebUI plugin management to reload plugin after code changes
13. Apply development principles before finishing:
   - tests and comments
   - store persistent data under data directory (not plugin root)
   - robust error handling
   - async HTTP clients preferred (aiohttp/httpx), avoid requests
   - format code with ruff before commit

## Required Outputs
- metadata.yaml created and validated
- requirements.txt created when needed
- code implementation generated from natural-language requirement
- test files created (at least smoke tests)
- implementation checklist delivered to user

## Use These Resources
- Official checklist: [plugin-new-checklist](./references/plugin-new-checklist.md)
- NL-to-implementation workflow: [nl-to-implementation](./references/nl-to-implementation.md)
- Compliance checklist: [compliance-checklist](./references/compliance-checklist.md)
- Testing guide: [testing-guide](./references/testing-guide.md)
- OpenAPI integration guide: [openapi-integration](./references/openapi-integration.md)
- Metadata template: [metadata.yaml.template](./assets/metadata.yaml.template)
- Dependency template: [requirements.txt.template](./assets/requirements.txt.template)
- Test template: [test_plugin_smoke.py.template](./assets/test_plugin_smoke.py.template)
- Startup commands: [dev-commands](./assets/dev-commands.txt)

## Constraints
- Keep generated examples minimal and runnable.
- Do not fabricate unsupported adapters or undocumented metadata keys.
- If runtime API details are uncertain, point user to "minimal example" docs and mark TODOs clearly.