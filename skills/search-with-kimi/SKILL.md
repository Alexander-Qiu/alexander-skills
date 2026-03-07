---
name: search-with-kimi
description: Use when needing to perform web searches, especially when the built-in WebSearch tool fails or returns errors. Use for parallel searches requiring isolation, Chinese-language queries, or when WebSearch returns 400/500 errors.
---

# Search with Kimi

## Overview

Use kimi-cli's native search capability as a fallback when WebSearch is unavailable or insufficient. **DEFAULT TO PARALLEL SEARCH** - always decompose the user's query into multiple related sub-topics and search them concurrently using sandbox isolation for better coverage and efficiency.

## When to Use

- WebSearch returns 400/500 errors
- WebSearch results are insufficient or empty
- Need real-time internet search for current events
- Require Chinese-language search results (kimi excels here)
- Running multiple searches in parallel (requires sandbox isolation)

## Core Principle: Parallel by Default

**ALWAYS decompose the search query into 3-5 related sub-topics and execute them in parallel.**

For example, if the user asks for "俄乌局势":
- 俄军战场动态
- 乌克兰方面回应
- 国际社会反应
- 和谈进展
- 经济影响

This approach leverages the fact that kimi is an external agent with built-in sandboxing - use parallelism to get comprehensive results faster.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `kimi -yp "query"` | Quick search with single response |
| `kimi -y "query"` | Interactive mode (avoid for automation) |

## Usage Patterns

### Default: Parallel Multi-Topic Search

**This is the RECOMMENDED way to use kimi search.** Decompose the query and run parallel searches:

```bash
# Step 1: Create isolated sandbox directories for each sub-topic
mkdir -p /tmp/kimi_search/{topic1,topic2,topic3,topic4,topic5}
for dir in /tmp/kimi_search/*; do
    cp ~/.kimi/config.toml "$dir/"
    cp -r ~/.kimi/credentials "$dir/"
done

# Step 2: Execute parallel searches (all run concurrently)
KIMI_SHARE_DIR=/tmp/kimi_search/topic1 kimi -yp "子主题1 搜索词" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic2 kimi -yp "子主题2 搜索词" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic3 kimi -yp "子主题3 搜索词" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic4 kimi -yp "子主题4 搜索词" &
KIMI_SHARE_DIR=/tmp/kimi_search/topic5 kimi -yp "子主题5 搜索词" &
wait

# Step 3: Synthesize results from all sub-topics
```

### Example: 俄乌局势 (Decomposed into 5 parallel searches)

```bash
# Setup sandboxes
mkdir -p /tmp/kimi_search/{russian,ukrainian,international,peace,economy}
for dir in /tmp/kimi_search/*; do
    cp ~/.kimi/config.toml "$dir/"
    cp -r ~/.kimi/credentials "$dir/"
done

# Parallel execution
KIMI_SHARE_DIR=/tmp/kimi_search/russian kimi -yp "俄军军事行动 乌克兰战场 最新" &
KIMI_SHARE_DIR=/tmp/kimi_search/ukrainian kimi -yp "乌克兰方面 泽连斯基 最新回应" &
KIMI_SHARE_DIR=/tmp/kimi_search/international kimi -yp "国际社会 欧盟 美国 对俄乌态度" &
KIMI_SHARE_DIR=/tmp/kimi_search/peace kimi -yp "俄乌和谈 谈判进展 停火协议" &
KIMI_SHARE_DIR=/tmp/kimi_search/economy kimi -yp "俄乌战争 经济影响 能源 制裁" &
wait
```

### Fallback: Single Search

Only use single search for very specific, narrow queries:

```bash
# Use only when the query is already extremely specific
kimi -yp "具体某个事件或事实"
```

## Integration in Workflows

### Default Parallel Search Implementation

```python
async def parallel_kimi_search(main_query: str, sub_topics: list[str]) -> dict[str, str]:
    """
    Run parallel kimi searches for multiple sub-topics.

    Args:
        main_query: The original user query (for context)
        sub_topics: List of 3-5 related sub-topics to search

    Returns:
        Dict mapping sub-topic to search result
    """
    import tempfile
    import shutil
    from pathlib import Path

    # Create temporary sandbox directories
    base_dir = Path(tempfile.mkdtemp(prefix="kimi_parallel_"))

    # Copy config to each sandbox
    for topic in sub_topics:
        sandbox = base_dir / topic.replace(" ", "_")
        sandbox.mkdir(parents=True)
        shutil.copy(Path.home() / ".kimi/config.toml", sandbox)
        shutil.copytree(Path.home() / ".kimi/credentials", sandbox / "credentials")

    # Run searches in parallel
    tasks = []
    for topic in sub_topics:
        sandbox = base_dir / topic.replace(" ", "_")
        env = f"KIMI_SHARE_DIR={sandbox}"
        cmd = f'{env} kimi -yp "{topic} 最新"'
        tasks.append((topic, bash(cmd)))

    results = {}
    for topic, task in tasks:
        results[topic] = await task

    # Cleanup
    shutil.rmtree(base_dir, ignore_errors=True)

    return results

# Usage example:
# results = await parallel_kimi_search(
#     "俄乌局势",
#     ["俄军战场动态", "乌克兰回应", "国际社会反应", "和谈进展", "经济影响"]
# )
```

### Query Decomposition Guidelines

When decomposing a query, create sub-topics that cover:

1. **Different perspectives** (e.g., 俄方 vs 乌方 vs 国际)
2. **Different aspects** (e.g., 军事, 外交, 经济, 人道)
3. **Time dimensions** (e.g., 最新进展, 背景, 预测)
4. **Geographic variations** (e.g., 不同地区反应)

**Example decompositions:**

| Original Query | Sub-topics |
|----------------|-----------|
| 中美贸易关系 | 美国对华政策, 中国回应措施, 关税影响, 企业动态, 国际反应 |
| 气候变化大会 | 大会决议内容, 发达国家承诺, 发展中国家立场, 具体减排目标, 争议焦点 |
| 科技公司财报 | 营收数据, 利润分析, 业务增长, 股价反应, 未来展望 |

## Output Format

Kimi returns markdown-formatted results with:
- Structured sections (often with emoji headers)
- Bullet points with key information
- Source URLs when available
- Summary synthesis

**After parallel searches, synthesize results into a cohesive response that covers all sub-topics.**

## Comparison with WebSearch

| Aspect | WebSearch | Kimi Search |
|--------|-----------|-------------|
| Speed | Faster | Slower (full LLM response) |
| Structure | Raw results | Synthesized, formatted |
| Languages | English-focused | Excellent Chinese support |
| Availability | Sometimes errors | Generally reliable |
| Token usage | Lower | Higher |
| Parallel execution | N/A | **Native support via sandbox** |
| Coverage | Single query | **Multi-topic by default** |

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

**Fix:** Always use sandbox isolation with `KIMI_SHARE_DIR` as shown in the parallel search pattern.

## Common Mistakes

- **❌ Don't use single search by default** - always consider parallel decomposition
- **❌ Don't use `-y` (interactive)** in automated workflows - it hangs waiting for input
- **❌ Don't run parallel searches without `KIMI_SHARE_DIR`** - causes file corruption
- **❌ Don't forget to copy `credentials/` to sandbox** - causes login errors
- **❌ Don't create too many parallel searches** - 3-5 is optimal, more may overwhelm
- **❌ Don't parse kimi's markdown literally** - extract key facts, not formatting

## Best Practices

- **Always decompose queries** into 3-5 related sub-topics for parallel search
- **Use descriptive sub-topic names** that clearly indicate the angle/perspective
- **Synthesize results** from all parallel searches into a cohesive response
- **Keep sub-topic queries concise** - let kimi do the synthesis
- **Use Chinese queries** for better Chinese news results
- **Always capture stderr**: use `2>&1` in bash commands
- **Clean up sandboxes** after use to save disk space

## Example Complete Workflow

```python
# User asks: "搜索今天的俄乌局势"

# Step 1: Decompose into sub-topics
sub_topics = [
    "俄军军事行动 乌克兰战场 最新进展",
    "乌克兰方面 泽连斯基 最新回应",
    "国际社会 欧盟 美国 对俄乌态度",
    "俄乌和谈 谈判进展 停火协议",
    "俄乌战争 经济影响 能源危机"
]

# Step 2: Execute parallel searches
results = await parallel_kimi_search("俄乌局势", sub_topics)

# Step 3: Synthesize into final response
# - Combine key findings from all sub-topics
# - Present in structured format
# - Highlight conflicting information if any
```
