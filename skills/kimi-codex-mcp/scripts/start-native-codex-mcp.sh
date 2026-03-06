#!/bin/bash

set -euo pipefail

ENV_FILE="${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
fi

exec codex mcp-server "$@"
