---
name: vv-field-app-parity
description: Review or implement parity for the Vastu Vihar engineering field app when engineering-frappe-api-contract.md is the source of truth and the task requires comparing Cloudflare routes, Frappe methods, actor/auth assumptions, DocType ownership, incremental endpoint delivery, legacy cleanup, and engineering reporting in this repo. Do not use for generic backend contract work outside this field-app surface.
---

# VV Field App Parity

Use this skill for the Vastu Vihar engineering field-app backend only.

The goal is not just to "match APIs." The goal is to:
- prove route-to-code parity against `engineering-frappe-api-contract.md`
- keep summary state and execution state at the correct data grain
- expose or repair endpoints incrementally
- remove temporary compatibility only when deployment state is explicitly safe
- ship reports and aggregate views on the same execution model

## Start Here

Always read:
- `engineering-frappe-api-contract.md`

Then use the smallest additional artifact that answers the task:
- route ownership and likely tests: `references/route-matrix.md`
- reuse vs extend vs new DocType vs remove: `references/decision-table.md`
- report design and aggregate views: `references/reporting-patterns.md`
- example requests and expected deliverables: `references/example-prompts.md`
- quick parity worksheet generation: `scripts/scaffold_parity_worksheet.py`

## Core Rules

1. Treat the contract as the source of truth for the active engineering surface.
2. Do not force execution history into `Construction Status Detail`.
3. Keep `Construction Status Tracker` and `Construction Status Detail` summary-only.
4. Put sub-stages, criteria, manpower logs, submissions, and photo evidence in execution-layer DocTypes.
5. Keep GET routes non-mutating.
6. Match the declared auth transport model instead of inferring new permission rules.
7. Do not remove compatibility surfaces unless deployment state is explicitly confirmed safe.
8. Update the contract, tests, and any mirrored skill references together when behavior changes.

## Minimal Workflow

### 1. Build the parity worksheet

Use the contract inventory as the route list.

If you want a structured starting artifact, generate one:

```bash
python3 scripts/scaffold_parity_worksheet.py engineering-frappe-api-contract.md
```

Capture for each route:
- route and method
- Frappe method path
- exposure mechanism
- params
- actor/auth inputs
- response and error shape
- owning DocType or storage path
- current tests
- status: present, partial, missing, wrong, obsolete, or intentionally removed

### 2. Trace only the owning files

Start with the route matrix, then read only the specific:
- controller
- bridge
- hook or exposure file
- owning DocType JSON/controller
- report JS/Python/JSON
- owning tests

Do not wander the repo blindly.

### 3. Make the data-ownership decision first

Use `references/decision-table.md`.

Current repo target:
- summary layer: `Construction Status Tracker`, `Construction Status Detail`
- execution layer: `Engineering Milestone`, `Engineering Sub Stage`, `Engineering Sub Stage Criterion`, `Manpower Daily Log`, `Manpower Daily Log Entry`, `Construction Sub Stage Progress Submission`, `Construction Sub Stage Progress Photo`

Treat that as the current repo target, not as a permanent law.

### 4. Implement in narrow increments

Preferred order:
1. method path and param compatibility
2. auth and transition rules
3. non-mutating reads
4. execution-model ownership fixes
5. safe legacy cleanup
6. contract and test updates
7. reports and workspace links

### 5. Verify like a parity task, not a generic code change

Run the smallest relevant set:

```bash
python3 -m py_compile <edited python files>
/home/prince/frappe-bench/env/bin/python -m unittest <test modules>
bench --site <site> migrate
bench --site <site> run-tests --app vastu_vihar --module <module>
bench --site <site> clear-cache
```

Also add route-level assertions when practical for:
- method path or exposure
- param compatibility
- auth boundaries
- non-mutating GET behavior
- declared error behavior
- report summary query shape
- site-sync artifacts when schema, workspace, fixture, or report records changed

## Deployment Safety Rule

If the task proposes deleting compatibility code, old DocTypes, or bridge behavior:
- verify deployment state explicitly first
- if deployment state is unknown, do not remove by default

## Deliverable Shape

When using this skill, return:
- findings or parity summary
- data-ownership decision
- implementation increment
- verification results
- residual risks or unresolved contract decisions

## References

- `references/route-matrix.md`
- `references/decision-table.md`
- `references/reporting-patterns.md`
- `references/example-prompts.md`
