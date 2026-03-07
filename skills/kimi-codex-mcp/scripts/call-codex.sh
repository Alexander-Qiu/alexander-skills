#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOLVER="$SCRIPT_DIR/select-codex-target.sh"
ENV_FILE="${CODEX_MCP_ENV_FILE:-$HOME/.codex/codex-mcp.env}"

MODE="exec"
PROMPT=""
CWD="$(pwd)"
SANDBOX="read-only"
APPROVAL_POLICY="never"
THREAD_ID=""
MODEL=""
PROVIDER=""
PROFILE=""
DEVELOPER_INSTRUCTIONS=""

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode)
            MODE="$2"
            shift 2
            ;;
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
        --help)
            cat <<'USAGE'
Usage: call-codex.sh [OPTIONS]

Options:
  --mode MODE                   exec|review|resume (default: exec)
  --prompt TEXT                 Prompt or review instructions
  --cwd PATH                    Working directory
  --sandbox LEVEL               read-only|workspace-write|danger-full-access
  --approval-policy POLICY      retained for compatibility; ignored by codex exec
  --thread-id ID                Session id for --mode resume
  --model NAME                  Override Codex model
  --provider NAME               Override config.model_provider
  --profile NAME                Use a Codex config profile
  --developer-instructions TEXT Prepended to exec-mode prompts
  --help                        Show this help

Behavior:
  The default path uses direct `codex exec` or `codex exec review` calls.
  If the first default-path call fails with quota/auth/provider errors, this
  script checks ~/.codex/config.toml first and then ~/.codex/codex-mcp.env for
  a usable `zenmux` fallback.
USAGE
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if [[ -z "$PROMPT" && "$MODE" != "review" ]]; then
    echo "Error: --prompt is required" >&2
    exit 1
fi

if [[ "$MODE" == "resume" && -z "$THREAD_ID" ]]; then
    echo "Error: --thread-id is required for --mode resume" >&2
    exit 1
fi

if [[ "$MODE" != "exec" && "$MODE" != "review" && "$MODE" != "resume" ]]; then
    echo "Error: --mode must be exec, review, or resume" >&2
    exit 1
fi

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

run_once() {
    local provider="$1"
    local model="$2"
    local output_file jsonl_file error_file combined_prompt
    output_file="$(mktemp)"
    jsonl_file="$(mktemp)"
    error_file="$(mktemp)"

    combined_prompt="$PROMPT"
    if [[ "$MODE" == "review" ]]; then
        combined_prompt="Review the current uncommitted changes in this repository. Return concise findings, risks, and a better next-step plan."
        if [[ -n "$PROMPT" ]]; then
            combined_prompt="$combined_prompt"$'\n\n'"Additional review instructions: $PROMPT"
        fi
    elif [[ -n "$DEVELOPER_INSTRUCTIONS" ]]; then
        combined_prompt="$DEVELOPER_INSTRUCTIONS"$'\n\n'"$PROMPT"
    fi

    local -a cmd
    case "$MODE" in
        review)
            cmd=(codex exec --json -o "$output_file" -s read-only)
            ;;
        exec)
            cmd=(codex exec --skip-git-repo-check --json -o "$output_file" -s "$SANDBOX")
            ;;
        resume)
            cmd=(codex exec resume --json -o "$output_file")
            ;;
    esac

    if [[ -n "$provider" ]]; then
        cmd+=(-c "model_provider=$provider")
    fi
    if [[ "$provider" == "zenmux" && -n "${ZENMUX_ONDEMAND_API_KEY:-}" ]]; then
        cmd+=(
            -c 'model_providers.zenmux.name="ZenMux On-Demand"'
            -c 'model_providers.zenmux.base_url="https://zenmux.ai/api/v1"'
            -c "model_providers.zenmux.experimental_bearer_token=\"$ZENMUX_ONDEMAND_API_KEY\""
            -c 'model_providers.zenmux.wire_api="responses"'
        )
    fi
    if [[ -n "$model" ]]; then
        cmd+=(-m "$model")
    fi
    if [[ -n "$PROFILE" ]]; then
        cmd+=(-p "$PROFILE")
    fi

    case "$MODE" in
        review)
            if [[ -n "$combined_prompt" ]]; then
                cmd+=("$combined_prompt")
            fi
            ;;
        exec)
            cmd+=("$combined_prompt")
            ;;
        resume)
            cmd+=("$THREAD_ID" "$combined_prompt")
            ;;
    esac

    set +e
    (
        cd "$CWD"
        "${cmd[@]}" >"$jsonl_file" 2>"$error_file"
    )
    local status=$?
    set -e

    python3 - "$status" "$MODE" "$jsonl_file" "$output_file" "$error_file" <<'PY'
import json
import pathlib
import sys

status = int(sys.argv[1])
mode = sys.argv[2]
jsonl_path = pathlib.Path(sys.argv[3])
output_path = pathlib.Path(sys.argv[4])
error_path = pathlib.Path(sys.argv[5])

thread_id = ""
if jsonl_path.exists():
    for raw_line in jsonl_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("type") == "thread.started":
            thread_id = payload.get("thread_id", "")

content = output_path.read_text(encoding="utf-8").strip() if output_path.exists() else ""
stderr = error_path.read_text(encoding="utf-8").strip() if error_path.exists() else ""

payload = {
    "isError": status != 0,
    "mode": mode,
    "threadId": thread_id,
    "content": content,
    "error": stderr,
}
print(json.dumps(payload, ensure_ascii=False))
PY

    local rc=$status
    rm -f "$output_file" "$jsonl_file" "$error_file"
    return "$rc"
}

set +e
first_json=$(run_once "$PROVIDER" "$MODEL")
first_status=$?
set -e

if [[ $first_status -eq 0 ]]; then
    printf '%s\n' "$first_json"
    exit 0
fi

if [[ -n "$PROVIDER" || -n "$MODEL" || "$MODE" == "resume" ]]; then
    printf '%s\n' "$first_json" >&2
    exit "$first_status"
fi

first_text=$(python3 -c 'import json,sys; data=json.load(sys.stdin); print("\n".join(x for x in [data.get("content",""), data.get("error","")] if x))' <<< "$first_json")
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
printf '%s\n' "$second_json"
exit "$second_status"
