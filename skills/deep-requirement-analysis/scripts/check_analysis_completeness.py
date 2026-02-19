#!/usr/bin/env python3
"""
Check if analysis report is complete before allowing implementation.
Usage: python check_analysis_completeness.py --report report.md
"""

import argparse
import re
from pathlib import Path


def check_completeness(report_path: str) -> dict:
    """Check analysis report completeness."""
    
    with open(report_path, 'r') as f:
        content = f.read()
    
    checks = {
        "problem_statement": bool(re.search(r'## 1\. Problem Statement.*?(?=## 2|\Z)', content, re.DOTALL) and 
                                  not re.search(r'## 1\. Problem Statement\s*\n\s*<!--', content)),
        "constraints": bool(re.search(r'## 2\. Key Constraints', content)),
        "multi_angle": bool(re.search(r'## 3\. Multi-Angle Analysis', content)),
        "verified_facts": bool(re.search(r'## 4\. Verified Facts', content)),
        "user_questions": bool(re.search(r'## 5\. Critical Questions for User', content)),
        "execution_plan": bool(re.search(r'## 6\. Proposed Execution Plan', content)),
        "open_questions": bool(re.search(r'## 7\. Open Questions', content)),
    }
    
    # Check for empty sections
    for section in ["Problem Statement", "Key Constraints", "Execution Plan"]:
        pattern = rf'## \d+\. {section}\s*\n\s*\n|## \d+\. {section}\s*\n\s*##'
        if re.search(pattern, content):
            checks[f"{section.lower().replace(' ', '_')}_empty"] = True
    
    # Overall status
    critical_sections = ["problem_statement", "constraints", "execution_plan"]
    critical_complete = all(checks.get(s, False) for s in critical_sections)
    
    all_complete = all(checks.values())
    
    return {
        "checks": checks,
        "critical_complete": critical_complete,
        "all_complete": all_complete,
        "can_proceed": critical_complete,
        "missing": [k for k, v in checks.items() if not v]
    }


def main():
    parser = argparse.ArgumentParser(description="Check analysis completeness")
    parser.add_argument("--report", required=True, help="Path to analysis report")
    
    args = parser.parse_args()
    
    result = check_completeness(args.report)
    
    print(f"Analysis Completeness Check")
    print(f"=" * 40)
    print(f"Can proceed to implementation: {'✅ Yes' if result['can_proceed'] else '❌ No'}")
    print(f"All sections complete: {'✅' if result['all_complete'] else '⚠️'}")
    print()
    print("Section Status:")
    for section, complete in result['checks'].items():
        print(f"  {section}: {'✅' if complete else '❌'}")
    
    if result['missing']:
        print(f"\nMissing/Incomplete: {', '.join(result['missing'])}")


if __name__ == "__main__":
    main()
