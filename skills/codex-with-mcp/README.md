# Codex with MCP

在 **Kimi** 和 **Claude Code** 中通过 MCP 调用 Codex CLI 进行代码分析、重构和审查。

## 快速开始

```bash
# 验证配置
./scripts/validate-codex-mcp.sh /path/to/codexmcp-0.7.4-py3-none-any.whl

# 在 Kimi 或 Claude Code 中说：
# "用 codex 分析一下这个项目的代码结构"
```

## 文档导航

| 文档 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | 完整使用指南和配置说明 |
| [USAGE.md](USAGE.md) | 5分钟快速入门 |
| [QUICKREF.md](QUICKREF.md) | 参数速查表 |
| [examples/](examples/) | 配置案例和故障排查 |

## 特性

- ✅ **双平台支持** - Kimi 和 Claude Code
- ✅ **配置验证** - 一键验证 MCP 配置
- ✅ **会话管理** - 支持多轮对话上下文
- ✅ **参数速查** - 完整的参数参考表

## 要求

- `codex` CLI (`pip install codex-cli`)
- `uvx` (`pip install uv`)
- MiniMax API Key
