---
name: kimi-mem
description: 跨会话记忆管理系统。自动保存重要发现、检索历史上下文，让 AI 记住之前的对话和决策。
compatibility: 需要 MCP 服务器 kimi-mem 运行
---

# kimi-mem 记忆管理

kimi-mem 是一个轻量级的记忆管理系统，帮助你在多个会话之间保持上下文连续性。

## 快速开始

### 1. 安装 MCP 服务器

```bash
# 克隆仓库
git clone <repo-url> kimi-mem
cd kimi-mem

# 安装依赖
npm install

# 构建
npm run build
```

### 2. 添加到 Kimi CLI

```bash
kimi mcp add --transport stdio kimi-mem -- node /path/to/kimi-mem/dist/mcp/server.js
```

### 3. 开始使用

使用 `/skill:kimi-mem` 加载此 skill，或让 AI 自动决定何时使用记忆功能。

## 核心工作流

### 何时保存记忆

**必须保存的情况**：
- 🔴 修复了重要的 bug（尤其是花了较长时间）
- ⚡ 做出了架构或设计决策
- 📚 学习到重要的技术知识
- 🐛 发现了坑/陷阱并解决
- 🔄 重构了关键代码

**建议保存的情况**：
- ✅ 完成了复杂的功能实现
- 📋 整理了项目结构或文档
- 🔧 配置了复杂的工具/环境

### 何时检索记忆

**项目开始时**：
```
"让我先查看一下之前在这个项目上的工作记录..."
→ 使用 memory_search 或 memory_recent
```

**遇到问题时**：
```
"我们之前是不是解决过类似的问题？"
→ 使用 memory_search 查找相关记忆
```

**代码审查时**：
```
"让我检查一下之前的决策和约定..."
→ 搜索 decision 类型的记忆
```

## 记忆类型指南

| 类型 | 图标 | 使用场景 | 示例 |
|------|------|----------|------|
| `observation` | 👁️ | 一般观察 | "发现 API 返回格式不一致" |
| `decision` | ⚡ | 重要决策 | "决定使用 SQLite 而不是 PostgreSQL" |
| `bugfix` | 🐛 | Bug 修复 | "修复了 race condition 导致的崩溃" |
| `feature` | ✨ | 功能实现 | "实现了用户认证模块" |
| `learning` | 📚 | 学习/发现 | "了解到 React 18 的并发特性" |
| `summary` | 📝 | 会话总结 | "本次会话完成了数据库设计" |
| `architecture` | 🏗️ | 架构决策 | "采用微服务架构，服务间使用 gRPC" |
| `refactor` | ♻️ | 重构 | "重构了路由层，提取公共中间件" |

## 标签规范

使用一致的标签体系便于检索：

**技术领域**：`frontend`, `backend`, `database`, `api`, `auth`, `performance`

**问题类型**：`bug`, `crash`, `slow`, `memory-leak`, `security`

**状态**：`wip`, `done`, `blocked`, `review-needed`

**优先级**：`critical`, `high`, `low`

## 最佳实践

### 保存记忆时的原则

1. **标题要具体**：
   ```
   ❌ "修复了 bug"
   ✅ "修复了用户登录时的 token 过期问题（issue #123）"
   ```

2. **内容要完整**：
   - 问题是什么
   - 如何解决的
   - 关键代码/配置
   - 参考链接

3. **选对类型和重要性**：
   - Critical bugfix → `bugfix` + importance: 5
   - 一般观察 → `observation` + importance: 2-3

4. **添加相关标签**：
   - 便于后续分类检索
   - 建议使用 2-5 个标签

### 检索记忆时的策略

1. **从宽泛到具体**：
   ```
   先搜索 "auth" → 再搜索 "auth token expire"
   ```

2. **使用类型过滤**：
   ```
   只看 bugfix：type="bugfix"
   只看决策：type="decision"
   ```

3. **查看时间线**：
   ```
   使用 memory_recent 了解最近的工作
   ```

## 使用示例

### 保存一个 Bug Fix

```
我发现并修复了一个重要的内存泄漏问题。

让我用 kimi-mem 保存这个发现：

memory_save({
  title: "修复 WebSocket 连接导致的内存泄漏",
  content: "问题：长时间运行后内存不断增长...\n\n原因：WebSocket 连接未正确关闭...\n\n解决：在组件卸载时调用 ws.close()...",
  type: "bugfix",
  importance: 5,
  tags: ["memory-leak", "websocket", "react", "performance"],
  files: ["/src/hooks/useWebSocket.ts", "/src/components/Chat.tsx"]
})
```

### 检索相关历史

```
用户：我们需要实现用户认证

AI：让我查看一下之前关于认证的工作：

memory_search({
  query: "authentication auth login",
  type: "decision",
  limit: 5
})

// 根据结果决定实现方案
```

### 会话总结

```
会话结束前：

memory_save({
  title: "会话总结：完成数据库设计和 API 规划",
  content: "本次会话完成：\n1. 设计了用户、订单、产品表结构\n2. 确定了使用 Prisma 作为 ORM\n3. 规划了 REST API 端点\n\n下一步：实现用户注册登录接口",
  type: "summary",
  importance: 4,
  tags: ["database", "api", "planning"]
})
```

## 作为子 Skill 使用

其他 Skill 可以声明依赖 kimi-mem：

```markdown
---
name: my-project-skill
description: 我的项目专用 skill
dependencies:
  - kimi-mem
---

## 工作流程

1. 使用 kimi-mem 检索项目历史
2. 分析需求
3. 实现功能
4. 使用 kimi-mem 保存关键决策
```

## 故障排除

### MCP 服务器未连接

```bash
# 检查服务器状态
kimi mcp list

# 重新添加
kimi mcp remove kimi-mem
kimi mcp add --transport stdio kimi-mem -- node /path/to/kimi-mem/dist/mcp/server.js
```

### 数据库位置

- 数据存储在 `~/.kimi-mem/kimi-mem.db`
- 可以直接用 SQLite 工具查看

## 与其他工具对比

| 特性 | kimi-mem | claude-mem | 纯手动笔记 |
|------|----------|------------|-----------|
| 自动捕获 | ❌ | ✅ | ❌ |
| 全文搜索 | ✅ | ✅ | 依赖工具 |
| 项目感知 | ✅ | ✅ | 手动管理 |
| 类型系统 | ✅ | ✅ | 自定义 |
| 侵入性 | 无 | 深度集成 | 无 |
| 可移植性 | 任何 MCP 客户端 | 仅限 Claude | 通用 |

## 路线图

- [ ] 向量语义搜索
- [ ] 记忆压缩和总结
- [ ] 时间线可视化
- [ ] 导入/导出功能
- [ ] Web UI 管理界面
