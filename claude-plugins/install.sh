#!/bin/bash
# Claude Plugins 安装脚本
# 支持全局安装 (~/.claude/plugins/) 或项目安装 (./.claude/plugins/)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGINS_DIR="$SCRIPT_DIR/plugins"

# 检查 plugins 目录是否存在
if [ ! -d "$PLUGINS_DIR" ]; then
    echo "错误: 找不到 plugins 目录: $PLUGINS_DIR"
    exit 1
fi

# 选择安装模式
echo "========================================"
echo "  Claude Plugins 安装脚本"
echo "========================================"
echo ""
echo "选择安装模式:"
echo "1) 全局安装 (~/.claude/plugins/)"
echo "2) 项目安装 (当前目录 .claude/plugins/)"
echo ""
read -p "请输入选项 (1/2): " choice

if [ "$choice" = "1" ]; then
    TARGET_DIR="$HOME/.claude/plugins/alexander-skills"
    echo ""
    echo "将安装到: $TARGET_DIR"
elif [ "$choice" = "2" ]; then
    TARGET_DIR="./.claude/plugins/alexander-skills"
    echo ""
    echo "将安装到: $TARGET_DIR (当前目录)"
else
    echo ""
    echo "无效选项，退出。"
    exit 1
fi

# 创建目标目录
mkdir -p "$TARGET_DIR"

# 统计 plugin 数量
PLUGIN_COUNT=$(ls -1 "$PLUGINS_DIR" | wc -l)

echo ""
echo "发现 $PLUGIN_COUNT 个 plugins，开始安装..."
echo ""

# 复制所有 plugins
INSTALLED=0
for plugin in "$PLUGINS_DIR"/*; do
    if [ -d "$plugin" ]; then
        name=$(basename "$plugin")
        echo "  [✓] 安装 $name"
        cp -r "$plugin" "$TARGET_DIR/"
        INSTALLED=$((INSTALLED + 1))
    fi
done

echo ""
echo "========================================"
echo "  安装完成!"
echo "========================================"
echo ""
echo "已安装 $INSTALLED 个 plugins 到:"
echo "  $TARGET_DIR"
echo ""
echo "使用方法:"
echo "  - 查看已安装 plugins: ls $TARGET_DIR"
echo "  - Claude Code 会自动加载这些 plugins"
echo "  - 使用 /plugin 命令查看 plugin 列表"
echo ""
