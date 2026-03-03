# Codex with MCP - 使用指南

## 快速开始

### 方式 1: 直接命令行调用（最简单）

```bash
# 进入项目目录
cd /mnt/data/qrz-dev/mem/alexander-skills/skills/codex-with-mcp

# 使用 codex CLI 直接调用
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Review the SKILL.md and suggest improvements"
```

### 方式 2: 通过脚本调用

```bash
# 使用提供的脚本
./scripts/call-codex.sh \
  --prompt "List all files" \
  --cd /path/to/project \
  --sandbox read-only
```

### 方式 3: 在 Kimi 中使用（推荐）

配置完成后，直接在对话中说：

```
用 codex 分析一下这个项目的代码结构
```

Kimi 会自动调用 MCP 工具。

---

## 实际使用示例

### 示例 1: Code Review

```bash
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Review this codebase for:
1. Security issues
2. Performance problems  
3. Code style violations

Provide specific line numbers and suggestions." \
  2>&1 | grep -A5 'agent_message'
```

### 示例 2: 生成代码

```bash
codex exec \
  --model MiniMax-M2.5 \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --json \
  -- "Create a Python script that:
- Reads a JSON file
- Validates the schema
- Outputs a summary

Save it to validate_json.py" \
  2>&1 | tee output.json
```

### 示例 3: 调试问题

```bash
# 先分析错误日志
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "This is my error log:
$(cat /tmp/error.log)

What caused this error and how do I fix it?" \
  2>&1 | grep 'agent_message'
```

---

## 输出解析

Codex 返回 JSON Lines 格式，每行是一个事件：

```json
{"type":"thread.started","thread_id":"..."}
{"type":"turn.started"}
{"type":"item.completed","item":{"type":"agent_message","text":"分析内容..."}}
{"type":"turn.completed","usage":{"input_tokens":1000,"output_tokens":500}}
```

**常用解析命令：**

```bash
# 只看分析结果
codex exec ... | grep 'agent_message' | python3 -c "
import sys, json
for line in sys.stdin:
    d = json.loads(line)
    if d.get('item', {}).get('type') == 'agent_message':
        print(d['item']['text'])
"

# 保存完整输出
codex exec ... 2>&1 | tee codex_output.jsonl

# 提取最后一条消息
codex exec ... | grep 'agent_message' | tail -1
```

---

## 高级用法

### 使用 Session 保持对话上下文

```bash
# Step 1: 开始对话，获取 SESSION_ID
output=$(codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Analyze the architecture of this project")

# 提取 SESSION_ID
SESSION_ID=$(echo "$output" | grep 'thread.started' | python3 -c "
import sys, json
print(json.loads(sys.stdin.read())['thread_id'])
")

# Step 2: 继续对话
codex exec resume "$SESSION_ID" --json -- "Now focus on the auth module"
```

### 批量处理文件

```bash
# 批量 review 多个文件
for file in src/*.py; do
  echo "=== Reviewing $file ==="
  codex exec \
    --model MiniMax-M2.5 \
    --sandbox read-only \
    --skip-git-repo-check \
    --json \
    -- "Review $file for bugs" \
    2>&1 | grep 'agent_message' | tail -1
  echo ""
done
```

---

## 配置检查清单

使用前请确认：

- [ ] `~/.kimi/mcp.json` 已配置
- [ ] `~/.codex/config.toml` 已配置（参考 examples/troubleshooting-minimax-setup.md）
- [ ] `MINIMAX_API_KEY` 环境变量已设置
- [ ] `codex --version` 能正常显示版本
- [ ] `./scripts/validate-codex-mcp.sh` 通过所有检查

---

## 故障排除

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| MCP 调用失败 | `Client failed to connect` | 直接使用 CLI 调用 |
| Provider 错误 | 日志显示 `provider_name=OpenAI` | 检查 `model_provider = "minimax"` |
| 400 错误 | `Bad Request` | 检查模型名称是 `MiniMax-M2.5` |
| 超时 | 长时间无响应 | 使用 `timeout` 命令限制时间 |

---

## 文件说明

```
codex-with-mcp/
├── SKILL.md              # Skill 定义文档
├── README.md             # 本文件
├── USAGE.md              # 详细使用指南
├── examples/
│   └── troubleshooting-minimax-setup.md  # 配置排查案例
└── scripts/
    ├── validate-codex-mcp.sh    # 配置验证脚本
    ├── show-mcp-config.sh       # 显示配置脚本
    └── call-codex.sh            # 直接调用脚本
```

---

## 现在就可以开始！

```bash
# 验证配置
./scripts/validate-codex-mcp.sh /mnt/data/qrz-dev/mem/misc-dev/codexmcp/dist/codexmcp-0.7.4-py3-none-any.whl

# 执行第一次 codex review
codex exec \
  --model MiniMax-M2.5 \
  --sandbox read-only \
  --skip-git-repo-check \
  --json \
  -- "Say hello and confirm you're working" \
  2>&1 | head -20
```
