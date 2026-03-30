# AstrBot Plugin New Checklist (Official-doc aligned)

## Environment Setup
1. Create plugin repository from template (helloworld):
   - https://github.com/Soulter/helloworld
2. Repository naming rules:
   - prefer prefix astrbot_plugin_
   - lowercase only
   - no spaces
   - keep short
3. Local setup example:

```bash
git clone https://github.com/AstrBotDevs/AstrBot
mkdir -p AstrBot/data/plugins
cd AstrBot/data/plugins
git clone <your_plugin_repo_url>
```

4. Open AstrBot project in VS Code and locate plugin under data/plugins/<plugin_name>.

## Must-have Metadata
AstrBot relies on metadata.yaml to identify plugin metadata.

Required minimum:
- name
- desc
- version
- author

Optional common fields:
- display_name
- support_platforms (list[str])
- astrbot_version (PEP 440 constraint, no v prefix)

AstrBot version examples:
- >=4.17.0
- >=4.16,<5
- ~=4.17

## Adapter Keys For support_platforms
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

## Optional Assets
- logo.png in plugin root
- 1:1 ratio, recommended 256x256

## Debug and Reload
- Start AstrBot runtime for plugin debugging.
- After code changes, use WebUI plugin management and reload plugin.
- If load fails, use one-click reload/repair option in management panel.

## Dependency Management
- Use requirements.txt for third-party dependencies.
- Missing dependencies can break plugin installation.

## Development Principles
- Test features before release.
- Keep useful comments.
- Store persistent data under data directory, not plugin directory.
- Add robust error handling.
- Prefer async HTTP clients (aiohttp/httpx), avoid requests.
- Run ruff formatting before commit.

## Related Docs
- New plugin guide: https://docs.astrbot.app/dev/star/plugin-new.html
- Minimal example: https://docs.astrbot.app/dev/star/guides/simple.html
- Plugin publish: https://docs.astrbot.app/dev/star/plugin-publish.html