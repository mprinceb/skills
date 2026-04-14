---
name: maintain-frappe-workflow-pack
description: Build or refresh a canonical business-workflow knowledge pack for a Frappe/ERPNext app. Use when Codex must inventory customizations across repo code, live site metadata, and ERPNext core touchpoints; replace overlapping legacy docs with canonical workflow docs; track baseline commits for diff-only reruns; and align AGENTS.md with the workflow documentation process.
---

# Frappe Workflow Pack Maintainer

## Overview

Use this skill to create or refresh a canonical `business-workflow/` pack for a Frappe app.

This skill is the documentation maintainer layer above `frappe-arch-hunter` and `frappe-staff-engineer`.
It does not replace those skills. It reuses their evidence-gathering and decomposition patterns inside one repeatable workflow.

## When To Use

Use this skill when the user asks to:

- hunt customizations across a Frappe or ERPNext app
- document business workflows in `business-workflow/`
- replace stale workflow notes or legacy docs
- align workflow docs with current code, site metadata, and ERPNext core behavior
- track a baseline commit for future diff-only reruns
- define or update `AGENTS.md` so future agents follow the workflow-pack process

Do not use this skill for isolated code fixes or one-off DocType explanation requests unless the user clearly wants canonical documentation.

## Core Rules

1. Treat `business-workflow/` as the only canonical workflow knowledge pack.
2. Treat old `docs/` notes as hints, not source of truth.
3. Verify every major claim from one or more of these evidence layers:
   - repo code
   - live site metadata
   - ERPNext or Frappe core touchpoints
4. Prefer diff-first refreshes over full rediscovery when a baseline exists.
5. Delete legacy docs only when the canonical replacement for that slice already exists.
6. Keep `AGENTS.md` stable and process-oriented. Put moving state such as commit hashes in workflow metadata files, not in `AGENTS.md`.

## Operating Modes

- `bootstrap-pack`
  First run. No canonical baseline exists yet.
- `refresh-pack`
  Re-run from a stored baseline commit and inspect only changed repo paths plus affected site and core touchpoints.
- `slice-hunt`
  Document one subsystem or business flow incrementally.
- `legacy-replace`
  Remove old docs only after the canonical replacement lands.
- `agents-sync`
  Create or refresh `AGENTS.md` so future agents follow this process.

## Workflow

1. Lock context.
   - Identify repo root, bench root, site, app package, current HEAD, and whether `business-workflow/_meta/baseline.json` exists.
   - Use explicit site scope for bench reads.
2. Choose mode.
   - If no baseline exists, run `bootstrap-pack`.
   - If baseline exists, run `refresh-pack`.
3. Build the inventory.
   - Scan hooks, overrides, custom metadata JSON, custom doctypes, public JS, public Python overrides, reports, print formats, APIs, services, scripts, tests, and existing documentation.
   - Record active site workflows and their states if a site is available.
   - Record ERPNext or Frappe base classes or helper modules touched by overrides or monkey patches.
   - Use `scripts/collect_workflow_inventory.py` for a first-pass machine summary.
4. Map affected domains.
   - Group findings into `sales`, `construction`, `purchase`, `accounting`, and `remaining`.
   - For refreshes, use `scripts/compute_diff_scope.py` to narrow the re-read scope.
5. Write or update canonical docs.
   - Follow the canonical layout in `references/pack-layout.md`.
   - Follow the section and evidence rules in `references/evidence-and-labeling.md`.
   - Use the markdown template in `references/output-template.md`.
6. Replace legacy docs slice-by-slice.
   - Update `business-workflow/_meta/legacy-doc-map.md`.
   - Delete overlapping `docs/*.md` files only after the replacement exists.
   - Follow `references/legacy-replacement-policy.md`.
7. Update metadata.
   - Update `baseline.md`, `baseline.json`, and `rerun-protocol.md` only after the canonical docs are aligned.
8. Sync `AGENTS.md` when needed.
   - Point future agents to this skill and the canonical workflow metadata.

## Evidence Layers

Always work across these layers when the touched workflow needs them:

1. Repo code
   - `hooks.py`
   - `public/js`
   - `public/py`
   - `custom/`
   - `custom_script/`
   - `doctype/`
   - `report/`
   - `print_format/`
   - `api/`
   - `services/`
   - `scripts/`
   - `tests/`
2. Live site metadata
   - `Workflow`
   - `Workflow Transition`
   - `Workflow Document State`
   - any in-scope `Client Script` or `Server Script`
3. ERPNext or Frappe core touchpoints
   - base DocType classes being subclassed or monkey patched
   - helper modules directly imported by overrides

## Required Outputs

For each major domain or workflow doc, return in this order:

1. scope and assumptions
2. ownership graph
3. write paths and side effects
4. reconstructed business flows
5. Mermaid diagrams
6. reports, print formats, dashboards, and live workflow states if relevant
7. unresolved gaps and next probes

## Mermaid Rules

- Use `flowchart TD` for structural ownership maps.
- Use `sequenceDiagram` for request-to-side-effect flows.
- Use `stateDiagram-v2` when workflow states or document statuses matter.
- Keep node labels short and move nuance into notes below the diagram.

## Baseline Model

The canonical metadata lives under `business-workflow/_meta/`.

Required files:

- `baseline.md`
- `baseline.json`
- `legacy-doc-map.md`
- `rerun-protocol.md`

Use `baseline.json` as the machine-readable contract for future reruns.
Track at least:

- `baseline_commit`
- `site`
- `app_versions`
- `workflow_names`
- `source_roots`
- `erpnext_core_touchpoints`
- `canonical_docs`
- `superseded_legacy_docs`
- `last_audit_date`

## Refresh Discipline

When a baseline exists:

1. Read `baseline.json` first.
2. Compute changed files from `baseline_commit` to `HEAD`.
3. Re-read only affected repo paths.
4. Re-read live workflows only for doctypes touched by the diff.
5. Re-read ERPNext or Frappe core only for touched overrides or direct core calls.
6. Update only affected canonical docs and metadata.
7. Advance the baseline only after alignment is complete.

Use `references/rerun-diff-playbook.md` and `scripts/compute_diff_scope.py`.

## AGENTS Sync Rules

If the repo needs `AGENTS.md` or its guidance is stale:

- point future agents to the canonical `business-workflow/` pack
- tell them to use this skill for pack creation and refreshes
- tell them to read `business-workflow/_meta/baseline.json` before refresh work
- tell them not to use legacy `docs/` as the source of truth

Keep `AGENTS.md` process-level and durable.
Do not store changing operational data such as the current baseline hash inside it.

## Escalation Rules

- Stay read-only during discovery unless the task explicitly includes writing docs or skill files.
- If site metadata is needed, use explicit bench and site scope.
- Record the exact bench commands used for live metadata checks.
- If the task turns into implementation or bug-fixing, switch to `frappe-staff-engineer` for planning and `frappe-developer` for code changes.

## Resources

- `references/pack-layout.md`
- `references/evidence-and-labeling.md`
- `references/rerun-diff-playbook.md`
- `references/legacy-replacement-policy.md`
- `references/output-template.md`
- `scripts/collect_workflow_inventory.py`
- `scripts/compute_diff_scope.py`
