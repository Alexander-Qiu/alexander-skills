#!/usr/bin/env python3
"""Tests for generate_analysis_report.py"""

import pytest
import sys
import json
import tempfile
from pathlib import Path

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_analysis_report import generate_report, format_section


class TestGenerateReport:
    """Test report generation."""
    
    def test_report_structure(self):
        """Test generated report has required sections."""
        analysis_data = {
            "task": "Test task",
            "mode": "quick",
            "findings": [{"topic": "Security", "analysis": "Needs auth"}],
            "recommendations": ["Add JWT"]
        }
        
        report = generate_report(analysis_data)
        assert "Test task" in report
        assert "Security" in report or "findings" in str(report).lower()
    
    def test_format_section(self):
        """Test section formatting."""
        content = ["Point 1", "Point 2"]
        formatted = format_section("Test Section", content)
        assert "Test Section" in formatted
        assert "Point 1" in formatted
        assert "Point 2" in formatted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
