# Alexander's Skills

Personal Agent Skills library for Kimi Code CLI and other AI agents.

## Skills

| Skill | Description |
|-------|-------------|
| [kimi-mem](./kimi-mem/) | Cross-session memory management system |

## Installation

### For Kimi Code CLI

```bash
# Clone the repository
git clone git@github.com:Alexander-Qiu/alexander-skills.git

# Install a skill to user directory
cp -r alexander-skills/kimi-mem ~/.config/agents/skills/

# Or install to project directory
cp -r alexander-skills/kimi-mem ./.agents/skills/
```

### Usage

```bash
# Start Kimi CLI and load skill
kimi /skill:kimi-mem
```

## Skill Structure

```
alexander-skills/
├── README.md
└── kimi-mem/
    └── SKILL.md
```

## License

MIT
