---
name: frappe-bench-cli
description: Operate and develop Frappe bench instances across development and production environments. Use when tasks involve bench discovery, site targeting, app install/uninstall, migrations, backups/restores, service control, DocType development, hooks, relations, imports/fixtures/patches, bug fixes, feature delivery, refactors, document-driven issue triage (including PDF error reports), or DB-state inspection/corrections via bench execute.
---

# Frappe Bench CLI

Use this skill to run `bench` safely and to implement Frappe app changes correctly.

## Quick Start

1. Discover benches and pick the correct one.
2. Confirm target site and environment (dev vs prod).
3. Confirm target app/module/doctype and current behavior.
4. Snapshot state before risky operations.
5. Execute command sequence.
6. Validate outcome (`list-apps`, `version`, tests, spot checks, logs).

## Discover Bench and Site

- Find benches from a known root:
  - `bench find /home/<user>`
- Verify current directory is a bench root (must contain `apps`, `sites`, `env`):
  - `pwd`
  - `ls -1`
- Enumerate sites:
  - `ls -1 sites`
- Set default site when useful:
  - `bench use <site>`

Always run site commands with explicit site when possible:
- `bench --site <site> <frappe-command>`

## Frappe Development Model

Use these rules when changing business logic.

### App and Module Layout

- App root: `apps/<app>/`
- Python package: `apps/<app>/<app>/`
- DocType path:
  - `apps/<app>/<app>/<module>/doctype/<doctype>/<doctype>.json`
  - `apps/<app>/<app>/<module>/doctype/<doctype>/<doctype>.py`
  - optional client script: `<doctype>.js`
- Hook configuration: `apps/<app>/<app>/hooks.py`
- Patch registration: `apps/<app>/patches.txt`

### DocType and Controller

- `<doctype>.json` defines schema, field types, permissions, naming, and metadata.
- `<doctype>.py` (class extending `Document`) defines behavior:
  - `validate`, `before_save`, `before_submit`, `on_submit`, `on_cancel`, etc.
- Prefer keeping cross-doctype orchestration in services/util modules, not oversized controllers.

### Relations in Frappe

- `Link` field:
  - Stores the target document name.
  - `options` is target DocType.
- `Dynamic Link` field:
  - Target DocType comes from another field.
- `Table` field:
  - Child table relation to another DocType (usually `istable=1`).
  - Child rows carry `parent`, `parenttype`, `parentfield`, `idx`.
- Refactor-safe rule:
  - Treat renames/deletions as migrations (patches + data backfill), not raw field edits.

### Imports and Data Movement

Two meanings of imports matter in Frappe work:

1. Python import paths:
  - Bench commands like `execute` and hooks use dotted paths (`app.module.func`).
  - Keep callable functions importable without side effects.
2. Data/config imports:
  - Fixtures (`hooks.py` + `bench export-fixtures`) for app-owned metadata.
  - Data import tooling (`bench --site <site> data-import`) for record-level imports.
  - Patches (`patches.txt`) for deterministic schema/data transitions.

## Environment Mode (Dev vs Prod)

Treat environment mode as an operational branch:

- Development:
  - Use `bench start` for foreground process orchestration.
  - Use `bench --site <site> migrate` after schema/patch changes.
  - Use `bench build` when assets need rebuilding.

- Production:
  - Use service-managed flows (`supervisor`/`systemd`) instead of `bench start`.
  - Typical setup commands:
    - `bench setup production <user>`
    - `bench restart --supervisor` or `bench restart --systemd`
  - Avoid broad `bench update` runs without explicit scope and backup posture.

## Core Operational Recipes

- App install:
  - `bench --site <site> install-app <app_name>`
- App uninstall (preview first):
  - `bench --site <site> uninstall-app <app_name> --dry-run`
  - `bench --site <site> uninstall-app <app_name> -y`
- Migration:
  - `bench --site <site> migrate`
- List installed apps:
  - `bench --site <site> list-apps`
- Site backup:
  - `bench --site <site> backup --with-files`
- Restore:
  - `bench --site <site> restore <sql_file_path> [options]`

For multi-site benches, avoid implicit "all sites" operations unless explicitly required.

## Development Workflows

### Issue Intake from Documents (PDF/Doc/Text)

Use this when the input is an error report document (for example a multi-page PDF).

1. Extract issues into structured items:
   - `issue_id`, `site`, `app`, `doctype`, `error_message`, `traceback`, `repro_steps`, `expected_behavior`.
2. Normalize each item:
   - infer missing `site`/`app` from traceback paths and command context.
3. De-duplicate similar errors by stack signature.
4. Prioritize:
   - data-loss/security/financial breakage first, then blocking workflow bugs, then minor defects.
5. Execute each item through Bug Fix Workflow and record:
   - root cause, files changed, migration needed, validation evidence.

When input is a PDF, pair this skill with PDF extraction workflow before debugging.

### Bug Fix Workflow

1. Reproduce on target site (or equivalent dev site).
2. Locate ownership:
   - DocType controller, hook, server method, report/query, client script, or patch.
3. Write minimal failing test where practical.
4. Implement fix in the smallest stable layer.
5. Run:
   - `bench --site <site> migrate` if schema/patch touched.
   - relevant test command(s).
6. Validate record state with read-only `bench execute` helper.

### New Feature Workflow

1. Model first:
   - DocType changes (`.json`), relations (`Link`/`Table`), constraints.
2. Implement behavior:
   - controller methods, services, hooks, client script.
3. Add migration/patch for existing data if required.
4. Run `bench --site <site> migrate`.
5. Verify end-to-end with representative records and permissions.

### Refactor Workflow

1. Preserve behavior first:
   - snapshot key outputs, queries, and side effects.
2. Extract logic into reusable service modules.
3. Keep public hook paths stable, or migrate callers in one change.
4. Use patches for renamed fields/doctypes and data rewrites.
5. Re-run tests + targeted `bench execute` state checks.

## Bench Execute First-Class Pattern

For DB/state inspection or targeted data corrections, prefer `bench execute` with importable functions instead of large inline shell snippets.

### Rules

- Write DB logic in a Python module file inside an app (or an existing utilities module).
- Expose a small function with clear inputs and return value.
- Execute via dotted import path with `bench --site <site> execute <module.func>`.
- Pass structured args with `--args` or `--kwargs`.
- Keep functions idempotent when possible.
- For write operations, implement a `dry_run` flag and default it to safe behavior.

### Example Function File

Create/update a module like:
- `apps/<app>/<app>/scripts/bench_tasks.py`

Use patterns like:

```python
import frappe


def count_docs(doctype: str, filters: dict | None = None):
    filters = filters or {}
    return {"doctype": doctype, "count": frappe.db.count(doctype, filters=filters)}


def fix_missing_field(doctype: str, fieldname: str, value, dry_run: bool = True):
    names = frappe.get_all(doctype, filters={fieldname: ["in", [None, ""]]}, pluck="name")
    if dry_run:
        return {"dry_run": True, "affected": len(names), "names": names[:50]}

    for name in names:
        frappe.db.set_value(doctype, name, fieldname, value, update_modified=False)

    frappe.db.commit()
    return {"dry_run": False, "updated": len(names)}
```

Execute examples:

```bash
bench --site <site> execute <app>.scripts.bench_tasks.count_docs --kwargs '{"doctype":"Sales Invoice"}'
bench --site <site> execute <app>.scripts.bench_tasks.fix_missing_field --kwargs '{"doctype":"Customer","fieldname":"territory","value":"India","dry_run":1}'
```

### Args and Kwargs Notes

`bench execute` evaluates `--args` / `--kwargs` as Python expressions.

- Prefer JSON-like literals with quotes.
- Avoid untrusted input.
- Booleans should be Python-style (`True`/`False`) if strictly evaluated as Python literals.
- When uncertain, pass `1`/`0` for flags and cast inside function.

## Safe Change Protocol

Before destructive or bulk updates:

1. Confirm bench root and target site explicitly.
2. Run read-only preview (`dry_run`, `count`, `get_all` sample).
3. Take backup (`bench --site <site> backup --with-files`) when impact is non-trivial.
4. Execute write path.
5. Re-validate with read query and app/site health checks.

Before DocType or relation changes:

1. Identify all dependent doctypes/hooks/reports/client scripts.
2. Plan forward migration (and rollback strategy if production).
3. Apply schema + code + data patch together.
4. Run `bench --site <site> migrate`.
5. Verify both new documents and legacy documents.

## Validation Checklist

After changes, run a minimal post-check set:

- `bench --site <site> list-apps`
- `bench --site <site> version`
- `bench --site <site> migrate` (only if required by the task)
- relevant `bench execute` readback function
- inspect logs in `logs/` when command errors are ambiguous

## References

Load only when needed:
- `references/command-reference.md`
- `references/execute-playbook.md`
- `references/frappe-development.md`
- `references/doctype-relations.md`
- `references/issue-intake-playbook.md`
