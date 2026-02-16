#!/usr/bin/env python3
"""
Complete validation suite for skills.
Runs all validation levels and generates a comprehensive report.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Import sibling scripts
sys.path.insert(0, str(Path(__file__).parent))
from validate_structure import StructureValidator
from run_skill_tests import run_tests
from check_compatibility import CompatibilityChecker


class SkillValidator:
    """Complete skill validation orchestrator."""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.report: Dict = {
            'skill_name': self.skill_name,
            'timestamp': datetime.now().isoformat(),
            'levels': {},
            'summary': {
                'passed': 0,
                'failed': 0,
                'warnings': 0
            }
        }
    
    def validate(self, full: bool = False) -> Dict:
        """
        Run complete validation.
        
        Args:
            full: If True, run all levels including integration tests
        """
        print(f"\n{'='*60}")
        print(f"🔍 Skill Validation: {self.skill_name}")
        print(f"{'='*60}\n")
        
        # Level 1: Structure
        self._run_level_1_structure()
        
        # Level 2: Unit Tests
        self._run_level_2_unit_tests()
        
        # Level 3: Compatibility Analysis
        self._run_level_3_compatibility()
        
        # Level 4+: Integration tests (if full mode)
        if full:
            self._run_level_4_integration()
        
        # Generate summary
        self._generate_summary()
        
        return self.report
    
    def _run_level_1_structure(self):
        """Level 1: Structure validation."""
        print("📋 Level 1: Structure Validation")
        print("-" * 40)
        
        validator = StructureValidator(self.skill_path)
        is_valid, errors, warnings = validator.validate()
        
        self.report['levels']['structure'] = {
            'status': 'PASSED' if is_valid else 'FAILED',
            'errors': errors,
            'warnings': warnings
        }
        
        if warnings:
            for w in warnings:
                print(f"  ⚠️  {w}")
        if errors:
            for e in errors:
                print(f"  ❌ {e}")
                
        if is_valid:
            print("  ✅ Structure validation PASSED\n")
        else:
            print("  ❌ Structure validation FAILED\n")
    
    def _run_level_2_unit_tests(self):
        """Level 2: Unit tests."""
        print("🧪 Level 2: Unit Tests")
        print("-" * 40)
        
        tests_dir = self.skill_path / 'tests'
        if not tests_dir.exists():
            self.report['levels']['unit_tests'] = {
                'status': 'SKIPPED',
                'reason': 'No tests directory'
            }
            print("  ⚠️  No tests found (skipped)\n")
            return
        
        success, output = run_tests(self.skill_path, coverage=True)
        
        # Parse output for summary
        passed = output.count('PASSED')
        failed = output.count('FAILED')
        
        self.report['levels']['unit_tests'] = {
            'status': 'PASSED' if success else 'FAILED',
            'summary': f"{passed} passed, {failed} failed",
            'output': output[:2000]  # Truncate for report
        }
        
        # Print key lines
        for line in output.split('\n'):
            if 'passed' in line.lower() or 'failed' in line.lower() or 'error' in line.lower():
                if line.strip():
                    print(f"  {line}")
        
        if success:
            print("  ✅ Unit tests PASSED\n")
        else:
            print("  ❌ Unit tests FAILED\n")
    
    def _run_level_3_compatibility(self):
        """Level 3: Compatibility analysis."""
        print("🔍 Level 3: Compatibility Analysis")
        print("-" * 40)
        
        checker = CompatibilityChecker(self.skill_path)
        analysis = checker.analyze()
        matrix = checker.generate_matrix()
        
        self.report['levels']['compatibility'] = {
            'status': 'PASSED' if not analysis['warnings'] else 'WARNING',
            'analysis': analysis,
            'matrix': matrix
        }
        
        # Print key compatibility info
        kimi = analysis['features']['kimi']
        claude = analysis['features']['claude']
        
        print(f"  Kimi features: MCP={kimi['mcp_tools']}, Shell={kimi['shell_commands']}")
        print(f"  Claude features: SkillTool={claude['skill_tool']}, Refs={claude['references_pattern']}")
        
        if analysis['warnings']:
            for w in analysis['warnings']:
                print(f"  ⚠️  {w}")
        else:
            print("  ✅ No compatibility warnings")
            
        print()
    
    def _run_level_4_integration(self):
        """Level 4: Integration tests (placeholder)."""
        print("🔌 Level 4: Integration Tests")
        print("-" * 40)
        
        # This would require actual agent environments
        # For now, just document what's needed
        self.report['levels']['integration'] = {
            'status': 'MANUAL',
            'required_tests': [
                'Kimi CLI loading test',
                'Claude Code loading test',
                'Script execution test',
                'E2E workflow test'
            ],
            'note': 'Must be run manually in respective agent environments'
        }
        
        print("  ⚠️  Integration tests require manual execution:")
        print("     1. Test skill loading in Kimi CLI")
        print("     2. Test skill loading in Claude Code")
        print("     3. Test core functionality in both agents")
        print("     4. Document results in test-reports/\n")
    
    def _generate_summary(self):
        """Generate final summary."""
        passed = 0
        failed = 0
        warnings = 0
        
        for level_name, level_data in self.report['levels'].items():
            status = level_data.get('status', 'UNKNOWN')
            if status == 'PASSED':
                passed += 1
            elif status == 'FAILED':
                failed += 1
            elif status in ['WARNING', 'SKIPPED', 'MANUAL']:
                warnings += 1
                
            # Count warnings in level
            if 'warnings' in level_data and level_data['warnings']:
                warnings += len(level_data['warnings'])
        
        self.report['summary'] = {
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'overall': 'PASSED' if failed == 0 else 'FAILED'
        }
    
    def print_summary(self):
        """Print validation summary."""
        print(f"\n{'='*60}")
        print("📊 Validation Summary")
        print(f"{'='*60}")
        
        for level_name, level_data in self.report['levels'].items():
            status = level_data.get('status', 'UNKNOWN')
            icon = {
                'PASSED': '✅',
                'FAILED': '❌',
                'WARNING': '⚠️',
                'SKIPPED': '⏭️',
                'MANUAL': '👤'
            }.get(status, '❓')
            print(f"  {icon} {level_name.replace('_', ' ').title()}: {status}")
        
        print(f"\n{'='*60}")
        summary = self.report['summary']
        if summary['overall'] == 'PASSED':
            print(f"✅ OVERALL: PASSED ({summary['passed']}/{summary['passed']+summary['failed']} levels)")
        else:
            print(f"❌ OVERALL: FAILED ({summary['failed']} failures, {summary['warnings']} warnings)")
        print(f"{'='*60}\n")
    
    def save_report(self, output_path: str):
        """Save report to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"📄 Detailed report saved to: {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Complete skill validation suite'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--full', action='store_true', 
                        help='Run full validation including integration tests')
    parser.add_argument('--output', '-o', help='Save report to JSON file')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json',
                        help='Report format')
    
    args = parser.parse_args()
    
    validator = SkillValidator(args.skill_path)
    report = validator.validate(full=args.full)
    validator.print_summary()
    
    if args.output:
        if args.format == 'json':
            validator.save_report(args.output)
        elif args.format == 'markdown':
            # Generate markdown report
            md_report = generate_markdown_report(report)
            with open(args.output, 'w') as f:
                f.write(md_report)
            print(f"📄 Markdown report saved to: {args.output}")
    
    # Exit with appropriate code
    sys.exit(0 if report['summary']['overall'] == 'PASSED' else 1)


def generate_markdown_report(report: Dict) -> str:
    """Generate markdown report from validation results."""
    lines = [
        f"# Validation Report: {report['skill_name']}",
        f"",
        f"**Timestamp:** {report['timestamp']}",
        f"",
        f"## Summary",
        f"",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Overall | {report['summary']['overall']} |",
        f"| Levels Passed | {report['summary']['passed']} |",
        f"| Levels Failed | {report['summary']['failed']} |",
        f"| Warnings | {report['summary']['warnings']} |",
        f"",
        f"## Detailed Results",
        f""
    ]
    
    for level_name, level_data in report['levels'].items():
        status = level_data.get('status', 'UNKNOWN')
        lines.extend([
            f"### {level_name.replace('_', ' ').title()}",
            f"",
            f"**Status:** {status}",
            f""
        ])
        
        if 'errors' in level_data and level_data['errors']:
            lines.extend(["**Errors:**", ""])
            for e in level_data['errors']:
                lines.append(f"- ❌ {e}")
            lines.append("")
            
        if 'warnings' in level_data and level_data['warnings']:
            lines.extend(["**Warnings:**", ""])
            for w in level_data['warnings']:
                lines.append(f"- ⚠️ {w}")
            lines.append("")
    
    return "\n".join(lines)


if __name__ == "__main__":
    main()
