# Frappe Development Reference

## Scope

Use this reference when implementing or debugging server-side and schema-level changes in Frappe apps.

## Canonical App Structure

- `apps/<app>/<app>/hooks.py`: extension points and event wiring.
- `apps/<app>/<app>/<module>/doctype/<doctype>/<doctype>.json`: schema and metadata.
- `apps/<app>/<app>/<module>/doctype/<doctype>/<doctype>.py`: server logic.
- `apps/<app>/<app>/patches/`: optional patch modules.
- `apps/<app>/patches.txt`: patch execution order.

## Lifecycle and Event Model

Typical `Document` lifecycle methods to use carefully:

- `validate`
- `before_save`
- `before_submit`
- `on_submit`
- `on_cancel`
- `on_update_after_submit`

Guidelines:

- Put pure validation in `validate`.
- Avoid expensive DB loops in high-frequency hooks.
- Keep financial/stock side effects confined to submit/cancel flows.
- Make write paths idempotent if hooks can re-run.

## Hooking Strategy (`hooks.py`)

Common patterns:

- `doc_events` for per-DocType event handlers.
- `override_doctype_class` to replace standard controllers.
- `doctype_js` / `doctype_list_js` for client-side behavior.
- `fixtures` to carry app-owned metadata.

Guidelines:

- Prefer explicit DocType names over wildcard hooks.
- Keep hook handlers small and delegate to service modules.
- Use stable dotted import paths; renames break runtime dispatch.

## DocType Change Discipline

When modifying a DocType:

1. Edit schema (`.json`) and controller (`.py`) coherently.
2. Add patch for backfill/migration when existing records require updates.
3. Run `bench --site <site> migrate`.
4. Verify with both new and legacy documents.

## Data and Schema Migrations

Use patches for deterministic transitions:

- Add patch module in app package.
- Register it in `patches.txt`.
- Keep patches re-runnable where possible.
- Return quickly when target state already exists.

Patch quality rules:

- No interactive prompts.
- Avoid broad unbounded updates without guard filters.
- Log summary counts for traceability.

## Query and Write Patterns

Prefer ORM/query APIs unless raw SQL is required:

- `frappe.get_doc`, `frappe.get_all`, `frappe.db.get_value`, `frappe.db.set_value`
- `frappe.qb` / query builder for complex queries

If using SQL:

- Parameterize inputs.
- Minimize vendor-specific assumptions.
- Validate row counts before and after writes.

## Development Command Sequence

Typical loop after code changes:

1. `bench --site <site> migrate` (if schema/patch changed)
2. `bench --site <site> clear-cache` (when metadata/cache effects appear)
3. targeted tests
4. readback check via `bench execute`

## Production Safety

For production-impacting changes:

1. Take backup.
2. Run patch dry-run logic when feasible.
3. Execute migration/change.
4. Verify business-critical doctypes and permissions.
5. Check logs and queues.
