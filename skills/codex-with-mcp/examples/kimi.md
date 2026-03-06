# Kimi Minimal Example

Use this default review policy in Kimi.

## Preferred behavior

1. Review with the normal Codex configuration first.
2. If that review fails because of quota, auth, or provider connectivity problems, retry with:
   - provider: `zenmux`
   - model: `google/gemini-3-flash-preview`
3. If the fallback is used, tell the user that the review was retried with the on-demand ZenMux path.
4. If both attempts fail, return the raw error.

## Kimi prompt

```text
Review the current repository changes.
Use the normal Codex review configuration first.
If that fails because of quota, auth, or provider connectivity issues, retry with provider `zenmux` and model `google/gemini-3-flash-preview`.
If fallback is used, explicitly tell the user that you switched to the on-demand ZenMux Gemini path.
If the Codex MCP tool is unavailable or uses a legacy schema, do not compose your own codex CLI command.
Run this command exactly and return its output verbatim:

/mnt/data/qrz-dev/mem/alexander-skills/skills/codex-with-mcp/scripts/codex-review.sh --uncommitted
```

## Why this example is written this way

- It keeps the default path as the first attempt.
- It uses the skill's built-in fallback policy instead of forcing the fallback on every run.
- It prevents Kimi from inventing its own broken `codex exec` flags.
- It preserves a deterministic escape hatch when native Codex MCP is unstable.
