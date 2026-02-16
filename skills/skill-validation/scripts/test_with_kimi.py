#!/usr/bin/env python3
"""
Headless testing of skills using Kimi CLI in prompt mode.
Usage: kimi -p "<prompt>" --skill <skill-name>
"""

import subprocess
import json
import sys
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class KimiTester:
    """Test skills using Kimi CLI in headless mode."""
    
    def __init__(self, skill_path: str, timeout: int = 120):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        self.timeout = timeout
        self.results: List[Dict] = []
        
    def test_trigger(self, prompt: str) -> Tuple[bool, str]:
        """
        Test if skill triggers on given prompt.
        
        Returns:
            (triggered, output)
        """
        cmd = ['kimi', '-p', prompt]
        
        # Install skill temporarily for testing
        self._install_skill_temp()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=self._get_test_env()
            )
            
            output = result.stdout + result.stderr
            
            # Check if skill was mentioned/loaded in output
            triggered = (
                self.skill_name in output or
                f"/skill:{self.skill_name}" in output or
                f"Loaded skill: {self.skill_name}" in output
            )
            
            return triggered, output
            
        except subprocess.TimeoutExpired:
            return False, f"Timeout after {self.timeout}s"
        except FileNotFoundError:
            return False, "kimi command not found. Is Kimi CLI installed?"
        except Exception as e:
            return False, f"Error: {e}"
    
    def test_script(self, script_name: str, args: List[str] = None) -> Tuple[bool, str]:
        """
        Test script execution through Kimi.
        
        Args:
            script_name: Name of script in scripts/ directory
            args: Arguments to pass to script
            
        Returns:
            (success, output)
        """
        args = args or []
        script_path = self.skill_path / 'scripts' / script_name
        
        if not script_path.exists():
            return False, f"Script not found: {script_path}"
        
        # Build prompt to execute script
        cmd_str = f"python {script_path} {' '.join(args)}"
        prompt = f"Run this command and report the result: {cmd_str}"
        
        return self.test_trigger(prompt)
    
    def test_mcp_tools(self, tool_name: str, params: Dict = None) -> Tuple[bool, str]:
        """
        Test MCP tool execution.
        
        Only applicable for MCP-based skills like kimi-mem.
        """
        params = params or {}
        
        # Build prompt to use MCP tool
        params_str = json.dumps(params) if params else "{}"
        prompt = f"Use the {tool_name} tool with params: {params_str}"
        
        return self.test_trigger(prompt)
    
    def run_full_test_suite(self) -> Dict:
        """
        Run complete test suite for the skill.
        
        Returns:
            Test report dictionary
        """
        print(f"🤖 Testing with Kimi CLI: {self.skill_name}")
        print("-" * 50)
        
        report = {
            'skill_name': self.skill_name,
            'agent': 'Kimi',
            'tests': {}
        }
        
        # 1. Basic loading test
        print("\n📦 Test 1: Basic Loading")
        triggered, output = self.test_trigger(
            f"Load the {self.skill_name} skill and confirm it's available"
        )
        report['tests']['loading'] = {
            'passed': triggered,
            'output': output[:1000] if len(output) > 1000 else output
        }
        print(f"  {'✅' if triggered else '❌'} Loading test")
        
        # 2. Get triggers from SKILL.md and test them
        print("\n🎯 Test 2: Trigger Detection")
        triggers = self._extract_triggers()
        trigger_results = []
        
        for trigger in triggers[:3]:  # Test up to 3 triggers
            triggered, output = self.test_trigger(trigger)
            trigger_results.append({
                'prompt': trigger,
                'triggered': triggered
            })
            print(f"  {'✅' if triggered else '❌'} '{trigger[:50]}...'")
            
        report['tests']['triggers'] = trigger_results
        
        # 3. Script execution test (if scripts exist)
        scripts_dir = self.skill_path / 'scripts'
        if scripts_dir.exists():
            print("\n🔧 Test 3: Script Execution")
            script_results = []
            
            for script in sorted(scripts_dir.iterdir())[:2]:  # Test up to 2 scripts
                if script.is_file() and script.suffix in ['.py', '.sh']:
                    success, output = self.test_script(script.name, ['--help'])
                    script_results.append({
                        'script': script.name,
                        'success': success,
                        'output': output[:500]
                    })
                    print(f"  {'✅' if success else '❌'} {script.name}")
                    
            report['tests']['scripts'] = script_results
        
        # Calculate overall result
        all_passed = all(
            t.get('passed', t.get('triggered', t.get('success', False)))
            for tests in report['tests'].values()
            for t in (tests if isinstance(tests, list) else [tests])
        )
        report['overall_passed'] = all_passed
        
        return report
    
    def _install_skill_temp(self):
        """Temporarily install skill for testing."""
        # Create temp skills directory
        temp_dir = Path(tempfile.gettempdir()) / 'kimi-test-skills'
        temp_dir.mkdir(exist_ok=True)
        
        # Copy skill to temp location
        import shutil
        dest = temp_dir / self.skill_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(self.skill_path, dest)
    
    def _get_test_env(self) -> Dict:
        """Get environment variables for testing."""
        env = os.environ.copy()
        # Point to temp skills directory
        temp_dir = Path(tempfile.gettempdir()) / 'kimi-test-skills'
        env['KIMI_SKILLS_PATH'] = str(temp_dir)
        return env
    
    def _extract_triggers(self) -> List[str]:
        """Extract potential trigger prompts from SKILL.md."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return [f"Use {self.skill_name}"]
        
        content = skill_md.read_text()
        
        # Extract description from frontmatter
        triggers = []
        
        # Look for "When to Use" section
        if '## When to Use' in content:
            lines = content.split('## When to Use')[1].split('##')[0].split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    trigger = line[2:].strip()
                    if trigger and len(trigger) > 10:
                        triggers.append(trigger)
        
        # Default triggers based on skill name
        if not triggers:
            triggers = [
                f"Help me with {self.skill_name}",
                f"I need to use {self.skill_name}",
                f"Activate {self.skill_name}"
            ]
        
        return triggers[:3]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test skills using Kimi CLI in headless mode'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--prompt', '-p', help='Test specific prompt')
    parser.add_argument('--timeout', '-t', type=int, default=120,
                        help='Timeout in seconds (default: 120)')
    parser.add_argument('--output', '-o', help='Save report to JSON file')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')
    
    args = parser.parse_args()
    
    tester = KimiTester(args.skill_path, timeout=args.timeout)
    
    if args.prompt:
        # Test single prompt
        triggered, output = tester.test_trigger(args.prompt)
        if not args.quiet:
            print(f"Prompt: {args.prompt}")
            print(f"Triggered: {'✅ Yes' if triggered else '❌ No'}")
            print(f"\nOutput:\n{output}")
        sys.exit(0 if triggered else 1)
    else:
        # Run full test suite
        report = tester.run_full_test_suite()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            if not args.quiet:
                print(f"\n📄 Report saved to: {args.output}")
        
        if not args.quiet:
            print(f"\n{'='*50}")
            print(f"Overall: {'✅ PASSED' if report['overall_passed'] else '❌ FAILED'}")
        
        sys.exit(0 if report['overall_passed'] else 1)


if __name__ == "__main__":
    main()
