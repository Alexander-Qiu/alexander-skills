# Provider and Model Matrix

Use this file when the task needs provider or model switching.

## Current tested combinations

Based on `/root/.codex/config.toml` and `/mnt/data/qrz-dev/CODEX_USAGE.md`:

| Provider | Model | Status | Notes |
|---|---|---|---|
| `zenmux-coding` | `openai/gpt-5.4` | unavailable | coding-plan quota exhausted |
| `zenmux` | `openai/gpt-5.4` | available | stable direct fallback |
| `zenmux` | `google/gemini-3-flash-preview` | available | preferred review fallback |
| `zenmux` | `volcengine/doubao-seed-2.0-code` | available | useful for Chinese-first discussion |
| `minimax` | any | unavailable | Codex requires `responses`; current MiniMax path does not work |

## Default fallback policy

When the user does not explicitly request a provider/model pair, this skill should behave like this:

1. Run with the normal Codex config first.
2. If the run fails because of quota, auth, or provider connectivity errors, inspect `~/.codex/config.toml`.
3. If a usable `zenmux` provider exists, retry with:
   - provider: `zenmux`
   - model: `google/gemini-3-flash-preview`
4. Tell the user that a fallback was applied.
5. If no usable `zenmux` provider exists, ask the user to provide a provider id and model name explicitly.

## How to switch inside native MCP

Pass both fields in the tool call:

```json
{
  "prompt": "Review the repository and identify risky modules.",
  "cwd": "/path/to/repo",
  "sandbox": "read-only",
  "approval-policy": "never",
  "model": "google/gemini-3-flash-preview",
  "config": {
    "model_provider": "zenmux"
  }
}
```

## How to switch in direct CLI

```bash
codex exec -c model_provider=zenmux -m google/gemini-3-flash-preview \
  --skip-git-repo-check "Review the auth flow and list risks"
```

For review mode:

```bash
codex exec review -c model_provider=zenmux -m google/gemini-3-flash-preview \
  --uncommitted
```

## Selection guidance

- Use `openai/gpt-5.4` when you want the most predictable output.
- Use `google/gemini-3-flash-preview` for code review, repository-wide synthesis, or long context.
- Use `volcengine/doubao-seed-2.0-code` when the user wants Chinese-first code discussion.
- Do not rely on `zenmux-coding` until quota is refreshed.
