#!/usr/bin/env python3
"""Tests for check_analysis_completeness.py"""

import pytest
import sys
from pathlib import Path

scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from check_analysis_completeness import check_completeness, get_checklist_for_mode


class TestGetChecklist:
    """Test checklist generation."""
    
    def test_quick_mode_checklist(self):
        """Test quick mode has shorter checklist."""
        checklist = get_checklist_for_mode("quick")
        assert isinstance(checklist, list)
        assert len(checklist) > 0
    
    def test_standard_mode_checklist(self):
        """Test standard mode checklist."""
        checklist = get_checklist_for_mode("standard")
        assert isinstance(checklist, list)
        assert len(checklist) >= len(get_checklist_for_mode("quick"))
    
    def test_deep_mode_checklist(self):
        """Test deep mode has longest checklist."""
        quick = get_checklist_for_mode("quick")
        standard = get_checklist_for_mode("standard")
        deep = get_checklist_for_mode("deep")
        
        assert len(deep) >= len(standard)
        assert len(standard) >= len(quick)


class TestCheckCompleteness:
    """Test completeness checking."""
    
    def test_complete_analysis(self):
        """Test complete analysis passes."""
        analysis = {
            "phases_completed": ["explore", "question", "analyze", "plan"],
            "outputs": ["design.md", "plan.md"],
            "mode": "standard"
        }
        
        result = check_completeness(analysis)
        assert "complete" in result
        assert "missing" in result
    
    def test_incomplete_analysis(self):
        """Test incomplete analysis is detected."""
        analysis = {
            "phases_completed": ["explore"],
            "outputs": [],
            "mode": "deep"
        }
        
        result = check_completeness(analysis)
        assert not result.get("complete", True)
        assert len(result.get("missing", [])) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
