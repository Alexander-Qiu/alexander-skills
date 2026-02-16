#!/usr/bin/env python3
"""
Compatibility checker for skills.
Generates compatibility matrix for Kimi vs Claude.
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set


class CompatibilityChecker:
    """Analyzes skill for cross-agent compatibility."""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.skill_name = self.skill_path.name
        
    def analyze(self) -> Dict:
        """Analyze skill and return compatibility report."""
        report = {
            'skill_name': self.skill_name,
            'features': {},
            'warnings': [],
            'recommendations': []
        }
        
        # Check for Kimi-specific features
        kimi_features = self._check_kimi_features()
        report['features']['kimi'] = kimi_features
        
        # Check for Claude-specific features
        claude_features = self._check_claude_features()
        report['features']['claude'] = claude_features
        
        # Check for potentially incompatible patterns
        warnings = self._check_incompatible_patterns()
        report['warnings'] = warnings
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        return report
    
    def _check_kimi_features(self) -> Dict:
        """Check for Kimi-specific features."""
        features = {
            'mcp_tools': False,
            'kimi_specific_syntax': False,
            'shell_commands': False
        }
        
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text().lower()
            
            # Check for MCP references
            if 'mcp' in content or 'tools:' in content:
                features['mcp_tools'] = True
                
            # Check for Kimi-specific references
            if 'kimi' in content:
                features['kimi_specific_syntax'] = True
                
            # Check for shell command patterns
            if 'shell(' in content or 'bash' in content or '```bash' in content:
                features['shell_commands'] = True
                
        return features
    
    def _check_claude_features(self) -> Dict:
        """Check for Claude-specific features."""
        features = {
            'skill_tool': False,
            'claude_specific_syntax': False,
            'references_pattern': False
        }
        
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            content = skill_md.read_text().lower()
            
            # Check for Claude references
            if 'claude' in content:
                features['claude_specific_syntax'] = True
                
            # Check for skill tool pattern
            if 'skill(' in content or 'readfile' in content:
                features['skill_tool'] = True
                
            # Check for references pattern (common in Claude skills)
            if 'references/' in content:
                features['references_pattern'] = True
                
        return features
    
    def _check_incompatible_patterns(self) -> List[str]:
        """Check for patterns that might cause issues."""
        warnings = []
        
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return warnings
            
        content = skill_md.read_text()
        
        # Check for absolute paths
        if '/home/' in content or '/Users/' in content:
            warnings.append("Absolute paths detected - may not work on all systems")
            
        # Check for hardcoded Python version
        if re.search(r'python3\.\d+', content):
            warnings.append("Hardcoded Python version - consider version-agnostic approach")
            
        # Check for platform-specific commands
        if 'brew install' in content:
            warnings.append("macOS-specific command (brew) - may not work on Linux/Windows")
            
        # Check for untested MCP patterns
        if 'mcp' in content.lower() and 'kimi-mem' not in self.skill_name:
            warnings.append("MCP usage detected - verify compatibility with target agent")
            
        return warnings
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate recommendations based on analysis."""
        recs = []
        
        kimi = report['features']['kimi']
        claude = report['features']['claude']
        
        # Check compatibility
        if kimi['mcp_tools'] and not claude['skill_tool']:
            recs.append("MCP tools may not work in Claude - consider adding Claude alternative")
            
        if kimi['kimi_specific_syntax'] and not claude['claude_specific_syntax']:
            recs.append("Kimi-specific content detected - test in Claude to ensure compatibility")
            
        if claude['claude_specific_syntax'] and not kimi['kimi_specific_syntax']:
            recs.append("Claude-specific content detected - test in Kimi to ensure compatibility")
            
        # Check for missing references
        if (self.skill_path / 'references').exists():
            recs.append("Reference files found - ensure they are loaded only when needed to save context")
            
        return recs
    
    def generate_matrix(self) -> str:
        """Generate markdown compatibility matrix."""
        report = self.analyze()
        
        lines = [
            f"## Compatibility Matrix: {report['skill_name']}",
            "",
            "### Agent Support",
            "",
            "| Feature | Kimi | Claude | Notes |",
            "|---------|------|--------|-------|"
        ]
        
        # Determine overall compatibility
        kimi_support = "✅" if report['features']['kimi']['kimi_specific_syntax'] or not report['features']['claude']['claude_specific_syntax'] else "⚠️"
        claude_support = "✅" if report['features']['claude']['claude_specific_syntax'] or not report['features']['kimi']['kimi_specific_syntax'] else "⚠️"
        
        lines.extend([
            f"| Basic Loading | {kimi_support} | {claude_support} | Based on content analysis |",
            f"| MCP Tools | {'✅' if report['features']['kimi']['mcp_tools'] else '❌'} | ❌ | Claude doesn't support MCP |",
            f"| Scripts | {'✅' if report['features']['kimi']['shell_commands'] else '⚠️'} | {'✅' if report['features']['claude']['skill_tool'] else '⚠️'} | Should work in both |",
            ""
        ])
        
        if report['warnings']:
            lines.extend([
                "### ⚠️ Warnings",
                ""
            ])
            for w in report['warnings']:
                lines.append(f"- {w}")
            lines.append("")
            
        if report['recommendations']:
            lines.extend([
                "### 💡 Recommendations",
                ""
            ])
            for r in report['recommendations']:
                lines.append(f"- {r}")
            lines.append("")
            
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: check_compatibility.py <skill-path> [--output <file>]")
        sys.exit(1)
        
    skill_path = sys.argv[1]
    output_file = None
    
    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    print(f"🔍 Checking compatibility: {skill_path}")
    print("-" * 50)
    
    checker = CompatibilityChecker(skill_path)
    matrix = checker.generate_matrix()
    
    print(matrix)
    
    if output_file:
        with open(output_file, 'w') as f:
            f.write(matrix)
        print(f"\nCompatibility matrix saved to: {output_file}")


if __name__ == "__main__":
    main()
