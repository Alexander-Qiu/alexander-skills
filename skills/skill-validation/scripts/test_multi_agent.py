#!/usr/bin/env python3
"""
Multi-agent testing harness for skills.
Tests skills in legacy Kimi and Claude headless modes.
"""

import subprocess
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Import sibling testers
sys.path.insert(0, str(Path(__file__).parent))
from test_with_kimi import KimiTester
from test_with_claude import ClaudeTester


class MultiAgentTester:
    """Test skills across multiple agents."""
    
    def __init__(self, skill_path: str, timeout: int = 120):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.timeout = timeout
        
    def test_all(self, agents: List[str] = None) -> Dict:
        """
        Test skill in all specified agents.
        
        Args:
            agents: List of agents to test ['kimi', 'claude'] or None for both
            
        Returns:
            Combined test report
        """
        agents = agents or ['kimi', 'claude']
        
        report = {
            'skill_name': self.skill_name,
            'timestamp': datetime.now().isoformat(),
            'agents_tested': agents,
            'results': {},
            'summary': {}
        }
        
        print(f"\n{'='*60}")
        print(f"🧪 Multi-Agent Testing: {self.skill_name}")
        print(f"{'='*60}\n")
        
        # Test Kimi
        if 'kimi' in agents:
            print("Testing with Kimi CLI...")
            print("-" * 40)
            try:
                kimi_tester = KimiTester(self.skill_path, self.timeout)
                kimi_report = kimi_tester.run_full_test_suite()
                report['results']['kimi'] = kimi_report
                report['summary']['kimi'] = 'PASSED' if kimi_report['overall_passed'] else 'FAILED'
            except Exception as e:
                report['results']['kimi'] = {'error': str(e), 'overall_passed': False}
                report['summary']['kimi'] = 'ERROR'
                print(f"  ❌ Error: {e}")
        
        # Test Claude
        if 'claude' in agents:
            print("\nTesting with Claude Code...")
            print("-" * 40)
            try:
                claude_tester = ClaudeTester(self.skill_path, self.timeout)
                claude_report = claude_tester.run_full_test_suite()
                report['results']['claude'] = claude_report
                report['summary']['claude'] = 'PASSED' if claude_report['overall_passed'] else 'FAILED'
            except Exception as e:
                report['results']['claude'] = {'error': str(e), 'overall_passed': False}
                report['summary']['claude'] = 'ERROR'
                print(f"  ❌ Error: {e}")
        
        # Overall result
        all_passed = all(
            r.get('overall_passed', False)
            for r in report['results'].values()
        )
        report['overall_passed'] = all_passed
        
        return report
    
    def print_summary(self, report: Dict):
        """Print test summary."""
        print(f"\n{'='*60}")
        print("📊 Multi-Agent Test Summary")
        print(f"{'='*60}\n")
        
        for agent, result in report['summary'].items():
            icon = {
                'PASSED': '✅',
                'FAILED': '❌',
                'ERROR': '💥',
                'SKIPPED': '⏭️'
            }.get(result, '❓')
            print(f"  {icon} {agent.title()}: {result}")
        
        print(f"\n{'='*60}")
        if report['overall_passed']:
            print("✅ ALL AGENTS PASSED")
        else:
            print("❌ SOME TESTS FAILED")
        print(f"{'='*60}\n")
    
    def generate_markdown_report(self, report: Dict) -> str:
        """Generate markdown report."""
        lines = [
            f"# Multi-Agent Test Report: {report['skill_name']}",
            f"",
            f"**Timestamp:** {report['timestamp']}",
            f"",
            f"## Summary",
            f"",
            f"| Agent | Status |",
            f"|-------|--------|",
        ]
        
        for agent, result in report['summary'].items():
            icon = '✅' if result == 'PASSED' else '❌'
            lines.append(f"| {agent.title()} | {icon} {result} |")
        
        lines.extend([
            f"",
            f"**Overall:** {'✅ PASSED' if report['overall_passed'] else '❌ FAILED'}",
            f"",
            f"## Detailed Results",
            f""
        ])
        
        # Add detailed results for each agent
        for agent, result in report['results'].items():
            lines.extend([
                f"### {agent.title()}",
                f"",
                f"**Status:** {'✅ PASSED' if result.get('overall_passed') else '❌ FAILED'}",
                f"",
            ])
            
            if 'tests' in result:
                lines.extend(["**Tests:**", ""])
                for test_name, test_result in result['tests'].items():
                    if isinstance(test_result, list):
                        passed = sum(1 for t in test_result if t.get('triggered') or t.get('success'))
                        total = len(test_result)
                        lines.append(f"- {test_name}: {passed}/{total} passed")
                    else:
                        status = '✅' if test_result.get('passed') or test_result.get('success') else '❌'
                        lines.append(f"- {test_name}: {status}")
                lines.append("")
            
            if 'error' in result:
                lines.extend([
                    f"**Error:** {result['error']}",
                    f""
                ])
        
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Test skills across legacy headless agents (Kimi + Claude)'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--agents', '-a', nargs='+', 
                        choices=['kimi', 'claude', 'both'],
                        default=['both'],
                        help='Agents to test (default: both)')
    parser.add_argument('--timeout', '-t', type=int, default=120,
                        help='Timeout per agent in seconds (default: 120)')
    parser.add_argument('--output', '-o', help='Save JSON report')
    parser.add_argument('--markdown', '-m', help='Save markdown report')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')
    
    args = parser.parse_args()
    
    # Normalize agents list
    agents = []
    if 'both' in args.agents:
        agents = ['kimi', 'claude']
    else:
        agents = args.agents
    
    # Run tests
    tester = MultiAgentTester(args.skill_path, args.timeout)
    report = tester.test_all(agents)
    
    if not args.quiet:
        tester.print_summary(report)
    
    # Save reports
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        if not args.quiet:
            print(f"📄 JSON report: {args.output}")
    
    if args.markdown:
        md_report = tester.generate_markdown_report(report)
        with open(args.markdown, 'w') as f:
            f.write(md_report)
        if not args.quiet:
            print(f"📄 Markdown report: {args.markdown}")
    
    # Exit code
    sys.exit(0 if report['overall_passed'] else 1)


if __name__ == "__main__":
    main()
