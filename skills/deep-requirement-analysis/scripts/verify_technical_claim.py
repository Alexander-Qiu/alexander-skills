#!/usr/bin/env python3
"""
Verify technical claims by checking source code or documentation.
Usage: python verify_technical_claim.py --claim "vLLM uses Ray by default" --source-dir /path/to/vllm
"""

import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple


def search_codebase(source_dir: str, pattern: str, file_pattern: str = "*.py") -> List[Tuple[str, int, str]]:
    """Search for pattern in codebase."""
    results = []
    source_path = Path(source_dir)
    
    for file_path in source_path.rglob(file_pattern):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        rel_path = file_path.relative_to(source_path)
                        results.append((str(rel_path), i, line.strip()))
        except Exception:
            continue
    
    return results


def verify_claim(claim: str, source_dir: str = None) -> dict:
    """Verify a technical claim and return evidence."""
    result = {
        "claim": claim,
        "verified": False,
        "confidence": "unknown",
        "evidence": [],
        "suggestions": []
    }
    
    # Extract key terms from claim
    terms = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', claim)
    
    if source_dir and os.path.exists(source_dir):
        # Search for evidence in source code
        for term in terms:
            if len(term) > 3:  # Skip short words
                matches = search_codebase(source_dir, term)
                if matches:
                    result["evidence"].extend(matches[:3])  # Top 3 matches
    
    # Determine confidence based on evidence
    if len(result["evidence"]) > 5:
        result["confidence"] = "high"
    elif len(result["evidence"]) > 0:
        result["confidence"] = "medium"
    else:
        result["confidence"] = "low"
        result["suggestions"].append("No direct evidence found. Consider checking official documentation.")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Verify technical claims")
    parser.add_argument("--claim", required=True, help="The claim to verify")
    parser.add_argument("--source-dir", help="Path to source code directory")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    
    args = parser.parse_args()
    
    result = verify_claim(args.claim, args.source_dir)
    
    if args.output == "json":
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Claim: {result['claim']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Evidence ({len(result['evidence'])} found):")
        for path, line, content in result['evidence'][:5]:
            print(f"  {path}:{line} | {content}")
        if result['suggestions']:
            print("Suggestions:")
            for s in result['suggestions']:
                print(f"  - {s}")


if __name__ == "__main__":
    main()
