---
name: project-knowledge-architecture
description: Use when designing or refactoring a project's standing knowledge-management structure for long-running AI agent work, including agent entrypoints, status surfaces, decision records, proof locations, project procedures, archives, and memory boundaries. Not for requirements brainstorming or single-task planning.
metadata:
  status: experimental
  maturity: thought
  platform: universal
---

# Project Knowledge Architecture

Experimental skill: this is a general method, not a finished framework. Use it as a design lens for project management structure. Do not force every project into the same folders.

## What This Is For

Use this when a project needs to be understandable and maintainable by future agents:

- a new repo needs agent-friendly project management files
- an existing repo has scattered README, status, plans, docs, and memories
- agents keep losing current state after context resets
- project-specific procedures are being mixed into global memory
- evidence for claims is hard to find
- Claude, Codex, or other agents need the same project map

Do not use this as a replacement for:

- `brainstorming`: use that to discover what the project should become
- `planning-with-files`: use that to track one active task
- a cleanup/sync workflow: use that when the job is to reconcile an existing knowledge base against current code

This skill's extra value is the structure rule: control loop for how knowledge changes, and memory palace for where knowledge lives.

## Core Idea

Design project knowledge as a controlled system.

| Control term | Project meaning |
|---|---|
| Target | What a future agent must be able to decide without old chat |
| State | Current project status and active work |
| Sensors | Files, tests, logs, metrics, reports, issues, docs, code |
| Actuators | Project docs, agent rules, skills, runbooks, code, tests |
| Feedback | Re-check claims against proof after each update |

Then design the repo as a memory palace. Each room answers one question. Rooms are roles, not mandatory folder names.

| Room | Question it answers | Common files |
|---|---|---|
| Rule Gate | What rules must every agent obey? | `AGENTS.md`, `CLAUDE.md`, or project-specific equivalents |
| Dashboard | What is true right now? | `.agent/STATUS.md`, `docs/status.md`, `README.md` top block |
| Ledger | How did decisions move over time? | `docs/decisions/`, `plans/`, `CHANGELOG.md`, `journal/` |
| Proof Layer | What proves a claim? | re-checkable artifacts; exact form varies by project type |
| Workshop | How do we repeat project-specific work? | project-local `skills/`, `docs/runbooks/`, scripts |
| Archive | What is old but traceable? | `_archive/`, `docs/archive/`, closed plans |
| Long-Term Memory | What stable rule changes future judgment? | short agent memory pointers only |

Small projects may merge rooms. Large projects may split them. The rule is one job per room, not one universal directory tree.

## Workflow

1. Identify project type.
   - Software product, research project, data pipeline, documentation site, prototype, or mixed.
   - If mixed, choose one main workflow and add only the extra rooms needed.

2. Write the five handoff questions.
   - What is the project for?
   - What is the current state?
   - What is the next action?
   - What proves current claims?
   - Which files or ideas are old, dropped, or only historical?

3. Map the control loop.
   - Target: answer the five questions.
   - State: choose the smallest live status surface.
   - Sensors: list proof sources.
   - Actuators: list files agents are allowed to update.
   - Feedback: define the check that must pass before an agent claims completion.

4. Assign the memory rooms.
   - Put each existing or planned file into one room.
   - If a file tries to be two rooms, split it or narrow its job.
   - If two files contain the same live fact, choose one authority and point the other to it.

5. Keep memory small.
   - Long-term memory stores stable judgment rules and authority pointers.
   - Repeatable procedures belong in project-local skills or runbooks.
   - Current status belongs in project files.
   - Exact proof stays in the proof layer.

6. Run the new-agent test.
   - Open only the rule gate and dashboard first.
   - Check whether a fresh agent can answer the five handoff questions in 5-10 minutes.
   - If not, fix the rooms before adding more process.

## Output Shape

When using this skill, produce a short architecture note with:

```markdown
# Project Knowledge Architecture

## Project Type
<type and why>

## Handoff Questions
1. ...

## Control Loop
- Target:
- State:
- Sensors:
- Actuators:
- Feedback:

## Memory Rooms
| Room | Authority | Update rule |
|---|---|---|

## Proposed File Changes
- create/update ...

## New-Agent Test
- command/read path:
- expected answers:
```

Only create files after the user asks to apply the design or when the task already asks for implementation.

## Project-Type Mapping

Read `references/project-type-mapping.md` to translate the rooms into the current project type.

## Common Mistakes

- Duplicating `brainstorming` or `planning-with-files` instead of designing the standing project structure.
- Treating the seven rooms as mandatory folders.
- Assuming every proof layer looks like research raw data. In software projects, tests and logs may be the proof.
- Putting command sequences into long-term memory.
- Letting README, status, and decision logs all claim to be the latest truth.
- Creating agent-specific entrances when the project is shared by multiple agents.
