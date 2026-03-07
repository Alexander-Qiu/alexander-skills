---
name: kimi-codex-review
description: "Use when Kimi CLI needs to invoke Codex for code review. Use this whenever the user mentions 'codex review', '让 codex 检查', 'codex 重构', 'inspect with codex', or wants AI-assisted code review through Codex CLI. This skill uses direct CLI invocation (not MCP) for stability."
---

# Kimi Codex Review

> 🟢 **Kimi CLI / Kimi Code ONLY** — Direct Codex CLI integration.
>
> 🔵 **Claude Code users**: Use `/skill:codex-with-mcp` instead.

---

## 🎯 Overview

Direct `codex exec review` CLI invocation — no MCP, no timeout issues.

**Verified Design:**
- ✅ 3 consecutive default calls succeed
- ✅ Fallback to `zenmux + gemini-3-flash-preview` succeeds

---

## 🚀 Quick Start

### Review Uncommitted Changes
```bash
./scripts/kimi-codex-review.sh --uncommitted
```

### Test 3x + Fallback
```bash
./scripts/kimi-codex-review.sh --test-3x
```

### Force Provider/Model
```bash
./scripts/kimi-codex-review.sh \
  --provider zenmux \
  --model google/gemini-3-flash-preview \
  --uncommitted
```

---

## 📋 Options

| Option | Description |
|--------|-------------|
| `--uncommitted` | Review unstaged changes (default) |
| `--base BRANCH` | Review against base branch |
| `--commit HASH` | Review specific commit |
| `--provider NAME` | Force provider (zenmux, openai) |
| `--model NAME` | Force model |
| `--timeout SECS` | Override 120s default |
| `--test-3x` | Run 3x test + fallback test |

---

## 🏗️ Architecture

```
Kimi CLI → kimi-codex-review.sh → codex exec review
                              ↓
                    Fallback on quota/auth error
                              ↓
                    zenmux + gemini-3-flash-preview
```

**No MCP. No server. Direct CLI.**

---

## 🔧 Configuration

### ~/.codex/config.toml

```toml
model_provider = "zenmux"
model = "google/gemini-3-flash-preview"

[model_providers.zenmux]
name = "ZenMux On-Demand"
base_url = "https://zenmux.ai/api/v1"
experimental_bearer_token = "sk-ai-v1-..."
wire_api = "responses"
```

### Auto Proxy Detection

If clash is running, script auto-sets:
```bash
HTTPS_PROXY=http://127.0.0.1:7890
```

---

## 📁 Files

| File | Purpose |
|------|---------|
| `scripts/kimi-codex-review.sh` | Main entry point |
| `docs/TROUBLESHOOTING.md` | Common issues |

---

## 🎨 Usage Examples

### Standard Review
```text
User: "codex review 一下"
→ ./scripts/kimi-codex-review.sh --uncommitted
```

### Security Review
```text
User: "让 codex 检查安全问题"
→ ./scripts/kimi-codex-review.sh --uncommitted
```

### Verify 3x + Fallback
```text
User: "测试 codex 连接"
→ ./scripts/kimi-codex-review.sh --test-3x
```

---

## ⚠️ Requirements

1. **Codex CLI installed**: `npm install -g @openai/codex`
2. **Logged in**: `codex login`
3. **Git repository**: Must run inside a git repo
4. **Network**: Proxy auto-detected if clash running

---

## 🔗 Related

- `codex exec review --help` — Native CLI help
- `../codex-with-mcp/` — Claude Code MCP integration
