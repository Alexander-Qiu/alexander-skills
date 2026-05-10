# Agent Rules

This repository is shared by Codex and Claude Code.

## Single Source

- `CLAUDE.md` is the authoritative agent instruction file.
- `AGENTS.md` must stay a symlink alias to `CLAUDE.md`.
- Do not maintain separate Codex-only and Claude-only rule files. Update `CLAUDE.md` once so both agents read the same rules.

## Skill Installation

- `manifests/skills.json` is the source of truth for Codex and Claude Code profiles.
- When adding a shared skill, add it to `skills`, `profiles.codex.default.skills`, and `profiles.claude-code.default.skills`.
- Third-party skills should live under `third-party/` and should keep all referenced support files intact.
- If a skill source is symlinked or provided by a submodule, agents must resolve and read the real target content before using it.

## Git Workflow

- Alexander Qiu (`ruizhi_qiu@foxmail.com`) is the repository owner and defaults to validated direct pushes to `main`.
- Other contributors and agents use feature branches and PRs unless Alexander explicitly authorizes a direct push.
- Before any push to `main`, run the relevant installer/tests and confirm `git status` only contains the intended commit.
- Do not mix unrelated local edits into a skill import or workflow-rule change.

## Current Shared Skill Additions

- `frontend-slides` is a shared Codex and Claude Code skill sourced from `third-party/frontend-slides/plugins/frontend-slides/skills/frontend-slides`.
- Both agents should use the manifest entry rather than copying this skill into separate agent-specific directories.
