# Planning with Files - 使用指南

> **Work like Manus** - 使用文件作为"磁盘上的工作记忆"

## 概述

这个技能实现了 Manus 风格的基于文件的规划，适用于复杂任务。通过创建三个核心文件来追踪进度：

1. **task_plan.md** - 任务计划（路线图）
2. **findings.md** - 研究发现（知识库）
3. **progress.md** - 进度跟踪（状态更新）

## 何时使用

- 复杂多步骤任务（需要 >5 个 tool calls）
- 研究项目
- 任何可能因上下文过长而遗忘目标的任务
- 需要跨会话保持进度的任务

## 核心文件说明

### 1. task_plan.md - 任务计划

**作用**: 整个任务的路线图，防止在 50+ tool calls 后遗忘原始目标

**关键部分**:
- **Goal**: 一句话描述最终目标
- **Current Phase**: 当前所处阶段
- **Phases**: 3-7 个可完成的逻辑阶段
- **Key Questions**: 需要回答的重要问题
- **Decisions Made**: 技术决策记录
- **Errors Encountered**: 错误日志（避免重复犯错）

**状态流转**: `pending` → `in_progress` → `complete`

### 2. findings.md - 研究发现

**作用**: 知识库，记录所有发现的信息

**关键部分**:
- **Summary**: 关键发现总结
- **Code Patterns**: 代码模式记录
- **Error Patterns**: 错误模式记录
- **Architecture Notes**: 架构笔记
- **API Documentation**: API 文档
- **Dependencies**: 依赖项记录

### 3. progress.md - 进度跟踪

**作用**: 实时状态更新，记录已完成和待办事项

**关键部分**:
- **Current Status**: 当前状态概览
- **Completed Tasks**: 已完成任务列表
- **Next Tasks**: 下一步任务
- **Blockers**: 阻碍项
- **Recent Updates**: 最近更新（带时间戳）

## 使用流程

### 步骤 1: 创建规划文件

在开始任何复杂任务前，先创建三个文件：

```bash
# 从模板复制
cp /home/abaka/qiurz/kaggle-test/tb-in-one-dev/alexander-skills/skills/planning-with-files/templates/*.md ./
```

### 步骤 2: 填充 task_plan.md

1. 填写 **Goal** - 清晰的目标描述
2. 定义 **Phases** - 3-7 个阶段
3. 设置 **Current Phase** 为 "Phase 1"
4. 列出 **Key Questions**

### 步骤 3: 开发过程中更新

**每个阶段完成后**:
1. 更新 `task_plan.md` 中的阶段状态
2. 在 `progress.md` 中记录完成的任务
3. 在 `findings.md` 中记录重要发现

**遇到错误时**:
1. 在 `task_plan.md` 的 Errors 表格中记录
2. 记录尝试次数和解决方案

**做重要决策时**:
1. 在 `task_plan.md` 的 Decisions 表格中记录
2. 写明决策理由（以后会忘记）

### 步骤 4: 定期回顾

- **每 10-15 个 tool calls 后**: 重新阅读 `task_plan.md`
- **遇到阻碍时**: 检查 `findings.md` 是否已有解决方案
- **会话恢复时**: 使用 session-catchup 脚本同步状态

## 实际示例

### 示例场景: 修复 8 个语法错误文件

#### task_plan.md

```markdown
# Task Plan: 修复语法错误文件

## Goal
修复 8 个 test_outputs.py 文件的语法错误，确保它们可以正常编译运行。

## Current Phase
Phase 2

## Phases

### Phase 1: 问题分析
- [x] 识别 8 个有语法错误的文件
- [x] 分类错误类型（未闭合字符串、f-string 等）
- [x] 分析错误原因
- **Status:** complete

### Phase 2: 修复实现
- [ ] 修复未闭合字符串错误
- [ ] 修复 f-string 错误
- [ ] 修复缩进错误
- [ ] 验证每个修复后的文件
- **Status:** in_progress

### Phase 3: 验证测试
- [ ] 运行 Python 语法检查
- [ ] 确保所有文件可编译
- [ ] 记录修复结果
- **Status:** pending

## Key Questions
1. 哪些文件有未闭合字符串？
2. 错误是原始代码问题还是生成时引入的？
3. 修复后是否需要重新运行 Oracle 检查？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 手动修复而非重新生成 | 错误简单，手动更快 |
| 保留原始文件备份 | 防止修复错误后可恢复 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| File not found | 1 | 检查路径正确性 |
```

#### findings.md

```markdown
# Findings: 语法错误修复

## Summary
发现 8 个文件有语法错误，主要为：
- 5 个未闭合 f-string
- 2 个未闭合普通字符串
- 1 个缩进错误

## Error Patterns

### Pattern 1: 未闭合 f-string
**症状**: `unterminated f-string literal`
**位置**: 多行 f-string 的最后一行未闭合
**修复**: 添加闭合引号

### Pattern 2: 未闭合普通字符串
**症状**: `unterminated string literal`
**位置**: 字符串跨行但未正确续行
**修复**: 使用括号或续行符

## Files Status
| File | Error Type | Status |
|------|------------|--------|
| dcf6ef... | 语法错误 | 待修复 |
| e2967e... | f-string | 待修复 |
```

#### progress.md

```markdown
# Progress: 语法错误修复

## Current Status
🔄 Phase 2: 修复实现 (3/8 文件已完成)

## Completed Tasks
- [x] 2026-02-22 10:00 - 识别所有 8 个错误文件
- [x] 2026-02-22 10:15 - 完成错误分类
- [x] 2026-02-22 10:30 - 修复文件 dcf6ef... (未闭合字符串)

## Next Tasks
- [ ] 修复 e2967e... (f-string 错误)
- [ ] 修复 65b563... (字符串错误)
- [ ] 验证所有修复后的文件

## Blockers
None

## Recent Updates
- 10:30 - 第一个文件修复完成，语法检查通过
- 10:15 - 完成错误分类，发现主要是字符串未闭合问题
- 10:00 - 开始分析 8 个错误文件
```

## 最佳实践

### DO (推荐做)

✅ **创建文件优先**: 任何复杂任务前先创建三个文件
✅ **及时更新**: 每完成一个阶段就更新状态
✅ **记录错误**: 所有错误都要记录，避免重复
✅ **定期回顾**: 每 10-15 个 tool calls 回顾一次计划
✅ **具体明确**: 任务描述要具体，避免模糊

### DON'T (避免做)

❌ **事后补录**: 不要等任务完成后才更新文件
❌ **忽略错误**: 不要觉得"小错误不用记"
❌ **阶段过大**: 每个阶段应该 2-5 分钟能完成
❌ **忘记回顾**: 不要一头扎进去忘记原始目标

## 会话恢复

如果上下文满了需要 `/clear`，使用 session-catchup 恢复：

```bash
# Linux/macOS
python3 ~/.claude/skills/planning-with-files/scripts/session-catchup.py "$(pwd)"
```

这个脚本会：
1. 检查之前的会话数据
2. 找到规划文件最后更新时间
3. 提取可能丢失的上下文
4. 生成同步报告

## 为什么这样做有效

1. **外部化记忆**: 将工作记忆外化到磁盘，不受上下文长度限制
2. **定期回顾**: 强制定期回顾目标，防止偏离
3. **错误预防**: 记录错误避免重复犯错
4. **决策记录**: 记录决策理由，防止遗忘
5. **进度可见**: 清晰的进度跟踪，防止迷失

## 相关技能

- `writing-plans` - 制定实施计划
- `executing-plans` - 执行制定的计划
- `subagent-driven-development` - 子代理驱动开发

---

**记住**: 这个技能的核心是"Work like Manus" - 用文件作为你的磁盘工作记忆。
