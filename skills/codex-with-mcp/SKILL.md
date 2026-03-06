---
name: codex-with-mcp
description: Use when Kimi or Claude Code needs to route work into Codex through MCP or a deterministic Codex wrapper, especially for code review, provider switching, model switching, session continuation, or debugging Codex hangs. Use this whenever the user mentions Codex MCP, `codex review`, switching `model_provider`, switching models such as `google/gemini-3-flash-preview`, or wants Kimi or Claude Code to invoke Codex with explicit provider and model control.
---

# Codex with MCP

This skill connects Kimi or Claude Code to Codex CLI and keeps provider and model selection explicit.

## Use this skill for

- starting Codex through the native `codex mcp-server`
- switching provider or model per request without editing the global default config
- running review-oriented Codex flows with a specific provider/model pair
- recovering automatically when the default Codex provider fails because of quota or auth issues
- debugging whether failures come from MCP wiring or the downstream provider

## Core rules

1. Prefer native Codex MCP for Claude Code and any client that correctly supports the native Codex tool schema.

```bash
codex mcp-server
```

2. For native Codex MCP, switch provider and model in the tool call itself.

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

3. For Kimi, first check which Codex tool schema it actually sees.

- If Kimi sees native fields such as `prompt`, `cwd`, `model`, and `config`, use native MCP.
- If Kimi sees legacy fields such as `PROMPT`, `cd`, `SESSION_ID`, or `profile`, do not try to force provider switching through that MCP tool. Use `scripts/codex-review.sh` or direct Codex CLI from shell instead.

4. Default provider policy for this skill:

- First try the normal Codex config with no override.
- If that fails because of quota, auth, or provider connectivity errors, inspect `~/.codex/config.toml`.
- If a usable `zenmux` provider exists there, retry with `zenmux` plus `google/gemini-3-flash-preview` and tell the user that a fallback was applied.
- If no usable `zenmux` provider exists, ask the user to provide a provider id and model name explicitly.

5. For review mode outside native MCP, use `scripts/codex-review.sh` so provider and model switching stay explicit and repeatable.

## Native MCP contract

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

Treat these names as legacy only:

- `PROMPT`
- `cd`
- `SESSION_ID`
- `return_all_messages`
- `profile`

## Which path to choose

- Claude Code: use native MCP and switch provider/model in tool args.
- Kimi with native schema: use native MCP and switch provider/model in tool args.
- Kimi with legacy Codex schema: use shell to run `scripts/codex-review.sh` or `codex exec`, not the legacy Codex MCP tool.

## References

- `references/providers.md` for tested provider/model combinations
- `references/review.md` for review workflows and Kimi guidance
- `scripts/select-codex-target.sh` for fallback target detection
- `scripts/call-codex.sh` for direct MCP smoke tests
- `scripts/codex-review.sh` for deterministic review runs with provider/model switching and fallback behavior
