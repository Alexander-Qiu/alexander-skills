# Skill-Specific Validation Rules

## Type 1: Pure Documentation Skills
Skills with only SKILL.md (no scripts)

**Validation:**
- [ ] Structure validation
- [ ] Kimi loads and triggers correctly
- [ ] Claude loads and triggers correctly
- [ ] Examples are copy-pasteable

## Type 2: Script-Based Skills
Skills with scripts/ directory

**Validation:**
- [ ] All levels
- [ ] Unit tests for all scripts
- [ ] Integration tests for script execution
- [ ] E2E tests for complete workflows

## Type 3: MCP-Based Skills
Skills using MCP protocol

**Validation:**
- [ ] All levels
- [ ] MCP server starts without errors
- [ ] Tools register correctly
- [ ] Tool execution returns valid results
- [ ] Error handling works via MCP

## Type 4: Asset-Based Skills
Skills with assets/ (templates, etc.)

**Validation:**
- [ ] All assets are valid (not corrupted)
- [ ] Assets can be loaded/copied
- [ ] Templates render correctly
- [ ] Assets are referenced correctly from SKILL.md
