---
name: "refactor-hunter"
description: |
  Use for JavaScript, TypeScript, and Python codebases to identify safe refactor candidates and code-splitting opportunities by analyzing the provided path.
---

# Refactor Hunter

Use this skill to diagnose refactor and code-splitting opportunities from repository code and recent activity in a provided path.

## Input Contract

- Required: `code_path` (absolute or workspace-relative path to folder or file).
- Optional: language overrides (`js`, `ts`, `jsx`, `tsx`, `py`).
- Optional: module boundaries or ownership constraints to preserve (team ownership, deployment boundary).
- If `code_path` is missing, ask for it and do not proceed with assumptions.

## Workflow

1. Parse the task and scope first.
- Confirm target repository, target paths, language(s), and hard constraints.
- Confirm acceptance criteria and risk tolerance before proposing large structural changes.
- If the scope includes multiple languages, track findings per language and keep split suggestions language-aware.

2. Build a concise evidence surface.
- Inspect file-level shape (size, depth, ownership, recent edit frequency).
- Inspect dependencies/import graph for hotspots, cycles, and tight coupling.
- Inspect route/module boundaries for mixed responsibilities.
- Inspect duplicate logic and copy-paste patterns across files.
- For JS/TS and Python: also inspect framework-specific hotspots (React components, service layers, ORM/data access modules, CLI entry paths).

3. Score candidates and group into themes.
- Group findings by theme: boundary violations, monolith pressure, shared utility extraction, feature boundaries, data access isolation.
- Assign each theme a priority (`high`, `medium`, `low`) using: risk reduction + test impact + implementation effort + user value.
- Maintain separate priority buckets for each language when mixed stacks are present.

4. Produce a safe, staged plan.
- Emit one `must fix first` slice, one `recommended` slice, and one `defer` list.
- For each action, include: rationale, exact evidence, expected file changes, and a rollback-safe step sequence.
- Flag any suggestion needing missing context as `needs clarification`.

5. Keep recommendations human-reviewable.
- Avoid proposing blind moves; each recommendation must be tied to observed evidence.
- Prefer single-responsibility boundaries and narrow interfaces.
- Prefer extracting modules over broad rewrites.
- When uncertain, ask clarifying questions instead of guessing.
- Always anchor JS/TS findings to exact import paths and Python findings to module/package paths.

## Decision Rules

- Mark `critical` only when there is a clear failure path (cyclic import, untestable hotspot, or repeated failures).
- Propose code-splitting only when the split boundary is semantically stable.
- Preserve public API contracts unless an explicit migration plan is included.
- Never recommend file splits that cross deployment/ownership boundaries without coordination.

## Default Output Shape

- `high` severity findings with evidence and first-step execution order.
- `medium` opportunities with phased rollout suggestions.
- `low` opportunities marked as optional cleanup.
- `unknown-context` items with exact missing inputs to unblock.

## Resource

Use [refactor-checklist.md](references/refactor-checklist.md) for detailed smell patterns and thresholds by language.
