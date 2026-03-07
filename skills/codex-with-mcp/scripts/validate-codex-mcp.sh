#!/bin/bash

set -euo pipefail

MCP_CONFIG="${HOME}/.kimi/mcp.json"
RECOMMENDED_WRAPPER="$(cd "$(dirname "$0")" && pwd)/start-codex-mcp.sh"

echo "Validating native Codex MCP setup"
echo "================================="
echo

echo -n "Checking codex CLI... "
if command -v codex >/dev/null 2>&1; then
    echo "OK ($(codex --version 2>/dev/null || echo unknown))"
else
    echo "FAILED"
    echo "Install Codex CLI first."
    exit 1
fi

echo -n "Checking native MCP server... "
if codex mcp-server --help >/dev/null 2>&1; then
    echo "OK"
else
    echo "FAILED"
    exit 1
fi

if [[ -f "$MCP_CONFIG" ]]; then
    echo -n "Checking Kimi MCP config... "
    if python3 - "$MCP_CONFIG" <<'PY'
import json
import sys
with open(sys.argv[1]) as handle:
    data = json.load(handle)
if not data.get("mcpServers", {}).get("codex"):
    raise SystemExit(1)
print("OK")
PY
    then
        :
    else
        echo "FAILED"
        echo "Add a codex server entry to ~/.kimi/mcp.json."
        exit 1
    fi

    echo -n "Checking whether Kimi points to native Codex MCP... "
    python3 - "$MCP_CONFIG" "$RECOMMENDED_WRAPPER" <<'PY'
import json
import os
import sys
config_path = sys.argv[1]
recommended_wrapper = os.path.realpath(sys.argv[2])
with open(config_path) as handle:
    data = json.load(handle)
server = data.get("mcpServers", {}).get("codex") or {}
command = server.get("command", "")
args = server.get("args") or []
command_text = " ".join([command, *args])
native_markers = ["codex mcp-server", recommended_wrapper]
if any(marker in command_text for marker in native_markers):
    print("OK")
else:
    print(f"WARNING: stale command -> {command_text.strip()}")
PY
fi

echo -n "Handshaking with recommended native wrapper... "
python3 - "$RECOMMENDED_WRAPPER" <<'PY'
import json
import select
import subprocess
import sys
wrapper = sys.argv[1]
process = subprocess.Popen([wrapper], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
def send(payload):
    process.stdin.write(json.dumps(payload) + "\n")
    process.stdin.flush()
def read(timeout=5):
    ready, _, _ = select.select([process.stdout], [], [], timeout)
    if not ready:
        raise RuntimeError("timeout waiting for MCP response")
    while True:
        line = process.stdout.readline()
        if not line:
            stderr = process.stderr.read()
            raise RuntimeError(f"empty response; stderr={stderr}")
        stripped = line.strip()
        if not stripped:
            continue
        return json.loads(stripped)
try:
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "validator", "version": "1.0"}}})
    read()
    send({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    response = read()
    tools = {tool["name"] for tool in response.get("result", {}).get("tools", [])}
    if {"codex", "codex-reply"}.issubset(tools):
        print("OK")
    else:
        raise RuntimeError(f"unexpected tools: {sorted(tools)}")
finally:
    process.terminate()
    try:
        process.wait(timeout=2)
    except Exception:
        process.kill()
PY

echo
echo "Native Codex MCP looks healthy."
