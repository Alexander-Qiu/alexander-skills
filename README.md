# Alexander's Skills

Personal Agent Skills library for Kimi Code CLI and other AI agents.

## Skills

| Skill | Description | Status |
|-------|-------------|--------|
| [kimi-mem](./kimi-mem/) | Cross-session memory management system | ✅ Ready |

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
- Or let Kimi auto-detect based on context

## Skill Structure

```
alexander-skills/
├── README.md
└── kimi-mem/
    ├── SKILL.md              # Skill definition for AI
    ├── package.json          # Node.js dependencies
    ├── tsconfig.json         # TypeScript config
    ├── install.sh            # Quick install script
    ├── src/                  # Source code
    │   ├── mcp/
    │   │   └── server.ts     # MCP server implementation
    │   ├── db/
    │   │   └── connection.ts
    │   ├── services/
    │   │   ├── memory.ts     # Memory CRUD + search
    │   │   └── project.ts    # Project auto-detection
    │   └── cli/
    │       └── index.ts      # CLI tool
    └── scripts/
        └── install.sh
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

1. Create directory: `mkdir my-skill`
2. Add `SKILL.md` with proper frontmatter
3. Add any supporting code/files
4. Update this README
5. Commit and push

### Update existing skill

1. Modify files in skill directory
2. Test locally
3. Update version in SKILL.md if needed
4. Commit and push

## License

MIT - See individual skill directories for details.

## Contributing

This is a personal skill library, but suggestions are welcome via GitHub Issues!
