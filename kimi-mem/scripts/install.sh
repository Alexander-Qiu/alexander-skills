#!/bin/bash

# kimi-mem 安装脚本

set -e

echo "🧠 Installing kimi-mem..."

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ first."
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js 18+ required, found $(node --version)"
    exit 1
fi

echo "✓ Node.js $(node --version)"

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

# 安装依赖
echo "📦 Installing dependencies..."
npm install

# 构建
echo "🔨 Building..."
npm run build

# 检查 kimi CLI
if ! command -v kimi &> /dev/null; then
    echo "⚠️  kimi CLI not found in PATH."
    echo "   Please install it from: https://github.com/MoonshotAI/kimi-cli"
    echo ""
    echo "   After installing kimi CLI, run:"
    echo "   kimi mcp add --transport stdio kimi-mem -- node $PROJECT_DIR/dist/mcp/server.js"
    exit 0
fi

# 添加到 MCP
echo "🔌 Adding to kimi MCP..."
kimi mcp add --transport stdio kimi-mem -- node "$PROJECT_DIR/dist/mcp/server.js"

echo ""
echo "✅ kimi-mem installed successfully!"
echo ""
echo "Usage:"
echo "  1. Start kimi CLI: kimi"
echo "  2. AI will automatically use memory functions"
echo "  3. Or manually: /skill:kimi-mem"
echo ""
echo "Data directory: ~/.kimi-mem"
echo ""

# 测试连接
echo "🧪 Testing connection..."
if kimi mcp test kimi-mem 2>/dev/null; then
    echo "✓ MCP server is working"
else
    echo "⚠️  MCP test failed. Please restart kimi CLI."
fi
