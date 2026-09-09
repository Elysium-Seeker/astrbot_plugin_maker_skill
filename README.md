# AstrBot Plugin Maker Skill

帮助编码 Agent 根据自然语言需求创建、修复和测试 AstrBot Python 插件。
包含可运行的插件脚手架、按需读取的 API 参考、静态检查工具和调用实际实现的测试。

## 使用 Skill

将完整的 `.github/skills/astrbot-plugin-maker/` 文件夹放进目标项目的
`.github/skills/` 下，保留 `references/`、`assets/` 和 `scripts/`。
在支持 Agent Skills 的 VS Code Copilot Chat 中输入 `/astrbot-plugin-maker`，
或描述 AstrBot 插件开发需求。参见 [VS Code Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)。

例如：

> 为 AstrBot 4.28.0 写一个 /divide 指令，接收两个数字，小数位数可以配置，除数为零时给出提示。实现并运行本地测试。

也可以指定现有插件路径和错误现象，让 Agent 做局部修复。
其他支持 `SKILL.md` 的工具应将**整个技能文件夹**放到各自支持的技能目录；
本仓库不修改全局 Agent 配置。

## 能力与材料

| 内容 | 入口 |
| --- | --- |
| 创建、修复、验证流程 | [SKILL.md](.github/skills/astrbot-plugin-maker/SKILL.md) |
| 官方文档、固定版本源码及已知差异 | [来源索引](.github/skills/astrbot-plugin-maker/references/sources.md) |
| 生命周期、命令、配置、存储、消息、LLM 工具 | [Python API 参考](.github/skills/astrbot-plugin-maker/references/api-patterns.md) |
| 元数据、平台声明、依赖、发布准备 | [插件打包](.github/skills/astrbot-plugin-maker/references/plugin-new-checklist.md) |
| HTTP 鉴权、scope、JSON/SSE/文件响应 | [OpenAPI 参考](.github/skills/astrbot-plugin-maker/references/openapi-integration.md) |
| 离线测试、真实 SDK 测试、重载排查 | [测试指南](.github/skills/astrbot-plugin-maker/references/testing-guide.md) |

资料核对日期为 **2026-09-09**，基线为 **AstrBot v4.28.0 / Python 3.12+**。
对应源码提交记录在来源索引中。旧版本开发应重新核对所用 API 和版本下限。

## 直接运行脚手架

从本仓库根目录执行，目标目录必须尚不存在：

```bash
python .github/skills/astrbot-plugin-maker/scripts/scaffold_plugin.py ../astrbot_plugin_demo --author "Your Name" --description "My plugin" --command greet
```

脚手架只使用 Python 标准库，生成配置问候语示例，包含 `main.py`、
`plugin_logic.py`、元数据、配置 schema、开发依赖和两层测试。
它拒绝覆盖现有目录，不安装运行时或发布插件。需要真实功能时应替换示例逻辑及其测试。

- `--repo URL`：填写已知的插件仓库地址；未提供时省略，避免生成虚构地址。
- `--astrbot-version ">=4.28.0"`：声明经过验证的版本约束，默认使用示例基线。
- `--with-openapi`：额外生成 `/im/bots` HTTP 客户端、运行时依赖和模拟传输测试。
  该客户端供实际功能接入，示例问候指令不会自动调用它。

进入生成目录，按其 `README.md` 安装开发依赖并运行测试。需要静态检查时：

```bash
python -m pip install PyYAML packaging
python .github/skills/astrbot-plugin-maker/scripts/validate_plugin.py ../astrbot_plugin_demo
```

## 维护与验证

从本仓库根目录，在独立开发环境中执行：

```bash
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
python -m ruff check .github/skills/astrbot-plugin-maker/scripts tests
python -m ruff format --check .github/skills/astrbot-plugin-maker/scripts tests
```

仓库测试覆盖普通/HTTP 两种脚手架、拒绝覆盖、中文与多行元数据、错误文件、
配置和版本约束、资源链接，以及生成测试能否发现实际实现的回归。
[CI](.github/workflows/validate.yml) 在 Windows/Linux 上运行这些检查，另用真实
`astrbot==4.28.0` 检查插件注册、配置注入和消息结果。

静态检查不导入插件；离线行为测试不连接服务；真实 SDK 检查也不启动 WebUI
或真实消息平台。插件加载、重载和目标适配器的实际行为需要在开发运行时验证，
不能把某一层检查通过写成完整集成或市场审核通过。
