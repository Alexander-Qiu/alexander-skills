# Contributing to alexander-skills

Thank you for your interest in contributing! This document outlines the development workflow.

## 🚀 Quick Start

1. **Fork the repository** (if external contributor)
2. **Clone locally**
3. **Create feature branch**: `git checkout -b feat/my-skill`
4. **Make changes and test**
5. **Commit with clear message**
6. **Push and create PR**

## 📋 Development Workflow

### Branch Naming

| Prefix | Use For | Example |
|--------|---------|---------|
| `feat/` | New skills | `feat/kimi-search` |
| `fix/` | Bug fixes | `fix/kimi-mem-error` |
| `docs/` | Documentation | `docs/install-guide` |
| `update/` | Updates to existing | `update/kimi-mem-v2` |

### Commit Messages

**Format:**
```
<type>: <short summary>

<optional body>
- Detail 1
- Detail 2
```

**Types:**
- `feat:` New skill or feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

**Examples:**
```
feat: Add kimi-search skill with vector search

- Implement SQLite + Chroma hybrid search
- Add CLI tool for manual operations
- Include comprehensive SKILL.md

fix: Resolve ES Module compatibility in kimi-mem

- Replace require() with ES imports
- Fix TypeScript strict null checks
```

## 🧪 Testing Requirements

### Pre-Testing: Brainstorm Test Points

**Before running full validation, use the `brainstorming` skill to identify test points:**

```bash
# Activate brainstorming mode
/skill:brainstorming

# Then think through:
# 1. What are the core functionalities of this skill?
# 2. What could go wrong at each step?
# 3. What are the edge cases?
# 4. How should it behave in error conditions?
```

**Document test points in**: `skills/<skill-name>/TEST_BRAINSTORM.md`

This helps ensure comprehensive testing coverage before running automated tests.

### Quick Validation (All Skills)

Before submitting PR, run automated validation:

```bash
# Structure validation (Level 1)
python skills/skill-validation/scripts/validate_structure.py skills/<skill-name>/

# Unit tests (Level 2) - if skill has scripts/
python skills/skill-validation/scripts/run_skill_tests.py skills/<skill-name>/ --coverage

# Compatibility check (Level 3)
python skills/skill-validation/scripts/check_compatibility.py skills/<skill-name>/

# Full validation suite
python skills/skill-validation/scripts/validate_skill.py skills/<skill-name>/ --full
```

### Pre-PR Checklist

**For all skills:**
- [ ] Level 1: Structure validation passing
- [ ] Level 2: Unit tests passing (if scripts exist)
- [ ] Kimi loads without errors (smoke test)
- [ ] Documentation is complete

**For Node.js skills (like kimi-mem):**
```bash
cd my-skill
npm install
npm run build
npm test                    # If tests exist
node dist/cli/index.js --help
```

### Multi-Agent Testing (Required Before Release)

**⚠️ CRITICAL:** All skills must be tested in BOTH agents before release:

| Agent | Test Type | Required Evidence |
|-------|-----------|-------------------|
| **Kimi** | Integration | Test report from template |
| **Claude** | Integration | Test report from template |

See `skills/skill-validation/templates/` for test report templates.

### Complete Validation Levels

See `/skill:skill-validation` for full validation framework details.

| Level | Name | Automated | Required For |
|-------|------|-----------|--------------|
| 1 | Structure | ✅ | All PRs |
| 2 | Unit Tests | ✅ | Skills with scripts |
| 3 | Compatibility | ✅ | All PRs |
| 4 | Kimi Integration | 👤 Manual | Release |
| 5 | Claude Integration | 👤 Manual | Release |
| 6 | E2E Scenarios | 👤 Manual | Complex skills |

## 📁 Skill Structure

```
skill-name/
├── SKILL.md              # Required: Main skill definition
├── package.json          # If Node.js based
├── tsconfig.json         # If TypeScript
├── src/                  # Source code
├── scripts/              # Executable scripts (Python/Bash)
│   ├── helper.py
│   └── utils.sh
├── tests/                # Unit tests (REQUIRED if scripts/ exists)
│   ├── test_helper.py
│   └── conftest.py
├── references/           # Reference documentation
│   └── api-docs.md
├── assets/               # Templates, images, etc.
│   └── template.docx
└── examples/             # Example usage
```

**Testing Requirements:**
- If `scripts/` exists, `tests/` MUST exist with ≥1 test per script
- Tests must be runnable with `pytest tests/`
- Coverage should be ≥80% for scripts

### SKILL.md Template

```markdown
---
name: skill-name
description: Use when [specific conditions]
---

# Skill Name

## Overview
One sentence description.

## When to Use
- Condition 1
- Condition 2

## Usage
### Method 1
Steps...

### Method 2
Steps...

## Examples
```bash
# Example command
```

## Notes
Additional information.
```

## 🔄 Git Workflow

### Direct Push to Main (验证过的用户)

以下用户可以直接 push 到 `main` 分支，**默认推送目标也是 `main`**，但必须遵循以下规则：

- **Alexander Qiu** (`ruizhi_qiu@foxmail.com`, 仓库所有者)

**⚠️ 直接 Push 规则：**
1. 变更必须已经过**充分验证**（测试通过、功能正常）
2. Alexander Qiu 的默认流程是本地验证后直接推送到 `main`
3. 外部贡献者、非 owner agent、或需要 review 的高风险变更使用 PR 流程
4. 如果变更可能影响他人，即使 owner 直推也必须先完成本地验证并保持提交范围单一

**🔀 Alexander Qiu 本地合并特权：**

作为仓库所有者，Alexander Qiu 可以执行以下操作：

1. **本地批量合并**：在本地将多个已充分验证的 feature 分支合并到 main
2. **直接推送到 remote main**：合并完成后直接 `git push origin main`

**前提条件：**
- 每个 feature 分支都**已通过所有验证**（Level 1-6，如适用）
- 合并前在本地再次验证 main 分支功能正常
- 合并后确保 `git status` 显示 working tree clean
- 推送后立即检查 remote main 状态正常

**推荐流程：**
```bash
# 1. 确保本地 main 最新
git checkout main
git pull origin main

# 2. 依次合并已验证的 feature 分支
git merge feat/skill-a  # 已验证的分支 A
git merge fix/skill-b      # 已验证的分支 B
git merge docs/update-c    # 已验证的分支 C

# 3. 最终验证
npm run build  # 如有构建步骤
npm test       # 如有测试

# 4. 推送到 remote
git push origin main

# 5. 清理本地已合并的分支
git branch -d feat/skill-a
git branch -d fix/skill-b
git branch -d docs/update-c
```

### 标准工作流程（推荐）

**DO:**
- Create feature branches from main
- Pull latest before starting work
- Write clear commit messages
- Test before pushing
- One logical change per commit
- **充分验证后再合并到 main 或发布分支**

**DON'T:**
- Push broken/untested code directly to main
- Mix unrelated changes
- Force push to shared branches
- **跳过验证直接合并到发布分支**

### 合并到 Main/发布分支的要求

任何合并到 `main` 或发布分支（如 `release/*`）的代码必须满足：

- [ ] **功能验证** - 核心功能已测试并正常工作
- [ ] **构建通过** - `npm run build` 无错误（如适用）
- [ ] **文档更新** - SKILL.md 和相关文档已同步更新
- [ ] **兼容性检查** - 不破坏现有 skills 的兼容性
- [ ] **Self-Review** - 作者已自行 review 代码

**高风险变更默认通过 PR；Alexander Qiu 可在充分验证后直接推送到 `main`：**
- 新 skill 添加
- API 接口变更
- 依赖版本升级
- 重构核心代码
- 配置/构建流程修改

### Step-by-Step

#### Alexander Qiu 直接推送流程（默认）

作为仓库所有者，**默认推送行为是直接推送到 `main`**，无需创建 PR。

```bash
# 1. 确保本地 main 最新
git checkout main
git pull origin main

# 2. 如果是新功能，创建临时分支开发（可选但推荐）
git checkout -b feat/my-skill
# ... 编辑代码 ...
# ... 本地验证 ...

# 3. 直接在 main 上合并或直接在 main 上开发
git checkout main
git merge feat/my-skill  # 如果有临时分支

# 4. 最终验证
npm run build
npm test

# 5. 直接推送到 remote main（默认行为）
git push origin main

# 6. 清理临时分支
git branch -d feat/my-skill
```

#### 标准 PR 流程（外部贡献者或需要 review 时）

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create branch
git checkout -b feat/my-skill

# 3. Make changes
# ... edit files ...

# 4. 本地验证（必须）
npm run build        # 如果有构建步骤
npm test             # 如果有测试
# 手动测试核心功能

# 5. Commit
git add .
git commit -m "feat: Add my-skill with X feature"

# 6. Push
git push -u origin feat/my-skill

# 7. Create PR on GitHub
# ... describe changes ...
# ... 确保 checklist 已勾选 ...

# 8. After merge, cleanup
git checkout main
git pull origin main
git branch -d feat/my-skill
```

#### Alexander Qiu 批量合并流程（多个已验证分支）

当有多个已经充分验证的 feature 分支需要合并时：

```bash
# 1. 确保本地 main 最新
git checkout main
git pull origin main

# 2. 依次合并已验证的 feature 分支
git merge feat/skill-a  # 已验证的分支 A
git merge fix/skill-b      # 已验证的分支 B
git merge docs/update-c    # 已验证的分支 C

# 3. 最终验证
npm run build
npm test

# 4. 直接推送到 remote main
git push origin main

# 5. 清理已合并的本地分支
git branch -d feat/skill-a
git branch -d fix/skill-b
git branch -d docs/update-c
```

## 📝 Code Style

### TypeScript/JavaScript
- Use TypeScript for complex skills
- ESLint/Prettier if applicable
- ES Modules (`import`/`export`)

### Documentation
- Clear, concise language
- Code examples for complex usage
- Troubleshooting section if needed

## 🐛 Reporting Issues

Include:
1. What you were trying to do
2. What happened
3. Steps to reproduce
4. Environment (OS, Node version)
5. Error messages

## 💡 Skill Ideas

Looking for contributions:
- [ ] Code review assistant
- [ ] Testing workflow
- [ ] Documentation generator
- [ ] API design helper
- [ ] Database migration tool

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## ❓ Questions?

- Open an issue for discussion
- Check existing skills for examples
- Review SKILL.md in `skills/git-workflow/` for detailed git workflow
