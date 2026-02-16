# Kimi Integration Test Report

## Skill Information

| Field | Value |
|-------|-------|
| **Skill Name** | {skill_name} |
| **Test Date** | YYYY-MM-DD |
| **Tester** | Your Name |
| **Kimi CLI Version** | x.x.x |
| **Test Environment** | OS / Shell |

## Pre-Test Setup

```bash
# Installation commands used
mkdir -p ~/.config/agents/skills
cp -r skills/{skill_name} ~/.config/agents/skills/

# Verify installation
ls ~/.config/agents/skills/{skill_name}/
```

## Test Results

### 1. Skill Loading Test

| Check | Expected | Actual | Pass |
|-------|----------|--------|------|
| Skill loads without YAML errors | No errors | ✅/❌ | ✅/❌ |
| Frontmatter parsed correctly | Valid metadata | ✅/❌ | ✅/❌ |
| No file permission issues | All readable | ✅/❌ | ✅/❌ |

**Notes:**

### 2. Trigger Detection Test

Test the skill triggers on appropriate prompts:

| Prompt Used | Expected Trigger | Triggered? | Pass |
|-------------|------------------|------------|------|
| "{example prompt 1}" | {skill_name} | ✅/❌ | ✅/❌ |
| "{example prompt 2}" | {skill_name} | ✅/❌ | ✅/❌ |
| "{negative example}" | Should NOT trigger | ✅/❌ | ✅/❌ |

**Notes:**

### 3. Script Execution Test

If skill has scripts:

| Script | Command Used | Expected Result | Actual | Pass |
|--------|--------------|-----------------|--------|------|
| script1.py | `python script1.py` | Success | ✅/❌ | ✅/❌ |
| script2.sh | `./script2.sh` | Success | ✅/❌ | ✅/❌ |

**Test Output Logs:**
```
# Paste relevant output here
```

### 4. Tool Integration Test

If skill uses MCP or tools:

| Tool | Expected | Works? | Pass |
|------|----------|--------|------|
| tool1 | Description | ✅/❌ | ✅/❌ |
| tool2 | Description | ✅/❌ | ✅/❌ |

**Notes:**

### 5. Error Handling Test

| Error Scenario | Expected Behavior | Actual | Pass |
|----------------|-------------------|--------|------|
| Invalid input | Graceful error | ✅/❌ | ✅/❌ |
| Missing file | Clear message | ✅/❌ | ✅/❌ |
| Wrong format | Helpful error | ✅/❌ | ✅/❌ |

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

<!-- Attach screenshots or logs as evidence -->

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
