# CI/CD Integration

## GitHub Actions Workflow

```yaml
# .github/workflows/skill-validation.yml
name: Skill Validation

on:
  pull_request:
    paths:
      - 'skills/**'
  push:
    branches: [main]

jobs:
  structure-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate skill structures
        run: python scripts/validate_all_skills.py

  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        skill: ${{ fromJson(needs.detect-changes.outputs.changed_skills) }}
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
          cd skills/${{ matrix.skill }} && pip install -r requirements.txt || true
      - name: Run tests
        run: |
          cd skills/${{ matrix.skill }} && pytest tests/ -v --cov=scripts

  compatibility-report:
    runs-on: ubuntu-latest
    needs: [structure-validation, unit-tests]
    steps:
      - uses: actions/checkout@v3
      - name: Generate compatibility matrix
        run: python scripts/generate_compatibility_matrix.py
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: compatibility-report
          path: reports/compatibility.md
```

## Headless Testing in CI

**Kimi Headless:**
```yaml
- name: Test with Kimi
  run: |
    python skills/skill-validation/scripts/test_with_kimi.py \
      skills/${{ matrix.skill }}/ -o kimi-report.json
  continue-on-error: true
```

**Claude Headless:**
```yaml
- name: Test with Claude
  run: |
    python skills/skill-validation/scripts/test_with_claude.py \
      skills/${{ matrix.skill }}/ -o claude-report.json
  continue-on-error: true
```

**Requirements:**
- Kimi CLI installed and authenticated
- Claude Code installed and authenticated
- Skills temporarily installed in agent-specific directories
