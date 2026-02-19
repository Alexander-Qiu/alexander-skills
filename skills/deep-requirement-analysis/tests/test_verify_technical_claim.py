#!/usr/bin/env python3
"""Tests for verify_technical_claim.py"""

import pytest
import sys
import tempfile
import os
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from verify_technical_claim import search_codebase, verify_claim


class TestSearchCodebase:
    """Test codebase search functionality."""
    
    def test_search_existing_pattern(self):
        """Test searching for pattern that exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello():\n    return 'world'\n")
            
            results = search_codebase(tmpdir, "hello")
            assert len(results) > 0
            assert any("hello" in r[2] for r in results)
    
    def test_search_nonexistent_pattern(self):
        """Test searching for pattern that doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def foo():\n    pass\n")
            
            results = search_codebase(tmpdir, "nonexistent")
            assert len(results) == 0
    
    def test_search_case_insensitive(self):
        """Test search is case insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def HelloWorld():\n    pass\n")
            
            results_lower = search_codebase(tmpdir, "helloworld")
            results_upper = search_codebase(tmpdir, "HELLOWORLD")
            
            assert len(results_lower) > 0
            assert len(results_upper) > 0


class TestVerifyClaim:
    """Test claim verification logic."""
    
    def test_claim_structure(self):
        """Test result has all required fields."""
        result = verify_claim("vLLM uses Ray")
        required_fields = ["claim", "verified", "confidence", "evidence", "suggestions"]
        for field in required_fields:
            assert field in result
    
    def test_no_source_dir(self):
        """Test verification without source directory."""
        result = verify_claim("Some technical claim")
        assert result["confidence"] == "low"
        assert len(result["suggestions"]) > 0
    
    def test_with_source_dir(self, tmp_path):
        """Test verification with source directory."""
        # Create test source
        (tmp_path / "test.py").write_text("import ray\nuse_ray = True\n")
        
        result = verify_claim("uses Ray", str(tmp_path))
        assert result["confidence"] in ["medium", "high"]
        assert len(result["evidence"]) > 0
    
    def test_confidence_levels(self, tmp_path):
        """Test confidence levels based on evidence."""
        # No evidence
        result_none = verify_claim("claim", str(tmp_path))
        assert result_none["confidence"] == "low"
        
        # Create some evidence
        for i in range(3):
            (tmp_path / f"test{i}.py").write_text(f"keyword{i}\n" * 2)
        
        result_some = verify_claim("keyword0 keyword1 keyword2", str(tmp_path))
        assert result_some["confidence"] in ["medium", "high"]


class TestIntegration:
    """Integration tests."""
    
    def test_end_to_end(self, tmp_path):
        """Test full workflow."""
        # Create mock codebase
        (tmp_path / "main.py").write_text("""
import asyncio
import ray

def main():
    ray.init()
    return True
""")
        
        result = verify_claim("vLLM uses Ray for distributed inference", str(tmp_path))
        
        assert result["claim"] == "vLLM uses Ray for distributed inference"
        assert isinstance(result["evidence"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
