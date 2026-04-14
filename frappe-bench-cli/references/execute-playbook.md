# Bench Execute Playbook

## Goal

Run precise DB-aware checks and corrective actions through importable Python functions.

## Module placement

Prefer:
- `apps/<app>/<app>/scripts/bench_tasks.py`

Keep utility functions narrow, deterministic, and testable.

## Function contract

- Accept explicit parameters only.
- Return JSON-serializable dicts/lists/scalars.
- For writes, expose `dry_run=True` default.
- Commit only when needed and only in write mode.

## Operational flow

1. Implement read function for baseline.
2. Implement write function with dry-run.
3. Run dry-run via `bench execute` and inspect count/sample.
4. Take backup if impact is meaningful.
5. Run non-dry execution.
6. Run read function again for verification.

## Execute examples

```bash
bench --site <site> execute <app>.scripts.bench_tasks.count_docs --kwargs '{"doctype":"Item"}'
bench --site <site> execute <app>.scripts.bench_tasks.fix_missing_field --kwargs '{"doctype":"Customer","fieldname":"territory","value":"India","dry_run":1}'
```

## Failure handling

- If import path fails, verify module path and app installation.
- `bench execute` already initializes site context; do not call `frappe.init()`/`frappe.connect()` again inside the function.
- If output is empty, ensure function returns data explicitly.
