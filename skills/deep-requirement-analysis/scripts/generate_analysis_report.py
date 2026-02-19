#!/usr/bin/env python3
"""
Generate a structured analysis report template.
Usage: python generate_analysis_report.py --task "Analyze vLLM" --output report.md
"""

import argparse
from datetime import datetime


def generate_report(task: str, findings: dict = None) -> str:
    """Generate analysis report template."""
    
    template = f"""# Analysis Report: {task}

**Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**Analyst**: AI Agent  
**Status**: 🔄 In Progress

---

## 1. Problem Statement

<!-- Restate the problem in your own words -->
**Goal**: 
**Success Criteria**: 

## 2. Key Constraints

### Hard Constraints (Non-negotiable)
- [ ] 
- [ ] 

### Soft Constraints (Preferred but flexible)
- [ ] 
- [ ] 

## 3. Multi-Angle Analysis

### 3.1 Feasibility Assessment
| Aspect | Status | Notes |
|--------|--------|-------|
| Technical | ✅/⚠️/❓ | |
| Resource | ✅/⚠️/❓ | |
| Timeline | ✅/⚠️/❓ | |

### 3.2 Scope Clarification
**In Scope**:
- 

**Out of Scope**:
- 

**Boundaries Need Clarification**:
- 

### 3.3 Risk Analysis
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | High/Med/Low | High/Med/Low | |

### 3.4 Alternative Approaches
| Approach | Pros | Cons | Effort |
|----------|------|------|--------|
| Option 1 | | | |
| Option 2 | | | |
| Option 3 | | | |

## 4. Verified Facts

| Claim | Status | Evidence | Source |
|-------|--------|----------|--------|
| | ✅ Verified / ⚠️ Unverified / ❌ Contradicted | | |

## 5. Critical Questions for User

1. **Question**: 
   - My recommendation: 
   - Need user input: Yes/No

2. **Question**: 
   - My recommendation: 
   - Need user input: Yes/No

## 6. Proposed Execution Plan

### Phase 1: [Name]
- **Tasks**: 
- **Deliverables**: 
- **Duration Estimate**: 

### Phase 2: [Name]
- **Tasks**: 
- **Deliverables**: 
- **Dependencies**: Phase 1

### Phase 3: [Name]
- **Tasks**: 
- **Deliverables**: 
- **Dependencies**: 

## 7. Open Questions

- [ ] 
- [ ] 

---

**Next Step**: Get user confirmation on questions in Section 5 before proceeding.
"""
    
    return template


def main():
    parser = argparse.ArgumentParser(description="Generate analysis report template")
    parser.add_argument("--task", required=True, help="Task name/description")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    report = generate_report(args.task)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"Report template generated: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
