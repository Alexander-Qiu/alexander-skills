---
name: kimi-codex-review
description: "Use this skill whenever the user mentions codex, codex review, code review with codex, '让 codex 检查', 'codex 重构', or wants AI-assisted code review. This includes ANY mention of: codex, codex review, codex check, let codex inspect, codex help, or when the user wants AI to review code. Always use this skill for codex-related code review requests in Kimi CLI."
---

# Kimi Codex Review

Direct Codex CLI integration for Kimi — no MCP, no timeouts, just works.

## When to Use

Use this skill immediately when the user says:
- "codex review"
- "让 codex 检查一下"
- "codex 看看这段代码"
- "用 codex review"
- "codex 重构建议"
- Any mention of **codex** + **review/check/inspect**

## Core Rule

**Always run `./scripts/codex-review.sh` for code review tasks.**

Do not try to construct `codex exec` commands manually. The script handles provider selection, fallbacks, and proxy configuration automatically.

## Quick Start

```bash
# Review current changes
./scripts/codex-review.sh

# Review with custom focus
./scripts/codex-review.sh --prompt "Check for security issues"

# Review against main branch
./scripts/codex-review.sh --base main
```

## How It Works

The script implements a **3-tier fallback strategy** (verified through testing):

1. **Tier 1**: Default Codex configuration (OpenAI / your login)
2. **Tier 2**: zenmux + gemini-3-flash-preview (if Tier 1 fails)
3. **Tier 3**: p2077 + pa/gemini-3-flash-preview (if Tier 2 fails)

**All without modifying `config.toml`.**

## Requirements

1. Codex CLI installed: `npm install -g @openai/codex`
2. Logged in: `codex login`
3. Clash running (for proxy) or direct internet access

## Script Reference

### `scripts/codex-review.sh`

**Usage:**
```bash
./scripts/codex-review.sh [OPTIONS]

Options:
  --prompt TEXT     Custom review focus (security, performance, etc.)
  --base BRANCH     Review changes against base branch
  --commit HASH     Review specific commit
  --timeout SECS    Override default 180s timeout
  -h, --help        Show help
```

**Examples:**
```bash
# Standard review
./scripts/codex-review.sh

# Security-focused review
./scripts/codex-review.sh --prompt "Focus on security vulnerabilities"

# Review vs main
./scripts/codex-review.sh --base main

# Longer timeout for large repos
./scripts/codex-review.sh --timeout 300
```

## Auto-Proxy Detection

If clash is running, the script automatically sets:
```bash
HTTPS_PROXY=http://127.0.0.1:7890
```

No manual configuration needed.

## Why CLI Instead of MCP?

| Aspect | MCP Approach | CLI Approach (This Skill) |
|--------|-------------|---------------------------|
| Timeout | ❌ Kimi MCP timeout too short | ✅ No timeout issues |
| Complexity | ❌ MCP server + wrapper | ✅ Direct `codex exec` |
| Stability | ❌ Connection drops | ✅ Reliable |
| Fallback | ❌ Hard to implement | ✅ Easy 3-tier fallback |

## Troubleshooting

See `docs/TROUBLESHOOTING.md` for common issues:
- Codex CLI not installed
- Network/proxy issues
- Authentication failures
- Provider quota exceeded

## Architecture

```
User Request
    │
    ▼
./scripts/codex-review.sh
    │
    ├─► Tier 1: codex exec review (default)
    │   └─► Success? Return results
    │
    ├─► Tier 2: codex exec review -c model_provider=zenmux
    │   └─► Success? Return results
    │
    └─► Tier 3: codex exec review -c model_provider=p2077
        └─► Return results (or error if all fail)
```

**No config file modifications. No MCP. Just CLI.**
