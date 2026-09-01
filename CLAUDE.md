# Agent Rules

This repository is shared by Codex and Claude Code.

## Single Source

- `CLAUDE.md` is the authoritative agent instruction file.
- `AGENTS.md` must stay a symlink alias to `CLAUDE.md`.
- Do not maintain separate Codex-only and Claude-only rule files. Update `CLAUDE.md` once so both agents read the same rules.

## Skill Installation

- `manifests/skills.json` is the source of truth for Codex and Claude Code profiles.
- When adding a skill, register it under `skills`, then add it only to the profiles whose agents and use cases it actually supports.
- Keep `default` small. Domain packs belong in named profiles such as `frontend`, `docs-media`, `infra`, `research`, and `repo-maintenance`.
- Put obsolete workflow compatibility in `legacy-compat`; never move it back into `default` without current agent validation.
- Third-party skills should live under `third-party/` and should keep all referenced support files intact.
- If a skill source is symlinked or provided by a submodule, agents must resolve and read the real target content before using it.

## Git Workflow

- Agents always use feature branches. Alexander Qiu (`ruizhi_qiu@foxmail.com`) remains the repository owner and decides when to merge.
- Before any push to `main`, run the relevant installer/tests and confirm `git status` only contains the intended commit.
- Do not mix unrelated local edits into a skill import or workflow-rule change.

## Current Shared Skill Additions

- `frontend-slides` is a shared Codex and Claude Code skill sourced from `third-party/frontend-slides/plugins/frontend-slides/skills/frontend-slides`.
- `swarming-with-luna` is Codex-only. It delegates fine-grained, low-risk leaf tasks to `gpt-5.6-luna` while a stronger controller integrates and verifies the work.
- Both agents should use the manifest entry rather than copying this skill into separate agent-specific directories.

## Modernization Boundary

- The legacy methodology skills remain available only for explicit compatibility profiles.
- Do not expose the whole repository or `claude-plugins/` as a recursive skill-discovery root.
- `third-party/pua` is not part of any default profile. Preserve unrelated local work in other checkouts.
