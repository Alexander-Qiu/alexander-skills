# Claude Code + Codex MCP 配置指南

本案例展示如何在 Claude Code 中配置和使用 Codex MCP 服务器。

## 前置条件

- Claude Code CLI 已安装 (`npm install -g @anthropic-ai/claude-code`)
- Codex CLI 已安装 (`pip install codex-cli`)
- uv/uvx 已安装 (`pip install uv`)
- codexmcp wheel 文件已构建

## 安装步骤

### 1. 添加 MCP 服务器

```bash
claude mcp add codex -s user --transport stdio -- \
  uvx --from /mnt/data/qrz-dev/mem/misc-dev/codexmcp/dist/codexmcp-0.7.4-py3-none-any.whl codexmcp
```

参数说明：
- `-s user`: 用户级配置（对所有项目可用）
- `--transport stdio`: 使用 stdio 传输方式
- `--`: 分隔符，后面是实际运行的命令

### 2. 验证安装

```bash
# 查看所有 MCP 服务器
claude mcp list

# 预期输出：
# plugin:claude-mem:mcp-search: ... - ✓ Connected
# codex: uvx --from ... - ✓ Connected

# 查看详细信息
claude mcp get codex
```

### 3. 测试使用

在 Claude Code 中输入：

```
用 codex 分析当前目录的代码结构
```

Claude 会自动调用 codex 工具并返回结果。

## 配置环境变量（可选）

如果需要传递 API key：

```bash
claude mcp add codex -s user -e MINIMAX_API_KEY=sk-api-xxx -- \
  uvx --from /path/to/codexmcp-0.7.4-py3-none-any.whl codexmcp
```

## 管理 MCP 服务器

```bash
# 移除服务器
claude mcp remove codex -s user

# 重新添加
claude mcp add codex -s user --transport stdio -- ...

# 查看帮助
claude mcp --help
```

## 与 Kimi 的对比

| 操作 | Kimi | Claude Code |
|------|------|-------------|
| 配置文件 | `~/.kimi/mcp.json` | `claude mcp add` 命令 |
| 验证状态 | 查看文件 | `claude mcp list` |
| 移除服务器 | 编辑 JSON | `claude mcp remove` |

## 常见问题

### MCP server not found

确保 Claude Code 版本支持 MCP：

```bash
claude --version  # 需要 >= 0.2.0
```

### Codex command failed

检查 codex CLI 是否可用：

```bash
codex --version
codex config list
```

### Wheel file not found

使用绝对路径：

```bash
ls -la /absolute/path/to/codexmcp-0.7.4-py3-none-any.whl
```

## 实际使用示例

### 示例 1：代码审查

用户输入：
```
用 codex 审查 src/utils.py 的实现质量
```

Claude 会：
1. 调用 codex 工具
2. 传递文件路径和分析需求
3. 整理返回结果给用户

### 示例 2：多步分析

```
步骤 1：用 codex 分析项目整体架构
步骤 2：基于分析结果，深入研究核心模块
步骤 3：提出优化建议
```

Codex 会维护会话状态，支持多轮对话。

### 示例 3：代码重构

```
用 codex 重构 auth 模块，改进错误处理
→ Sandbox: workspace-write
→ 自动应用修改
```

## 参考资料

- [Claude Code MCP 文档](https://code.claude.com/docs/en/mcp)
- [Codex CLI](https://github.com/openai/codex)
- [CodexMCP](https://github.com/GuDaStudio/codexmcp)
