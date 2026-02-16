---
name: skill-validation
description: Comprehensive validation workflow for ensuring skills are highly available across different AI agents. Use when creating new skills, updating existing skills, or preparing skills for release. Enforces multi-agent testing (Kimi + Claude required), automated testing, and verification checklists.
---

# Skill Validation Framework

## Overview

This skill defines the comprehensive validation workflow required to ensure all skills are **highly available** across different AI agents.

**Core Principle:** A skill is not "ready" until it has been tested and verified across multiple agents with evidence.

## The Golden Rule

```
NO SKILL RELEASE WITHOUT:
- ✅ Kimi Code CLI validation
- ✅ Claude Code validation  
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ Documentation verified
- ✅ Cross-agent compatibility confirmed
```

## Validation Levels

### Level 1: Structure Validation (Automated)
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
# Run structure validation
python scripts/validate_structure.py skills/<skill-name>/
```

### Level 2: Unit Testing (Required)
**Required for:** All skills with scripts/

Every script in `scripts/` MUST have corresponding tests:

```
skill-name/
├── scripts/
│   ├── rotate_pdf.py
│   └── merge_docs.py
├── tests/                    # Required if scripts/ exists
│   ├── test_rotate_pdf.py
│   ├── test_merge_docs.py
│   └── conftest.py          # Test fixtures
```

**Test Requirements:**
- [ ] Every script has ≥1 test
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Tests run in CI (GitHub Actions)

**Commands:**
```bash
# Run all tests for a skill
cd skills/<skill-name> && pytest tests/ -v

# Run with coverage
cd skills/<skill-name> && pytest tests/ --cov=scripts --cov-report=term-missing
```

**Coverage Requirements:**
| File Type | Minimum Coverage |
|-----------|------------------|
| Critical scripts (data processing) | 90% |
| Utility scripts | 80% |
| Simple wrappers | 70% |

### Level 3: Multi-Agent Integration Testing (CRITICAL)
**Required for:** All skills before release

This is the **most critical** validation level. Every skill must be tested across:

| Agent | Priority | Test Focus |
|-------|----------|------------|
| **Kimi Code CLI** | Required | Trigger detection, skill loading, tool execution |
| **Claude Code** | Required | Trigger detection, skill loading, workflow execution |
| **Other agents** | Optional | If targeting broader compatibility |

#### Kimi Testing Protocol

```bash
# 1. Install skill to Kimi
mkdir -p ~/.config/agents/skills
cp -r skills/<skill-name> ~/.config/agents/skills/

# 2. Start Kimi CLI and test:
# - Does skill trigger correctly? (description triggers)
# - Does skill load without errors?
# - Do scripts execute correctly?
# - Are tools accessible (if MCP-based)?
```

**Kimi Test Checklist:**
- [ ] Skill triggers on expected prompts
- [ ] Skill loads without YAML/parser errors
- [ ] All referenced scripts are executable
- [ ] MCP tools register correctly (if applicable)
- [ ] No Kimi-specific syntax issues

#### Claude Testing Protocol

```bash
# 1. Install skill to Claude
# (Copy to Claude's skill directory or use Claude's skill loading mechanism)

# 2. Test with Claude Code:
# - Does skill trigger correctly?
# - Does Claude follow the workflow?
# - Are examples clear and executable?
```

**Claude Test Checklist:**
- [ ] Skill triggers on expected prompts
- [ ] Skill content loads properly
- [ ] Claude can follow the instructions
- [ ] Examples work as documented
- [ ] No Claude-specific rendering issues

### Level 4: End-to-End Scenario Testing
**Required for:** Complex skills before release

Test real-world usage scenarios:

```python
# Example E2E test structure
tests/e2e/
├── test_pdf_workflow.py          # Full PDF processing workflow
├── test_docx_creation.py         # Document creation end-to-end
└── test_webapp_deployment.py     # Multi-step deployment
```

**E2E Test Requirements:**
- [ ] Tests real user workflows (not just functions)
- [ ] Tests error handling and recovery
- [ ] Tests with realistic data
- [ ] Tests complete from trigger to output

### Level 5: Cross-Agent Compatibility Matrix
**Required for:** Skills claiming multi-agent support

Create compatibility report:

```markdown
## Compatibility Matrix

| Feature | Kimi | Claude | Notes |
|---------|------|--------|-------|
| Trigger detection | ✅ | ✅ | Works on both |
| Script execution | ✅ | ✅ | Python 3.8+ required |
| MCP tools | ✅ | ❌ | Claude doesn't support MCP yet |
| File references | ✅ | ✅ | Relative paths work |
```

## Validation Workflow

### Phase 1: Development Validation
**When:** During skill development

```bash
# After each significant change:
1. Structure validation
2. Unit tests (if scripts)
3. Self-review against checklist
```

### Phase 2: Pre-PR Validation
**When:** Before creating PR

```bash
# Complete validation suite:
1. Structure validation
2. Full unit test suite
3. Kimi smoke test (basic loading)
4. Documentation review
```

**Pre-PR Checklist:**
- [ ] Level 1 (Structure) ✅
- [ ] Level 2 (Unit Tests) ✅ (if applicable)
- [ ] Kimi loads without errors ✅
- [ ] No TODO/FIXME in code ✅
- [ ] Documentation is complete ✅

### Phase 3: Pre-Release Validation
**When:** Before merging to main or releasing

```bash
# Full validation:
1. All previous levels
2. Full Kimi integration test
3. Full Claude integration test
4. E2E scenario tests
5. Compatibility matrix
```

**Pre-Release Checklist:**
- [ ] Level 1-4 all passing ✅
- [ ] Kimi integration test passed ✅
- [ ] Claude integration test passed ✅
- [ ] Compatibility matrix documented ✅
- [ ] No blocking issues ✅

## Automated CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/skill-validation.yml
name: Skill Validation

on:
  pull_request:
    paths:
      - 'skills/**'
  push:
    branches: [main]

jobs:
  structure-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate skill structures
        run: python scripts/validate_all_skills.py

  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        skill: ${{ fromJson(needs.detect-changes.outputs.changed_skills) }}
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
          cd skills/${{ matrix.skill }} && pip install -r requirements.txt || true
      - name: Run tests
        run: |
          cd skills/${{ matrix.skill }} && pytest tests/ -v --cov=scripts

  compatibility-report:
    runs-on: ubuntu-latest
    needs: [structure-validation, unit-tests]
    steps:
      - uses: actions/checkout@v3
      - name: Generate compatibility matrix
        run: python scripts/generate_compatibility_matrix.py
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: compatibility-report
          path: reports/compatibility.md
```

## Manual Testing Templates

### Kimi Test Session Template

```markdown
## Kimi Integration Test: <skill-name>

Date: YYYY-MM-DD
Tester: <name>
Kimi Version: <version>

### Trigger Tests
| Prompt | Expected Trigger | Actual | Pass |
|--------|------------------|--------|------|
| "Process this PDF" | pdf skill | ✅ | ✅ |
| "Create a docx" | docx skill | ✅ | ✅ |

### Functionality Tests
| Feature | Expected | Actual | Pass |
|---------|----------|--------|------|
| Script execution | Runs without error | ✅ | ✅ |
| Output format | Correct format | ✅ | ✅ |
| Error handling | Graceful error | ✅ | ✅ |

### Issues Found
- <list any issues>

### Verdict
- [ ] Ready for release
- [ ] Needs fixes (see issues)
```

### Claude Test Session Template

```markdown
## Claude Integration Test: <skill-name>

Date: YYYY-MM-DD
Tester: <name>
Claude Code Version: <version>

### Trigger Tests
| Prompt | Expected Trigger | Actual | Pass |
|--------|------------------|--------|------|
| <test prompt> | <skill-name> | ✅/❌ | ✅/❌ |

### Workflow Tests
| Step | Expected | Actual | Pass |
|------|----------|--------|------|
| Step 1 | ... | ... | ✅/❌ |

### Issues Found
- <list any issues>

### Verdict
- [ ] Ready for release
- [ ] Needs fixes (see issues)
```

## Skill-Specific Validation Rules

### Type 1: Pure Documentation Skills
Skills with only SKILL.md (no scripts)

**Validation:**
- [ ] Structure validation
- [ ] Kimi loads and triggers correctly
- [ ] Claude loads and triggers correctly
- [ ] Examples are copy-pasteable

### Type 2: Script-Based Skills
Skills with scripts/ directory

**Validation:**
- [ ] All levels
- [ ] Unit tests for all scripts
- [ ] Integration tests for script execution
- [ ] E2E tests for complete workflows

### Type 3: MCP-Based Skills
Skills using MCP protocol (like kimi-mem)

**Validation:**
- [ ] All levels
- [ ] MCP server starts without errors
- [ ] Tools register correctly
- [ ] Tool execution returns valid results
- [ ] Error handling works via MCP

### Type 4: Asset-Based Skills
Skills with assets/ (templates, etc.)

**Validation:**
- [ ] All assets are valid (not corrupted)
- [ ] Assets can be loaded/copied
- [ ] Templates render correctly
- [ ] Assets are referenced correctly from SKILL.md

## Validation Tools

### 1. Structure Validator
```bash
# Validates YAML frontmatter, file structure
python scripts/validate_structure.py skills/<skill-name>/
```

### 2. Test Runner
```bash
# Runs all tests for a skill with coverage
python scripts/run_skill_tests.py skills/<skill-name>/ --coverage
```

### 3. Compatibility Checker
```bash
# Generates compatibility matrix
python scripts/check_compatibility.py skills/<skill-name>/
```

### 4. Full Validation Suite
```bash
# Runs all validation levels
python scripts/validate_skill.py skills/<skill-name>/ --full
```

## Release Gate

### Before ANY Release (main merge or tag):

**MUST HAVE:**
1. ✅ Structure validation passing
2. ✅ Unit tests passing (if applicable)
3. ✅ Kimi integration test passed (with evidence)
4. ✅ Claude integration test passed (with evidence)
5. ✅ Compatibility matrix documented
6. ✅ All TODOs resolved
7. ✅ Documentation complete

**BLOCKING ISSUES (cannot release):**
- ❌ Skill fails to load in Kimi
- ❌ Skill fails to load in Claude
- ❌ Core functionality broken
- ❌ Tests failing
- ❌ Security issues in scripts

**NON-BLOCKING (can release with notes):**
- ⚠️ Minor documentation typos
- ⚠️ Edge case not covered
- ⚠️ Performance could be improved

## Validation Checklist Summary

### For Skill Developers

```markdown
Before submitting PR:
- [ ] Level 1: Structure validation ✅
- [ ] Level 2: Unit tests passing (if scripts) ✅
- [ ] Kimi loads without errors ✅
- [ ] Self-review complete ✅

Before release:
- [ ] Level 3: Kimi full integration test ✅
- [ ] Level 3: Claude full integration test ✅
- [ ] Level 4: E2E tests (if complex skill) ✅
- [ ] Level 5: Compatibility matrix ✅
```

### For Reviewers

```markdown
PR Review Checklist:
- [ ] Structure validation passing
- [ ] Tests present and passing (if applicable)
- [ ] Kimi test evidence provided
- [ ] Code quality acceptable
- [ ] Documentation clear

Release Review Checklist:
- [ ] All validation levels passing
- [ ] Both Kimi and Claude tested
- [ ] No blocking issues
- [ ] Compatibility documented
```

## Common Validation Failures

| Failure | Cause | Fix |
|---------|-------|-----|
| Skill not triggering | Description too vague | Make description specific with triggers |
| Script fails in Kimi | Python version issue | Test with Kimi's Python version |
| Script fails in Claude | Path issue | Use relative paths, test in both |
| MCP tools not registering | Server not starting | Check server.js, test manually |
| Tests pass locally, fail in CI | Environment difference | Pin dependencies, use containers |

## Best Practices

1. **Test early, test often** - Don't wait until release
2. **Automate what you can** - Use CI for structure and unit tests
3. **Document everything** - Keep test evidence
4. **Cross-agent by design** - Consider both agents when writing
5. **Fail fast** - Run structure validation before complex tests
6. **Evidence over claims** - Screenshots/logs > "it works"
