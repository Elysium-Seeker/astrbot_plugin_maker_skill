# astrbot-plugin-maker-skill

用于 VS Code Copilot 的工作区 Skill，目标是把自然语言需求转换为 AstrBot 插件实现，并自动包含合规检查与测试骨架。

## 功能
- 自然语言需求 -> 插件实现计划与代码落地
- `metadata.yaml` 合规生成
- `requirements.txt` 依赖模板
- 测试模板（smoke / behavior / OpenAPI 鉴权与响应结构）
- AstrBot OpenAPI 集成参考（`X-API-Key`、`/api/v1/*`、401/403 处理）

## 目录
- `.github/skills/astrbot-plugin-maker/SKILL.md`
- `.github/skills/astrbot-plugin-maker/references/`
- `.github/skills/astrbot-plugin-maker/assets/`

## 使用
1. 在 VS Code Chat 输入 `/astrbot-plugin-maker`
2. 直接描述需求：功能、触发方式、平台、约束
3. 让其按合规清单实现并生成测试

## 参考
- AstrBot 插件开发指南: https://docs.astrbot.app/dev/star/plugin-new.html
- AstrBot OpenAPI: https://docs.astrbot.app/scalar.html
