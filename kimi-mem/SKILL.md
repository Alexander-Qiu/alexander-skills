---
name: kimi-mem
description: 跨会话记忆管理系统。保存重要发现、检索历史上下文、保持项目连续性。需要 MCP 服务器支持。
compatibility: 可选 MCP 服务器，也支持文件降级模式
---

# 🧠 kimi-mem 记忆管理

一个完整的记忆管理系统，支持 MCP 服务器模式（推荐）或纯文件模式（降级）。

## 快速开始（30 秒）

### Step 1: 检查 MCP 状态

```
让我检查 kimi-mem MCP 服务器是否可用...
```

**如果可用** → 直接使用 MCP 工具
**如果不可用** → 进入安装流程

### Step 2: 自动安装（如需要）

```bash
# 1. 进入 skill 目录
cd ~/.config/agents/skills/kimi-mem  # 或你的 skill 安装路径

# 2. 安装依赖
npm install

# 3. 构建
npm run build

# 4. 添加到 Kimi MCP
kimi mcp add --transport stdio kimi-mem -- node $(pwd)/dist/mcp/server.js

# 5. 重启 Kimi CLI
```

### Step 3: 验证

```
让我保存一条测试记忆...
memory_save({
  title: "测试记忆",
  content: "kimi-mem 安装成功",
  type: "observation"
})
```

## 两种工作模式

### 模式 A: MCP 服务器模式（推荐）

**特点**：
- ✅ 高性能 SQLite + FTS5 全文搜索
- ✅ 9 个专用工具
- ✅ 项目自动检测
- ⚠️ 需要 Node.js 和安装步骤

**适用**：长期使用、大量记忆、需要高效搜索

### 模式 B: 文件模式（降级）

**特点**：
- ✅ 零依赖，纯 Markdown
- ✅ 任何 Agent 可用
- ✅ 人类可读
- ⚠️ 搜索靠 AI 解析，性能较低

**适用**：快速尝试、简单场景、无 Node 环境

---

## 核心工作流

### 何时保存记忆

| 优先级 | 场景 | 类型 | 示例 |
|--------|------|------|------|
| 🔴 必须 | 重要 Bug 修复 | `bugfix` | "修复内存泄漏..." |
| 🔴 必须 | 架构决策 | `decision` | "决定使用 SQLite..." |
| 🟡 建议 | 功能实现 | `feature` | "实现了用户认证..." |
| 🟡 建议 | 学习发现 | `learning` | "了解到 React 18..." |
| 🟢 可选 | 会话总结 | `summary` | "本次完成..." |

### 保存流程

```
检测到有价值的发现
        │
        ├─ MCP 可用? ─┬─ Yes ──► 使用 memory_save
        │             │
        │             └─ No ───► 保存到 .kimi-memory/memories.md
        │
        ▼
   记忆已保存
```

### 检索流程

```
项目开始 / 遇到问题
        │
        ├─ MCP 可用? ─┬─ Yes ──► memory_search / memory_recent
        │             │
        │             └─ No ───► 读取 .kimi-memory/memories.md
        │                           由 AI 分析内容
        ▼
   获取相关上下文
```

---

## MCP 工具详解

### 记忆管理

#### `memory_save`

保存一条记忆。

```json
{
  "title": "修复 WebSocket 内存泄漏",
  "content": "问题：...\n原因：...\n解决：...",
  "type": "bugfix",
  "importance": 5,
  "tags": ["memory-leak", "websocket"],
  "files": ["/src/hooks/useWebSocket.ts"]
}
```

**类型选项**：
- `observation` - 一般观察
- `decision` - 重要决策
- `bugfix` - Bug 修复
- `feature` - 功能实现
- `learning` - 学习发现
- `summary` - 会话总结
- `architecture` - 架构决策
- `refactor` - 重构

#### `memory_search`

全文搜索历史记忆。

```json
{
  "query": "authentication",
  "type": "decision",
  "tags": ["auth"],
  "limit": 10
}
```

#### `memory_recent`

获取最近的记忆。

```json
{
  "limit": 5,
  "projectName": "my-project"
}
```

#### `memory_get`

根据 ID 获取详情。

```json
{ "id": 42 }
```

#### `memory_get_batch`

批量获取多条记忆。

```json
{ "ids": [42, 43, 44] }
```

#### `memory_delete`

删除记忆。

```json
{ "id": 42 }
```

### 项目管理

#### `project_list`

列出所有项目。

#### `project_get_current`

获取当前项目（自动检测）。

### 统计

#### `stats_get`

获取记忆统计。

```json
{ "projectName": "my-project" }
```

---

## 文件模式详情

当 MCP 不可用时，使用 Markdown 文件保存记忆。

### 文件位置

```
.kimi-memory/
├── memories.md       # 主记忆文件
└── index.md          # 索引/目录
```

### 格式规范

```markdown
# Project Memory

## 2024-01-15

### [决策] 使用 SQLite 替代 PostgreSQL {#memory-1}
**标签**: #database #architecture  
**重要性**: ⭐⭐⭐⭐

决策原因：
- 项目规模小
- 减少部署复杂度
- 足够满足需求

---

### [Bug修复] 修复用户登录 Token 过期问题 {#memory-2}
**标签**: #auth #bugfix  
**重要性**: ⭐⭐⭐⭐⭐

问题：用户报告登录后一段时间后自动退出

原因：refresh token 未正确存储

解决：修复 localStorage key 名称
```

### 保存模板

```markdown
### [{{type}}] {{title}} {#memory-{{timestamp}}}
**标签**: {{tags}}  
**重要性**: {{importance}}

{{content}}

**相关文件**: {{files}}

---
```

---

## 最佳实践

### 标题写作

```
❌ "修复了 bug"
✅ "修复用户登录时的 Token 过期问题（issue #123）"

❌ "做了优化"
✅ "优化用户列表查询，减少 N+1 问题，性能提升 80%"
```

### 内容结构

```markdown
问题/背景：
- 什么情况下发现的
- 影响范围

解决方案：
- 具体步骤
- 关键代码

结果/验证：
- 测试通过
- 性能数据

参考：
- 相关链接
- issue 编号
```

### 标签规范

**技术领域**: `frontend` `backend` `database` `api` `auth` `performance`

**问题类型**: `bug` `crash` `memory-leak` `security` `optimization`

**状态**: `wip` `done` `blocked` `review-needed`

**优先级**: `critical` `high` `low`

---

## 使用示例

### 示例 1: Bug 修复后保存

```
用户：终于找到那个内存泄漏的原因了！

AI：太好了！让我详细记录下来，避免以后踩同样的坑。

[使用 memory_save]
{
  "title": "修复 WebSocket 连接未关闭导致的内存泄漏",
  "content": "**问题**：长时间运行后内存不断增长，最终 OOM crash\n\n**排查过程**：\n1. 使用 Chrome DevTools Memory 面板分析\n2. 发现 WebSocket 对象大量累积\n3. 检查代码发现组件卸载时未关闭连接\n\n**根本原因**：\nReact 组件卸载时，useEffect 的 cleanup 函数未正确调用 ws.close()\n\n**解决方案**：\n```typescript\nuseEffect(() => {\n  const ws = new WebSocket(url);\n  wsRef.current = ws;\n  \n  return () => {\n    if (ws.readyState === WebSocket.OPEN) {\n      ws.close();\n    }\n  };\n}, []);\n```\n\n**验证**：\n修复后运行 24 小时，内存稳定，无泄漏",
  "type": "bugfix",
  "importance": 5,
  "tags": ["memory-leak", "websocket", "react", "performance"],
  "files": ["/src/hooks/useWebSocket.ts"]
}

✅ 已保存记忆 (ID: 123)
```

### 示例 2: 项目开始时检索

```
用户：我们继续做那个认证功能

AI：让我先查看一下之前的相关工作和决策。

[使用 memory_search]
{
  "query": "authentication auth login",
  "type": "decision",
  "limit": 5
}

// 结果显示：
// [42] decision: 决定使用 JWT 而非 Session (2024-01-15)
// [38] architecture: 认证服务架构设计 (2024-01-14)
// [35] learning: 了解 refresh token 最佳实践 (2024-01-13)

AI：根据之前的决策，我们使用 JWT + Refresh Token 方案。让我查看详情...

[使用 memory_get]
{ "id": 42 }

AI：好的，基于之前的架构决策（使用 JWT，access token 15分钟，refresh token 7天），我们继续实现登录接口。
```

### 示例 3: 会话总结

```
会话结束前：

AI：让我保存本次会话的总结...

[使用 memory_save]
{
  "title": "会话总结：完成用户认证 API 设计和实现",
  "content": "**本次会话完成**：\n\n1. API 设计\n   - POST /api/auth/register - 用户注册\n   - POST /api/auth/login - 用户登录\n   - POST /api/auth/refresh - 刷新 token\n   - POST /api/auth/logout - 退出登录\n\n2. 数据库设计\n   - users 表：id, email, password_hash, created_at\n   - refresh_tokens 表：id, user_id, token, expires_at\n\n3. 实现细节\n   - 使用 bcrypt 进行密码哈希（cost factor: 10）\n   - JWT access token 有效期 15 分钟\n   - Refresh token 有效期 7 天\n   - 实现 token 黑名单机制\n\n**待办事项**：\n- [ ] 添加邮箱验证\n- [ ] 实现密码重置功能\n- [ ] 添加登录速率限制\n- [ ] 编写单元测试",
  "type": "summary",
  "importance": 4,
  "tags": ["auth", "api", "database", "session-summary", "planning"]
}

✅ 会话总结已保存
```

---

## 故障排除

### MCP 服务器未连接

**症状**：调用 memory_save 报错 "tool not found"

**解决**：
```bash
# 1. 检查 MCP 状态
kimi mcp list

# 2. 如果没安装，执行安装
cd ~/.config/agents/skills/kimi-mem
npm install && npm run build
kimi mcp add --transport stdio kimi-mem -- node $(pwd)/dist/mcp/server.js

# 3. 重启 Kimi CLI
```

### 数据库位置

- MCP 模式：`~/.kimi-mem/kimi-mem.db`
- 文件模式：`.kimi-memory/memories.md`

### 数据备份

```bash
# 备份 MCP 数据库
cp ~/.kimi-mem/kimi-mem.db ~/.kimi-mem/kimi-mem-backup.db

# 备份文件模式记忆
cp .kimi-memory/memories.md .kimi-memory/memories-backup.md
```

---

## 与其他工具对比

| 特性 | kimi-mem (MCP) | kimi-mem (File) | claude-mem | 纯手动笔记 |
|------|----------------|-----------------|------------|-----------|
| 自动捕获 | ❌ | ❌ | ✅ | ❌ |
| 全文搜索 | ✅ (FTS5) | ⚠️ (AI解析) | ✅ | ❌ |
| 结构化 | ✅ | ⚠️ | ✅ | ❌ |
| 项目感知 | ✅ | ✅ | ✅ | 手动 |
| 零依赖 | ❌ (需Node) | ✅ | ❌ | ✅ |
| 跨 Agent | MCP客户端 | 任何Agent | 仅限Claude | 通用 |
| 人类可读 | ❌ | ✅ | ❌ | ✅ |

---

## 路线图

### v0.2 (近期)
- [ ] 向量语义搜索
- [ ] 记忆自动压缩
- [ ] Web UI 管理界面

### v0.3 (中期)
- [ ] 导入/导出功能
- [ ] 多用户支持
- [ ] 云端同步选项

### v1.0 (长期)
- [ ] 与 Kimi CLI 深度集成
- [ ] 自动捕获建议
- [ ] 智能上下文注入

---

## 更多信息

- 源代码：本目录 `src/` 下
- 完整文档：`docs/` 目录（如有）
- 问题反馈：GitHub Issues
