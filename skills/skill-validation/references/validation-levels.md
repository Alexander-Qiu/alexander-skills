# Validation Levels

## Level 1: Structure Validation (Automated)
**Required for:** All skills before any PR

```yaml
Checks:
  - SKILL.md exists and has valid frontmatter
  - name and description fields present
  - Description is comprehensive (>100 chars)
  - No extraneous files (README, CHANGELOG, etc.)
  - scripts/ are executable (if present)
  - references/ files are referenced from SKILL.md
```

**Command:**
```bash
python scripts/validate_structure.py skills/<skill-name>/
```

## Level 2: Unit Testing (Required)
**Required for:** All skills with scripts/

Every script MUST have corresponding tests:

```
skill-name/
├── scripts/
│   ├── rotate_pdf.py
│   └── merge_docs.py
├── tests/
│   ├── test_rotate_pdf.py
│   ├── test_merge_docs.py
│   └── conftest.py
```

**Coverage Requirements:**
| File Type | Minimum Coverage |
|-----------|------------------|
| Critical scripts | 90% |
| Utility scripts | 80% |
| Simple wrappers | 70% |

## Level 3: Multi-Agent Integration Testing (CRITICAL)
**Required for:** All skills before release

| Agent | Priority | Test Focus |
|-------|----------|------------|
| **Kimi Code CLI** | Required | Trigger detection, skill loading, tool execution |
| **Claude Code** | Required | Trigger detection, skill loading, workflow execution |

See [testing-protocols.md](testing-protocols.md) for detailed testing procedures.

## Level 4: End-to-End Scenario Testing
**Required for:** Complex skills before release

Test real-world usage scenarios:
- Real user workflows (not just functions)
- Error handling and recovery
- Realistic data
- Complete from trigger to output

## Level 5: Cross-Agent Compatibility Matrix
**Required for:** Skills claiming multi-agent support

```markdown
## Compatibility Matrix

| Feature | Kimi | Claude | Notes |
|---------|------|--------|-------|
| Trigger detection | ✅ | ✅ | Works on both |
| Script execution | ✅ | ✅ | Python 3.8+ required |
| MCP tools | ✅ | ❌ | Claude doesn't support MCP yet |
```
