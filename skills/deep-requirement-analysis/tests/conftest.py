#!/usr/bin/env python3
"""Pytest configuration for deep-requirement-analysis tests."""

import pytest
import sys
from pathlib import Path

# Add scripts directory to Python path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))


@pytest.fixture
def sample_task_description():
    """Return a sample task description for testing."""
    return "设计一个用户认证系统，支持JWT和OAuth2"


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory with some files."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("def main():\n    pass\n")
    (tmp_path / "src" / "utils.py").write_text("def helper():\n    return True\n")
    return tmp_path
