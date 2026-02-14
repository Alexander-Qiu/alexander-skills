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

**DO:**
- Create feature branches from main
- Pull latest before starting work
- Write clear commit messages
- Test before pushing
- One logical change per commit

**DON'T:**
- Push directly to main
- Commit broken code
- Mix unrelated changes
- Force push to shared branches

### Step-by-Step

```bash
# 1. Start from main
git checkout main
git pull origin main

# 2. Create branch
git checkout -b feature/my-skill

# 3. Make changes
# ... edit files ...

# 4. Commit
git add .
git commit -m "feat: Add my-skill with X feature"

# 5. Push
git push -u origin feature/my-skill

# 6. Create PR on GitHub
# ... describe changes ...

# 7. After merge, cleanup
git checkout main
git pull origin main
git branch -d feature/my-skill
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
