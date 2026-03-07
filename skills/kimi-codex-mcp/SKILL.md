---
name: kimi-codex-mcp
description: Use when Kimi CLI needs to invoke Codex through MCP reliably, including Kimi MCP setup, `kimi -yp` with Codex, Kimi calling Codex for review or coding help, or when native `codex mcp-server` fails under Kimi with errors like `initialize called more than once`.
---

# Kimi Codex MCP

KIMI-ONLY: This skill is designed only for Kimi, Kimi Code, and Kimi CLI.
If the current agent is not Kimi-family, do not use this skill.

Use this skill for Kimi-specific Codex integration only.

## When to use this instead of `codex-with-mcp`

- The client is Kimi CLI.
- You want `kimi -yp` or `kimi --mcp-config-file ...` to call Codex.
- Native `codex mcp-server` works in `kimi mcp test` but fails in real tool use.
- You see `initialize called more than once`.

## Core rule

For Kimi, prefer the compatibility MCP wrapper in `scripts/start-kimi-codex-mcp.sh`.
Do not point Kimi directly at native `codex mcp-server` unless you are debugging protocol compatibility.
When the user says `codex review`, `let codex check`, `让 codex 检查`, `inspect with codex`, or asks Codex for refactor advice, prefer a single `codex_review` call.
Do not use multi-step Codex conversations unless the user explicitly asks to continue a previous Codex thread.
Keep each review/check/refactor pass stateless by default.

## Why

Kimi's MCP loading path and Codex's native MCP server are not consistently compatible in long-lived sessions.
The compatibility wrapper keeps only the Kimi-facing edge as MCP and performs the actual work through direct `codex exec` calls.
That removes the previous MCP-over-MCP hop and makes one-shot review calls simpler and more stable.

## Recommended setup

Create an MCP config like this:

```json
{
  "mcpServers": {
    "codex": {
      "command": "/mnt/data/qrz-dev/mem/alexander-skills/skills/kimi-codex-mcp/scripts/start-kimi-codex-mcp.sh",
      "args": [],
      "env": {
        "ZENMUX_ONDEMAND_API_KEY": "sk-ai-v1-..."
      }
    }
  }
}
```

Then run:

```bash
kimi --mcp-config-file /path/to/mcp.json -yp "Use the codex MCP tool ..."
```

## Routes

The wrapper exposes two routes through the same `codex` tool:

- `default`: use Codex's normal subscription-backed configuration
- `ondemand-gemini`: use `zenmux` with `google/gemini-3-flash-preview`

For `default`, the wrapper first tries the normal logged-in Codex configuration with no override.
If that fails because of quota, auth, or provider connectivity issues, it checks `~/.codex/config.toml` first and then `~/.codex/codex-mcp.env` for `ZENMUX_ONDEMAND_API_KEY`.
If a usable fallback exists, it retries with `zenmux` and `google/gemini-3-flash-preview`.

Use `ondemand-gemini` only when you want to force the fallback route immediately instead of waiting for the default route to fail first.

## Recommended usage

For Kimi review workflows, use a single stateless call:

```text
Use the codex_review tool once on the current repository.
Return:
1. findings
2. risks
3. a better next-step plan
Do not call codex multiple times.
```

This is the most reliable path for prompts like:

- "让 codex review 一下这个工作"
- "让 codex 检查完后，返回问题和改进方案"
- "让 codex 看看这个实现有没有更好的重构方式"

If the user only says `codex` in a Kimi session, default to interpreting it as a request for a single Codex review/check pass unless they clearly ask for a continued Codex conversation.

## Tools

- `codex(prompt, cwd='.', route='default', sandbox='read-only', approval_policy='never', developer_instructions=None)`
- `codex_review(prompt='Review the current uncommitted changes and propose improvements.', cwd='.', route='default')`
- `codex_reply(thread_id, prompt, route='default')`

Both return a JSON object with:

- `threadId`
- `content`
- `route`
- `mode`

## Architecture

```
Kimi CLI → MCP Config → start-kimi-codex-mcp.sh → kimi_codex_mcp_server.py
                                           ↓
                                    call-codex.sh → codex exec
```

## References

### 启动脚本
- **`scripts/start-kimi-codex-mcp.sh`** - 主入口，启动 Kimi-compatible wrapper
- **`scripts/start-native-codex-mcp.sh`** - 启动原生 Codex MCP server（含代理自动检测）

### 实现文件
- **`scripts/kimi_codex_mcp_server.py`** - FastMCP 实现的兼容层
- **`scripts/call-codex.sh`** - 底层调用脚本，处理 fallback 逻辑
- **`scripts/select-codex-target.sh`** - 目标选择和配置解析

### 故障排查
遇到超时、连接失败等问题时阅读：
- **`docs/TROUBLESHOOTING.md`** - 详细排查指南（中文）
