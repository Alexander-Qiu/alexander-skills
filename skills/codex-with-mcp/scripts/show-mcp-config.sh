#!/bin/bash

set -euo pipefail

MCP_CONFIG="${HOME}/.kimi/mcp.json"
WRAPPER_PATH="$(cd "$(dirname "$0")" && pwd)/start-codex-mcp.sh"

echo "Codex MCP configuration"
echo "======================="
echo

if [[ -f "$MCP_CONFIG" ]]; then
    echo "Config location: $MCP_CONFIG"
    echo
    python3 -m json.tool "$MCP_CONFIG" 2>/dev/null || cat "$MCP_CONFIG"
else
    echo "No Kimi MCP config found at $MCP_CONFIG"
    echo
    echo "Recommended native config:"
    cat <<CONFIG
{
  "mcpServers": {
    "codex": {
      "command": "$WRAPPER_PATH",
      "args": []
    }
  }
}
CONFIG
fi

echo
echo "Wrapper script: $WRAPPER_PATH"
echo "Optional env file: ${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"
