# Alexander's Skills

Personal Agent Skills library for Kimi Code CLI and other AI agents.

> ⚠️ **Development Note**: This project uses strict git workflow. See [CONTRIBUTING.md](./CONTRIBUTING.md) and `/skill:git-workflow` before making changes.

## Skills

| Skill | Description | Status | Platform |
|-------|-------------|--------|----------|
| [kimi-mem](./skills/kimi-mem/) | Cross-session memory management system | ✅ Ready | 🟢 Kimi |
| [codex-with-mcp](./skills/codex-with-mcp/) | Use Codex CLI through MCP in Kimi | ✅ Ready | 🟢 Kimi |
| [vllm-deploy-simple](./skills/vllm-deploy-simple/) | Quick install and deploy vLLM locally | ✅ Ready | 🟣 Universal |
| [vllm-deploy-docker](./skills/vllm-deploy-docker/) | Deploy vLLM with Docker | ✅ Ready | 🟣 Universal |
| [find-skills](./skills/find-skills/) | Discover and install agent skills | ✅ Ready | 🟣 Universal |
| [git-workflow](./skills/git-workflow/) | Git workflow for skill development | ✅ Ready | 🟣 Universal |
| [algorithmic-art](./skills/algorithmic-art/) | Creating algorithmic art using p5.js | ✅ Ready | 🟣 Universal |
| [brainstorming](./skills/brainstorming/) | Explore user intent before implementation | ✅ Ready | 🟣 Universal |
| [brand-guidelines](./skills/brand-guidelines/) | Anthropic's official brand colors and typography | ✅ Ready | 🟣 Universal |
| [canvas-design](./skills/canvas-design/) | Create beautiful visual art in PNG/PDF | ✅ Ready | 🟣 Universal |
| [dispatching-parallel-agents](./skills/dispatching-parallel-agents/) | Dispatch 2+ independent tasks in parallel | ✅ Ready | 🟣 Universal |
| [doc-coauthoring](./skills/doc-coauthoring/) | Structured workflow for co-authoring documentation | ✅ Ready | 🟣 Universal |
| [deep-requirement-analysis](./skills/deep-requirement-analysis/) | Production-grade task planner with progressive disclosure | ✅ Ready | 🟢 Kimi |
| [docx](./skills/docx/) | Create and manipulate Word documents | ✅ Ready | 🟣 Universal |
| [executing-plans](./skills/executing-plans/) | Execute written implementation plans | ✅ Ready | 🟣 Universal |
| [finishing-a-development-branch](./skills/finishing-a-development-branch/) | Complete development work with structured options | ✅ Ready | 🟣 Universal |
| [frontend-design](./skills/frontend-design/) | Production-grade frontend interfaces | ✅ Ready | 🟣 Universal |
| [internal-comms](./skills/internal-comms/) | Resources for internal communications | ✅ Ready | 🟣 Universal |
| [mcp-builder](./skills/mcp-builder/) | Guide for creating MCP servers | ✅ Ready | 🟣 Universal |
| [pdf](./skills/pdf/) | Read, extract, create, and manipulate PDFs | ✅ Ready | 🟣 Universal |
| [pptx](./skills/pptx/) | Create and edit PowerPoint presentations | ✅ Ready | 🟣 Universal |
| [receiving-code-review](./skills/receiving-code-review/) | Handle code review feedback properly | ✅ Ready | 🟣 Universal |
| [requesting-code-review](./skills/requesting-code-review/) | Request comprehensive code reviews | ✅ Ready | 🟣 Universal |
| [skill-creator](./skills/skill-creator/) | Guide for creating effective skills | ✅ Ready | 🟣 Universal |
| [slack-gif-creator](./skills/slack-gif-creator/) | Create animated GIFs optimized for Slack | ✅ Ready | 🟣 Universal |
| [subagent-driven-development](./skills/subagent-driven-development/) | Execute plans with independent tasks | ✅ Ready | 🟣 Universal |
| [systematic-debugging](./skills/systematic-debugging/) | Debug bugs and test failures | ✅ Ready | 🟣 Universal |
| [test-driven-development](./skills/test-driven-development/) | TDD workflow for features and bugfixes | ✅ Ready | 🟣 Universal |
| [theme-factory](./skills/theme-factory/) | Styling artifacts with themes | ✅ Ready | 🟣 Universal |
| [using-git-worktrees](./skills/using-git-worktrees/) | Create isolated git worktrees | ✅ Ready | 🟣 Universal |
| [using-superpowers](./skills/using-superpowers/) | How to find and use skills | ✅ Ready | 🟣 Universal |
| [verification-before-completion](./skills/verification-before-completion/) | Verify work before claiming completion | ✅ Ready | 🟣 Universal |
| [web-artifacts-builder](./skills/web-artifacts-builder/) | Create elaborate multi-component web artifacts | ✅ Ready | 🟣 Universal |
| [webapp-testing](./skills/webapp-testing/) | Test local web applications with Playwright | ✅ Ready | 🟣 Universal |
| [writing-plans](./skills/writing-plans/) | Create implementation plans before coding | ✅ Ready | 🟣 Universal |
| [writing-skills](./skills/writing-skills/) | Create and verify skills before deployment | ✅ Ready | 🟣 Universal |
| [xlsx](./skills/xlsx/) | Create and manipulate Excel spreadsheets | ✅ Ready | 🟣 Universal |

**Platform Legend:**
- 🟣 **Universal** - Works with both Kimi and Claude (documentation-based skills)
- 🟢 **Kimi** - Kimi-specific (requires MCP or Kimi-specific features)
- 🔵 **Claude** - Claude-specific (requires Claude-specific features)

> 💡 **Note:** Most documentation-based skills are marked as Universal since the core concepts work across agents. Platform-specific skills typically involve MCP integration or agent-specific tool usage.

## 🧪 Skill Validation

All skills must pass comprehensive validation before release:

```bash
# Quick validation (Levels 1-3)
python skills/skill-validation/scripts/validate_skill.py skills/<skill-name>/

# Headless agent testing (Levels 4-5)
python skills/skill-validation/scripts/test_multi_agent.py skills/<skill-name>/

# Or test specific agent
kimi -p "Test the <skill-name> skill"
claude -p "Test the <skill-name> skill"
```

**Validation Levels:**
| Level | Test | Automated | Required |
|-------|------|-----------|----------|
| 1 | Structure (YAML, files) | ✅ | PR |
| 2 | Unit Tests | ✅ | If scripts |
| 3 | Compatibility | ✅ | PR |
| 4 | **Kimi Integration** | ✅ Headless | **Release** |
| 5 | **Claude Integration** | ✅ Headless | **Release** |

See `/skill:skill-validation` for complete validation framework.

## Quick Start

### 1. Clone the repository

```bash
git clone git@github.com:Alexander-Qiu/alexander-skills.git
cd alexander-skills
```

### 2. Install a skill

> 💡 **Pro Tip:** Kimi CLI automatically loads skills from `~/.config/agents/skills/` and `./.agents/skills/` directories. Place frequently-used skills at user-level, project-specific skills at project-level.

#### Option A: User-level (available in all projects)

```bash
mkdir -p ~/.config/agents/skills
cp -r skills/kimi-mem ~/.config/agents/skills/
```

#### Option B: Project-level (only in current project)

```bash
mkdir -p .agents/skills
cp -r skills/kimi-mem .agents/skills/
```

#### Option C: Symlink for development (auto-update when repo changes)

```bash
# User-level symlink
mkdir -p ~/.config/agents/skills
ln -s $(pwd)/skills/kimi-mem ~/.config/agents/skills/kimi-mem

# Or project-level symlink
mkdir -p .agents/skills
ln -s $(pwd)/skills/kimi-mem .agents/skills/kimi-mem
```

#### Option D: Bulk install all skills

```bash
# Install all skills to user-level
mkdir -p ~/.config/agents/skills
cp -r skills/* ~/.config/agents/skills/

# Or install specific skills only
for skill in kimi-mem git-workflow; do
  cp -r skills/$skill ~/.config/agents/skills/
done
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
