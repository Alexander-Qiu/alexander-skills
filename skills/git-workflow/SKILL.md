---
name: git-workflow
description: Use when contributing to alexander-skills repository or any skill development work that requires git version control
---

# Git Workflow for alexander-skills

## Overview

Standardized git workflow for skill development. Prevents messy history and broken main branch.

**Core principle:** Feature branches + PR review = clean history + quality code.

## When to Use

- Adding new skills
- Modifying existing skills
- Fixing bugs in skills
- Updating documentation

## The Workflow

### Step 1: Start from Fresh Main

```bash
# Ensure you're on main
git checkout main

# Get latest
git pull origin main
```

**If you have uncommitted changes:**
```bash
# Option A: Stash them
git stash

# Option B: Commit to current branch first
git add .
git commit -m "WIP: current work"
```

### Step 2: Create Feature Branch

**Naming convention:**
```
feature/<skill-name>          # New skill
fix/<skill-name>-<issue>      # Bug fix
docs/<what>                   # Documentation
update/<skill-name>           # Update existing
```

**Examples:**
```bash
git checkout -b feature/kimi-search
git checkout -b fix/kimi-mem-cli-error
git checkout -b docs/install-guide
```

### Step 3: Make Changes

**Do:**
- One logical change per commit
- Clear, descriptive commit messages
- Test before committing

**Don't:**
- Mix unrelated changes
- Commit broken code
- Use vague messages like "fix" or "update"

### Step 4: Commit

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Add kimi-search skill with vector search support

- Implement SQLite + Chroma hybrid search
- Add CLI tool for manual operations
- Include comprehensive SKILL.md"
```

**Commit message format:**
```
<short summary>

<optional longer description>
- Bullet points for details
- What changed and why
```

### Step 5: Push and Create PR

```bash
# Push branch
git push -u origin feature/name
```

**Create PR with:**
- Clear title
- Description of changes
- Testing done
- Screenshots if applicable

### Step 6: Review and Merge

**Self-review checklist:**
- [ ] Code builds without errors
- [ ] Skill loads correctly
- [ ] Documentation updated
- [ ] No sensitive data committed

**After merge:**
```bash
git checkout main
git pull origin main

# Optional: Delete local branch
git branch -d feature/name
```

## Emergency Fixes

### Oops, committed to main directly

```bash
# If not pushed yet
git reset --soft HEAD~1
git stash
git checkout -b fix/emergency

# If already pushed - DON'T FORCE PUSH
# Create revert commit instead
git revert HEAD
git push origin main
```

### Oops, wrong files committed

```bash
# Unstage files
git reset HEAD <file>

# Or undo last commit keeping changes
git reset --soft HEAD~1
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `git status` | See current state |
| `git branch` | List branches |
| `git log --oneline` | View commit history |
| `git diff` | See unstaged changes |
| `git stash` | Temporarily save changes |
| `git stash pop` | Restore stashed changes |

## Red Flags

**Never:**
- Push directly to main
- Commit without testing
- Use `git push --force` on shared branches
- Mix unrelated changes in one commit
- Commit secrets or sensitive data

**Always:**
- Create feature branches
- Write clear commit messages
- Test before pushing
- Pull latest main before starting work
