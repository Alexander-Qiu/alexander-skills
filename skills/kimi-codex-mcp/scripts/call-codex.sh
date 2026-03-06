#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

PROMPT=""
CWD="$(pwd)"
SANDBOX="read-only"
APPROVAL_POLICY="never"
THREAD_ID=""
DEVELOPER_INSTRUCTIONS=""
SERVER_CMD=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt)
            PROMPT="$2"
            shift 2
            ;;
        --cwd|--cd)
            CWD="$2"
            shift 2
            ;;
        --sandbox)
            SANDBOX="$2"
            shift 2
            ;;
        --approval-policy)
            APPROVAL_POLICY="$2"
            shift 2
            ;;
        --thread-id|--session-id)
            THREAD_ID="$2"
            shift 2
            ;;
        --developer-instructions)
            DEVELOPER_INSTRUCTIONS="$2"
            shift 2
            ;;
        --server-cmd)
            SERVER_CMD="$2"
            shift 2
            ;;
        --help)
            cat <<'USAGE'
Usage: call-codex.sh [OPTIONS]

Options:
  --prompt TEXT                  Prompt to send (required)
  --cwd PATH                     Working directory
  --sandbox LEVEL                read-only|workspace-write|danger-full-access
  --approval-policy POLICY       untrusted|on-failure|on-request|never
  --thread-id ID                 Continue an existing thread
  --developer-instructions TEXT  Inject developer instructions
  --server-cmd CMD               Override MCP server command
  --help                         Show this help
USAGE
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$PROMPT" ]]; then
    echo "Error: --prompt is required" >&2
    exit 1
fi

if [[ -z "$SERVER_CMD" ]]; then
    SERVER_CMD="$SCRIPT_DIR/start-native-codex-mcp.sh"
fi

python3 - "$SERVER_CMD" "$PROMPT" "$CWD" "$SANDBOX" "$APPROVAL_POLICY" "$THREAD_ID" "$DEVELOPER_INSTRUCTIONS" <<'PY'
import json
import shlex
import subprocess
import sys

(
    server_cmd,
    prompt,
    cwd,
    sandbox,
    approval_policy,
    thread_id,
    developer_instructions,
) = sys.argv[1:8]

command = shlex.split(server_cmd)
process = subprocess.Popen(
    command,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
)


def request(method, params=None, request_id=None):
    payload = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        payload["params"] = params
    if request_id is not None:
        payload["id"] = request_id
    process.stdin.write(json.dumps(payload) + "\n")
    process.stdin.flush()
    if request_id is None:
        return None
    while True:
        line = process.stdout.readline()
        if not line:
            stderr = process.stderr.read()
            raise RuntimeError(f"No MCP response. stderr: {stderr}")
        message = json.loads(line)
        if message.get("id") != request_id:
            continue
        return message


try:
    try:
        init_response = request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "kimi-codex-mcp", "version": "1.0"},
            },
            1,
        )
        if "result" not in init_response:
            raise RuntimeError(f"Initialize failed: {init_response}")

        request("notifications/initialized", {})

        if thread_id:
            tool_name = "codex-reply"
            arguments = {"threadId": thread_id, "prompt": prompt}
        else:
            tool_name = "codex"
            arguments = {
                "prompt": prompt,
                "cwd": cwd,
                "sandbox": sandbox,
                "approval-policy": approval_policy,
            }
            if developer_instructions:
                arguments["developer-instructions"] = developer_instructions

        tool_response = request(
            "tools/call",
            {"name": tool_name, "arguments": arguments},
            2,
        )

        if "result" not in tool_response:
            raise RuntimeError(f"Tool call failed: {tool_response}")

        result = tool_response["result"]
        payload = {
            "isError": bool(result.get("isError")),
            "structuredContent": result.get("structuredContent") or {},
            "content": result.get("content") or [],
        }
        print(json.dumps(payload, ensure_ascii=False))
    except Exception as exc:
        payload = {
            "isError": True,
            "structuredContent": {},
            "content": [{"type": "text", "text": str(exc)}],
        }
        print(json.dumps(payload, ensure_ascii=False))
        raise SystemExit(1)
finally:
    process.terminate()
    try:
        process.wait(timeout=2)
    except Exception:
        process.kill()
PY
