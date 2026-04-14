# Rerun Diff Playbook

Use this when `business-workflow/_meta/baseline.json` already exists.

## Inputs

- repo root
- current HEAD
- `baseline_commit`
- site name
- source roots from `baseline.json`
- workflow names or doctypes recorded in `baseline.json`

## Diff-First Procedure

1. Read `baseline.json` first.
2. Compute changed files from `baseline_commit..HEAD`.
3. Group changed files by workflow domain.
4. Re-read only the changed repo paths.
5. Re-read site metadata only for affected doctypes or workflow names.
6. Re-read ERPNext or Frappe core only for touched overrides or direct imports.
7. Update only the affected canonical docs and appendices.
8. Update `legacy-doc-map.md` if a changed canonical doc now replaces an old legacy note.
9. Advance `baseline_commit` only after all touched docs are aligned.

## Repo Roots To Prefer

For most Frappe apps, check these first:

- `hooks.py`
- `public/js`
- `public/py`
- `*/custom`
- `*/custom_script`
- `*/doctype`
- `*/report`
- `*/print_format`
- `api`
- `services`
- `scripts`
- `tests`

## Site Metadata To Re-Read

Check only for doctypes touched by the diff:

- `Workflow`
- `Workflow Transition`
- `Workflow Document State`
- `Client Script`
- `Server Script`

## Outputs To Update

- touched domain docs
- `appendices/live-site-workflows.md` if workflow states changed
- `appendices/erpnext-core-touchpoints.md` if override or core-call boundaries changed
- `_meta/baseline.md`
- `_meta/baseline.json`
- `_meta/legacy-doc-map.md` if legacy replacements changed

## Safety Rule

Do not rerun a full repo rediscovery unless:

- no baseline exists
- the canonical pack is clearly incomplete
- repo layout changed enough that domain mapping is no longer trustworthy
