#!/bin/bash
# Alexander Skills — Claude Plugins 一键安装脚本
# 用法: ./install.sh
# 通过 claude plugin CLI 安装全部 22 个 plugins

set -e

echo "========================================"
echo "  Alexander Skills — Claude Plugins"
echo "  一键安装 22 个 plugins"
echo "========================================"
echo ""

# ── 1. 添加 Marketplaces ──────────────────────────────────────────────────────
echo "▶ Step 1: 注册 marketplaces..."

claude plugin marketplace add anthropics/claude-plugins-official --name claude-plugins-official 2>/dev/null \
  && echo "  ✓ claude-plugins-official" \
  || echo "  · claude-plugins-official (已存在，跳过)"

claude plugin marketplace add tanweai/pua --name pua-skills 2>/dev/null \
  && echo "  ✓ pua-skills" \
  || echo "  · pua-skills (已存在，跳过)"

claude plugin marketplace add openai/codex-plugin-cc --name openai-codex 2>/dev/null \
  && echo "  ✓ openai-codex" \
  || echo "  · openai-codex (已存在，跳过)"

claude plugin marketplace add thedotmack/claude-mem --name thedotmack 2>/dev/null \
  && echo "  ✓ thedotmack" \
  || echo "  · thedotmack (已存在，跳过)"

echo ""

# ── 2. 安装 claude-plugins-official ──────────────────────────────────────────
echo "▶ Step 2: 安装 claude-plugins-official 插件..."

OFFICIAL_PLUGINS=(
  agent-sdk-dev
  claude-code-setup
  claude-md-management
  code-review
  code-simplifier
  commit-commands
  feature-dev
  frontend-design
  github
  learning-output-style
  notion
  plugin-dev
  pr-review-toolkit
  ralph-loop
  remember
  rust-analyzer-lsp
  skill-creator
  superpowers
  telegram
)

for plugin in "${OFFICIAL_PLUGINS[@]}"; do
  claude plugin install "${plugin}@claude-plugins-official" 2>/dev/null \
    && echo "  ✓ $plugin" \
    || echo "  · $plugin (已安装或失败，跳过)"
done

echo ""

# ── 3. 安装 marketplace 插件 ──────────────────────────────────────────────────
echo "▶ Step 3: 安装第三方 marketplace 插件..."

claude plugin install "pua@pua-skills" 2>/dev/null \
  && echo "  ✓ pua" \
  || echo "  · pua (已安装或失败，跳过)"

claude plugin install "codex@openai-codex" 2>/dev/null \
  && echo "  ✓ codex" \
  || echo "  · codex (已安装或失败，跳过)"

claude plugin install "claude-mem@thedotmack" 2>/dev/null \
  && echo "  ✓ claude-mem" \
  || echo "  · claude-mem (已安装或失败，跳过)"

echo ""

# ── 4. 验证 ───────────────────────────────────────────────────────────────────
echo "▶ Step 4: 验证安装..."
INSTALLED=$(claude plugin list 2>/dev/null | grep -c "✔\|enabled" || true)
echo "  已安装并启用的插件数量: $INSTALLED"

echo ""
echo "========================================"
echo "  安装完成！重启 Claude Code 生效。"
echo "========================================"
