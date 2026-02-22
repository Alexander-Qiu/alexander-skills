# Planning with Files - 测试点头脑风暴

## 测试目标
确保 planning-with-files 技能在 Kimi 和 Claude 中都能正常工作。

## 1. 结构验证测试 (Level 1)

### 1.1 必需文件存在性
- [ ] SKILL.md 存在且不为空
- [ ] templates/task_plan.md 存在
- [ ] templates/findings.md 存在
- [ ] templates/progress.md 存在
- [ ] 所有模板文件都有有效的 Markdown 格式

### 1.2 可选文件完整性
- [ ] examples.md 存在（帮助用户理解用法）
- [ ] reference.md 存在（详细参考文档）
- [ ] USAGE_GUIDE.md 存在（使用指南）
- [ ] scripts/ 目录存在（辅助脚本）

### 1.3 元数据验证
- [ ] SKILL.md 包含有效的 YAML frontmatter
- [ ] name 字段不为空
- [ ] version 字段格式正确
- [ ] description 字段不为空

## 2. 内容质量测试

### 2.1 模板完整性
- [ ] task_plan.md 包含所有必需部分（Goal, Current Phase, Phases, Key Questions, Decisions Made, Errors Encountered）
- [ ] findings.md 包含所有必需部分（Summary, Code Patterns, Error Patterns, Architecture Notes）
- [ ] progress.md 包含所有必需部分（Current Status, Completed Tasks, Next Tasks, Blockers, Recent Updates）
- [ ] 所有模板都有清晰的注释说明

### 2.2 文档完整性
- [ ] SKILL.md 清晰说明技能用途
- [ ] SKILL.md 包含使用时机说明
- [ ] SKILL.md 包含使用步骤
- [ ] USAGE_GUIDE.md 包含实际示例
- [ ] USAGE_GUIDE.md 包含最佳实践

### 2.3 示例有效性
- [ ] examples.md 中的示例完整可用
- [ ] 示例覆盖不同场景（简单任务、复杂任务、研究项目）

## 3. 脚本功能测试 (Level 2)

### 3.1 脚本可执行性
- [ ] scripts/session-catchup.py 可执行（有 shebang 且权限正确）
- [ ] scripts/check-complete.sh 语法正确
- [ ] scripts/init-session.sh 语法正确

### 3.2 脚本功能验证
- [ ] session-catchup.py 能在正确路径下运行
- [ ] check-complete.sh 能正确检测任务完成状态
- [ ] init-session.sh 能正确初始化会话

### 3.3 跨平台兼容性
- [ ] 脚本在 Linux 下正常工作
- [ ] 脚本在 macOS 下正常工作（如适用）
- [ ] 有 Windows PowerShell 版本（check-complete.ps1, init-session.ps1）

## 4. 集成测试 (Level 3-4)

### 4.1 Kimi 集成测试
- [ ] Kimi 能正确读取 SKILL.md
- [ ] Kimi 能识别 skill 的触发条件
- [ ] Kimi 能使用模板创建文件
- [ ] Kimi 能根据模板指导用户完成规划

### 4.2 Claude 集成测试
- [ ] Claude 能正确读取 SKILL.md
- [ ] Claude 能识别 skill 的触发条件
- [ ] Claude 能使用模板创建文件
- [ ] Claude 能根据模板指导用户完成规划

### 4.3 Hooks 功能测试
- [ ] PreToolUse hook 能正确显示 task_plan.md
- [ ] PostToolUse hook 能正确提示更新状态
- [ ] Stop hook 能正确运行 check-complete 脚本

## 5. 实际使用流程测试

### 5.1 简单任务场景
- [ ] 创建一个简单任务（<10 steps）
- [ ] 使用 task_plan.md 规划
- [ ] 完成所有阶段并更新 progress.md
- [ ] 验证流程顺畅

### 5.2 复杂任务场景
- [ ] 创建一个复杂任务（>50 steps）
- [ ] 使用所有三个文件协同工作
- [ ] 测试会话恢复功能（模拟 /clear）
- [ ] 验证不会遗忘原始目标

### 5.3 错误处理场景
- [ ] 测试文件不存在时的行为
- [ ] 测试权限错误时的行为
- [ ] 测试格式错误时的行为

## 6. 边界情况测试

### 6.1 空内容处理
- [ ] 空 task_plan.md 的处理
- [ ] 空 findings.md 的处理
- [ ] 空 progress.md 的处理

### 6.2 超长内容处理
- [ ] 超长的 phases 列表
- [ ] 超长的 errors 列表
- [ ] 超长的 notes 内容

### 6.3 特殊字符处理
- [ ] 文件名包含特殊字符
- [ ] 内容包含特殊字符（emoji、Unicode）
- [ ] 内容包含代码块

## 7. 性能测试

### 7.1 大文件处理
- [ ] 处理 1MB+ 的 findings.md
- [ ] 处理 1000+ 行的 task_plan.md

### 7.2 并发处理
- [ ] 多个项目同时使用该技能
- [ ] 快速切换不同项目

## 8. 用户体验测试

### 8.1 易用性
- [ ] 新手能理解如何使用
- [ ] 模板填写有明确指导
- [ ] 注释清晰有用

### 8.2 实用性
- [ ] 实际使用后确实能防止遗忘目标
- [ ] 错误记录确实能防止重复犯错
- [ ] 进度跟踪确实有帮助

## 测试优先级

| 优先级 | 测试项 | 原因 |
|--------|--------|------|
| P0 | 结构验证测试 | 基础要求，必须满足 |
| P0 | 内容质量测试 | 基础要求，必须满足 |
| P1 | Kimi/Claude 集成测试 | 核心功能 |
| P1 | 实际使用流程测试 | 验证可用性 |
| P2 | 脚本功能测试 | 有 scripts 目录需要测试 |
| P2 | 边界情况测试 | 健壮性 |
| P3 | 性能测试 | 优化项 |
| P3 | 用户体验测试 | 主观评估 |

## 测试执行计划

1. **第一阶段**: 运行自动化验证脚本（Level 1-3）
2. **第二阶段**: Kimi 集成测试（手动）
3. **第三阶段**: Claude 集成测试（手动）
4. **第四阶段**: 实际使用流程测试（手动）
5. **第五阶段**: 边界情况测试
