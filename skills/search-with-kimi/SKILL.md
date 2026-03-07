---
name: search-with-kimi
description: Use when needing to perform web searches, especially when the built-in WebSearch tool fails or returns errors. Use for parallel searches requiring isolation, Chinese-language queries, or when WebSearch returns 400/500 errors.
---

# Search with Kimi

## Overview

Use kimi-cli's native search capability as a fallback when WebSearch is unavailable or insufficient. Kimi uses Moonshot Search API and typically returns structured, detailed results.

## When to Use

- WebSearch returns 400/500 errors
- WebSearch results are insufficient or empty
- Need real-time internet search for current events
- Require Chinese-language search results (kimi excels here)
- Running multiple searches in parallel (requires sandbox isolation)

## Quick Reference

| Command | Purpose |
|---------|---------|
| `kimi -yp "query"` | Quick search with single response |
| `kimi -y "query"` | Interactive mode (avoid for automation) |

## Usage Patterns

### Simple Search

```bash
# Quick single search
kimi -yp "your search query"

# Example: World news
kimi -yp "world news today"

# Example: Technical query
kimi -yp "Python 3.12 new features"
```

### Parallel Search with Isolation

When running multiple kimi searches concurrently, use `KIMI_SHARE_DIR` environment variable to create isolated sandboxes. Without isolation, concurrent instances may corrupt shared state files.

```bash
# Setup: Create isolated directories and copy config
mkdir -p /tmp/kimi_search/{topic1,topic2,topic3}
for dir in /tmp/kimi_search/*; do
    cp ~/.kimi/config.toml "$dir/"
    cp -r ~/.kimi/credentials "$dir/"
done

# Execute parallel searches with isolation
KIMI_SHARE_DIR=/tmp/kimi_search/topic1 kimi -yp "AI news" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic2 kimi -yp "politics news" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic3 kimi -yp "sports news" &
wait
```

**Key points for parallel execution:**
- Each instance needs its own `KIMI_SHARE_DIR` directory
- Copy `config.toml` and `credentials/` to each sandbox before running
- Isolation prevents file corruption and login conflicts
- Each sandbox maintains separate sessions, logs, and metadata

## Integration in Workflows

### Basic Usage

```python
# Simple search via Bash tool
result = bash("kimi -yp 'search query'")
```

### Parallel Search Helper

```python
import asyncio
import tempfile
import shutil
from pathlib import Path

async def parallel_kimi_search(queries: dict[str, str]) -> dict[str, str]:
    """
    Run multiple kimi searches in parallel with isolation.

    Args:
        queries: Dict mapping search name to query string

    Returns:
        Dict mapping search name to result
    """
    # Create temporary sandbox directories
    base_dir = Path(tempfile.mkdtemp(prefix="kimi_parallel_"))

    # Copy config to each sandbox
    for name in queries.keys():
        sandbox = base_dir / name
        sandbox.mkdir(parents=True)
        shutil.copy("~/.kimi/config.toml", sandbox)
        shutil.copytree("~/.kimi/credentials", sandbox / "credentials")

    # Run searches in parallel
    tasks = []
    for name, query in queries.items():
        sandbox = base_dir / name
        env = f"KIMI_SHARE_DIR={sandbox}"
        cmd = f'{env} kimi -yp "{query}"'
        tasks.append(bash(cmd))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Cleanup
    shutil.rmtree(base_dir, ignore_errors=True)

    return dict(zip(queries.keys(), results))
```

## Output Format

Kimi returns markdown-formatted results with:
- Structured sections (often with emoji headers)
- Bullet points with key information
- Source URLs when available
- Summary synthesis

## Comparison with WebSearch

| Aspect | WebSearch | Kimi Search |
|--------|-----------|-------------|
| Speed | Faster | Slower (full LLM response) |
| Structure | Raw results | Synthesized, formatted |
| Languages | English-focused | Excellent Chinese support |
| Availability | Sometimes errors | Generally reliable |
| Token usage | Lower | Higher |
| Parallel execution | N/A | Requires sandbox isolation |

## Troubleshooting

### "LLM not set, send '/login' to login"

This error means the sandbox directory doesn't have valid credentials. Solutions:

1. **Copy credentials to sandbox:**
   ```bash
   cp ~/.kimi/config.toml /path/to/sandbox/
   cp -r ~/.kimi/credentials /path/to/sandbox/
   ```

2. **Or re-login in a fresh terminal:**
   - Open a new terminal (not in this session)
   - Run: `kimi /login`
   - Complete the login flow
   - Then retry your search

3. **Verify main config exists:**
   ```bash
   ls -la ~/.kimi/
   # Should show: config.toml, credentials/, kimi.json
   ```

### File Corruption / Concurrent Write Errors

If running multiple kimi instances without `KIMI_SHARE_DIR`, you may see:
- JSON decode errors
- Session file corruption
- Metadata conflicts

**Fix:** Use sandbox isolation as described in Parallel Search section.

## Common Mistakes

- **Don't use `-y` (interactive)** in automated workflows - it hangs waiting for input
- **Don't run parallel searches without `KIMI_SHARE_DIR`** - causes file corruption
- **Don't forget to copy `credentials/` to sandbox** - causes login errors
- **Don't parse kimi's markdown literally** - extract key facts, not formatting
- **Don't chain multiple searches** without reviewing first result

## Tips

- Keep queries concise for better results
- For complex topics, do one broad search first, then follow up with specific queries
- Kimi search works well for news, current events, and general knowledge
- Use Chinese queries for better Chinese news results
- Always use `2>&1` to capture both stdout and stderr in scripts
