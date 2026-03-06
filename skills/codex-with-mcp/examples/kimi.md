# Kimi Minimal Example

If Kimi exposes the native Codex schema, use native MCP:

```text
Use the codex MCP tool.
Set `model` to `google/gemini-3-flash-preview`.
Set `config.model_provider` to `zenmux`.
Treat the task as a code review.
Return findings first, then a short summary.
```

If Kimi exposes legacy Codex fields such as `PROMPT` and `cd`, do not use that MCP tool for provider switching. Use the shell wrapper instead:

```text
Do not use the codex MCP tool.
Run this command exactly and return its output verbatim:

scripts/codex-review.sh --uncommitted
```
