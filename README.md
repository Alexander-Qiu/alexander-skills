# Alexander's Skills

Personal Agent Skills library for Kimi Code CLI and other AI agents.

> ⚠️ **Development Note**: This project uses strict git workflow. See [CONTRIBUTING.md](./CONTRIBUTING.md) and `/skill:git-workflow` before making changes.

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [kimi-mem](./kimi-mem/) | Cross-session memory management system (Kimi) | ✅ Ready |
| [claude-mem](./skills/claude-mem/) | Cross-session memory management system (Claude) | ✅ Ready |
| [git-workflow](./skills/git-workflow/) | Git workflow for skill development | ✅ Ready |

## Quick Start

### 1. Clone the repository

```bash
git clone git@github.com:Alexander-Qiu/alexander-skills.git
cd alexander-skills
```

### 2. Install a skill

#### Option A: User-level (available in all projects)

```bash
mkdir -p ~/.config/agents/skills
cp -r kimi-mem ~/.config/agents/skills/
```

#### Option B: Project-level (only in current project)

```bash
mkdir -p .agents/skills
cp -r kimi-mem .agents/skills/
```

### 3. Setup kimi-mem (if using memory skill)

```bash
cd ~/.config/agents/skills/kimi-mem  # or your install path
npm install
npm run build
kimi mcp add --transport stdio kimi-mem -- node $(pwd)/dist/mcp/server.js
```

### 4. Use in Kimi CLI

```bash
kimi
```

Then:
- `/skill:kimi-mem` - Load the skill manually
- `/skill:git-workflow` - Load git workflow skill
- Or let Kimi auto-detect based on context

## Skill Structure

```
alexander-skills/
├── README.md
├── CONTRIBUTING.md       # ⭐ Development workflow
├── skills/               # Meta skills
│   └── git-workflow/     # Git workflow skill
└── kimi-mem/             # Functional skills
    ├── SKILL.md          # Skill definition for AI
    ├── package.json      # Node.js dependencies
    ├── tsconfig.json     # TypeScript config
    ├── src/              # Source code
    └── ...
```

## 🛠️ Development Workflow

**⚠️ IMPORTANT: Never push directly to main!**

### Quick Workflow

```bash
# 1. Start from fresh main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/my-skill

# 3. Make changes and test
# ... edit files ...
npm run build  # if applicable

# 4. Commit
git add .
git commit -m "feat: Add my-skill"

# 5. Push and create PR
git push -u origin feature/my-skill
# ... create PR on GitHub ...

# 6. After merge, cleanup
git checkout main
git pull origin main
git branch -d feature/my-skill
```

**See full workflow:**
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Detailed contribution guide
- [skills/git-workflow/SKILL.md](./skills/git-workflow/SKILL.md) - AI workflow skill

### Branch Naming

```
feature/<skill-name>     # New skill
fix/<skill-name>-<issue> # Bug fix
docs/<what>              # Documentation
update/<skill-name>      # Update existing
```

## Requirements

### For kimi-mem

- Node.js 18+
- Kimi Code CLI
- SQLite (bundled)

## Usage Examples

### Save a memory

```
User: We fixed that memory leak issue!

AI: Let me record this important finding...

[Uses memory_save tool]
✅ Memory saved (ID: 123)
```

### Search memories

```
User: How did we handle authentication before?

AI: Let me search our memory bank...

[Uses memory_search tool]
Found 3 related memories:
- [42] decision: Use JWT instead of Session
- [38] architecture: Auth service design
- [35] bugfix: Fixed token expiration issue
```

## CLI Tool

Each skill may provide CLI tools:

```bash
# After npm install and build
cd kimi-mem

# Save memory via CLI
node dist/cli/index.js save -t "Important fix" -c "Details..." --type bugfix

# Search memories
node dist/cli/index.js search -q "authentication"

# View recent memories
node dist/cli/index.js recent
```

## Development

### Add a new skill

1. **Create feature branch**: `git checkout -b feature/my-skill`
2. **Create directory**: `mkdir my-skill`
3. **Add SKILL.md** with proper frontmatter
4. **Add supporting code/files**
5. **Test locally**
6. **Commit and push**: Follow [CONTRIBUTING.md](./CONTRIBUTING.md)
7. **Create PR** for review

### Update existing skill

1. **Create fix branch**: `git checkout -b fix/skill-name`
2. **Modify files**
3. **Test locally**
4. **Commit with clear message**
5. **Push and create PR**

## Inspired By

This project is inspired by:
- [obra/superpowers](https://github.com/obra/superpowers) - Complete software development workflow for coding agents

Key lessons from superpowers:
- Systematic development workflow
- Composable, auto-triggering skills
- Test-driven skill development
- Clear documentation patterns

## License

MIT - See individual skill directories for details.

## Contributing

This is a personal skill library, but suggestions are welcome via GitHub Issues!

**Before contributing:**
1. Read [CONTRIBUTING.md](./CONTRIBUTING.md)
2. Use `/skill:git-workflow` in Kimi CLI
3. Follow feature branch workflow
