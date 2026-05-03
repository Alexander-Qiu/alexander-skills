# Testing Protocols

## Codex Testing

**Installer wiring check:**
```bash
./install.sh --agent codex --dry-run
```

**Isolated install smoke test:**
```bash
TMP_HOME="$(mktemp -d)"
./install.sh --agent codex --home "$TMP_HOME"
test -f "$TMP_HOME/.codex/skills/<skill-name>/SKILL.md"
```

**Codex Test Checklist:**
- [ ] Skill appears in the Codex profile in `manifests/skills.json`
- [ ] Skill links into `~/.codex/skills`
- [ ] Prompt entries link into `~/.codex/prompts` if applicable
- [ ] Existing user files are not overwritten without `--replace`

## Claude Code Testing

**Installer wiring check:**
```bash
./install.sh --agent claude-code --dry-run
```

**Skills-only isolated install smoke test:**
```bash
TMP_HOME="$(mktemp -d)"
./install.sh --agent claude-code --skip-plugins --home "$TMP_HOME"
test -f "$TMP_HOME/.claude/skills/<skill-name>/SKILL.md"
```

**Plugin command check:**
```bash
./install.sh --agent claude-code --dry-run | grep "claude plugin install"
```

**Claude Code Test Checklist:**
- [ ] Skill appears in the Claude Code profile in `manifests/skills.json`
- [ ] Skill links into `~/.claude/skills`
- [ ] Required plugins are listed in the profile
- [ ] `--skip-plugins` provides a local-skills-only path

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

## Legacy Claude Headless Testing

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

**Legacy Claude Test Checklist:**
- [ ] Skill triggers on expected prompts
- [ ] Skill content loads properly
- [ ] Claude can follow the instructions
- [ ] Examples work as documented
- [ ] No Claude-specific rendering issues

## Multi-Agent Testing

Test legacy Kimi and Claude headless harnesses in one command:

```bash
# Test in both Kimi and legacy Claude harnesses
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
