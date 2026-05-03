# Codex Target

Codex uses native skill discovery from `~/.codex/skills`.

```bash
./install.sh --agent codex
```

The default profile is defined in `manifests/skills.json`. It installs shared
skills plus the Codex-specific PUA skill and prompt entrypoint.

Useful checks:

```bash
./install.sh --agent codex --dry-run
ls ~/.codex/skills/pdf/SKILL.md
ls ~/.codex/prompts/pua.md
```
