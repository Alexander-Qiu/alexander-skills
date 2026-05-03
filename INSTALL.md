# Agent Install Guide

This repository can install the same skill source tree into Codex or Claude Code.
The installer uses symlinks, so updates in this folder are picked up by the
agent-specific skill directory without copying files.

## Codex

```bash
./install.sh --agent codex
```

This links the default profile into:

- `~/.codex/skills`
- `~/.codex/prompts` for prompt entrypoints such as `pua.md`

Preview without writing:

```bash
./install.sh --agent codex --dry-run
```

## Claude Code

```bash
./install.sh --agent claude-code
```

This links shared skills into `~/.claude/skills` and installs the Claude Code
plugins listed in `manifests/skills.json`.

Install only local skill symlinks and skip marketplace/plugin commands:

```bash
./install.sh --agent claude-code --skip-plugins
```

Preview plugin commands and skill links without writing:

```bash
./install.sh --agent claude-code --dry-run
```

## Safety

The installer refuses to overwrite existing non-symlink files or directories.
Use `--replace` only after checking `--dry-run` output.

Agent target directories can be overridden for isolated tests:

```bash
./install.sh --agent codex --home /tmp/alexander-skills-test
```
