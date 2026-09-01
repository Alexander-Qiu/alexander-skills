# Codex Target

Codex uses native skill discovery from `~/.codex/skills`.

```bash
./install.sh --agent codex
```

The default profile is defined in `manifests/skills.json`. It contains a small
shared core plus the Codex-specific `swarming-with-luna` skill. PUA is available
only from the explicit `legacy-compat` profile.

Useful checks:

```bash
./install.sh --agent codex --dry-run
ls ~/.codex/skills/pdf/SKILL.md
ls ~/.codex/skills/swarming-with-luna/SKILL.md
```
