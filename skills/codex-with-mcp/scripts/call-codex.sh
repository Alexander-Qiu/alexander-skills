#!/bin/bash

# call-codex.sh
# Direct script to call Codex via MCP (for testing/debugging)

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Default values
PROMPT=""
CD="$(pwd)"
SANDBOX="read-only"
SESSION_ID=""
RETURN_ALL="false"
WHEEL_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --prompt)
            PROMPT="$2"
            shift 2
            ;;
        --cd)
            CD="$2"
            shift 2
            ;;
        --sandbox)
            SANDBOX="$2"
            shift 2
            ;;
        --session-id)
            SESSION_ID="$2"
            shift 2
            ;;
        --return-all)
            RETURN_ALL="true"
            shift
            ;;
        --wheel)
            WHEEL_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Usage: call-codex.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --prompt TEXT       Task description (required)"
            echo "  --cd PATH           Working directory (default: current)"
            echo "  --sandbox LEVEL     read-only|workspace-write|danger-full-access"
            echo "  --session-id ID     Resume previous session"
            echo "  --return-all        Return full message history"
            echo "  --wheel PATH        Path to codexmcp wheel file"
            echo "  --help              Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required args
if [[ -z "$PROMPT" ]]; then
    echo -e "${RED}Error: --prompt is required${NC}"
    echo "Use --help for usage information"
    exit 1
fi

# Find wheel path if not provided
if [[ -z "$WHEEL_PATH" ]]; then
    # Try to get from mcp.json
    MCP_CONFIG="${HOME}/.kimi/mcp.json"
    if [[ -f "$MCP_CONFIG" ]]; then
        WHEEL_PATH=$(python3 -c "
import json
try:
    with open('$MCP_CONFIG') as f:
        config = json.load(f)
    args = config.get('mcpServers', {}).get('codex', {}).get('args', [])
    for arg in args:
        if arg.endswith('.whl'):
            print(arg)
            break
except:
    pass
" 2>/dev/null)
    fi
fi

if [[ -z "$WHEEL_PATH" || ! -f "$WHEEL_PATH" ]]; then
    echo -e "${RED}Error: Cannot find codexmcp wheel file${NC}"
    echo "Please specify with --wheel /path/to/codexmcp-0.7.4-py3-none-any.whl"
    exit 1
fi

echo -e "${BLUE}🚀 Calling Codex via MCP...${NC}"
echo "   Prompt: ${PROMPT:0:50}..."
echo "   Directory: $CD"
echo "   Sandbox: $SANDBOX"
[[ -n "$SESSION_ID" ]] && echo "   Session: $SESSION_ID"
echo ""

# Build JSON-RPC request
PYTHON_SCRIPT=$(cat << EOF
import subprocess
import json
import sys
import time
import uuid

wheel_path = "${WHEEL_PATH}"
prompt = """${PROMPT}"""
cd_path = "${CD}"
sandbox = "${SANDBOX}"
session_id = "${SESSION_ID}"
return_all = True if "${RETURN_ALL}" == "true" else False

# Start MCP server
process = subprocess.Popen(
    ['uvx', '--from', wheel_path, 'codexmcp'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

def send_request(method, params, req_id):
    request = {
        'jsonrpc': '2.0',
        'id': req_id,
        'method': method,
        'params': params
    }
    process.stdin.write(json.dumps(request) + '\n')
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    return json.loads(response_line)

try:
    # Initialize
    init_response = send_request('initialize', {
        'protocolVersion': '2024-11-05',
        'capabilities': {},
        'clientInfo': {'name': 'codex-cli', 'version': '1.0'}
    }, 1)
    
    if 'result' not in init_response:
        print(f"Initialize failed: {init_response}")
        sys.exit(1)
    
    # Call codex tool
    tool_params = {
        'name': 'codex',
        'arguments': {
            'PROMPT': prompt,
            'cd': cd_path,
            'sandbox': sandbox,
            'skip_git_repo_check': True,
            'return_all_messages': return_all
        }
    }
    
    if session_id:
        tool_params['arguments']['SESSION_ID'] = session_id
    
    tool_response = send_request('tools/call', tool_params, 2)
    
    if 'result' in tool_response:
        result = tool_response['result']
        if result.get('isError'):
            print(f"Error: {result.get('content', 'Unknown error')}")
        else:
            content = result.get('content', [])
            for item in content:
                if item.get('type') == 'text':
                    print(item.get('text', ''))
    else:
        print(f"Tool call failed: {tool_response}")
        
finally:
    process.terminate()
    try:
        process.wait(timeout=2)
    except:
        process.kill()
EOF
)

python3 -c "$PYTHON_SCRIPT"
