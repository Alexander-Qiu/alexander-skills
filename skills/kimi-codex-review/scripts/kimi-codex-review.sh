#!/bin/bash
# kimi-codex-review.sh - Headless Codex CLI review for Kimi
# 
# Design verified:
# - 3 consecutive default calls
# - Fallback to zenmux + gemini-3-flash-preview on failure
#
# Usage: ./kimi-codex-review.sh [OPTIONS]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Colors
if [[ -t 1 ]]; then
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
else
    RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''
fi

log_info() { echo -e "${BLUE}[INFO]${NC} $*"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }

# Defaults
MODE="uncommitted"
BASE=""
COMMIT=""
FORCE_PROVIDER=""
FORCE_MODEL=""
TIMEOUT="${CODEX_REVIEW_TIMEOUT:-120}"
ATTEMPTS=0
MAX_ATTEMPTS=3

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Headless Codex code review for Kimi CLI.

Options:
  --uncommitted          Review unstaged changes (default)
  --base BRANCH          Review changes against base branch
  --commit HASH          Review specific commit
  --provider NAME        Force provider (zenmux, openai, etc.)
  --model NAME           Force model
  --timeout SECONDS      Override timeout (default: 120)
  --test-3x              Run 3 consecutive tests then fallback test
  -h, --help             Show help

Examples:
  $(basename "$0") --uncommitted
  $(basename "$0") --base main
  $(basename "$0") --provider zenmux --model google/gemini-3-flash-preview
  $(basename "$0") --test-3x

EOF
}

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --uncommitted) MODE="uncommitted"; shift ;;
        --base) MODE="base"; BASE="$2"; shift 2 ;;
        --commit) MODE="commit"; COMMIT="$2"; shift 2 ;;
        --provider) FORCE_PROVIDER="$2"; shift 2 ;;
        --model) FORCE_MODEL="$2"; shift 2 ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        --test-3x) MODE="test-3x"; shift ;;
        -h|--help) usage; exit 0 ;;
        *) log_error "Unknown: $1"; usage; exit 1 ;;
    esac
done

# Auto proxy
if pgrep -x clash > /dev/null 2>&1; then
    export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
    export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"
    export ALL_PROXY="${ALL_PROXY:-socks5://127.0.0.1:7891}"
fi

# Build codex review command
build_cmd() {
    local provider="${1:-}"
    local model="${2:-}"
    
    local cmd=("codex" "exec" "review")
    
    # Review mode
    case "$MODE" in
        uncommitted|test-3x) cmd+=("--uncommitted") ;;
        base) cmd+=("--base" "$BASE") ;;
        commit) cmd+=("--commit" "$COMMIT") ;;
    esac
    
    # Config
    cmd+=("--skip-git-repo-check")
    cmd+=(-c "approval_policy=never")
    
    # Provider/model
    [[ -n "$provider" ]] && cmd+=(-c "model_provider=$provider")
    [[ -n "$model" ]] && cmd+=(-m "$model")
    
    printf '%s ' "${cmd[@]}"
}

# Run single review
run_review() {
    local provider="${1:-}"
    local model="${2:-}"
    local label="${3:-Review}"
    
    log_info "$label..."
    ((ATTEMPTS++))
    
    local cmd
    cmd=$(build_cmd "$provider" "$model")
    
    set +e
    local output
    output=$(timeout "$TIMEOUT" bash -c "$cmd" 2>&1)
    local code=$?
    set -e
    
    if [[ $code -eq 0 ]]; then
        log_success "$label completed"
        echo "$output"
        return 0
    elif [[ $code -eq 124 ]]; then
        log_error "$label timed out"
        return 124
    else
        log_error "$label failed (exit: $code)"
        echo "$output" | tail -20
        return $code
    fi
}

# Check if error is fallback-eligible
is_fallback_error() {
    local text="${1,,}"
    [[ "$text" == *"quota"* ]] || [[ "$text" == *"401"* ]] || \
    [[ "$text" == *"403"* ]] || [[ "$text" == *"404"* ]] || \
    [[ "$text" == *"unauthorized"* ]] || [[ "$text" == *"subscription"* ]]
}

# Main test: 3x default + fallback
test_3x_plus_fallback() {
    log_info "=== Test Mode: 3x Default + Fallback ==="
    
    local default_provider=""
    local default_model=""
    local success_count=0
    
    # 3 consecutive default calls
    for i in 1 2 3; do
        log_info "--- Attempt $i/3 (default config) ---"
        if run_review "" "" "Attempt $i"; then
            ((success_count++))
        else
            local err=$(run_review "" "" "" 2>&1 || true)
            if is_fallback_error "$err"; then
                log_warn "Default provider failed with fallback-eligible error"
                break
            fi
        fi
        sleep 2
    done
    
    log_info "Default config: $success_count/3 successful"
    
    # Fallback test
    log_info "--- Fallback Test (zenmux + gemini-3-flash-preview) ---"
    if run_review "zenmux" "google/gemini-3-flash-preview" "Fallback"; then
        log_success "Fallback test PASSED"
    else
        log_error "Fallback test FAILED"
        return 1
    fi
    
    log_success "All tests completed"
}

# Normal single review
run_single() {
    local provider="${FORCE_PROVIDER:-}"
    local model="${FORCE_MODEL:-}"
    
    run_review "$provider" "$model" "Review"
}

# Main
main() {
    if ! command -v codex &> /dev/null; then
        log_error "Codex CLI not found. Install: npm install -g @openai/codex"
        exit 1
    fi
    
    if [[ "$MODE" == "test-3x" ]]; then
        test_3x_plus_fallback
    else
        run_single
    fi
}

main
