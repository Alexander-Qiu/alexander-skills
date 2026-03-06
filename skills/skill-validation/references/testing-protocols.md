# Testing Protocols

## Kimi Testing

**Option A: Headless/Automated (Recommended for CI)**
```bash
# Full automated test suite
python skills/skill-validation/scripts/test_with_kimi.py skills/<skill-name>/

# Test with specific prompt
python skills/skill-validation/scripts/test_with_kimi.py skills/<skill-name>/ \
  -p "Your test prompt here"

# Save report
python skills/skill-validation/scripts/test_with_kimi.py skills/<skill-name>/ \
  -o reports/kimi-test.json
```

**Option B: Interactive Testing**
```bash
# Install skill to Kimi
mkdir -p ~/.config/agents/skills
cp -r skills/<skill-name> ~/.config/agents/skills/

# Start Kimi CLI and test interactively
kimi
```

**Kimi Test Checklist:**
- [ ] Skill triggers on expected prompts
- [ ] Skill loads without YAML/parser errors
- [ ] All referenced scripts are executable
- [ ] MCP tools register correctly (if applicable)
- [ ] No Kimi-specific syntax issues

## Claude Testing

**Option A: Headless/Automated (Recommended for CI)**
```bash
# Full automated test suite
python skills/skill-validation/scripts/test_with_claude.py skills/<skill-name>/

# Workflow testing
python skills/skill-validation/scripts/test_with_claude.py skills/<skill-name>/ \
  -p "Complete this task" --workflow

# Save report
python skills/skill-validation/scripts/test_with_claude.py skills/<skill-name>/ \
  -o reports/claude-test.json
```

**Option B: Interactive Testing**
```bash
# Start Claude Code and test interactively
claude
```

**Claude Test Checklist:**
- [ ] Skill triggers on expected prompts
- [ ] Skill content loads properly
- [ ] Claude can follow the instructions
- [ ] Examples work as documented
- [ ] No Claude-specific rendering issues

## Multi-Agent Testing

Test both agents in one command:

```bash
# Test in both Kimi and Claude
python skills/skill-validation/scripts/test_multi_agent.py skills/my-skill/

# Test specific agents
python skills/skill-validation/scripts/test_multi_agent.py skills/my-skill/ \
  -a kimi claude

# With reports
python skills/skill-validation/scripts/test_multi_agent.py skills/my-skill/ \
  -o reports/test.json -m reports/test.md
```

**Output:**
- JSON report with detailed results
- Markdown report for human review
- Exit code 0 = all passed, 1 = any failed
