#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RESOLVER="$SCRIPT_DIR/select-codex-target.sh"

PROVIDER=""
MODEL=""
PROMPT=""
BASE=""
COMMIT=""
TITLE=""
UNCOMMITTED="false"
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
    case "$1" in
        --provider)
            PROVIDER="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --prompt)
            PROMPT="$2"
            shift 2
            ;;
        --base)
            BASE="$2"
            shift 2
            ;;
        --commit)
            COMMIT="$2"
            shift 2
            ;;
        --title)
            TITLE="$2"
            shift 2
            ;;
        --uncommitted)
            UNCOMMITTED="true"
            shift
            ;;
        --help)
            cat <<'USAGE'
Usage: codex-review.sh [OPTIONS]

Options:
  --provider NAME     Provider id, e.g. zenmux
  --model NAME        Model name, e.g. google/gemini-3-flash-preview
  --prompt TEXT       Extra review instructions
  --base BRANCH       Review changes against a base branch
  --commit SHA        Review a single commit
  --title TEXT        Optional review title
  --uncommitted       Review staged, unstaged, and untracked changes
  --help              Show this help

Behavior:
  If no provider/model override is supplied, this script first runs with the
  normal Codex config. If that fails due to quota, auth, or provider errors, it
  checks ~/.codex/config.toml for a usable `zenmux` provider and retries with
  `google/gemini-3-flash-preview`. If no usable fallback is found, it asks for
  an explicit provider and model.
USAGE
            exit 0
            ;;
        *)
            EXTRA_ARGS+=("$1")
            shift
            ;;
    esac
done

if [[ -n "$PROMPT" && ( "$UNCOMMITTED" == "true" || -n "$BASE" || -n "$COMMIT" ) ]]; then
    echo "Error: --prompt cannot be combined with --uncommitted, --base, or --commit for codex review." >&2
    exit 1
fi

if [[ "$UNCOMMITTED" != "true" && -z "$BASE" && -z "$COMMIT" && -z "$PROMPT" ]]; then
    UNCOMMITTED="true"
fi

build_cmd() {
    local provider="$1"
    local model="$2"
    local -a cmd=(codex exec review --json)

    if [[ -n "$provider" ]]; then
        cmd+=(-c "model_provider=$provider")
    fi
    if [[ -n "$model" ]]; then
        cmd+=(-m "$model")
    fi
    if [[ "$UNCOMMITTED" == "true" ]]; then
        cmd+=(--uncommitted)
    fi
    if [[ -n "$BASE" ]]; then
        cmd+=(--base "$BASE")
    fi
    if [[ -n "$COMMIT" ]]; then
        cmd+=(--commit "$COMMIT")
    fi
    if [[ -n "$TITLE" ]]; then
        cmd+=(--title "$TITLE")
    fi
    if [[ -n "$PROMPT" ]]; then
        cmd+=("$PROMPT")
    fi
    cmd+=("${EXTRA_ARGS[@]}")
    printf '%s\0' "${cmd[@]}"
}

run_cmd() {
    local provider="$1"
    local model="$2"
    mapfile -d '' CMD < <(build_cmd "$provider" "$model")
    printf 'Running:' >&2
    printf ' %q' "${CMD[@]}" >&2
    printf '\n' >&2

    local output
    local status
    set +e
    output=$("${CMD[@]}" 2>&1)
    status=$?
    set -e
    printf '%s' "$output"
    return "$status"
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

if [[ -n "$PROVIDER" || -n "$MODEL" ]]; then
    run_cmd "$PROVIDER" "$MODEL"
    exit $?
fi

set +e
first_output=$(run_cmd "" "")
first_status=$?
set -e
if [[ $first_status -eq 0 ]]; then
    printf '%s\n' "$first_output"
    exit 0
fi

if ! needs_fallback "$first_output"; then
    printf '%s\n' "$first_output"
    exit "$first_status"
fi

fallback_json="$($RESOLVER)"
fallback_available=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["has_fallback"])' <<< "$fallback_json")
fallback_message=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["message"])' <<< "$fallback_json")
fallback_provider=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["fallback_provider"])' <<< "$fallback_json")
fallback_model=$(python3 -c 'import json,sys; print(json.load(sys.stdin)["fallback_model"])' <<< "$fallback_json")

if [[ "$fallback_available" != "True" ]]; then
    printf '%s\n' "$first_output"
    echo "$fallback_message" >&2
    echo "Please provide --provider and --model explicitly." >&2
    exit "$first_status"
fi

echo "$fallback_message" >&2
set +e
fallback_output=$(run_cmd "$fallback_provider" "$fallback_model")
fallback_status=$?
set -e
printf '%s\n' "$fallback_output"
exit "$fallback_status"
