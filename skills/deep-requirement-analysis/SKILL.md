---
name: deep-requirement-analysis
description: Use ONLY when user explicitly says "使用深度分析", "深度分析", "深度思考", "deep analysis", "系统分析", or "完整分析". Production-grade task planner that orchestrates brainstorming, multi-angle analysis, and execution planning.
---

# Deep Requirement Analysis - Production Task Planner

企业级任务规划器，结合头脑风暴、多角度技术分析和执行计划制定。采用渐进披露设计，根据任务复杂度自动选择分析深度。

## 核心设计理念

```
┌─────────────────────────────────────────────────────────────┐
│                    深度分析工作流                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  用户请求 ──→ 复杂度评估 ──→ 选择模式                        │
│                               │                             │
│              ┌────────────────┼────────────────┐            │
│              ▼                ▼                ▼            │
│         [快速模式]      [标准模式]        [深度模式]         │
│         5分钟/1-2问      完整5阶段          +原型验证         │
│              │                │                │            │
│              └────────────────┼────────────────┘            │
│                               ▼                             │
│                    调用 brainstorming                        │
│                               │                             │
│                               ▼                             │
│                    按需读取子代理模板                         │
│                               │                             │
│                               ▼                             │
│                         迭代式分析                           │
│                      (问→分析→再问)                          │
│                               │                             │
│                               ▼                             │
│                    调用 writing-plans                        │
│                               │                             │
│                               ▼                             │
│                         执行计划                             │
└─────────────────────────────────────────────────────────────┘
```

**本 Skill 的定位**：编排器（Orchestrator），不替代其他 skill，而是按序调用它们。

## 触发条件（强度分级）

### 普通分析 → Use brainstorming
**以下关键词触发 brainstorming，不走深度分析：**
- "分析一下"、"分析下"、"分析"
- "思考一下"、"思考下"
- "看看"、"看一下"
- "说说你的看法"
- "有什么想法"
- "怎么设计"
- "怎么做"

### 深度分析 → Use this skill  
**必须包含"强化修饰词"才算深度分析：**
- **"深度"** + 分析/思考/看一下（如"深度分析一下"、"深度思考"）
- **"仔细"** + 分析/思考/看一下（如"仔细分析一下"、"仔细看看"）
- **"认真"** + 分析/思考/看一下（如"认真分析一下"、"认真看看"）
- **"详细"** + 分析/思考/评估（如"详细分析"、"详细评估"）
- **"系统"** + 分析/思考（如"系统分析"）
- **"完整"** + 分析/方案（如"完整分析"）
- **"全面"** + 分析/评估（如"全面分析"）
- **"深入"** + 分析/研究（如"深入分析"）
- **"使用深度分析"**（显式调用）
- **"deep analysis"**、**"detailed analysis"**

### 判断逻辑
```
IF 请求匹配 "排除模式":
    → 调用 brainstorming
ELSE IF 请求包含 "强化修饰词" + "分析/思考":
    → 调用 deep-requirement-analysis
ELSE IF 请求只包含 "分析/思考/看":
    → 调用 brainstorming
```

### 排除模式（强制走 brainstorming）
即使包含强化修饰词，以下模式仍触发 brainstorming：

| 排除模式 | 示例 | 原因 |
|---------|------|------|
| **"看看...对不对/对吗"** | "仔细看看我写的对不对" | 代码审查/检查，非深度分析 |
| **"说说...问题/看法"** | "详细说说这个问题" | 讨论/解释，非系统分析 |
| **"回答...问题"** | "认真回答我的问题" | 问答模式，非分析任务 |
| **"读一下/看一下...代码"** | "认真看一下这段代码" | 代码阅读，非架构分析 |
| **"检查一下"** | "仔细检查一下配置" | 检查任务，非设计分析 |
| **"解释/说明一下"** | "详细解释一下原理" | 解释说明，非分析设计 |

**排除关键词**（即使前面有强化修饰词）：
- "对不对"、"对吗"、"是否正确" → 验证类请求
- "说说看"、"讲讲"、"聊一下" → 讨论类请求  
- "回答"、"回应" → 问答类请求
- "检查一下"、"核对一下" → 检查类请求
- "读一下"、"扫一眼" → 阅读类请求
- "解释一下"、"说明一下" → 解释类请求

**示例对比：**
| 用户输入 | 触发 Skill | 原因 |
|---------|-----------|------|
| "分析一下这个方案" | brainstorming | 无强化修饰词 |
| "深度分析一下这个方案" | deep-requirement-analysis | 有"深度"+"分析" |
| "思考一下怎么做" | brainstorming | 无强化修饰词 |
| "仔细思考一下" | deep-requirement-analysis | 有"仔细"+"思考" |
| "看一下这段代码" | brainstorming | 无强化修饰词 |
| "认真看一下这个问题" | deep-requirement-analysis | 有"认真"+"看"+"问题" |
| "说说你的想法" | brainstorming | 普通询问 |
| "详细分析下技术可行性" | deep-requirement-analysis | 有"详细"+"分析" |
| **"详细说说这个方案"** | **brainstorming** | **"说说"在排除列表** |
| **"仔细看看我写的对不对"** | **brainstorming** | **"对不对"触发排除** |
| **"认真回答我的问题"** | **brainstorming** | **"回答"触发排除** |
| **"详细解释一下原理"** | **brainstorming** | **"解释"触发排除** |

**DO NOT trigger on:**
- "帮我写...", "实现...", "创建一个..." → Use brainstorming
- "优化...", "修复..." → Use systematic-debugging

## 三层分析模式

根据任务复杂度选择：

### 快速模式 (Quick) - 5-10分钟

**适用**: 简单任务、时间敏感、已有明确方向
**流程**:
1. **智能问题生成** (1-2个关键问题)
2. **轻量分析** (读取 feasibility_agent 模板作为分析指引)
3. **快速计划** → 调用 writing-plans

**触发方式**:
- 用户明确说"快速分析"
- 或根据复杂度评估推荐（代码行数 < 100, 依赖 < 3）

### 标准模式 (Standard) - 15-30分钟

**适用**: 中等复杂度、需要多角度审视（默认模式）
**流程**:
1. **调用 brainstorming** (创意探索)
2. **按需读取子代理模板** (作为分析检查清单)
3. **关键问题确认** (3-5个)
4. **执行计划** → 调用 writing-plans

**触发方式**:
- 默认模式
- 用户说"标准分析"或未指定模式

### 深度模式 (Deep) - 30-60分钟

**适用**: 复杂系统、高风险、需要技术验证
**流程**:
1. **调用 brainstorming** (完整探索)
2. **读取全部相关子代理模板**
3. **技术验证** (搜索文档/读取源码验证关键声明)
4. **关键问题确认** (5-8个)
5. **深度执行计划** → 调用 writing-plans

**触发方式**:
- 用户明确说"深度分析"或"完整分析"
- 或根据复杂度评估推荐（代码行数 > 1000, 涉及架构变更）

## 执行流程详解

### Phase 0: 复杂度评估

**目的**: 帮助用户选择合适的分析模式

**执行方式**:
```
1. 读取 scripts/complexity_assessor.py 的评估逻辑作为参考
2. 基于任务描述进行启发式评估
3. 向用户推荐合适的模式
4. 等待用户确认
```

**复杂度评估参考标准**:
| 指标 | 低 (快速) | 中 (标准) | 高 (深度) |
|------|-----------|-----------|-----------|
| 代码规模 | < 100行 | 100-1000行 | > 1000行 |
| 依赖数量 | < 3个 | 3-10个 | > 10个 |
| 架构影响 | 无 | 模块级 | 系统级 |
| 技术风险 | 低 | 中 | 高 |

### Phase 1: 动态问题生成

**目的**: 收集关键上下文，而非固定问题列表

**执行方式**:
```
1. 基于任务类型和模式，生成最相关的 1-5 个问题
2. 每个问题提供选项或开放式回答
3. 根据用户回答，动态调整后续问题
4. 终止条件：已获得足够信息进入下一阶段
```

**示例**:
```
基于您的需求【设计用户认证API】：

【关键问题 1/2】
使用什么认证机制？
- A: JWT (推荐：无状态，适合分布式)
- B: Session (传统方式，需要存储)
- C: OAuth2 (第三方集成场景)

【关键问题 2/2】
预期的并发量是多少？
- A: < 100 QPS
- B: 100-1000 QPS
- C: > 1000 QPS
```

### Phase 2: 调用 Brainstorming

**目的**: 进行创意探索，产出设计方案

**执行方式**:
```
1. 读取 /skills/brainstorming/SKILL.md
2. 按照其中的流程执行：
   - Explore project context
   - Ask clarifying questions  
   - Propose 2-3 approaches
   - Present design
3. 获取输出：design.md
4. 返回本 skill 继续执行
```

**注意**: Brainstorming 是本 skill 的前置步骤，不是替代关系。

### Phase 3: 按需读取子代理模板

**目的**: 从多角度审视技术可行性

**执行方式**:
```
1. 根据任务类型和模式，选择需要加载的子代理模板
2. 从 references/agents/ 目录读取对应的 .md 文件
3. 使用模板中的"Analysis Dimensions"作为检查清单
4. 模拟子代理视角进行分析（而非真正派遣子代理）
```

**子代理模板清单** (位于 references/agents/):
```
references/agents/
├── technical/
│   ├── feasibility_agent.md      # 可行性分析
│   ├── security_agent.md         # 安全分析
│   └── performance_agent.md      # 性能分析
├── business/
│   ├── cost_agent.md             # 成本分析
│   └── risk_agent.md             # 风险分析
└── implementation/
    ├── architecture_agent.md     # 架构设计
    ├── testing_agent.md          # 测试策略
    └── deployment_agent.md       # 部署方案
```

**参考文档：**
- `references/analysis-patterns.md` - 常见分析模式参考
- `references/question-bank.md` - 问题库模板
- `references/cases/` - 典型案例（快速模式/标准模式）

**按需加载策略**:
- **快速模式**: 仅 feasibility_agent
- **标准模式**: feasibility_agent + 相关领域 agent（如涉及安全则加 security_agent）
- **深度模式**: 全部相关 agents

### Phase 4: 迭代式分析

**目的**: 逐步深入，而非一次性完成所有分析

**执行方式**:
```
Iteration 1:
  基于已有信息 → 初步分析 → 识别知识缺口 → 生成追问

Iteration 2 (如有需要):
  追问 → 深入分析 → 发现技术风险 → 生成新的追问

Iteration 3 (如有需要):
  再问 → 完善分析 → 形成结论

终止条件:
  - 用户说"够了，进入下一阶段"
  - 达到最大迭代次数（快速:1, 标准:2, 深度:3）
  - 分析已收敛（无新知识增益）
```

### Phase 5: 调用 Writing-Plans

**目的**: 将分析结果转化为可执行的计划

**执行方式**:
```
1. 整理本 skill 的输出物：
   - design.md (from brainstorming)
   - 技术分析结果
   - 风险评估
   - 关键决策

2. 读取 /skills/writing-plans/SKILL.md
3. 将上述输出作为输入，调用 writing-plans
4. 生成 implementation-plan.md
```

## 输出物规范

### 快速模式
```
output/
├── quick-analysis.md          # 快速分析报告
├── key-decisions.md           # 关键决策
└── implementation-plan.md     # 执行计划 (from writing-plans)
```

### 标准模式
```
output/
├── design.md                  # 设计文档 (from brainstorming)
├── analysis-report.md         # 分析报告
├── risk-assessment.md         # 风险评估
├── key-decisions.md           # 关键决策
└── implementation-plan.md     # 执行计划
```

### 深度模式
```
output/
├── design.md                  # 设计文档
├── analysis-report.md         # 完整分析报告
├── technical-verification.md  # 技术验证报告
├── risk-assessment.md         # 风险评估
├── architecture-review.md     # 架构评审
├── key-decisions.md           # 关键决策
└── implementation-plan.md     # 详细执行计划
```

## 关键设计原则

### 1. 渐进披露
- 不一次性展示所有信息
- 根据用户反馈逐步深入
- 用户可随时说"够了"进入下一阶段

### 2. 按需加载
- 不读取所有子代理模板
- 根据任务类型和复杂度选择必要的模板
- 保持上下文精简

### 3. 技能编排
- 不替代 brainstorming 和 writing-plans
- 明确调用它们并传递上下文
- 每个 skill 做自己擅长的事

### 4. 用户确认点
以下节点必须获得用户确认：
- 分析模式选择（Phase 0 后）
- 关键决策（Phase 4 后）
- 执行计划（Phase 5 后）

## Anti-Patterns

❌ **Don't**: 未经用户确认自动选择深度模式
❌ **Don't**: 读取所有子代理模板（只读必要的）
❌ **Don't**: 跳过 brainstorming 直接进入分析
❌ **Don't**: 一次性问完所有问题（违反渐进披露）
❌ **Don't**: 不与 writing-plans 对接直接输出计划

✅ **Do**: 让用户选择或确认分析模式
✅ **Do**: 按需读取子代理模板
✅ **Do**: 必须调用 brainstorming 进行创意探索
✅ **Do**: 迭代式提问，根据回答调整
✅ **Do**: 最终调用 writing-plans 生成执行计划

## 使用示例

### 示例 1: API 设计（快速模式）

**用户**: "使用深度分析，帮我设计一个用户认证的 API"

**Agent**:
```
我将对您的需求进行深度分析。

【复杂度评估】
任务类型: API 设计
预估规模: 小型（标准 CRUD 操作）

建议使用【快速模式】进行分析：
- 预计时间: 5-10 分钟
- 包含: 2 个关键问题 + 可行性分析 + 执行计划

确认开始？[Y/n]: Y

【关键问题 1/2】
使用什么认证机制？
- A: JWT (无状态，适合分布式)
- B: Session (有状态，传统方式)
- C: OAuth2 (第三方集成)

用户: A

【关键问题 2/2】
需要支持多设备同时登录吗？
- A: 是
- B: 否

用户: A

[调用 brainstorming...]
[读取 feasibility_agent 模板...]
[调用 writing-plans...]

✅ 分析完成！

输出物:
- quick-analysis.md: 包含 API 接口定义
- implementation-plan.md: 2 小时开发计划
```

### 示例 2: 微服务拆分（标准模式）

**用户**: "深度分析单体应用如何拆分为微服务"

**Agent**:
```
【复杂度评估】
任务类型: 架构重构
预估规模: 大型（涉及多个模块）
风险级别: 高

建议使用【标准模式】进行分析：
- 预计时间: 20-30 分钟
- 包含: 头脑风暴 + 多角度分析 + 执行计划

确认开始？[Y/n]: Y

[开始执行标准模式流程...]
```

## 部署前检查清单

- [ ] references/agents/ 目录存在且包含子代理模板
- [ ] scripts/ 目录存在且脚本可执行
- [ ] tests/ 目录存在且包含对应测试（每个脚本至少一个测试）
- [ ] references/cases/ 目录存在且包含示例
- [ ] 运行 `pytest tests/` 所有测试通过
- [ ] 测试过快速模式的完整流程
- [ ] 测试过标准模式的完整流程
- [ ] 确认与 brainstorming skill 的集成正常
- [ ] 确认与 writing-plans skill 的集成正常

## 版本信息

- **Version**: v2.2 - Production Ready
- **Last Updated**: 2024-02-19
- **Changelog**:
  - v2.2: 修复目录结构规范 - 移动 agents/ 到 references/agents/，添加 tests/ 目录，修复脚本权限，添加"深度思考"触发词
  - v2.1: 修复 Phase 编号重复，明确执行语义，添加部署检查清单
  - v2.0: 重大重构 - 显式触发、三层模式、渐进披露、子代理模板库
  - v1.0: 初始版本 - 固定5阶段流程
