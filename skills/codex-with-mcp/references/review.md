# Review Flows

> 🔵 **Claude Code ONLY** — This reference is for Claude Code native MCP.
> 
> Kimi users: See `../../kimi-codex-mcp/docs/TROUBLESHOOTING.md` and `../../kimi-codex-mcp/SKILL.md`

Use this file when the user wants `codex review` behavior with explicit provider/model control.

## Claude Code Native MCP

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

## Direct CLI Review

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

## Failure Triage

- If MCP fails during `initialize`, the wiring is broken.
- If the tool call returns provider HTTP errors such as `401` or `403`, MCP is healthy and the provider is the failing layer.
