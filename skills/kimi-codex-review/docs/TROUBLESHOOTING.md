# Troubleshooting

## Common Issues

### 1. Codex CLI Not Found

```
[ERROR] Codex CLI not found
```

**Fix:**
```bash
npm install -g @openai/codex
codex login
```

---

### 2. Not in Git Repository

```
[ERROR] Not in a git repository
```

**Fix:**
```bash
cd /your/git/repo
./scripts/codex-review.sh
```

---

### 3. Network/Proxy Issues

**Symptoms:**
- Timeouts
- Connection errors
- "Host is unreachable"

**Fix:**

Check if clash is running:
```bash
pgrep -x clash
```

If clash is running, the script auto-detects it. If not, manually set:
```bash
export HTTPS_PROXY=http://127.0.0.1:7890
./scripts/codex-review.sh
```

---

### 4. Authentication Failed

```
401 Unauthorized
Not authenticated
```

**Fix:**
```bash
codex login
# or
codex auth
```

---

### 5. All Providers Failed

If you see:
```
[ERROR] All providers failed
Tried: default → zenmux → p2077
```

**Check:**
1. Network connection
2. Proxy settings
3. `codex login` status
4. Provider quota (zenmux/p2077 may be exhausted)

**Debug mode:**
```bash
./scripts/codex-review.sh --timeout 60 2>&1 | head -50
```

---

## Provider Status

| Provider | Model | Status |
|----------|-------|--------|
| default (OpenAI) | gpt-5.4 | Requires subscription |
| zenmux | gemini-3-flash-preview | Pay-as-you-go |
| p2077 | pa/gemini-3-flash-preview | Experimental |

---

## Debug Tips

Test individual providers:
```bash
# Default
codex exec review --uncommitted --skip-git-repo-check

# Zenmux
codex exec review --uncommitted --skip-git-repo-check \
  -c "model_provider=zenmux" \
  -m "google/gemini-3-flash-preview"

# p2077
codex exec review --uncommitted --skip-git-repo-check \
  -c "model_provider=p2077" \
  -m "pa/gemini-3-flash-preview"
```
