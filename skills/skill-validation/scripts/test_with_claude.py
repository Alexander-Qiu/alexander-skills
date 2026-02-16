#!/usr/bin/env python3
"""
Headless testing of skills using Claude Code in prompt mode.
Usage: claude -p "<prompt>" [--skill-dir <dir>]
"""

import subprocess
import json
import sys
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class ClaudeTester:
    """Test skills using Claude Code in headless mode."""
    
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
        # Claude Code command structure
        # Note: Adjust based on actual Claude CLI syntax
        cmd = ['claude', '-p', prompt]
        
        # Set up skill directory for Claude
        env = self._get_test_env()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env=env
            )
            
            output = result.stdout + result.stderr
            
            # Check if skill was mentioned/loaded
            triggered = (
                self.skill_name in output or
                f"Skill({self.skill_name})" in output or
                f"Using {self.skill_name}" in output or
                "I'll help you" in output  # Claude typically responds positively
            )
            
            return triggered, output
            
        except subprocess.TimeoutExpired:
            return False, f"Timeout after {self.timeout}s"
        except FileNotFoundError:
            return False, "claude command not found. Is Claude Code installed?"
        except Exception as e:
            return False, f"Error: {e}"
    
    def test_workflow(self, task: str) -> Tuple[bool, str, List[str]]:
        """
        Test if Claude can follow the skill workflow.
        
        Args:
            task: Task description for Claude
            
        Returns:
            (success, output, steps_executed)
        """
        prompt = f"{task}\n\nPlease follow the appropriate skill workflow and show each step."
        
        success, output = self.test_trigger(prompt)
        
        # Extract steps from output (look for numbered lists or step indicators)
        steps = []
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', 'Step', '-')):
                steps.append(line)
        
        return success, output, steps
    
    def test_example(self, example_prompt: str, expected_keywords: List[str]) -> Tuple[bool, str]:
        """
        Test if an example from SKILL.md works correctly.
        
        Args:
            example_prompt: The example prompt from documentation
            expected_keywords: Keywords that should appear in successful output
            
        Returns:
            (success, output)
        """
        success, output = self.test_trigger(example_prompt)
        
        # Check for expected keywords
        found_keywords = [kw for kw in expected_keywords if kw.lower() in output.lower()]
        
        # Success if triggered and found at least half of expected keywords
        success = success and len(found_keywords) >= len(expected_keywords) / 2
        
        return success, output
    
    def run_full_test_suite(self) -> Dict:
        """
        Run complete test suite for the skill.
        
        Returns:
            Test report dictionary
        """
        print(f"🤖 Testing with Claude Code: {self.skill_name}")
        print("-" * 50)
        
        report = {
            'skill_name': self.skill_name,
            'agent': 'Claude',
            'tests': {}
        }
        
        # 1. Basic loading test
        print("\n📦 Test 1: Basic Loading")
        triggered, output = self.test_trigger(
            f"I need help with something that requires the {self.skill_name} skill"
        )
        report['tests']['loading'] = {
            'passed': triggered,
            'output': output[:1000] if len(output) > 1000 else output
        }
        print(f"  {'✅' if triggered else '❌'} Loading test")
        
        # 2. Trigger detection
        print("\n🎯 Test 2: Trigger Detection")
        triggers = self._extract_triggers()
        trigger_results = []
        
        for trigger in triggers[:3]:
            triggered, output = self.test_trigger(trigger)
            trigger_results.append({
                'prompt': trigger,
                'triggered': triggered
            })
            print(f"  {'✅' if triggered else '❌'} '{trigger[:50]}...'")
            
        report['tests']['triggers'] = trigger_results
        
        # 3. Workflow test
        print("\n📋 Test 3: Workflow Execution")
        workflow_task = self._get_workflow_task()
        success, output, steps = self.test_workflow(workflow_task)
        report['tests']['workflow'] = {
            'success': success,
            'steps_detected': len(steps),
            'steps': steps[:5],  # First 5 steps
            'output': output[:800]
        }
        print(f"  {'✅' if success else '❌'} Workflow test ({len(steps)} steps)")
        
        # 4. Example test (if examples exist in SKILL.md)
        examples = self._extract_examples()
        if examples:
            print("\n💡 Test 4: Example Verification")
            example_results = []
            
            for example in examples[:2]:  # Test up to 2 examples
                success, output = self.test_example(
                    example['prompt'],
                    example['expected_keywords']
                )
                example_results.append({
                    'example': example['description'],
                    'success': success
                })
                print(f"  {'✅' if success else '❌'} {example['description']}")
                
            report['tests']['examples'] = example_results
        
        # Calculate overall result
        all_passed = all(
            t.get('passed', t.get('triggered', t.get('success', False)))
            for tests in report['tests'].values()
            for t in (tests if isinstance(tests, list) else [tests])
        )
        report['overall_passed'] = all_passed
        
        return report
    
    def _get_test_env(self) -> Dict:
        """Get environment variables for testing."""
        env = os.environ.copy()
        
        # Set Claude skills directory
        # Adjust variable name based on actual Claude Code config
        temp_dir = Path(tempfile.gettempdir()) / 'claude-test-skills'
        temp_dir.mkdir(exist_ok=True)
        
        # Copy skill to temp location
        import shutil
        dest = temp_dir / self.skill_name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(self.skill_path, dest)
        
        # Claude might use different env vars
        env['CLAUDE_SKILLS_DIR'] = str(temp_dir)
        env['ANTHROPIC_SKILL_DIR'] = str(temp_dir)
        
        return env
    
    def _extract_triggers(self) -> List[str]:
        """Extract potential trigger prompts from SKILL.md."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return [f"Help me with {self.skill_name}"]
        
        content = skill_md.read_text()
        triggers = []
        
        # Look for description field (triggers are often here)
        import re
        desc_match = re.search(r'description:\s*(.+?)(?:\n\w|\n---|$)', content, re.DOTALL)
        if desc_match:
            # Extract trigger phrases from description
            desc = desc_match.group(1).strip()
            # Use full description as trigger
            if len(desc) > 20:
                triggers.append(desc[:200])
        
        # Look for "When to Use" section
        if '## When to Use' in content:
            lines = content.split('## When to Use')[1].split('##')[0].split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('- ') or line.startswith('* '):
                    trigger = line[2:].strip()
                    if trigger and len(trigger) > 10:
                        triggers.append(trigger)
        
        # Default triggers
        if not triggers:
            triggers = [
                f"Help me with {self.skill_name}",
                f"I need to use {self.skill_name}",
                f"Can you use the {self.skill_name} skill?"
            ]
        
        return triggers[:3]
    
    def _get_workflow_task(self) -> str:
        """Generate a workflow test task based on skill content."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return f"Demonstrate how to use {self.skill_name}"
        
        content = skill_md.read_text()
        
        # Try to find a concrete example
        if '## Example' in content:
            return f"Walk me through the example in the {self.skill_name} skill"
        
        # Or look for usage section
        if '## Usage' in content:
            return f"Show me how to use {self.skill_name} following the usage guide"
        
        return f"Help me complete a task using the {self.skill_name} skill"
    
    def _extract_examples(self) -> List[Dict]:
        """Extract examples from SKILL.md."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return []
        
        content = skill_md.read_text()
        examples = []
        
        import re
        
        # Find example sections
        example_sections = re.findall(
            r'## Examples?(.*?)## |## Examples?$',
            content,
            re.DOTALL
        )
        
        for section in example_sections:
            # Look for code blocks or lists
            code_blocks = re.findall(r'```(?:\w+)?\n(.*?)```', section, re.DOTALL)
            
            for i, code in enumerate(code_blocks[:2]):
                examples.append({
                    'description': f'Example {i+1}',
                    'prompt': code.strip()[:200],
                    'expected_keywords': ['success', 'completed', 'done', 'result']
                })
        
        return examples


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Test skills using Claude Code in headless mode'
    )
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--prompt', '-p', help='Test specific prompt')
    parser.add_argument('--timeout', '-t', type=int, default=120,
                        help='Timeout in seconds (default: 120)')
    parser.add_argument('--output', '-o', help='Save report to JSON file')
    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Minimal output')
    parser.add_argument('--workflow', '-w', action='store_true',
                        help='Test workflow execution')
    
    args = parser.parse_args()
    
    tester = ClaudeTester(args.skill_path, timeout=args.timeout)
    
    if args.prompt:
        # Test single prompt
        if args.workflow:
            success, output, steps = tester.test_workflow(args.prompt)
            if not args.quiet:
                print(f"Task: {args.prompt}")
                print(f"Success: {'✅ Yes' if success else '❌ No'}")
                print(f"Steps: {len(steps)}")
                print(f"\nOutput:\n{output}")
        else:
            triggered, output = tester.test_trigger(args.prompt)
            if not args.quiet:
                print(f"Prompt: {args.prompt}")
                print(f"Triggered: {'✅ Yes' if triggered else '❌ No'}")
                print(f"\nOutput:\n{output}")
        sys.exit(0 if (success if args.workflow else triggered) else 1)
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
