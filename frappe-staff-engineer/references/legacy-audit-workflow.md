# Legacy Audit Workflow

## Goal

Build a reliable map of legacy Frappe behavior before proposing changes.

## Step 1: Context Lock

- identify bench root and target site explicitly
- list installed apps on the target site
- identify target app(s) for audit scope

Commands:

```bash
pwd
ls -1
bench --site <site> list-apps
bench --site <site> version
```

## Step 2: Structural Inventory

Collect these artifacts per app:

- `hooks.py`
- all DocType JSON and controller files
- patch registry (`patches.txt`)
- utility/service modules used by doctypes

Commands:

```bash
rg --files apps/<app>/<app>
rg -n "doc_events|override_doctype_class|override_whitelisted_methods|fixtures|scheduler_events" apps/<app>/<app>/hooks.py
rg --files apps/<app>/<app> | rg "doctype/.+/.+\\.json$|doctype/.+/.+\\.py$"
rg -n "class .*\(Document\)|def validate\(|def before_submit\(|def on_submit\(" apps/<app>/<app>
```

## Step 3: Ownership Graph

For each critical DocType, map:

- schema file
- controller class and lifecycle methods
- hook handlers bound to that doctype
- downstream utilities and shared services

Output as a compact table:

- `doctype`
- `controller`
- `doc_events handlers`
- `shared utils`
- `risk notes`

## Step 4: Runtime Truth Checks

Add read-only execute helpers if needed and validate:

- orphan links
- duplicate child rows
- invalid status transitions
- accounting/state mismatches

Pattern:

1. run read helper (`dry_run=1`)
2. record baseline counts
3. apply fix/migration
4. run helper again

## Step 5: Risk Register

Label findings:

- `critical`: corruption/security/financial defects
- `high`: workflow blocker or broad side-effect risk
- `medium`: localized defects/refactor debt
- `low`: maintainability and style debt

Prioritize remediation by business impact, not file size.
