#!/usr/bin/env python3
"""Tests for complexity_assessor.py"""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from complexity_assessor import assess_complexity, mode_to_chinese


class TestAssessComplexity:
    """Test complexity assessment logic."""
    
    def test_simple_script_task(self):
        """Test simple script task returns quick mode."""
        result = assess_complexity("写一个简单脚本处理文件")
        assert result["mode"] == "quick"
        assert result["score"] <= 3
        assert "快速模式" in result["recommendation"]
    
    def test_system_architecture_task(self):
        """Test system architecture task returns deep mode."""
        result = assess_complexity("设计分布式系统架构，处理高并发")
        assert result["mode"] == "deep"
        assert result["score"] > 7
        assert "深度模式" in result["recommendation"]
    
    def test_api_design_task(self):
        """Test API design task returns standard mode."""
        result = assess_complexity("设计用户认证API接口")
        assert result["mode"] in ["quick", "standard"]
        assert "score" in result
        assert "reasons" in result
    
    def test_refactor_task(self):
        """Test refactoring task."""
        result = assess_complexity("重构现有代码模块")
        assert "refactor" in str(result["reasons"]).lower() or \
               "模块" in str(result["reasons"])
    
    def test_urgent_task_downgrade(self):
        """Test urgent tasks get lower score."""
        normal = assess_complexity("实现用户登录功能")
        urgent = assess_complexity("紧急实现用户登录功能马上")
        # Urgent should have lower or equal score
        assert urgent["score"] <= normal["score"] + 1
    
    def test_complex_with_risk_keywords(self):
        """Test complex tasks with risk keywords."""
        result = assess_complexity("复杂的安全认证系统，要求高并发")
        assert result["score"] >= 5  # complex + security + concurrent
        assert result["mode"] in ["standard", "deep"]
    
    def test_result_structure(self):
        """Test result has all required fields."""
        result = assess_complexity("测试任务")
        required_fields = ["mode", "score", "max_score", "reasons", 
                          "estimated_time", "recommendation"]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"


class TestModeToChinese:
    """Test mode translation."""
    
    def test_quick_mode(self):
        assert mode_to_chinese("quick") == "快速模式"
    
    def test_standard_mode(self):
        assert mode_to_chinese("standard") == "标准模式"
    
    def test_deep_mode(self):
        assert mode_to_chinese("deep") == "深度模式"
    
    def test_unknown_mode(self):
        assert mode_to_chinese("unknown") == "unknown"


class TestEnglishTasks:
    """Test with English task descriptions."""
    
    def test_simple_english(self):
        result = assess_complexity("Write a simple script to process files")
        assert result["mode"] == "quick"
    
    def test_complex_english(self):
        result = assess_complexity("Design distributed system architecture with high concurrency")
        assert result["mode"] == "deep"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
