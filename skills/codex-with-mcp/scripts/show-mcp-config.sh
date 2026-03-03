#!/bin/bash

# show-mcp-config.sh
# Displays current MCP configuration

MCP_CONFIG="${HOME}/.kimi/mcp.json"

echo "📋 Current MCP Configuration"
echo "============================"
echo ""

if [[ -f "$MCP_CONFIG" ]]; then
    echo "Config location: $MCP_CONFIG"
    echo ""
    echo "Content:"
    echo "--------"
    cat "$MCP_CONFIG" | python3 -m json.tool 2>/dev/null || cat "$MCP_CONFIG"
else
    echo "❌ Configuration file not found: $MCP_CONFIG"
    echo ""
    echo "Create one with the following content:"
    echo '{'
    echo '  "mcpServers": {'
    echo '    "codex": {'
    echo '      "command": "uvx",'
    echo '      "args": ['
    echo '        "--from",'
    echo '        "/absolute/path/to/codexmcp-0.7.4-py3-none-any.whl",'
    echo '        "codexmcp"'
    echo '      ]'
    echo '    }'
    echo '  }'
    echo '}'
fi

echo ""
echo "📁 Available MCP Servers:"
echo "------------------------"
if [[ -f "$MCP_CONFIG" ]]; then
    python3 -c "
import json
try:
    with open('$MCP_CONFIG') as f:
        config = json.load(f)
    servers = config.get('mcpServers', {})
    if servers:
        for name, cfg in servers.items():
            cmd = cfg.get('command', 'N/A')
            print(f'  • {name}: {cmd}')
    else:
        print('  (none configured)')
except Exception as e:
    print(f'  Error: {e}')
"
fi
