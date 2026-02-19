#!/usr/bin/env python3
"""
智能复杂度评估器
根据任务描述评估复杂度，推荐分析模式
"""

import argparse
import json
import re


def assess_complexity(task_description: str, context: dict = None) -> dict:
    """
    评估任务复杂度
    
    返回:
        - mode: quick/standard/deep
        - score: 1-10
        - reasons: 评估理由
        - estimated_time: 预计分析时间
    """
    score = 0
    reasons = []
    
    text = task_description.lower()
    
    # 1. 任务类型评分
    task_type_scores = {
        "脚本": 1, "script": 1, "工具": 1, "utility": 1,
        "功能": 3, "feature": 3, "api": 2, "接口": 2,
        "模块": 4, "module": 4, "组件": 4, "component": 4,
        "系统": 5, "system": 5, "架构": 5, "architecture": 5,
        "重构": 4, "refactor": 4, "优化": 3, "optimize": 3,
        "迁移": 5, "migration": 5, "拆分": 5, "拆分": 5,
    }
    
    for keyword, task_score in task_type_scores.items():
        if keyword in text:
            score += task_score
            reasons.append(f"任务类型 '{keyword}' (+{task_score})")
            break
    else:
        score += 3  # 默认中等
        reasons.append("未识别具体类型，默认中等复杂度 (+3)")
    
    # 2. 规模关键词
    scale_indicators = {
        "简单": -2, "simple": -2, "小": -1, "small": -1,
        "快速": -1, "quick": -1, "临时": -1, "temporary": -1,
        "复杂": 2, "complex": 2, "大": 2, "large": 2,
        "核心": 2, "core": 2, "关键": 2, "critical": 2,
    }
    
    for keyword, scale_score in scale_indicators.items():
        if keyword in text:
            score += scale_score
            reasons.append(f"规模描述 '{keyword}' ({scale_score:+d})")
    
    # 3. 技术债务/风险关键词
    risk_indicators = [
        "性能", "performance", "并发", "concurrent",
        "安全", "security", "分布式", "distributed",
        "事务", "transaction", "一致性", "consistency",
    ]
    
    for keyword in risk_indicators:
        if keyword in text:
            score += 1
            reasons.append(f"技术风险 '{keyword}' (+1)")
    
    # 4. 依赖数量（从文本中估算）
    dependency_patterns = [
        r"集成 (\w+)", r"integrate (\w+)",
        r"连接 (\w+)", r"connect (\w+)",
        r"使用 (\w+)", r"use (\w+)",
    ]
    
    deps_found = set()
    for pattern in dependency_patterns:
        matches = re.findall(pattern, text)
        deps_found.update(matches)
    
    if deps_found:
        dep_score = min(len(deps_found), 3)  # 最多 +3
        score += dep_score
        reasons.append(f"发现依赖项: {', '.join(list(deps_found)[:3])} (+{dep_score})")
    
    # 5. 时间紧迫性
    if any(kw in text for kw in ["紧急", "urgent", " asap", "马上"]):
        score -= 1
        reasons.append("时间紧急，建议降级分析深度 (-1)")
    
    # 确定模式和预计时间
    if score <= 3:
        mode = "quick"
        estimated_time = "5 分钟"
    elif score <= 7:
        mode = "standard"
        estimated_time = "15-25 分钟"
    else:
        mode = "deep"
        estimated_time = "30-60 分钟"
    
    return {
        "mode": mode,
        "score": score,
        "max_score": 10,
        "reasons": reasons,
        "estimated_time": estimated_time,
        "recommendation": f"建议使用【{mode_to_chinese(mode)}】进行分析"
    }


def mode_to_chinese(mode: str) -> str:
    mapping = {
        "quick": "快速模式",
        "standard": "标准模式",
        "deep": "深度模式"
    }
    return mapping.get(mode, mode)


def main():
    parser = argparse.ArgumentParser(description="评估任务复杂度")
    parser.add_argument("--task", required=True, help="任务描述")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    
    args = parser.parse_args()
    
    result = assess_complexity(args.task)
    
    if args.output == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"复杂度评估结果")
        print(f"=" * 40)
        print(f"推荐模式: {result['recommendation']}")
        print(f"复杂度评分: {result['score']}/{result['max_score']}")
        print(f"预计时间: {result['estimated_time']}")
        print()
        print("评估理由:")
        for reason in result['reasons']:
            print(f"  - {reason}")


if __name__ == "__main__":
    main()
