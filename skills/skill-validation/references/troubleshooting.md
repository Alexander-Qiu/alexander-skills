# Common Validation Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| Skill not triggering | Description too vague | Make description specific with triggers |
| Script fails in Kimi | Python version issue | Test with Kimi's Python version |
| Script fails in Claude | Path issue | Use relative paths, test in both |
| MCP tools not registering | Server not starting | Check server.js, test manually |
| Tests pass locally, fail in CI | Environment difference | Pin dependencies, use containers |

# Best Practices

1. **Test early, test often** - Don't wait until release
2. **Automate what you can** - Use CI for structure and unit tests
3. **Document everything** - Keep test evidence
4. **Cross-agent by design** - Consider both agents when writing
5. **Fail fast** - Run structure validation before complex tests
6. **Evidence over claims** - Screenshots/logs > "it works"

# Manual Testing Templates

## Kimi Test Session Template

```markdown
## Kimi Integration Test: <skill-name>

Date: YYYY-MM-DD
Tester: <name>

### Trigger Tests
| Prompt | Expected | Actual | Pass |
|--------|----------|--------|------|
| "Process this PDF" | pdf skill | ✅ | ✅ |

### Verdict
- [ ] Ready for release
- [ ] Needs fixes
```

## Claude Test Session Template

```markdown
## Claude Integration Test: <skill-name>

Date: YYYY-MM-DD
Tester: <name>

### Trigger Tests
| Prompt | Expected | Actual | Pass |
|--------|----------|--------|------|
| <test> | <skill> | ✅/❌ | ✅/❌ |

### Verdict
- [ ] Ready for release
- [ ] Needs fixes
```
