# Review Flows

Use this file when the user wants `codex review` behavior with explicit provider/model control.

## Claude Code and native MCP clients

Use the native Codex MCP tool and pass both fields in the call:

```json
{
  "prompt": "Act as a code reviewer. Inspect the current repository changes, prioritize bugs, regressions, and missing tests, and return findings first.",
  "cwd": "/path/to/repo",
  "sandbox": "read-only",
  "approval-policy": "never",
  "model": "google/gemini-3-flash-preview",
  "config": {
    "model_provider": "zenmux"
  }
}
```

## Kimi guidance

Kimi needs a branch in the workflow.

### Case 1: Kimi exposes the native Codex schema

If the tool fields are `prompt`, `cwd`, `model`, and `config`, use the same native MCP pattern as above.

### Case 2: Kimi exposes the legacy Codex schema

If Kimi exposes fields such as `PROMPT`, `cd`, `SESSION_ID`, or `profile`, do not try to switch provider with that MCP tool.

Use the shell wrapper instead:

```bash
scripts/codex-review.sh --uncommitted
```

That wrapper follows the skill's default policy:

1. Try the normal Codex config first.
2. If that fails because of quota, auth, or provider errors, inspect `~/.codex/config.toml`.
3. If a usable `zenmux` provider exists, retry with `google/gemini-3-flash-preview` and tell the user a fallback was applied.
4. If no usable fallback exists, ask the user to provide `--provider` and `--model` explicitly.

This is the preferred Kimi path when explicit provider/model switching matters.

## Direct CLI review

`codex exec review` is the most deterministic non-MCP path.

```bash
scripts/codex-review.sh --uncommitted
```

To bypass the fallback and force a specific pair:

```bash
scripts/codex-review.sh \
  --provider zenmux \
  --model google/gemini-3-flash-preview \
  --uncommitted
```

Or against a base branch:

```bash
scripts/codex-review.sh --base main
```

`codex exec review` currently rejects custom prompt text when combined with `--uncommitted`, `--base`, or `--commit`. Use built-in review mode without an extra prompt in those cases.

## Failure triage

- If MCP fails during `initialize`, the wiring is broken.
- If the tool call returns provider HTTP errors such as `401` or `403`, MCP is healthy and the provider is the failing layer.
- If Kimi still calls old fields like `PROMPT` and `cd`, it is using a legacy Codex MCP implementation rather than native Codex MCP.
