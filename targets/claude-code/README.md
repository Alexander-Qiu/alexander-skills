# Claude Code Target

Claude Code has two layers:

- shared skills linked into `~/.claude/skills`
- Claude Code plugins installed with `claude plugin marketplace add` and
  `claude plugin install`

```bash
./install.sh --agent claude-code
./install.sh --agent claude-code --profile plugins
```

For a local-skills-only install:

```bash
./install.sh --agent claude-code --profile frontend --skip-plugins
```

For a safe preview:

```bash
./install.sh --agent claude-code --profile plugins --dry-run
```
