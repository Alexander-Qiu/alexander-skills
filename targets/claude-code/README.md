# Claude Code Target

Claude Code has two layers:

- shared skills linked into `~/.claude/skills`
- Claude Code plugins installed with `claude plugin marketplace add` and
  `claude plugin install`

```bash
./install.sh --agent claude-code
```

For a local-skills-only install:

```bash
./install.sh --agent claude-code --skip-plugins
```

For a safe preview:

```bash
./install.sh --agent claude-code --dry-run
```
