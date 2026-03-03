# 排查案例：Codex + MiniMax API 配置

## 问题描述

Codex CLI 配置了 MiniMax provider，但调用时：
1. 超时无响应，或
2. 返回 400 Bad Request 错误

## 环境信息

- Codex CLI: v0.57.0
- MiniMax API: https://api.minimaxi.com/v1
- 环境变量: `MINIMAX_API_KEY` 已设置

## 初始（错误）配置

```toml
# ~/.codex/config.toml (错误版本)
model = "minimax/minimax-2.5-highspeed"  # ❌ 错误

[model_providers.minimax]
name = "MiniMax Chat Completions API"
base_url = "https://api.minimaxi.com/v1"
env_key = "MINIMAX_API_KEY"
wire_api = "chat"
requires_openai_auth = false
```

## 排查步骤

### Step 1: 验证 MiniMax API 直接调用

```bash
curl -X POST https://api.minimaxi.com/v1/chat/completions \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -d '{"model": "MiniMax-M2.5", "messages": [{"role": "user", "content": "hi"}]}'
```

✅ **结果**: API 直接调用成功，说明 API Key 有效

### Step 2: 检查 Codex 日志

```bash
RUST_LOG=debug codex exec --model minimax-2.5-highspeed ...
```

发现关键日志：
```
provider=ModelProviderInfo { name: "OpenAI", ... }  # ❌ 使用了 OpenAI provider
```

**问题 1**: Codex 没有识别 MiniMax provider，而是使用了默认的 OpenAI

### Step 3: 查阅 Codex 源码

在 `codex-rs/core/src/config/mod.rs` 中发现：
```rust
let model_provider_id = model_provider
    .or(config_profile.model_provider)
    .or(cfg.model_provider)
```

Codex 从 `model_provider` 配置项获取 provider，而不是从 model 字符串解析！

### Step 4: 添加 model_provider 配置

```toml
model = "minimax-2.5-highspeed"
model_provider = "minimax"  # ✅ 添加这行
```

再次测试，日志显示：
```
provider_name=MiniMax Chat Completions API  # ✅ 正确识别
```

但出现新的错误：
```
POST to https://api.minimaxi.com/v1/chat/completions status=400 Bad Request
```

### Step 5: 验证模型名称

```bash
# 测试 Codex 使用的模型名称
curl ... -d '{"model": "minimax-2.5-highspeed", ...}'
# 返回: invalid params, unknown model 'minimax-2.5-highspeed'

curl ... -d '{"model": "MiniMax-M2.5", ...}'
# ✅ 成功
```

**问题 2**: MiniMax API 不识别 `minimax-2.5-highspeed`，需要使用 `MiniMax-M2.5`

## 解决方案

### 正确的 config.toml

```toml
# ~/.codex/config.toml (正确版本)

# 1. 使用 MiniMax 支持的模型名称
model = "MiniMax-M2.5"

# 2. 必须指定 model_provider，否则 Codex 会使用默认的 OpenAI
model_provider = "minimax"

model_reasoning_effort = "medium"
sandbox = "workspace-write"
ask_for_approval = "on-failure"

[model_providers.minimax]
name = "MiniMax Chat Completions API"
base_url = "https://api.minimaxi.com/v1"
env_key = "MINIMAX_API_KEY"
wire_api = "chat"  # MiniMax 只支持 chat API
requires_openai_auth = false
request_max_retries = 4
stream_max_retries = 10
stream_idle_timeout_ms = 300000
```

### MCP 配置 (~/.kimi/mcp.json)

```json
{
  "mcpServers": {
    "codex": {
      "command": "uvx",
      "args": [
        "--from",
        "/path/to/codexmcp-0.7.4-py3-none-any.whl",
        "codexmcp"
      ],
      "env": {
        "MINIMAX_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## 验证测试

```bash
# 测试 Codex 调用
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Say hello"
```

预期输出：
```json
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"type":"agent_message","text":"Hello! How can I help you today?"}}
{"type":"turn.completed",...}
```

## 关键要点

| 配置项 | 错误值 | 正确值 | 说明 |
|--------|--------|--------|------|
| `model` | `minimax-2.5-highspeed` | `MiniMax-M2.5` | 必须使用 MiniMax 支持的模型名称 |
| `model_provider` | 未设置 | `minimax` | 必须显式指定，否则使用默认 OpenAI |
| `wire_api` | `responses` | `chat` | MiniMax 只支持 chat API |

## 相关命令

```bash
# 验证配置
~/.claude/skills/codex-with-mcp/scripts/validate-codex-mcp.sh

# 查看 MCP 配置
~/.claude/skills/codex-with-mcp/scripts/show-mcp-config.sh

# 启用调试日志
RUST_LOG=debug codex exec ...
```

## 参考资料

- [MiniMax API 文档](https://www.minimaxi.com/document)
- [Codex CLI 配置文档](https://github.com/openai/codex/blob/main/docs/config.md)
- [Codex Model Provider 源码](https://github.com/openai/codex/blob/main/codex-rs/core/src/model_provider_info.rs)
