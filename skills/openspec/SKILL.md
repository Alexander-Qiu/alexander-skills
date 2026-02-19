---
name: openspec
description: Use when the user mentions OpenSpec, /opsx: commands, spec-driven development, or wants to use the OpenSpec framework for structured specification and change management. This skill provides guidance on using OpenSpec for documentation-first development with specs, changes, and artifacts.
---

# OpenSpec 规范驱动开发

OpenSpec 是一个面向文档的规范框架，通过结构化规格（Specs）和变更（Changes）管理软件开发。

## 何时使用 OpenSpec

**适合场景**:
- 需要结构化记录需求和设计决策
- 团队协作需要明确的规格文档
- 需要追踪变更历史和决策依据
- 项目需要长期的可维护性和知识传承

**触发词**:
- `/opsx:`, `openspec`, `spec-driven`
- "需要写规格文档", "怎么记录这个变更"
- "规范驱动开发", "文档优先"

## 核心概念

```
openspec/
├── specs/           # 源头真相 - 系统当前行为规格
└── changes/         # 变更提案 - 独立文件夹直到合并
    ├── add-feature/
    │   ├── proposal.md     # 为什么和做什么
    │   ├── design.md       # 技术方案
    │   ├── tasks.md        # 实现任务清单
    │   └── specs/          # 增量规格
    └── archive/            # 归档的变更
```

## 与 Superpowers Skills 的关系

| 维度 | OpenSpec | Superpowers |
|------|----------|-------------|
| **定位** | 文档/规范管理 | 代码实现最佳实践 |
| **产出** | specs/, changes/ | 高质量代码 |
| **互补** | 记录"做什么"和"为什么" | 指导"怎么做" |

**推荐组合**:
```
OpenSpec (规划层)     Superpowers (执行层)
     │                       │
     ├─ specs/               ├─ brainstorming
     ├─ changes/             ├─ writing-plans
     │   ├─ proposal.md      ├─ executing-plans
     │   ├─ design.md        ├─ test-driven-development
     │   └─ tasks.md         └─ requesting-code-review
     │
     └─ archive/             └─ kimi-mem (记忆)
```

## 工作流命令

### 探索阶段
```
/opsx:explore [topic]
```
在承诺变更前探索想法、调查问题、澄清需求。

### 创建变更
```
/opsx:new <change-name> [--schema <schema>]
```
创建新的变更文件夹，开始规划。

### 快速前进
```
/opsx:ff
```
一次性创建所有规划文档（proposal + specs + design + tasks）。

### 继续下一步
```
/opsx:continue [change-name]
```
基于依赖关系创建下一个 artifact。

### 应用实现
```
/opsx:apply [change-name]
```
基于 tasks.md 执行实现任务。

### 验证
```
/opsx:verify [change-name]
```
验证实现是否符合 artifacts。

### 归档
```
/opsx:archive [change-name]
```
将完成的变更归档到 `changes/archive/YYYY-MM-DD-<name>/`。

### 引导教程
```
/opsx:onboard
```
完整的引导式教程，带你走一遍完整工作流。

## 完整工作流示例

### 场景：添加暗黑模式

```text
User: /opsx:new add-dark-mode

AI: Created openspec/changes/add-dark-mode/
    Schema: spec-driven
    Ready to create: proposal
    Use /opsx:continue or /opsx:ff

User: /opsx:ff

AI: Creating all planning artifacts...
    ✓ proposal.md — why and what
    ✓ specs/ — requirements and scenarios
    ✓ design.md — technical approach
    ✓ tasks.md — implementation checklist
    Ready for implementation!

User: /opsx:apply

AI: Implementing tasks...
    ✓ 1.1 Add theme context provider
    ✓ 1.2 Create toggle component
    ✓ 2.1 Add CSS variables
    ✓ 2.2 Wire up localStorage
    All tasks complete!

User: /opsx:archive

AI: Archived to openspec/changes/archive/2025-01-23-add-dark-mode/
    Specs updated. Ready for the next feature.
```

## Spec 文件格式

```markdown
# Auth Specification

## Purpose
Authentication and session management for the application.

## Requirements

### Requirement: User Authentication
The system SHALL issue a JWT token upon successful login.

#### Scenario: Valid credentials
- GIVEN a user with valid credentials
- WHEN the user submits login form
- THEN a JWT token is returned
- AND the user is redirected to dashboard

#### Scenario: Invalid credentials
- GIVEN invalid credentials
- WHEN the user submits login form
- THEN an error message is displayed
- AND no token is issued
```

## 与现有 Skills 协作

### 方案 A：分层使用（推荐）

```
阶段 1：OpenSpec 规划
├── /opsx:explore           (如需探索)
├── /opsx:new               创建变更
├── /opsx:ff                生成 artifacts
└── [AI 使用 Superpowers 辅助]
    ├── brainstorming       如需深入设计讨论
    └── writing-plans       生成更详细的 tasks.md

阶段 2：Superpowers 执行
├── executing-plans         执行任务
├── test-driven-development TDD 开发
└── requesting-code-review  代码审查

阶段 3：OpenSpec 收尾
├── /opsx:verify            验证实现
└── /opsx:archive           归档变更
```

### 方案 B：OpenSpec 为主

如果用户明确要求使用 OpenSpec 工作流：
1. 跟随用户的 `/opsx:` 命令
2. 在执行阶段自然融入 Superpowers 的最佳实践
3. 不强制打断 OpenSpec 流程

### 方案 C：混合触发

- 用户输入 `/opsx:` 命令 → 走 OpenSpec 流程
- 用户自然语言描述需求 → 触发 Superpowers skills

## 安装 OpenSpec

```bash
npm install -g @fission-ai/openspec@latest

# 初始化项目
cd your-project
openspec init
```

## 最佳实践

1. **保持轻量**：大部分变更使用 Lite spec，只有高风险变更需要 Full spec
2. **渐进严格**：从简单开始，根据需要增加规范程度
3. **行为优先**：Specs 描述"做什么"，不是"怎么做"
4. **及时归档**：完成的变更及时归档，保持 changes/ 目录整洁
5. **结合记忆**：关键决策用 kimi-mem 保存，跨会话保持上下文

## 故障排除

### OpenSpec 未初始化
```
/opsx:new
→ Error: OpenSpec not initialized
→ Run: openspec init
```

### 变更名称冲突
```
/opsx:new add-feature
→ Error: Change already exists
→ Use different name or archive existing
```

## 参考资源

- 官网：https://openspec.dev
- 文档：https://github.com/Fission-AI/OpenSpec/tree/main/docs
- Skills 目录：https://skills.sh
