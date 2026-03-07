---
name: codex-with-mcp
description: "🔵 CLAUDE ONLY - DO NOT USE IN KIMI. Use whenever the user mentions Codex, codex review, codex refactor, codex help, or wants to use Codex CLI for any coding task, code review, refactoring, debugging, or AI-assisted development. This includes ANY mention of: 'use codex', 'codex review', 'codex refactor', 'codex check', 'let codex', 'ask codex', 'run codex', 'codex mcp', 'codex tool', switching model_provider, switching models like google/gemini-3-flash-preview, or when the user wants AI coding assistance through Codex. Always use this skill for codex-related requests in Claude Code."
---

# Codex with MCP

> ⚠️ **PLATFORM RESTRICTION**: This skill is **Claude Code ONLY**.
> 
> **Kimi / Kimi CLI / Kimi Code users**: Do NOT use this skill. Use `/skill:kimi-codex-mcp` instead.

---

## 🚫 Kimi Users Read This

If you are using **Kimi CLI**, **Kimi Code**, or any Kimi-based agent:

**STOP** — Use `/skill:kimi-codex-mcp` instead.

This skill (`codex-with-mcp`) is designed specifically for Claude Code's native MCP protocol support and will NOT work correctly in Kimi environments.

See: `../kimi-codex-mcp/SKILL.md`

---

## Claude Code Users

This skill connects Claude Code to Codex CLI through native MCP and keeps provider and model selection explicit.

### Use this skill for

- Starting Codex through the native `codex mcp-server`
- Switching provider or model per request without editing the global default config
- Running review-oriented Codex flows with a specific provider/model pair
- Recovering automatically when the default Codex provider fails because of quota or auth issues
- Debugging whether failures come from MCP wiring or the downstream provider

### Core rules

1. **Claude Code uses native Codex MCP.**

```bash
codex mcp-server
```

2. **Switch provider and model in the tool call itself.**

```json
{
  "prompt": "Review the current changes and list the top risks.",
  "cwd": "/path/to/repo",
  "sandbox": "read-only",
  "approval-policy": "never",
  "model": "google/gemini-3-flash-preview",
  "config": {
    "model_provider": "zenmux"
  }
}
```

3. **Default provider policy:**

- First try the normal Codex config with no override.
- If that fails because of quota, auth, or provider connectivity errors, inspect `~/.codex/config.toml` first.
- If no usable fallback provider is defined there, inspect `~/.codex/codex-mcp.env` for `ZENMUX_ONDEMAND_API_KEY`.
- If a usable `zenmux` fallback exists in either place, retry with `zenmux` plus `google/gemini-3-flash-preview` and tell the user that a fallback was applied.
- If no usable `zenmux` provider exists, ask the user to provide a provider id and model name explicitly.

4. **For review mode,** use `scripts/codex-review.sh` so provider and model switching stay explicit and repeatable.

### Native MCP contract

The native server exposes:

- `codex` for a new session
- `codex-reply` for continuing an existing session

Use these field names exactly:

- `prompt`
- `cwd`
- `sandbox`
- `approval-policy`
- `model`
- `config`
- `threadId`

### References

- `references/providers.md` for tested provider/model combinations
- `references/review.md` for review workflows
- `scripts/select-codex-target.sh` for fallback target detection
- `scripts/call-codex.sh` for direct MCP smoke tests
- `scripts/codex-review.sh` for deterministic review runs with provider/model switching

---

## Why Two Separate Skills?

| Skill | Platform | Protocol | Reason |
|-------|----------|----------|--------|
| `codex-with-mcp` | 🔵 Claude Code | Native MCP | Claude supports native Codex MCP schema |
| `kimi-codex-mcp` | 🟢 Kimi CLI | Compatibility wrapper | Kimi needs a compatibility layer to handle protocol differences |

Kimi's MCP implementation reconnects after tool listing, which causes Codex's native MCP server to fail with "initialize called more than once". The `kimi-codex-mcp` skill provides a wrapper to handle this.
