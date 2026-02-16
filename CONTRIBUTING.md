# Contributing to alexander-skills

Thank you for your interest in contributing! This document outlines the development workflow.

## 🚀 Quick Start

1. **Fork the repository** (if external contributor)
2. **Clone locally**
3. **Create feature branch**: `git checkout -b feature/my-skill`
4. **Make changes and test**
5. **Commit with clear message**
6. **Push and create PR**

## 📋 Development Workflow

### Branch Naming

| Prefix | Use For | Example |
|--------|---------|---------|
| `feature/` | New skills | `feature/kimi-search` |
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

Before submitting PR:

- [ ] Skill loads without errors
- [ ] If TypeScript: `npm run build` succeeds
- [ ] Basic functionality tested
- [ ] Documentation is clear

**For kimi-mem type skills:**
```bash
cd my-skill
npm install
npm run build
node dist/cli/index.js --help
```

## 📁 Skill Structure

```
skill-name/
├── SKILL.md              # Required: Main skill definition
├── package.json          # If Node.js based
├── tsconfig.json         # If TypeScript
├── README.md             # Optional: Additional docs
├── src/                  # Source code
├── docs/                 # Additional documentation
└── examples/             # Example usage
```

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

以下用户可以直接 push 到 `main` 分支，**但必须遵循以下规则**：

- **Alexander Qiu** (仓库所有者)

**⚠️ 直接 Push 规则：**
1. 变更必须已经过**充分验证**（测试通过、功能正常）
2. 仅限文档更新、README 修改、小的配置调整
3. 代码变更、新功能添加必须使用 PR 流程
4. 如果变更可能影响他人，即使小改动也建议使用 PR

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

**高风险变更必须通过 PR：**
- 新 skill 添加
- API 接口变更
- 依赖版本升级
- 重构核心代码
- 配置/构建流程修改

### Step-by-Step

#### 标准 PR 流程

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create branch
git checkout -b feature/my-skill

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
git push -u origin feature/my-skill

# 7. Create PR on GitHub
# ... describe changes ...
# ... 确保 checklist 已勾选 ...

# 8. After merge, cleanup
git checkout main
git pull origin main
git branch -d feature/my-skill
```

#### 验证过的用户直接 Push 流程

```bash
# 仅适用于小改动且已充分验证的情况
git checkout main
git pull origin main

# 创建临时分支（即使直接 push，也先创建分支做验证）
git checkout -b docs/quick-fix
# ... 编辑 ...
# ... 本地验证 ...
git commit -m "docs: Quick fix"

# 合并到 main 并推送
git checkout main
git merge docs/quick-fix
git push origin main

# 清理
git branch -d docs/quick-fix
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
