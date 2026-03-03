# Codex with MCP - 5分钟快速入门

## 环境要求

- `codex` CLI 已安装 (`pip install codex-cli`)
- `uvx` 已安装 (`pip install uv`)
- MCP 服务器已配置（见 [SKILL.md](SKILL.md)）

## 1分钟验证

```bash
# 验证配置
./scripts/validate-codex-mcp.sh /path/to/codexmcp-0.7.4-py3-none-any.whl

# 验证 MCP 服务器（Claude Code）
claude mcp list
```

## 3种使用方式

| 方式 | 命令/操作 | 适用场景 |
|------|----------|---------|
| **Kimi MCP** | 直接说 "用 codex 分析代码" | 自然语言交互 |
| **Claude Code MCP** | 直接说 "用 codex 分析代码" | 自然语言交互 |
| **直接 CLI** | `codex exec -- "prompt"` | 脚本自动化 |

## 3分钟上手

### 方式一：通过 AI 助手（推荐）

**Kimi 或 Claude Code 中直接说：**
```
用 codex 分析一下这个项目的代码结构
```

### 方式二：直接命令行

```bash
cd /your/project

codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  -- "Review this code for bugs"
```

### 方式三：使用脚本

```bash
./scripts/call-codex.sh \
  --prompt "List all functions" \
  --cd /your/project \
  --sandbox read-only
```

## 常用命令速查

```bash
# 代码审查
codex exec --sandbox read-only -- "Review this code"

# 代码重构（可写入）
codex exec --sandbox workspace-write -- "Refactor auth module"

# 继续上次会话
codex exec resume <SESSION_ID> -- "Continue analysis"

# 查看帮助
codex exec --help
```

## 详细文档

- **[SKILL.md](SKILL.md)** - 完整使用指南和配置说明
- **[QUICKREF.md](QUICKREF.md)** - 参数速查表
- **[examples/](examples/)** - 配置案例和故障排查

## 故障快速排查

| 问题 | 快速解决 |
|------|---------|
| MCP 连不上 | `claude mcp list` 或检查 `~/.kimi/mcp.json` |
| 400 错误 | 检查模型名称是否为 `MiniMax-M2.5` |
| Provider 错误 | 检查 `config.toml` 中 `model_provider = "minimax"` |

详细排查：[troubleshooting-minimax-setup.md](examples/troubleshooting-minimax-setup.md)
