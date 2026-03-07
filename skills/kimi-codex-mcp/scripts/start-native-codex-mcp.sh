#!/bin/bash

set -euo pipefail

# 设置代理（如果 clash 在运行）
if pgrep -x clash > /dev/null 2>&1; then
    export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
    export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"
    export ALL_PROXY="${ALL_PROXY:-socks5://127.0.0.1:7891}"
    export http_proxy="${http_proxy:-http://127.0.0.1:7890}"
    export https_proxy="${https_proxy:-http://127.0.0.1:7890}"
    export all_proxy="${all_proxy:-socks5://127.0.0.1:7891}"
fi

ENV_FILE="${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
fi

exec codex mcp-server "$@"
