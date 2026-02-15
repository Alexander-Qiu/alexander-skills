---
name: git-workflow
description: Use when contributing to alexander-skills repository, developing new skills, or any git-based collaboration requiring feature branches and PR workflow
---

# Git Workflow for alexander-skills

## Overview

Standardized git workflow for skill development in alexander-skills repository. Ensures clean history, prevents main branch pollution, and maintains code quality through mandatory PR review.

**Core principle:** Feature branches + mandatory PR review = clean history + quality code + zero main branch incidents.

**Golden Rule:** 🚫 **NEVER push directly to main branch** 🚫

---

## When to Use

- Adding new skills to alexander-skills repository
- Modifying existing skill implementations
- Fixing bugs in deployed skills
- Updating skill documentation or metadata
- Creating or updating MCP servers
- Any collaborative git-based development

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
│  │ git status  │───▶│ git branch  │───▶│ Ensure: NOT on main │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│                                           │ on main?             │
│                              ┌────────────┴────────────┐         │
│                              ▼                         ▼         │
│                    ┌─────────────────┐      ┌─────────────────┐  │
│                    │ Stay on branch  │      │ git checkout    │  │
│                    │ (good to go)    │      │ -b feature/xxx  │  │
│                    └─────────────────┘      └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. DEVELOP                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ Make changes│───▶│ Test skill  │───▶│ git add <files>     │  │
│  │ in SKILL.md │    │ mcp dev     │    │ git commit -m ""    │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. VALIDATE                                                     │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Pre-Push Checklist:                                        │ │
│  │  □ Skill loads without errors                               │ │
│  │  □ Tests pass (if applicable)                               │ │
│  │  □ No secrets/API keys committed                            │ │
│  │  □ SKILL.md follows format                                  │ │
│  │  □ Commit messages are descriptive                          │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. SUBMIT                                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ git push -u │───▶│ Create PR   │───▶│ Request review      │  │
│  │ origin feat │    │ on GitHub   │    │ & merge             │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. CLEANUP                                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ git checkout│───▶│ git pull    │───▶│ git branch -d       │  │
│  │ main        │    │ origin main │    │ feature/xxx         │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Step-by-Step Guide

### Step 1: Check Current State

**AI detects current state automatically:**

```bash
# Check current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if on main
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
| On `main`, clean | Create new feature branch: `git checkout -b feature/xxx` |
| On `main`, dirty | Stash or commit, then create branch |
| On feature branch, clean | Continue working |
| On feature branch, dirty | Continue working, commit when ready |

---

### Step 2: Create Feature Branch

**Naming conventions for alexander-skills:**

```
skill/<skill-name>              # New skill (e.g., skill/kimi-search)
fix/<skill-name>-<issue>        # Bug fix (e.g., fix/kimi-mem-cli-error)
docs/<what>                     # Documentation updates
update/<skill-name>             # Update existing skill
mcp/<server-name>               # MCP server development
refactor/<description>          # Code refactoring
```

**Commands:**

```bash
# Start from fresh main
git checkout main
git pull origin main

# Create and switch to feature branch
git checkout -b skill/kimi-search

# Verify branch created
git branch -vv
```

---

### Step 3: Develop and Test

**Skill development workflow:**

```bash
# 1. Create skill structure
mkdir -p skills/<skill-name>
touch skills/<skill-name>/SKILL.md

# 2. Edit SKILL.md following template
# ... edit content ...

# 3. Test skill loading (if applicable)
# For MCP servers:
cd servers/<server-name> && npm run dev

# For skills - validate markdown structure
# Ensure: Frontmatter, Overview, When to Use, Step-by-Step
```

**MCP Server Development Notes:**

```bash
# Before committing MCP server changes:

# 1. Test server starts without errors
npm run dev

# 2. Verify environment variables documented
# Check README.md or .env.example exists

# 3. Ensure no hardcoded secrets
grep -r "api_key\|password\|secret" --include="*.js" --include="*.ts" . \
    | grep -v "\.env\|example\|template"

# 4. Test key functionality manually
# Use MCP inspector or manual test client
```

---

### Step 4: Commit with Clear Messages

**Stage changes:**

```bash
# Check what will be committed
git status
git diff --cached

# Stage specific files (preferred)
git add skills/kimi-search/SKILL.md
git add servers/my-server/index.ts

# Or stage all changes in current directory
git add .
```

**Commit message format:**

```bash
# Single line for simple changes
git commit -m "Add kimi-search skill with vector memory support"

# Multi-line for complex changes
git commit -m "Add kimi-search skill with vector memory support

Features:
- Hybrid SQLite + Chroma search implementation
- CLI tool for manual memory operations
- Comprehensive SKILL.md with examples

Testing:
- Verified search accuracy >95%
- Tested with 1000+ memory entries"
```

**Commit message guidelines:**

| Good ✅ | Bad ❌ |
|---------|--------|
| `Add kimi-search skill with vector memory` | `update` |
| `Fix kimi-mem CLI error on empty input` | `fix bug` |
| `Update docs: add installation troubleshooting` | `doc update` |
| `Refactor: extract search logic to module` | `refactor` |

---

### Step 5: Pre-Push Validation

**Mandatory checklist before pushing:**

```bash
# Run this validation script

echo "=== Pre-Push Validation ==="

# 1. Check current branch
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
    echo "❌ ERROR: Cannot push directly to main!"
    echo "   Create a feature branch: git checkout -b feature/xxx"
    exit 1
fi

# 2. Check for uncommitted secrets
if grep -r "sk-[a-zA-Z0-9]{20,}" . 2>/dev/null | grep -v ".git"; then
    echo "❌ WARNING: Possible API keys detected!"
    echo "   Review and use environment variables instead"
fi

# 3. Verify SKILL.md structure (if skill modified)
if [ -f "SKILL.md" ]; then
    if ! grep -q "^---" SKILL.md; then
        echo "❌ WARNING: Missing frontmatter in SKILL.md"
    fi
    if ! grep -q "## Overview" SKILL.md; then
        echo "❌ WARNING: Missing Overview section in SKILL.md"
    fi
fi

echo "✅ Validation complete"
```

---

### Step 6: Push and Create PR

```bash
# Push branch to remote
git push -u origin skill/kimi-search

# Output will include PR creation URL
# Example: https://github.com/alexander-naumov/alexander-skills/pull/new/skill/kimi-search
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
- [ ] MCP server added/modified

## Testing
- [ ] Skill loads without errors
- [ ] MCP server starts successfully
- [ ] Manual testing completed
- [ ] No secrets committed

## Checklist
- [ ] Follows SKILL.md format
- [ ] Clear commit messages
- [ ] Branch is up-to-date with main
```

---

### Step 7: Post-Merge Cleanup

```bash
# Switch back to main
git checkout main

# Get latest changes (including your merge)
git pull origin main

# Delete local feature branch
git branch -d skill/kimi-search

# (Optional) Delete remote branch
git push origin --delete skill/kimi-search

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
| Stage changes | `git add filename` or `git add .` |
| Commit | `git commit -m "message"` |
| Push new branch | `git push -u origin feature/name` |
| Update main | `git checkout main && git pull` |
| View log | `git log --oneline --graph -10` |
| Stash changes | `git stash` |
| Pop stash | `git stash pop` |

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| New skill | `skill/<name>` | `skill/kimi-search` |
| Bug fix | `fix/<skill>-<issue>` | `fix/kimi-mem-crash` |
| Documentation | `docs/<what>` | `docs/install-guide` |
| MCP server | `mcp/<name>` | `mcp/filesystem-server` |
| Update | `update/<skill>` | `update/kimi-search` |

### Emergency Commands

| Situation | Command |
|-----------|---------|
| Undo last commit (keep changes) | `git reset --soft HEAD~1` |
| Unstage file | `git reset HEAD filename` |
| Discard file changes | `git checkout -- filename` |
| View diff | `git diff` |
| View staged diff | `git diff --cached` |

---

## Common Mistakes & Fixes

### ❌ Committed to main locally (not pushed)

```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Stash the changes
git stash

# Create proper feature branch
git checkout -b feature/my-feature

# Restore changes
git stash pop

# Commit and push normally
git commit -m "..."
git push -u origin feature/my-feature
```

### ❌ Wrong files staged

```bash
# Unstage specific file
git reset HEAD filename

# Unstage all files
git reset HEAD

# Then stage only correct files
git add correct-file-1 correct-file-2
```

### ❌ Forgot to create branch, made commits on main

```bash
# Save your commits to a new branch
git checkout -b feature/saved-work

# Reset main to origin state
git checkout main
git reset --hard origin/main

# Continue on feature branch
git checkout feature/saved-work
```

### ❌ Pushed to wrong branch

```bash
# DO NOT force push to shared branches!

# Option 1: Revert commits with new commit
git revert HEAD
git push origin main  # Creates revert commit

# Option 2: If you have admin access, use GitHub to revert PR
```

### ❌ Merge conflicts

```bash
# When pulling main into feature branch
git pull origin main

# If conflicts:
# 1. Edit conflicted files (look for <<<<<<< HEAD)
# 2. Stage resolved files
git add resolved-file

# 3. Complete merge
git commit -m "Merge main into feature branch"
```

---

## Red Flags

### 🚫 NEVER DO

| Forbidden | Why |
|-----------|-----|
| `git push origin main` | Pollutes main branch, breaks CI/CD |
| `git push --force` on shared branches | Destroys others' work |
| Commit secrets/API keys | Security breach |
| Mix unrelated changes in one commit | Hard to review/revert |
| Commit without testing | Broken code in repo |
| Ignore failing tests | Technical debt |

### ✅ ALWAYS DO

| Required | Why |
|----------|-----|
| Create feature branches | Isolates work, enables PR review |
| Write clear commit messages | Enables git archaeology |
| Test before pushing | Ensures quality |
| Pull latest main before starting | Avoids merge conflicts |
| Delete merged branches | Keeps repo clean |
| Use `.gitignore` for secrets | Prevents accidents |

---

## Integration

**Called by:**
- Any skill modifying alexander-skills repository
- MCP server development tasks
- Documentation updates
- Repository maintenance

**Pairs with:**
- `skill-creator` - when creating new skills
- `mcp-server-dev` - when developing MCP servers
- `code-review` - before submitting PRs

---

## AI Detection Script

**Use this to automatically detect repository state:**

```bash
#!/bin/bash
# Detect git workflow state

echo "=== Git Workflow State Detection ==="

# Current branch
BRANCH=$(git branch --show-current)
echo "Branch: $BRANCH"

# Check if main
if [ "$BRANCH" = "main" ]; then
    echo "⚠️  WARNING: Currently on main branch"
    echo "   Action needed: Create feature branch before making changes"
fi

# Uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "Changes: Uncommitted changes present"
    git status -s
else
    echo "Changes: Clean working directory"
fi

# Sync status with origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u} 2>/dev/null || echo "none")
BASE=$(git merge-base @ @{u} 2>/dev/null || echo "none")

if [ "$REMOTE" != "none" ]; then
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo "Sync: Up to date with origin"
    elif [ "$LOCAL" = "$BASE" ]; then
        echo "Sync: Behind origin (need to pull)"
    elif [ "$REMOTE" = "$BASE" ]; then
        echo "Sync: Ahead of origin (need to push)"
    else
        echo "Sync: Diverged from origin"
    fi
else
    echo "Sync: No upstream branch set"
fi

# Recent commits
echo ""
echo "Recent commits:"
git log --oneline -3
```
