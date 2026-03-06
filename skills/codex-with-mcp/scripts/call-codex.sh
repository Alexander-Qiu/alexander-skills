#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOLVER="$SCRIPT_DIR/select-codex-target.sh"

PROMPT=""
CWD="$(pwd)"
SANDBOX="read-only"
APPROVAL_POLICY="never"
THREAD_ID=""
MODEL=""
PROVIDER=""
PROFILE=""
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
        --model)
            MODEL="$2"
            shift 2
            ;;
        --provider)
            PROVIDER="$2"
            shift 2
            ;;
        --profile)
            PROFILE="$2"
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
  --model NAME                   Override Codex model
  --provider NAME                Override config.model_provider
  --profile NAME                 Use a Codex config profile
  --developer-instructions TEXT  Inject developer instructions
  --server-cmd CMD               Override MCP server command
  --help                         Show this help

Behavior:
  If no provider/model override is supplied and the first call fails with a
  quota/auth/provider error, this script checks ~/.codex/config.toml for a usable
  `zenmux` provider and retries with `google/gemini-3-flash-preview`.
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
    SERVER_CMD="$SCRIPT_DIR/start-codex-mcp.sh"
fi

run_once() {
    local provider="$1"
    local model="$2"
    local effective_server_cmd="$SERVER_CMD"

    if [[ -n "$provider" ]]; then
        effective_server_cmd+=" -c model_provider=$provider"
    fi
    if [[ -n "$model" ]]; then
        effective_server_cmd+=" -c model=$model"
    fi

    python3 - "$effective_server_cmd" "$PROMPT" "$CWD" "$SANDBOX" "$APPROVAL_POLICY" "$THREAD_ID" "$model" "$provider" "$PROFILE" "$DEVELOPER_INSTRUCTIONS" <<'PY'
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
    model,
    provider,
    profile,
    developer_instructions,
) = sys.argv[1:11]

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
                "clientInfo": {"name": "call-codex.sh", "version": "1.0"},
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
            if model:
                arguments["model"] = model
            if profile:
                arguments["profile"] = profile
            if developer_instructions:
                arguments["developer-instructions"] = developer_instructions
            if provider:
                arguments["config"] = {"model_provider": provider}

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
}

needs_fallback() {
    local text="$1"
    [[ "$text" == *"quota"* ]] || \
    [[ "$text" == *"403 Forbidden"* ]] || \
    [[ "$text" == *"401 Unauthorized"* ]] || \
    [[ "$text" == *"subscription quota limit"* ]] || \
    [[ "$text" == *"Missing API key"* ]] || \
    [[ "$text" == *"stream disconnected"* ]] || \
    [[ "$text" == *"Model provider"* ]] || \
    [[ "$text" == *"error loading config"* ]]
}

set +e
first_json=$(run_once "$PROVIDER" "$MODEL")
first_status=$?
set -e

if [[ $first_status -eq 0 ]]; then
    python3 -c 'import json,sys; data=json.load(sys.stdin); print(json.dumps(data["structuredContent"], ensure_ascii=False, indent=2))' <<< "$first_json"
    exit 0
fi

if [[ -n "$PROVIDER" || -n "$MODEL" || -n "$THREAD_ID" ]]; then
    printf '%s\n' "$first_json" >&2
    exit "$first_status"
fi

first_text=$(python3 -c 'import json,sys; data=json.load(sys.stdin); text=[]; text.append(json.dumps(data.get("structuredContent", {}), ensure_ascii=False)); text.extend(item.get("text", "") for item in data.get("content", []) if isinstance(item, dict)); print("\n".join(text))' <<< "$first_json")
if ! needs_fallback "$first_text"; then
    printf '%s\n' "$first_json" >&2
    exit "$first_status"
fi

fallback_json="$($RESOLVER)"
fallback_available=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["has_fallback"])' <<< "$fallback_json")
fallback_message=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["message"])' <<< "$fallback_json")
fallback_provider=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["fallback_provider"])' <<< "$fallback_json")
fallback_model=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["fallback_model"])' <<< "$fallback_json")

if [[ "$fallback_available" != "True" ]]; then
    printf '%s\n' "$first_json" >&2
    echo "$fallback_message" >&2
    echo "Please provide --provider and --model explicitly." >&2
    exit "$first_status"
fi

echo "$fallback_message" >&2
set +e
second_json=$(run_once "$fallback_provider" "$fallback_model")
second_status=$?
set -e
python3 -c 'import json,sys; data=json.load(sys.stdin); print(json.dumps(data["structuredContent"], ensure_ascii=False, indent=2))' <<< "$second_json"
exit "$second_status"
