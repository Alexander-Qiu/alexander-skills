#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVER_SCRIPT="$SCRIPT_DIR/kimi_codex_mcp_server.py"
KIMI_FASTMCP_PROJECT="${KIMI_FASTMCP_PROJECT:-/mnt/data/qrz-dev/agents/kimi-cli}"
ENV_FILE="${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
fi

if python3 -c 'import fastmcp' >/dev/null 2>&1; then
    exec python3 "$SERVER_SCRIPT" "$@"
fi

if command -v uv >/dev/null 2>&1 && [[ -d "$KIMI_FASTMCP_PROJECT" ]]; then
    exec uv run --directory "$KIMI_FASTMCP_PROJECT" python "$SERVER_SCRIPT" "$@"
fi

echo "Unable to start kimi-codex-mcp: fastmcp not available." >&2
echo "Either install fastmcp for python3 or set KIMI_FASTMCP_PROJECT to a kimi-cli checkout." >&2
exit 1
