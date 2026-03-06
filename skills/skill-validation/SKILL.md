---
name: skill-validation
description: Use this skill when creating new skills, updating existing skills, or preparing skills for release. MUST validate all skills through this framework before release. Enforces multi-agent testing (Kimi + Claude required), automated testing, and verification checklists.
license: MIT
---

# Skill Validation Framework

## Overview

Comprehensive validation workflow to ensure all skills are **highly available** across different AI agents.

**Core Principle:** A skill is not "ready" until tested and verified across multiple agents with evidence.

## The Golden Rule

```
NO SKILL RELEASE WITHOUT:
- ✅ Kimi Code CLI validation
- ✅ Claude Code validation  
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ Cross-agent compatibility confirmed
```

---

## Validation Levels

| Level | Name | Required For | Key Checks |
|-------|------|--------------|------------|
| 1 | Structure | All skills | YAML frontmatter, file structure |
| 2 | Unit Tests | Skills with scripts | Test coverage ≥80% |
| 3 | Multi-Agent | All skills | Kimi + Claude integration |
| 4 | E2E Scenarios | Complex skills | Real-world workflows |
| 5 | Compatibility | Multi-agent skills | Compatibility matrix |

See [references/validation-levels.md](references/validation-levels.md) for detailed level requirements.

---

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

**Checklist:**
- [ ] Level 1 (Structure) ✅
- [ ] Level 2 (Unit Tests) ✅ (if applicable)
- [ ] Kimi loads without errors ✅
- [ ] No TODO/FIXME in code ✅

### Phase 3: Pre-Release Validation
**When:** Before merging to main

```bash
# Full validation:
1. All previous levels
2. Full Kimi integration test
3. Full Claude integration test
4. E2E scenario tests
5. Compatibility matrix
```

**Commands:**
```bash
# Test with Kimi
python skills/skill-validation/scripts/test_with_kimi.py skills/my-skill/

# Test with Claude  
python skills/skill-validation/scripts/test_with_claude.py skills/my-skill/

# Multi-agent test
python skills/skill-validation/scripts/test_multi_agent.py skills/my-skill/
```

---

## Quick Commands

### Validation Tools

```bash
# Structure validation
python scripts/validate_structure.py skills/<skill-name>/

# Run all tests with coverage
python scripts/run_skill_tests.py skills/<skill-name>/ --coverage

# Full validation suite
python scripts/validate_skill.py skills/<skill-name>/ --full
```

### Headless Testing

```bash
# Kimi headless mode
kimi -p "Use <skill-name> to <do something>"

# Claude headless mode
claude -p "Use <skill-name> to <do something>"
```

---

## Release Gate

### MUST HAVE Before Release:
1. ✅ Structure validation passing
2. ✅ Unit tests passing (if applicable)
3. ✅ Kimi integration test passed
4. ✅ Claude integration test passed
5. ✅ Compatibility matrix documented
6. ✅ All TODOs resolved

### BLOCKING Issues (cannot release):
- ❌ Skill fails to load in Kimi or Claude
- ❌ Core functionality broken
- ❌ Tests failing
- ❌ Security issues in scripts

---

## Checklist Summary

### For Skill Developers

**Before PR:**
- [ ] Level 1: Structure validation ✅
- [ ] Level 2: Unit tests passing ✅
- [ ] Kimi loads without errors ✅

**Before Release:**
- [ ] Level 3: Kimi full integration test ✅
- [ ] Level 3: Claude full integration test ✅
- [ ] Level 4: E2E tests ✅
- [ ] Level 5: Compatibility matrix ✅

### For Reviewers

**PR Review:**
- [ ] Structure validation passing
- [ ] Tests present and passing
- [ ] Kimi test evidence provided

**Release Review:**
- [ ] All validation levels passing
- [ ] Both Kimi and Claude tested
- [ ] No blocking issues

---

## References

- [Validation Levels](references/validation-levels.md) - Detailed level requirements
- [Testing Protocols](references/testing-protocols.md) - Kimi & Claude testing procedures
- [CI/CD Integration](references/cicd-integration.md) - GitHub Actions setup
- [Skill Types](references/skill-types.md) - Type-specific validation rules
- [Troubleshooting](references/troubleshooting.md) - Common failures & templates
