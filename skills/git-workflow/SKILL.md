---
name: git-workflow
description: Use when contributing to alexander-skills repository, developing new skills, or any git-based collaboration requiring branch, push, PR, or merge workflow. Alexander Qiu defaults to validated direct pushes to main; other contributors use feature branches and PRs.
license: MIT
---

# Git Workflow for alexander-skills

## Overview

Standardized git workflow for skill development. Ensures clean history, keeps main validated, and documents the owner direct-push exception.

**Core principle:** Validate before merging or pushing to shared branches. Use PRs for normal collaboration; use owner direct-push only for Alexander Qiu.

**Golden Rule:** Alexander Qiu (`ruizhi_qiu@foxmail.com`) defaults to validated direct pushes to `main`; everyone else uses feature branches and PRs unless explicitly authorized.

> **Note:** Repository owners have special privileges. See [references/owner-privileges.md](references/owner-privileges.md) for details.

---

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     START: New Task                              │
└───────────────────────────┬─────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  1. PREPARE                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ git status  │───▶│ git branch  │───▶│ owner/main or branch │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. DEVELOP                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ Make changes│───▶│ Test skill  │───▶│ git add + commit    │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. VALIDATE                                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  □ Skill loads without errors                               │ │
│  │  □ Tests pass                                               │ │
│  │  □ No secrets/API keys committed                            │ │
│  │  □ SKILL.md follows format                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. SUBMIT                                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ git push -u │───▶│ Create PR   │───▶│ Request review      │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. CLEANUP                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ git checkout│───▶│ git pull    │───▶│ git branch -d       │  │
│  │ main        │    │ origin main │    │ feature/xxx         │  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Guide

### Step 1: Check Current State

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"

# Check for uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  Uncommitted changes detected"
    git status -s
else
    echo "✅ Working directory clean"
fi
```

**Decision matrix:**

| Current State | Action |
|--------------|--------|
| On `main`, clean | Alexander Qiu may work directly after pulling latest; others create a feature branch |
| On `main`, dirty | Keep changes scoped and validate before commit; non-owner contributors move work to a branch |
| On feature branch, clean | Continue working |
| On feature branch, dirty | Continue working, commit when ready |

---

### Step 2: Create Feature Branch (standard contributors)

**Naming conventions:**

```
feat/<skill-name>              # New skill (e.g., feat/kimi-search)
fix/<skill-name>-<issue>       # Bug fix (e.g., fix/kimi-mem-cli-error)
docs/<what>                    # Documentation updates
update/<skill-name>            # Update existing skill
mcp/<server-name>              # MCP server development
refactor/<description>         # Code refactoring
```

**Commands:**

```bash
# Start from fresh main
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b feat/kimi-search

# Verify branch created
git branch -vv
```

---

### Step 3: Develop and Test

```bash
# Create skill structure
mkdir -p skills/<skill-name>
touch skills/<skill-name>/SKILL.md

# Edit SKILL.md following template
# ... edit content ...

# For MCP servers: test server starts
npm run dev
```

**MCP Development Checklist:**
- [ ] Server starts without errors
- [ ] Environment variables documented
- [ ] No hardcoded secrets
- [ ] Key functionality tested

---

### Step 4: Commit with Clear Messages

```bash
# Check what will be committed
git status
git diff --cached

# Stage specific files (preferred)
git add skills/kimi-search/SKILL.md

# Commit
git commit -m "Add kimi-search skill with vector memory support"
```

**Commit message format:**

| Good ✅ | Bad ❌ |
|---------|--------|
| `Add kimi-search skill with vector memory` | `update` |
| `Fix kimi-mem CLI error on empty input` | `fix bug` |
| `Update docs: add installation troubleshooting` | `doc update` |

---

### Step 5: Push and Create PR (standard contributors)

```bash
# Push branch to remote
git push -u origin feat/kimi-search

# Create PR via GitHub UI (link shown in push output)
```

**PR description template:**

```markdown
## Summary
Brief description of changes

## Changes
- [ ] New skill added
- [ ] Existing skill updated
- [ ] Bug fixed
- [ ] Documentation updated

## Testing
- [ ] Skill loads without errors
- [ ] No secrets committed
```

---

### Step 6: Post-Merge Cleanup

```bash
# Switch back to main
git checkout main

# Get latest changes
git pull origin main

# Delete local feature branch
git branch -d feat/kimi-search

# Verify clean state
git status
git branch -vv
```

---

## Quick Reference

### Essential Commands

| Task | Command |
|------|---------|
| Check status | `git status` |
| View branches | `git branch -vv` |
| Create & switch branch | `git checkout -b feature/name` |
| Stage changes | `git add filename` |
| Commit | `git commit -m "message"` |
| Push new branch | `git push -u origin feature/name` |
| Owner direct push | `git push origin main` |
| Update main | `git checkout main && git pull` |
| View log | `git log --oneline --graph -10` |

### Emergency Commands

| Situation | Command |
|-----------|---------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Unstage file | `git reset HEAD filename` |
| Discard file changes | `git checkout -- filename` |
| View diff | `git diff` |

---

## Red Flags

### 🚫 NEVER DO

| Forbidden | Why |
|-----------|-----|
| Non-owner `git push origin main` | Bypasses review and pollutes main branch |
| `git push --force` on shared branches | Destroys others' work |
| Commit secrets/API keys | Security breach |
| Ignore failing tests | Technical debt |

### ✅ ALWAYS DO

| Required | Why |
|----------|-----|
| Create feature branches | Isolates work, enables PR review |
| Write clear commit messages | Enables git archaeology |
| Test before pushing | Ensures quality |
| Use `.gitignore` for secrets | Prevents accidents |

---

## References

- [Owner Privileges](references/owner-privileges.md) - Special permissions for repo owners
- [Common Mistakes & Fixes](references/common-mistakes.md) - How to recover from git errors
- [AI Detection Script](references/ai-detection-script.md) - Automatic state detection
