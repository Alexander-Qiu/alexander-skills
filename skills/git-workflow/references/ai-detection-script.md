# AI Detection Script

Use this to automatically detect repository state:

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

Save as `scripts/detect-state.sh` and run before starting any work.
