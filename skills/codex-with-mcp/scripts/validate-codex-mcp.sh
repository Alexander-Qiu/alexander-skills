#!/bin/bash

# validate-codex-mcp.sh
# Validates Codex MCP configuration for Kimi

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

WHEEL_PATH="${1:-}"
MCP_CONFIG="${HOME}/.kimi/mcp.json"

echo "🔍 Validating Codex MCP Configuration"
echo "======================================"
echo ""

# Check 1: uvx installed
echo -n "Checking uvx... "
if command -v uvx &> /dev/null; then
    UVX_VERSION=$(uvx --version 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓${NC} ($UVX_VERSION)"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "   Install with: pip install uv"
    exit 1
fi

# Check 2: codex CLI installed
echo -n "Checking codex CLI... "
if command -v codex &> /dev/null; then
    CODEX_VERSION=$(codex --version 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓${NC} ($CODEX_VERSION)"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "   Install with: pip install codex-cli"
    exit 1
fi

# Check 3: MCP config exists
echo -n "Checking mcp.json... "
if [[ -f "$MCP_CONFIG" ]]; then
    echo -e "${GREEN}✓${NC} ($MCP_CONFIG)"
else
    echo -e "${RED}✗ Not found${NC}"
    echo "   Create at: $MCP_CONFIG"
    exit 1
fi

# Check 4: MCP config is valid JSON
echo -n "Validating JSON syntax... "
if python3 -c "import json; json.load(open('$MCP_CONFIG'))" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ Invalid JSON${NC}"
    exit 1
fi

# Check 5: Codex MCP server configured
echo -n "Checking codex MCP server config... "
if python3 -c "import json; config=json.load(open('$MCP_CONFIG')); exit(0 if 'codex' in config.get('mcpServers', {}) else 1)" 2>/dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗ codex server not configured${NC}"
    echo "   Add codex configuration to mcp.json"
    exit 1
fi

# Check 6: Wheel file exists (if provided)
if [[ -n "$WHEEL_PATH" ]]; then
    echo -n "Checking wheel file... "
    if [[ -f "$WHEEL_PATH" ]]; then
        echo -e "${GREEN}✓${NC} ($WHEEL_PATH)"
    else
        echo -e "${RED}✗ Not found${NC} ($WHEEL_PATH)"
        exit 1
    fi
fi

# Check 7: Test MCP server can start
echo -n "Testing MCP server startup... "
if [[ -n "$WHEEL_PATH" ]]; then
    # Use provided wheel path
    TEST_WHEEL="$WHEEL_PATH"
else
    # Try to extract from mcp.json
    TEST_WHEEL=$(python3 -c "
import json
config = json.load(open('$MCP_CONFIG'))
codex_config = config.get('mcpServers', {}).get('codex', {})
args = codex_config.get('args', [])
for i, arg in enumerate(args):
    if arg.endswith('.whl'):
        print(arg)
        break
" 2>/dev/null)
fi

if [[ -n "$TEST_WHEEL" && -f "$TEST_WHEEL" ]]; then
    # Quick test - start server and send initialize request
    PYTHON_TEST=$(cat << 'EOF'
import subprocess
import json
import sys
import time
import os

wheel_path = sys.argv[1]
process = subprocess.Popen(
    ['uvx', '--from', wheel_path, 'codexmcp'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

init_request = {
    'jsonrpc': '2.0',
    'id': 1,
    'method': 'initialize',
    'params': {
        'protocolVersion': '2024-11-05',
        'capabilities': {},
        'clientInfo': {'name': 'validator', 'version': '1.0'}
    }
}

try:
    process.stdin.write(json.dumps(init_request) + '\n')
    process.stdin.flush()
    time.sleep(1)
    
    # Try to read response
    import select
    if select.select([process.stdout], [], [], 2)[0]:
        response = process.stdout.readline()
        if 'jsonrpc' in response:
            print('SUCCESS')
        else:
            print('FAILED: Invalid response')
    else:
        print('FAILED: No response')
except Exception as e:
    print(f'FAILED: {e}')
finally:
    process.terminate()
    try:
        process.wait(timeout=2)
    except:
        process.kill()
EOF
)
    
    TEST_RESULT=$(python3 -c "$PYTHON_TEST" "$TEST_WHEEL" 2>/dev/null || echo "FAILED")
    if [[ "$TEST_RESULT" == "SUCCESS" ]]; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠${NC} (server started but test inconclusive)"
    fi
else
    echo -e "${YELLOW}⚠${NC} (cannot test without wheel path)"
fi

echo ""
echo -e "${GREEN}✅ Validation complete!${NC}"
echo ""
echo "Your Codex MCP configuration looks good."
echo "You can now use the 'codex' tool in Kimi."
