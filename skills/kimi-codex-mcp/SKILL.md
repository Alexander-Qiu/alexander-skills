---
name: kimi-codex-mcp
description: Use when Kimi CLI needs to invoke Codex through MCP reliably, including Kimi MCP setup, `kimi -yp` with Codex, Kimi calling Codex for review or coding help, or when native `codex mcp-server` fails under Kimi with errors like `initialize called more than once`.
---

# Kimi Codex MCP

This is a dedicated skill for Kimi CLI.
Use this skill for Kimi-specific Codex integration.

## When to use this instead of `codex-with-mcp`

- The client is Kimi CLI.
- You want `kimi -yp` or `kimi --mcp-config-file ...` to call Codex.
- Native `codex mcp-server` works in `kimi mcp test` but fails in real tool use.
- You see `initialize called more than once`.

## Core rule

For Kimi, prefer the compatibility MCP wrapper in `scripts/start-kimi-codex-mcp.sh`.
Do not point Kimi directly at native `codex mcp-server` unless you are debugging protocol compatibility.

## Why

Kimi's MCP loading path connects once to list tools, then reconnects to call tools.
Codex's native MCP server rejects repeated `initialize` on the same client lifecycle.
The compatibility wrapper avoids that path by exposing Kimi-friendly MCP tools and delegating each call to `../codex-with-mcp/scripts/call-codex.sh`.

## Recommended setup

Create an MCP config like this:

```json
{
  "mcpServers": {
    "codex": {
      "command": "/mnt/data/qrz-dev/mem/alexander-skills/skills/kimi-codex-mcp/scripts/start-kimi-codex-mcp.sh",
      "args": [],
      "env": {
        "ZENMUX_ONDEMAND_API_KEY": "sk-ai-v1-..."
      }
    }
  }
}
```

Then run:

```bash
kimi --mcp-config-file /path/to/mcp.json -yp "Use the codex MCP tool ..."
```

## Routes

The wrapper exposes two routes through the same `codex` tool:

- `default`: use Codex's normal subscription-backed configuration
- `ondemand-gemini`: use `zenmux` with `google/gemini-3-flash-preview`

For `ondemand-gemini`, the wrapper injects provider and model at server startup time instead of passing the model through the Codex MCP tool arguments. This matches the currently working path.

For `default`, the wrapper first tries the subscription-backed route. If that path returns a known transport or provider failure and `ZENMUX_ONDEMAND_API_KEY` is available, it automatically retries through `ondemand-gemini`.

## Tools

- `codex(prompt, cwd='.', route='default', sandbox='read-only', approval_policy='never', developer_instructions=None)`
- `codex_reply(thread_id, prompt, route='default')`

Both return a JSON object with:

- `threadId`
- `content`
- `route`

## References

- `scripts/start-kimi-codex-mcp.sh` to launch the wrapper
- `scripts/kimi_codex_mcp_server.py` for the Kimi-compatible server
- `../codex-with-mcp/scripts/call-codex.sh` for the actual Codex invocation
