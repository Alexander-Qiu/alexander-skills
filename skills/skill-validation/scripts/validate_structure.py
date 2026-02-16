#!/usr/bin/env python3
"""
Structure validation for skills.
Checks YAML frontmatter, file organization, and basic requirements.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Tuple


class StructureValidator:
    """Validates skill structure and requirements."""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validations. Returns (is_valid, errors, warnings)."""
        self.errors = []
        self.warnings = []
        
        # Check SKILL.md exists
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("SKILL.md not found")
            return False, self.errors, self.warnings
            
        # Validate frontmatter
        self._validate_frontmatter(skill_md)
        
        # Check for extraneous files
        self._check_extraneous_files()
        
        # Check scripts are executable
        self._check_scripts_executable()
        
        # Check references are used
        self._check_references_used(skill_md)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_frontmatter(self, skill_md: Path):
        """Validate YAML frontmatter."""
        content = skill_md.read_text()
        
        # Check for frontmatter
        if not content.startswith('---'):
            self.errors.append("SKILL.md missing YAML frontmatter")
            return
            
        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.errors.append("Invalid frontmatter format")
            return
            
        try:
            frontmatter = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in frontmatter: {e}")
            return
            
        if not frontmatter:
            self.errors.append("Frontmatter is empty")
            return
            
        # Check required fields
        if 'name' not in frontmatter:
            self.errors.append("Frontmatter missing 'name' field")
        elif not frontmatter['name']:
            self.errors.append("'name' field is empty")
            
        if 'description' not in frontmatter:
            self.errors.append("Frontmatter missing 'description' field")
        elif not frontmatter['description']:
            self.errors.append("'description' field is empty")
        elif len(frontmatter['description']) < 50:
            self.warnings.append("'description' should be >50 chars for good triggering")
            
    def _check_extraneous_files(self):
        """Check for files that shouldn't be in skills."""
        forbidden_files = ['README.md', 'CHANGELOG.md', 'INSTALLATION_GUIDE.md', 'QUICK_REFERENCE.md']
        
        for filename in forbidden_files:
            if (self.skill_path / filename).exists():
                self.warnings.append(f"Extraneous file found: {filename}")
                
    def _check_scripts_executable(self):
        """Check that scripts are executable."""
        scripts_dir = self.skill_path / 'scripts'
        if not scripts_dir.exists():
            return
            
        for script in scripts_dir.iterdir():
            if script.is_file() and not script.name.startswith('.'):
                # Check shebang for Python/Bash scripts
                content = script.read_text()
                if content.startswith('#!'):
                    if not os.access(script, os.X_OK):
                        self.warnings.append(f"Script {script.name} has shebang but is not executable")
                        
    def _check_references_used(self, skill_md: Path):
        """Check that reference files are referenced in SKILL.md."""
        references_dir = self.skill_path / 'references'
        if not references_dir.exists():
            return
            
        skill_content = skill_md.read_text()
        
        for ref_file in references_dir.iterdir():
            if ref_file.is_file():
                # Check if file is referenced
                if ref_file.name not in skill_content:
                    self.warnings.append(f"Reference file {ref_file.name} not referenced in SKILL.md")


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_structure.py <skill-path>")
        sys.exit(1)
        
    skill_path = sys.argv[1]
    
    print(f"🔍 Validating structure: {skill_path}")
    print("-" * 50)
    
    validator = StructureValidator(skill_path)
    is_valid, errors, warnings = validator.validate()
    
    if warnings:
        print("⚠️  Warnings:")
        for w in warnings:
            print(f"   - {w}")
        print()
        
    if errors:
        print("❌ Errors:")
        for e in errors:
            print(f"   - {e}")
        print()
        print("Validation FAILED")
        sys.exit(1)
    else:
        print("✅ Structure validation PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
