# Agent Install Guide

This repository can install the same skill source tree into Codex or Claude Code.
The installer uses symlinks, so updates in this folder are picked up by the
agent-specific skill directory without copying files.

If this is a fresh clone, initialize bundled third-party skill sources first:

```bash
git submodule update --init --recursive
```

## Codex

```bash
./install.sh --agent codex
```

This links the small default profile into:

- `~/.codex/skills`

Preview without writing:

```bash
./install.sh --agent codex --dry-run
```

Install additional packs explicitly; repeated runs add links without removing
the existing default links:

```bash
./install.sh --agent codex --profile frontend
./install.sh --agent codex --profile infra
./install.sh --agent codex --profile repo-maintenance
./install.sh --agent codex --profile legacy-compat
```

## Claude Code

```bash
./install.sh --agent claude-code
```

This links the small shared default into `~/.claude/skills`. Plugins are an
explicit pack:

```bash
./install.sh --agent claude-code --profile plugins
```

Preview plugin commands without running them:

```bash
./install.sh --agent claude-code --profile plugins --dry-run
```

Install an optional skill pack without any plugin commands:

```bash
./install.sh --agent claude-code --profile frontend --skip-plugins
```

## Safety

The installer validates every source and target before creating the first
link. It refuses to overwrite existing non-symlink files or directories.
Replacing a regular file or directory requires a backup destination:

```bash
./install.sh --agent codex --dry-run --replace --backup-dir /tmp/alexander-skills-backup
./install.sh --agent codex --replace --backup-dir /tmp/alexander-skills-backup
```

Existing backups are never overwritten. Review dry-run output before the
live migration.

Agent target directories can be overridden for isolated tests:

```bash
./install.sh --agent codex --home /tmp/alexander-skills-test
```
