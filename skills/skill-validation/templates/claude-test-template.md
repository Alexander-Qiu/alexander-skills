# Claude Integration Test Report

## Skill Information

| Field | Value |
|-------|-------|
| **Skill Name** | {skill_name} |
| **Test Date** | YYYY-MM-DD |
| **Tester** | Your Name |
| **Claude Code Version** | x.x.x |
| **Test Environment** | OS / Shell |

## Pre-Test Setup

### Option A: Automated/Headless Testing
```bash
# Run full automated test suite
python skills/skill-validation/scripts/test_with_claude.py skills/{skill_name}/ \
  -o reports/claude-test.json

# Or test specific prompt
claude -p "Load the {skill_name} skill and show me what it can do"
```

### Option B: Manual Installation
```bash
# Installation commands used
# (Method depends on Claude's skill loading mechanism)

# Verify installation
ls ~/.claude/skills/{skill_name}/  # or appropriate path
```

## Test Results

### 1. Skill Loading Test

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Skill loads without errors | No errors | ✅/❌ | ✅/❌ |
| Frontmatter parsed correctly | Valid metadata | ✅/❌ | ✅/❌ |
| SKILL.md renders properly | Clear formatting | ✅/❌ | ✅/❌ |

**Notes:**

### 2. Trigger Detection Test

Test the skill triggers on appropriate prompts:

| Prompt Used | Expected Trigger | Triggered? | Pass |
|-------------|------------------|------------|------|
| "{example prompt 1}" | {skill_name} | ✅/❌ | ✅/❌ |
| "{example prompt 2}" | {skill_name} | ✅/❌ | ✅/❌ |
| "{negative example}" | Should NOT trigger | ✅/❌ | ✅/❌ |

**Notes:**

### 3. Workflow Execution Test

Test Claude can follow the skill workflow:

| Step | Expected Action | Claude's Action | Pass |
|------|-----------------|-----------------|------|
| 1 | Action description | ✅/❌ | ✅/❌ |
| 2 | Action description | ✅/❌ | ✅/❌ |
| 3 | Action description | ✅/❌ | ✅/❌ |

**Notes:**

### 4. Script/Tool Usage Test

| Script/Tool | Expected Usage | Used Correctly? | Pass |
|-------------|----------------|-----------------|------|
| script1.py | Run with params | ✅/❌ | ✅/❌ |
| Reference file | Load when needed | ✅/❌ | ✅/❌ |

**Claude's Execution Log:**
```
# Paste relevant Claude output here
```

### 5. Example Verification

Test the examples in SKILL.md work as documented:

| Example | Expected Result | Actual Result | Pass |
|---------|-----------------|---------------|------|
| Example 1 | Description | ✅/❌ | ✅/❌ |
| Example 2 | Description | ✅/❌ | ✅/❌ |

**Notes:**

### 6. Error Handling Test

| Error Scenario | Expected Behavior | Actual | Pass |
|----------------|-------------------|--------|------|
| Invalid input | Graceful handling | ✅/❌ | ✅/❌ |
| Missing resource | Clear message | ✅/❌ | ✅/❌ |
| Wrong format | Helpful guidance | ✅/❌ | ✅/❌ |

## Issues Found

### Critical (Blocking Release)
- [ ] Issue 1: Description
  - **Impact:** 
  - **Reproduction:** 
  - **Suggested Fix:** 

### Minor (Non-blocking)
- [ ] Issue 1: Description
  - **Impact:** 
  - **Workaround:** 

## Screenshots / Evidence

<!-- Attach screenshots or conversation logs as evidence -->

## Comparison with Kimi

| Aspect | Kimi | Claude | Notes |
|--------|------|--------|-------|
| Trigger accuracy | ✅/❌ | ✅/❌ | |
| Execution speed | ✅/❌ | ✅/❌ | |
| Error handling | ✅/❌ | ✅/❌ | |
| Ease of use | ✅/❌ | ✅/❌ | |

## Overall Verdict

- [ ] **PASSED** - Ready for release
- [ ] **PASSED WITH NOTES** - Minor issues, can release
- [ ] **FAILED** - Critical issues must be fixed

**Additional Comments:**

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Tester | | | |
| Reviewer | | | |
