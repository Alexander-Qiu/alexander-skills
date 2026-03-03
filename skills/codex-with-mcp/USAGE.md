# Codex with MCP - 使用指南

## 快速开始

### 1. 验证配置

```bash
# 运行验证脚本
./scripts/validate-codex-mcp.sh /path/to/codexmcp-0.7.4-py3-none-any.whl
```

### 2. 使用 Codex 工具

配置完成后，在 Kimi 中直接使用自然语言调用：

```
用 codex 分析一下这个项目的代码质量
```

Kimi 会自动调用 MCP 工具。

---

## 三种使用方式

### 方式 1: 通过 Kimi MCP 工具（推荐）

直接使用 `codex` MCP 工具：

```json
{
  "PROMPT": "Review this code for potential bugs",
  "cd": "/path/to/project",
  "sandbox": "read-only"
}
```

或者自然语言：
```
使用 codex 工具帮我 review 这段代码
```

### 方式 2: 通过脚本直接调用

```bash
# 直接调用 Codex（不通过 MCP）
./scripts/call-codex.sh \
  --prompt "Review the SKILL.md file" \
  --cd /path/to/project \
  --sandbox read-only
```

### 方式 3: 直接调用 Codex CLI

```bash
# 直接命令行调用
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Your prompt here"
```

---

## 常见使用场景

### 场景 1: 代码审查 (Code Review)

```bash
# 使用 codex CLI 进行代码审查
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Review this codebase and suggest improvements for:
1. Code readability
2. Potential bugs
3. Best practices violations

Focus on the src/ directory." 2>&1 | tee review_result.json
```

**输出解析：**
- `type: item.completed` + `type: agent_message` = Codex 的分析结果
- `type: turn.completed` = 任务完成

### 场景 2: 重构代码

```bash
codex exec \
  --model MiniMax-M2.5 \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --json \
  -- "Refactor the auth module to use async/await pattern.
Show me the unified diff patch first, then apply the changes."
```

### 场景 3: 多轮会话分析

```bash
# Step 1: 开始分析，获取 SESSION_ID
result=$(codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Analyze the architecture of this project")

# 从 result 中提取 SESSION_ID
# 然后继续会话...

codex exec resume <SESSION_ID> --json -- "Now dive deeper into the auth module"
```

---

## 输出格式解析

Codex 返回 JSON Lines 格式：

```json
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"type":"agent_message","text":"分析结果..."}}
{"type":"item.completed","item":{"type":"command_execution","command":"ls -la",...}}
{"type":"turn.completed","usage":{...}}
```

**关键字段：**
| 类型 | 说明 |
|------|------|
| `agent_message` | Codex 的回复文本 |
| `command_execution` | 执行的 shell 命令 |
| `file_edit` | 文件修改操作 |
| `turn.completed` | 本轮任务完成 |

---

## 完整示例：Review + 改进建议

```bash
#!/bin/bash

PROJECT_DIR="/mnt/data/qrz-dev/mem/alexander-skills/skills/codex-with-mcp"
REVIEW_PROMPT="请作为代码审查员，review 这个 skill 项目：

1. 检查 SKILL.md 是否清晰完整
2. 检查脚本是否有错误
3. 检查 examples 是否实用
4. 给出 3-5 条具体改进建议

请给出详细的分析结果。"

echo "=== 开始 Code Review ==="

codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "$REVIEW_PROMPT" \
  2>&1 | while read line; do
    # 解析 JSON 输出
    if echo "$line" | grep -q "agent_message"; then
      # 提取文本内容
      echo "$line" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print('\n[分析]', d['item']['text'][:500])"
    elif echo "$line" | grep -q "turn.completed"; then
      echo "\n[完成]"
    fi
  done

echo "=== Review 完成 ==="
```

---

## 调试技巧

### 启用调试日志

```bash
RUST_LOG=debug codex exec ... 2>&1 | grep -i "minimax\|provider\|error"
```

### 查看 MCP 配置

```bash
./scripts/show-mcp-config.sh
```

### 测试 MCP 服务器

```bash
# 验证 MCP 配置
./scripts/validate-codex-mcp.sh /path/to/wheel
```

---

## 故障排除

### 问题 1: MCP 工具调用超时

**现象**: `Timeout while calling MCP tool`
**解决**: 
1. 检查 MCP 配置: `cat ~/.kimi/mcp.json`
2. 手动测试 Codex CLI 是否工作
3. 直接使用 CLI 而非 MCP 工具

### 问题 2: Provider 不正确

**现象**: 日志显示 `provider_name=OpenAI` 而非 MiniMax
**解决**: 确保 `config.toml` 中设置了 `model_provider = "minimax"`

### 问题 3: 400 Bad Request

**现象**: API 返回 400 错误
**解决**: 
1. 检查模型名称是否正确（`MiniMax-M2.5`）
2. 检查 `wire_api` 设置为 `"chat"`

详细排查步骤参考: [examples/troubleshooting-minimax-setup.md](examples/troubleshooting-minimax-setup.md)

---

## 最佳实践

1. **始终使用 `--sandbox read-only` 进行分析任务**
2. **需要修改文件时，先要求显示 diff，确认后再应用**
3. **复杂任务使用 `--return_all_messages` 获取完整思考过程**
4. **长时间任务使用 `timeout` 命令避免卡死**
5. **保存 SESSION_ID 以便后续继续对话**

---

## 参考

- [troubleshooting-minimax-setup.md](examples/troubleshooting-minimax-setup.md) - MiniMax 配置排查
- [Codex CLI 文档](https://github.com/openai/codex)
- [MCP 协议](https://modelcontextprotocol.io)
