# Common Mistakes & Fixes

## ❌ Committed to main locally (not pushed)

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

## ❌ Wrong files staged

```bash
# Unstage specific file
git reset HEAD filename

# Unstage all files
git reset HEAD

# Then stage only correct files
git add correct-file-1 correct-file-2
```

## ❌ Forgot to create branch, made commits on main

```bash
# Save your commits to a new branch
git checkout -b feature/saved-work

# Reset main to origin state
git checkout main
git reset --hard origin/main

# Continue on feature branch
git checkout feature/saved-work
```

## ❌ Pushed to wrong branch

```bash
# DO NOT force push to shared branches!

# Option 1: Revert commits with new commit
git revert HEAD
git push origin main  # Creates revert commit

# Option 2: If you have admin access, use GitHub to revert PR
```

## ❌ Merge conflicts

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
