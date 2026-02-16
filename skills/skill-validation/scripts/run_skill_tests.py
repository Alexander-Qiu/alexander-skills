#!/usr/bin/env python3
"""
Test runner for skill unit tests.
Handles pytest execution and coverage reporting.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple


def run_tests(skill_path: str, coverage: bool = False) -> Tuple[bool, str]:
    """
    Run tests for a skill.
    
    Returns:
        (success, output)
    """
    skill_path = Path(skill_path)
    tests_dir = skill_path / 'tests'
    
    if not tests_dir.exists():
        return True, "No tests directory found (skipping)"
        
    if not any(tests_dir.iterdir()):
        return True, "Tests directory is empty (skipping)"
    
    # Build pytest command
    cmd = ['pytest', str(tests_dir), '-v']
    
    if coverage:
        scripts_dir = skill_path / 'scripts'
        if scripts_dir.exists():
            cmd.extend(['--cov=str(scripts_dir)', '--cov-report=term-missing'])
    
    # Run tests
    try:
        result = subprocess.run(
            cmd,
            cwd=str(skill_path),
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        output = result.stdout + "\n" + result.stderr
        success = result.returncode == 0
        
        return success, output
        
    except subprocess.TimeoutExpired:
        return False, "Tests timed out after 5 minutes"
    except FileNotFoundError:
        return False, "pytest not found. Install with: pip install pytest pytest-cov"
    except Exception as e:
        return False, f"Error running tests: {e}"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Run skill tests')
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--coverage', action='store_true', help='Enable coverage reporting')
    parser.add_argument('--output', '-o', help='Save output to file')
    
    args = parser.parse_args()
    
    print(f"🧪 Running tests for: {args.skill_path}")
    print("-" * 50)
    
    success, output = run_tests(args.skill_path, args.coverage)
    
    print(output)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"\nOutput saved to: {args.output}")
    
    if success:
        print("\n✅ Tests PASSED")
        sys.exit(0)
    else:
        print("\n❌ Tests FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
