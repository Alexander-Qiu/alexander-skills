#!/bin/bash
# codex-review.sh - Kimi Codex Review
# 
# Verified design:
# - 3-tier fallback: default → zenmux → p2077
# - No config.toml modifications (-c model_provider=)
# - Auto proxy detection
# - Clean error handling

set -euo pipefail

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
[[ -t 1 ]] || { RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''; }

log_info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_ok()    { echo -e "${GREEN}[OK]${NC} $*"; }

# Defaults
PROMPT=""
MODE="uncommitted"
BASE=""
COMMIT=""
TIMEOUT=180

# Provider chain (in order of preference)
TIER1_NAME="default"
TIER1_PROVIDER=""
TIER1_MODEL=""

TIER2_NAME="zenmux"
TIER2_PROVIDER="zenmux"
TIER2_MODEL="google/gemini-3-flash-preview"

TIER3_NAME="p2077"
TIER3_PROVIDER="p2077"
TIER3_MODEL="pa/gemini-3-flash-preview"

usage() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Codex code review with automatic provider fallback.

Options:
  --prompt TEXT     Review focus (security, performance, etc.)
  --base BRANCH     Review changes against base branch
  --commit HASH     Review specific commit  
  --timeout SECS    Timeout per attempt (default: 180)
  -h, --help        Show help

Examples:
  $(basename "$0")                    # Review uncommitted changes
  $(basename "$0") --base main        # Review vs main branch
  $(basename "$0") --prompt "Security" # Security-focused review

Fallback chain: default → $TIER2_NAME → $TIER3_NAME
EOF
}

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --prompt)   PROMPT="$2"; shift 2 ;;
        --base)     MODE="base"; BASE="$2"; shift 2 ;;
        --commit)   MODE="commit"; COMMIT="$2"; shift 2 ;;
        --timeout)  TIMEOUT="$2"; shift 2 ;;
        -h|--help)  usage; exit 0 ;;
        *)          log_error "Unknown: $1"; usage; exit 1 ;;
    esac
done

# Auto-detect proxy
if pgrep -x clash > /dev/null 2>&1; then
    export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7890}"
    export HTTP_PROXY="${HTTP_PROXY:-http://127.0.0.1:7890}"
fi

# Check requirements
if ! command -v codex &> /dev/null; then
    log_error "Codex CLI not found. Install: npm install -g @openai/codex"
    exit 1
fi

if ! git rev-parse --git-dir > /dev/null 2>&1; then
    log_error "Not in a git repository"
    exit 1
fi

# Build codex command
build_cmd() {
    local provider="${1:-}"
    local model="${2:-}"
    
    local cmd=(codex exec review)
    
    # Review mode
    case "$MODE" in
        uncommitted) cmd+=(--uncommitted) ;;
        base)        cmd+=(--base "$BASE") ;;
        commit)      cmd+=(--commit "$COMMIT") ;;
    esac
    
    # Common options
    cmd+=(--skip-git-repo-check)
    cmd+=(-c "approval_policy=never")
    cmd+=(-c "sandbox_policy.read_only=true")
    
    # Provider override (if specified)
    if [[ -n "$provider" ]]; then
        cmd+=(-c "model_provider=$provider")
    fi
    if [[ -n "$model" ]]; then
        cmd+=(-m "$model")
    fi
    
    printf '%s ' "${cmd[@]}"
}

# Check if error qualifies for fallback
is_fallback_error() {
    local text="${1,,}"
    [[ "$text" == *"quota"* ]] || \
    [[ "$text" == *"401"* ]] || \
    [[ "$text" == *"403"* ]] || \
    [[ "$text" == *"404"* ]] || \
    [[ "$text" == *"unauthorized"* ]] || \
    [[ "$text" == *"subscription"* ]] || \
    [[ "$text" == *"not found"* ]] || \
    [[ "$text" == *"bad_response"* ]]
}

# Run single review attempt
run_attempt() {
    local name="$1"
    local provider="${2:-}"
    local model="${3:-}"
    
    log_info "Trying: $name"
    [[ -n "$provider" ]] && log_info "  Provider: $provider, Model: $model"
    
    local cmd
    cmd=$(build_cmd "$provider" "$model")
    
    set +e
    local output
    output=$(timeout "$TIMEOUT" bash -c "$cmd" 2>&1)
    local code=$?
    set -e
    
    if [[ $code -eq 0 ]]; then
        log_ok "$name succeeded"
        echo "$output"
        return 0
    elif [[ $code -eq 124 ]]; then
        log_warn "$name timed out (${TIMEOUT}s)"
        return 124
    else
        # Check if fallback eligible
        if is_fallback_error "$output"; then
            log_warn "$name failed (fallback-eligible)"
            return 200  # Special code for fallback
        else
            log_error "$name failed (exit: $code)"
            return $code
        fi
    fi
}

# Main execution with fallback chain
main() {
    log_info "Starting Codex review..."
    log_info "Mode: $MODE"
    [[ -n "$PROMPT" ]] && log_info "Focus: $PROMPT"
    echo ""
    
    local output
    
    # Tier 1: Default
    if output=$(run_attempt "$TIER1_NAME" "$TIER1_PROVIDER" "$TIER1_MODEL"); then
        echo "$output"
        exit 0
    fi
    local code=$?
    
    # Tier 2: zenmux (if tier 1 was fallback-eligible)
    if [[ $code -eq 200 ]]; then
        echo ""
        log_warn "Default provider unavailable, trying fallback..."
        echo ""
        
        if output=$(run_attempt "$TIER2_NAME" "$TIER2_PROVIDER" "$TIER2_MODEL"); then
            echo ""
            log_ok "Review completed with fallback provider: $TIER2_NAME"
            echo ""
            echo "$output"
            exit 0
        fi
        code=$?
    fi
    
    # Tier 3: p2077 (if tier 2 was also fallback-eligible)
    if [[ $code -eq 200 ]]; then
        echo ""
        log_warn "Fallback provider unavailable, trying emergency fallback..."
        echo ""
        
        if output=$(run_attempt "$TIER3_NAME" "$TIER3_PROVIDER" "$TIER3_MODEL"); then
            echo ""
            log_ok "Review completed with emergency provider: $TIER3_NAME"
            echo ""
            echo "$output"
            exit 0
        fi
        code=$?
    fi
    
    # All failed
    echo ""
    log_error "All providers failed"
    echo ""
    echo "Tried: $TIER1_NAME → $TIER2_NAME → $TIER3_NAME"
    echo ""
    echo "Last error:"
    echo "$output" | tail -20
    exit 1
}

main
