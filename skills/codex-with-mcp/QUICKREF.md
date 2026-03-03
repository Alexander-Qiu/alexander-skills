# Codex with MCP - 参数速查表

快速查找所有配置参数、命令和选项。

## 目录

- [MCP 配置参数](#mcp-配置参数)
- [Codex CLI 参数](#codex-cli-参数)
- [Sandbox 级别](#sandbox-级别)
- [常用命令模板](#常用命令模板)
- [输出字段参考](#输出字段参考)

---

## MCP 配置参数

### Kimi (`~/.kimi/mcp.json`)

```json
{
  "mcpServers": {
    "codex": {
      "command": "uvx",
      "args": [
        "--from",
        "/absolute/path/to/codexmcp-0.7.4-py3-none-any.whl",
        "codexmcp"
      ],
      "env": {
        "MINIMAX_API_KEY": "sk-api-xxx"
      }
    }
  }
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `command` | string | ✅ | 启动命令 (`uvx`) |
| `args` | array | ✅ | 命令参数 |
| `env` | object | ❌ | 环境变量 |

### Claude Code (`claude mcp`)

```bash
# 添加服务器
claude mcp add codex -s user --transport stdio -- \
  uvx --from /path/to/codexmcp-0.7.4-py3-none-any.whl codexmcp

# 带环境变量
claude mcp add codex -s user -e MINIMAX_API_KEY=xxx -- \
  uvx --from /path/to/wheel codexmcp
```

| 参数 | 说明 |
|------|------|
| `-s user` | 用户级配置（所有项目可用） |
| `-s project` | 项目级配置（仅当前项目） |
| `-e KEY=VALUE` | 设置环境变量 |
| `--transport stdio` | 传输方式 |

---

## Codex CLI 参数

### 全局选项

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--model` | `-m` | `MiniMax-M2.5` | 模型名称 |
| `--config` | `-c` | - | 配置键值对 |
| `--sandbox` | - | `read-only` | 沙盒级别 |
| `--cd` | `-C` | 当前目录 | 工作目录 |
| `--skip-git-repo-check` | - | false | 跳过 git 检查 |
| `--json` | - | false | JSON 输出格式 |
| `--full-auto` | - | false | 全自动模式 |
| `--return_all_messages` | - | false | 返回完整消息 |

### 配置项 (`--config`)

| 配置键 | 可选值 | 说明 |
|--------|--------|------|
| `model_reasoning_effort` | `low`, `medium`, `high`, `xhigh` | 推理 effort 级别 |
| `model_provider` | `minimax`, `openai` | 模型提供商 |

---

## Sandbox 级别

| 级别 | 权限 | 风险 | 适用场景 |
|------|------|------|----------|
| `read-only` | 只读文件系统 | ⭐⭐⭐ 最安全 | 代码审查、分析 |
| `workspace-write` | 可修改工作区 | ⭐⭐ 中等 | 重构、编辑文件 |
| `danger-full-access` | 完全系统访问 | ⭐ 危险 | 系统级更改 |

**推荐：始终从 `read-only` 开始，确认安全后再升级。**

---

## 常用命令模板

### 代码审查

```bash
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Review this code for bugs and suggest improvements"
```

### 代码重构

```bash
codex exec \
  --model MiniMax-M2.5 \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --full-auto \
  --json \
  -- "Refactor auth module to use async/await"
```

### 多轮会话

```bash
# 开始会话
result=$(codex exec --json -- "Initial analysis")
# 提取 SESSION_ID...

# 继续会话
codex exec resume <SESSION_ID> --json -- "Continue analysis"
```

### 分析特定目录

```bash
codex exec \
  -C /path/to/project \
  --sandbox read-only \
  -- "Analyze the src/ directory"
```

---

## 输出字段参考

Codex 返回 JSON Lines 格式。

### 事件类型

| 类型 | 字段 | 说明 |
|------|------|------|
| `thread.started` | `thread_id` | 会话开始 |
| `turn.started` | - | 轮次开始 |
| `item.completed` | `item` | 项目完成 |
| `turn.completed` | `usage` | 轮次完成 |

### Item 子类型

| 类型 | 字段 | 内容 |
|------|------|------|
| `agent_message` | `text` | AI 回复文本 |
| `command_execution` | `command`, `output` | 执行的命令 |
| `file_edit` | `path`, `contents` | 文件修改 |
| `tool_call` | `name`, `arguments` | 工具调用 |

### 解析示例

```bash
# 提取 AI 回复
codex exec ... | grep 'agent_message' | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    print(d['item']['text'])
"

# 提取使用量
codex exec ... | grep 'turn.completed' | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    print(d['usage'])
"
```

---

## 环境变量

| 变量 | 说明 | 配置位置 |
|------|------|----------|
| `MINIMAX_API_KEY` | MiniMax API 密钥 | `mcp.json` env 或 `-e` |
| `RUST_LOG` | 调试日志级别 | 运行时设置 |

---

## 平台对比速查

| 功能 | Kimi | Claude Code |
|------|------|-------------|
| 配置方式 | `~/.kimi/mcp.json` | `claude mcp add` |
| 查看配置 | `cat ~/.kimi/mcp.json` | `claude mcp list` |
| 验证状态 | 脚本验证 | `claude mcp get codex` |
| 移除服务器 | 编辑 JSON | `claude mcp remove codex` |
| 调用方式 | 自然语言 | 自然语言 |

---

## 故障代码速查

| 错误 | 原因 | 解决 |
|------|------|------|
| `400 Bad Request` | 模型名称错误 | 使用 `MiniMax-M2.5` |
| `Provider=OpenAI` | 未设置 `model_provider` | 设置 `model_provider = "minimax"` |
| `MCP not found` | 服务器未配置 | 检查 mcp.json 或 `claude mcp list` |
| `Timeout` | 请求超时 | 检查网络/API 状态 |

---

## 相关文档

- [SKILL.md](SKILL.md) - 完整使用指南
- [USAGE.md](USAGE.md) - 5分钟快速入门
- [examples/](examples/) - 配置案例
