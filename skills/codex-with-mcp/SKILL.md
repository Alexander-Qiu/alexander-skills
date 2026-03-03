---
name: codex-with-mcp
description: Use when needing to invoke Codex CLI through MCP in Kimi, with configuration validation, health checks, and proper session management for AI-assisted coding tasks.
---

# Codex with MCP

A skill for using Codex CLI through Model Context Protocol (MCP) in Kimi.

## Overview

This skill enables seamless Codex integration in Kimi:
- **Configuration validation**: Verify MCP setup is correct
- **Health check**: Test if Codex MCP server is accessible
- **Smart invocation**: Best practices for calling Codex
- **Session management**: Handle session persistence

## When to Use

- Need Codex for code analysis, refactoring, or editing in Kimi
- Want to validate MCP configuration before use
- Need to debug Codex MCP connection issues
- Want proper session management

## Prerequisites

- Kimi CLI with MCP support (`kimi --version` >= 0.1.0)
- `codex` CLI installed and working
- `uvx` installed (`pip install uv`)
- MCP server configured in `~/.kimi/mcp.json`

## Quick Reference

| Task | Method |
|------|--------|
| Validate config | `/scripts/validate-codex-mcp.sh <wheel_path>` |
| Health check | Use `codex` tool with test prompt |
| Call Codex | Direct MCP tool invocation |
| View config | `/scripts/show-mcp-config.sh` |

## Configuration

### Step 1: Install Dependencies

```bash
# Install uv/uvx
pip install uv

# Verify codex CLI
codex --version
```

### Step 2: Configure MCP Server

Edit `~/.kimi/mcp.json`:

```json
{
  "mcpServers": {
    "codex": {
      "command": "uvx",
      "args": [
        "--from",
        "/absolute/path/to/codexmcp-0.7.4-py3-none-any.whl",
        "codexmcp"
      ]
    }
  }
}
```

**Important:** Use absolute path for the wheel file.

### Step 3: Validate Configuration

```bash
# Run validation script
./scripts/validate-codex-mcp.sh /path/to/codexmcp-0.7.4-py3-none-any.whl
```

## Usage

### Basic Codex Invocation

Once configured, Kimi automatically manages the MCP server. Just use the `codex` tool:

```
Use codex to analyze this codebase and suggest improvements.
```

Kimi will:
1. Auto-start MCP server if needed
2. Call the `codex` tool with appropriate parameters
3. Return the results

### Manual Parameters

For fine control, specify parameters explicitly:

```json
{
  "PROMPT": "Refactor this function to use async/await",
  "cd": "/path/to/project",
  "sandbox": "read-only",
  "return_all_messages": false,
  "skip_git_repo_check": true
}
```

### Session Management

**Start new session:**
```json
{
  "PROMPT": "Initial analysis task",
  "cd": "/project",
  "sandbox": "read-only"
}
```
→ Response includes `SESSION_ID`

**Resume session:**
```json
{
  "PROMPT": "Continue the analysis",
  "cd": "/project",
  "sandbox": "read-only",
  "SESSION_ID": "previous-session-id"
}
```

## Parameters Reference

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `PROMPT` | string | ✅ | - | Task description |
| `cd` | string | ✅ | - | Working directory |
| `sandbox` | string | ❌ | "read-only" | Safety level: "read-only" / "workspace-write" / "danger-full-access" |
| `SESSION_ID` | string | ❌ | "" | Session to resume |
| `skip_git_repo_check` | bool | ❌ | true | Allow non-git dirs |
| `return_all_messages` | bool | ❌ | false | Include reasoning |
| `image` | array | ❌ | [] | Image attachments |

## Sandbox Levels

| Level | Safety | Use Case |
|-------|--------|----------|
| `read-only` | ⭐⭐⭐ Safest | Analysis, code review |
| `workspace-write` | ⭐⭐ Medium | Refactoring, file edits |
| `danger-full-access` | ⭐ Risky | System-level changes |

**Recommendation:** Always start with `read-only`.

## Troubleshooting

### MCP Server Not Found

**Symptom:** Tool not available
**Fix:** 
```bash
# Check mcp.json exists and valid
cat ~/.kimi/mcp.json

# Validate with script
./scripts/validate-codex-mcp.sh /path/to/wheel
```

### Codex Command Failed

**Symptom:** Server starts but Codex fails
**Fix:**
```bash
# Verify codex CLI
codex --version

# Check credentials
codex config list
```

### Wheel File Not Found

**Symptom:** uvx cannot find package
**Fix:**
```bash
# Use absolute path in mcp.json
# Check file exists
ls -la /absolute/path/to/codexmcp-0.7.4-py3-none-any.whl
```

## Best Practices

1. **Always use absolute paths** in mcp.json
2. **Start with read-only** sandbox for new projects
3. **Save SESSION_ID** to resume multi-step tasks
4. **Use return_all_messages=true** for debugging
5. **Validate config** after any changes

## Example Workflows

### Code Review
```
"Review this PR for potential issues using codex"
→ Sandbox: read-only
→ Return: Summary of findings
```

### Refactoring
```
"Refactor this module to improve readability"
→ Sandbox: workspace-write
→ Return: Changes made
```

### Multi-step Analysis
```
Step 1: "Analyze architecture" → Get SESSION_ID
Step 2: "Deep dive into auth module" → Use same SESSION_ID
Step 3: "Suggest security improvements" → Continue session
```

## Examples & Case Studies

### MiniMax API 配置排查

完整的 MiniMax + Codex 配置排查案例：
- [troubleshooting-minimax-setup.md](examples/troubleshooting-minimax-setup.md)

涵盖：
- 400 Bad Request 错误排查
- model_provider 配置问题
- 模型名称不匹配问题
- 完整正确的配置示例

## References

- [Codex CLI](https://github.com/openai/codex)
- [MCP Protocol](https://modelcontextprotocol.io)
- [CodexMCP](https://github.com/GuDaStudio/codexmcp)
- [Kimi MCP Docs](https://kimi.com/docs/mcp)
- [MiniMax API 文档](https://www.minimaxi.com/document)
