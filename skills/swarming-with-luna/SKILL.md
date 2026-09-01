---
name: swarming-with-luna
description: Use in Codex when two or more simple, independent, low-risk tasks can be delegated to gpt-5.6-luna; avoid coupled, ambiguous, or high-consequence work.
---

# Swarming with Luna

Use `gpt-5.6-luna` as a fast, economical leaf-task executor. A stronger controller owns decomposition, architectural judgment, integration, and final verification.

## Delegation gate

Delegate only tasks that are:

- independent of other in-flight tasks;
- narrow enough to complete from explicit inputs;
- limited to one file, one check, or one mechanical transformation;
- easy for the controller to verify with a diff, assertion, or command.

Keep ambiguous requirements, cross-cutting refactors, security decisions, conflict resolution, production changes, and final review with the stronger controller.

## Shape tasks for Luna

Split more finely than for a flagship model. Give each worker:

1. one concrete objective;
2. exact files or facts it may read;
3. explicit write ownership, or state that the task is read-only;
4. one expected output format;
5. one verification command or acceptance check;
6. relevant constraints inline, without requiring broad repository exploration.

Workers editing files must have disjoint ownership. If safe ownership cannot be stated in one sentence, do not parallelize the edits.

## Dispatch

- Select model `gpt-5.6-luna` with low or medium reasoning.
- Use the host's Fast service tier only when that control is actually exposed. Luna is a model choice; it does not by itself prove Fast-tier execution.
- Respect available concurrency rather than hard-coding a worker count.
- If the host exposes `AgentSwarm`, provide at least two distinct `items` and a `prompt_template` containing the literal `{{item}}` placeholder.
- With individual subagents, create one worker per leaf task and give every worker a distinct scope.

## Controller review

Treat worker output as a proposal. The controller reads every changed file or evidence item, checks scope, and runs the relevant verification. Give Luna one focused correction when the issue is local and obvious; otherwise move the task to a stronger model. Never ask Luna workers to approve one another's final result.
