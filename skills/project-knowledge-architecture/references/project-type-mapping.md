# Project Type Mapping

Use this reference only when the generic rooms need translation into a concrete project.

## Software Product

| Room | Typical authority |
|---|---|
| Rule Gate | `AGENTS.md`, `CLAUDE.md`, `.agent/rules.md` |
| Dashboard | `README.md` top status, `.agent/STATUS.md`, issue board |
| Ledger | ADRs, `CHANGELOG.md`, release notes, planning docs |
| Proof Layer | tests, CI logs, API contracts, fixtures, metrics, production logs |
| Workshop | runbooks, project-local skills, scripts, deployment docs |
| Archive | old ADRs, retired features, migration notes |
| Long-Term Memory | cross-session rule pointers only |

## Research Project

| Room | Typical authority |
|---|---|
| Rule Gate | agent rules, experiment integrity rules |
| Dashboard | current experiment status, latest report |
| Ledger | experiment ledger, plans, reports index |
| Proof Layer | raw outputs, notebooks, audit scripts, statistical reports |
| Workshop | reusable analysis skills, runner docs, code map |
| Archive | old studies, deprecated methods |
| Long-Term Memory | stable judgment rules and authority pointers |

## Data Pipeline

| Room | Typical authority |
|---|---|
| Rule Gate | data handling rules, privacy/security policy |
| Dashboard | pipeline health, current incident or release state |
| Ledger | schema decisions, migration history, data contracts |
| Proof Layer | validation reports, sample fixtures, lineage, monitoring dashboards |
| Workshop | ingestion runbooks, backfill procedures, local scripts |
| Archive | old schemas, retired jobs, past incidents |
| Long-Term Memory | reusable cautions and authority pointers |

## Documentation or Content Site

| Room | Typical authority |
|---|---|
| Rule Gate | style guide, publishing rules |
| Dashboard | current publishing state, open editorial tasks |
| Ledger | content decisions, changelog, release notes |
| Proof Layer | source docs, link checks, build logs, screenshots, review notes |
| Workshop | templates, editorial checklists, publishing scripts |
| Archive | superseded pages, old drafts |
| Long-Term Memory | reader assumptions and authority pointers |

## Early Prototype

Keep it minimal:

- Rule Gate: `AGENTS.md`
- Dashboard: `README.md` top block
- Ledger: `docs/decisions.md` or `plans/`
- Proof Layer: screenshots, test output, demo notes
- Workshop: scripts or `docs/runbook.md`
- Archive: `_archive/` only when needed

Do not create a large governance tree before the project has enough surface area to justify it.
