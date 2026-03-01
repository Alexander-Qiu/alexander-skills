---
name: cli-agent-caller
description: |
  通过 CLI 调用其他 AI Agent（Kimi、Claude 等）进行协作。
  使用场景：(1) 需要不同模型的能力互补，(2) 并行处理多个任务，
  (3) 验证结果一致性，(4) 利用特定 agent 的专长。
author: Alexander Qiu
version: 1.0.0
date: 2026-03-01
---

# CLI Agent 调用器

## 概述

通过命令行界面调用其他 AI Agent（Kimi、Claude 等），实现多 Agent 协作。

## 支持的 Agent

### 1. Kimi CLI

**安装**: `npm install -g kimi-cli`

**基本用法**:
```bash
# 查看帮助
kimi --help

# 自动确认模式（-y/--yes/--yolo）
kimi -y

# 指定工作目录
kimi -w /path/to/project

# 继续上次会话
kimi -c
# 或
kimi --continue

# 添加额外目录到工作区
kimi --add-dir /another/path
```

**可用命令**:
- `kimi login` - 登录 Kimi 账号
- `kimi logout` - 退出登录
- `kimi term` - 启动 TUI 界面
- `kimi acp` - 运行 ACP 服务器
- `kimi info` - 显示版本信息
- `kimi mcp` - 管理 MCP 服务器配置
- `kimi web` - 启动 Web 界面

### 2. Claude CLI (Claude Code)

**安装**: 通过 Anthropic 官方安装

**基本用法**:
```bash
# 查看帮助
claude --help

# 非交互式输出（-p/--print）
claude -p "你的提示"

# 自动确认（危险模式，仅用于沙箱环境）
claude --dangerously-skip-permissions
claude -y

# 继续上次会话
claude -c
# 或
claude --continue

# 指定工作目录
claude -w /path/to/project

# 添加额外目录
claude --add-dir /another/path

# 指定模型
claude --model sonnet
claude --model opus

# 指定 effort 级别
claude --effort low
claude --effort medium
claude --effort high

# 调试模式
claude -d
claude --debug
```

## 多 Agent 协作模式

### 模式 1: 结果验证
```bash
# 使用 Kimi 生成代码
kimi -y "写一个 Python 函数计算斐波那契数列"

# 使用 Claude 验证结果
claude -p "请验证这段代码的正确性和性能"
```

### 模式 2: 并行处理
```bash
# 并行启动多个 agent 处理不同任务
kimi -y "分析代码结构" &
claude -p "检查潜在 bug" &
wait
```

### 模式 3: 专业分工
```bash
# Kimi 擅长代码生成和调试
kimi -y "生成 React 组件"

# Claude 擅长架构设计
claude -p "设计数据库模型"
```

## 注意事项

1. **权限问题**: 
   - Claude CLI 默认会询问权限
   - 使用 `-y` 或 `--dangerously-skip-permissions` 可跳过（仅限沙箱环境）

2. **会话管理**:
   - 使用 `-c` 或 `--continue` 继续上次会话
   - 使用 `--session <id>` 指定特定会话

3. **工作目录**:
   - 默认使用当前目录
   - 使用 `-w` 指定特定目录
   - 使用 `--add-dir` 添加额外目录到工作区

4. **成本考虑**:
   - 多 Agent 调用会增加 API 费用
   - 使用 `--max-budget-usd` 限制 Claude 的开销

## 集成示例

### 在 OpenClaw 中使用
```bash
# 调用 Kimi 进行代码审查
exec("kimi -y '请审查这段代码'", workdir="/project/path")

# 调用 Claude 进行架构建议
exec("claude -p '设计系统架构'", workdir="/project/path")
```

### 在脚本中使用
```bash
#!/bin/bash

# 多 Agent 代码审查流程
echo "=== Kimi 代码分析 ==="
kimi -y "分析代码质量和潜在问题"

echo "=== Claude 架构评估 ==="
claude -p "评估代码架构设计"

echo "=== 结果汇总 ==="
# 合并结果...
```

## 故障排除

### Kimi CLI 无法连接
- 检查网络连接
- 运行 `kimi login` 重新登录
- 检查 `~/.kimi/config` 配置

### Claude CLI 权限被拒绝
- 检查 API key 配置
- 确保有访问权限
- 使用 `claude login` 重新认证

### 会话无法恢复
- 检查会话 ID 是否正确
- 确认会话文件存在
- 使用 `claude --list-sessions` 查看可用会话

## 相关技能

- `agent-cluster` - 多 Agent 集群编排
- `dispatching-parallel-agents` - 并行 Agent 调度
- `subagent-driven-development` - 子 Agent 驱动开发

## 参考链接

- [Kimi CLI 文档](https://moonshotai.github.io/kimi-cli/)
- [Claude Code 文档](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)
