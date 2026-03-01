#!/usr/bin/env python3
"""Tests for Claudeception skill."""

import os
import subprocess
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_skill_structure():
    """Test that skill has required files."""
    required_files = ['SKILL.md', 'README.md', 'LICENSE']
    for file in required_files:
        path = os.path.join(SKILL_DIR, file)
        assert os.path.exists(path), f"Missing required file: {file}"
    print("✅ Structure test passed")


def test_skill_md_exists():
    """Test SKILL.md exists and has content."""
    skill_md = os.path.join(SKILL_DIR, 'SKILL.md')
    assert os.path.exists(skill_md), "SKILL.md not found"
    
    with open(skill_md, 'r') as f:
        content = f.read()
    
    assert len(content) > 1000, "SKILL.md seems too short"
    assert '---' in content, "SKILL.md missing YAML frontmatter"
    assert 'name:' in content, "SKILL.md missing name field"
    print("✅ SKILL.md test passed")


def test_scripts_executable():
    """Test that scripts are executable."""
    scripts_dir = os.path.join(SKILL_DIR, 'scripts')
    if os.path.exists(scripts_dir):
        for script in os.listdir(scripts_dir):
            script_path = os.path.join(scripts_dir, script)
            if os.path.isfile(script_path):
                assert os.access(script_path, os.X_OK), f"{script} is not executable"
    print("✅ Scripts executable test passed")


def test_examples_structure():
    """Test examples directory structure."""
    examples_dir = os.path.join(SKILL_DIR, 'examples')
    assert os.path.exists(examples_dir), "examples/ directory not found"
    
    examples = os.listdir(examples_dir)
    assert len(examples) >= 3, f"Expected at least 3 examples, found {len(examples)}"
    
    for example in examples:
        example_path = os.path.join(examples_dir, example)
        if os.path.isdir(example_path):
            skill_file = os.path.join(example_path, 'SKILL.md')
            assert os.path.exists(skill_file), f"{example}/SKILL.md not found"
    
    print("✅ Examples structure test passed")


def test_shell_script_syntax():
    """Test shell script syntax."""
    script_path = os.path.join(SKILL_DIR, 'scripts', 'claudeception-activator.sh')
    if os.path.exists(script_path):
        result = subprocess.run(
            ['bash', '-n', script_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Shell script syntax error: {result.stderr}"
    print("✅ Shell script syntax test passed")


if __name__ == '__main__':
    print("Running Claudeception tests...")
    print("=" * 50)
    
    test_skill_structure()
    test_skill_md_exists()
    test_scripts_executable()
    test_examples_structure()
    test_shell_script_syntax()
    
    print("=" * 50)
    print("✅ All tests passed!")
