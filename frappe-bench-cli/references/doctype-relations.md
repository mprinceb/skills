# DocType Relations and Imports

## Relation Primitives

### Link

- Field type: `Link`
- `options` points to target DocType.
- Stored value is target document `name`.

Use for explicit foreign-key-like references.

### Dynamic Link

- Field type: `Dynamic Link`
- Target DocType is dynamic, usually from another field.

Use when one field may point to multiple DocTypes.

### Table (Child Table)

- Field type: `Table`
- `options` points to child DocType.
- Child rows include relation metadata: `parent`, `parenttype`, `parentfield`, `idx`.

Use for one-to-many detail rows tightly owned by parent.

## Modeling Guidelines

- Prefer `Link` when entity identity matters across transactions.
- Prefer `Table` when line items are lifecycle-bound to one parent.
- Avoid duplicating master data in child rows unless denormalization is required.
- For heavy read paths, add indexes to frequently filtered link fields.

## Refactor and Migration Rules

When renaming/removing fields or doctypes:

1. Identify all consumers:
   - server logic, hooks, client scripts, reports, print formats, fixtures.
2. Create patch to migrate data/state.
3. Update references atomically in one deployment unit.
4. Validate relation integrity with readback checks.

## Import Concepts in Frappe Projects

### Python imports (runtime wiring)

Used by hooks and `bench execute`:

- Example: `my_app.module.path.function_name`

Rules:

- Keep modules import-safe (no side effects at import time).
- Keep callable entrypoints stable or migrate all references.

### Fixture export/import (metadata)

- Define fixture filters in `hooks.py`.
- Export with `bench --site <site> export-fixtures`.
- Commit fixture files with app changes.

Use fixtures for app-owned metadata such as custom fields, property setters, and print formats.

### Record data imports

- Use `bench --site <site> data-import --file <path> --doctype <doctype> --type Insert|Update`.
- Prefer for controlled bulk record loading rather than schema migration.

## Bench Execute Relation Checks

Use read helpers before and after changes:

- Count orphan links.
- Count child rows with missing parents.
- Validate unique constraints at application level.

Pattern:

1. Implement read helper in module.
2. Run with `bench --site <site> execute ...`.
3. Apply patch/fix.
4. Run helper again and compare counts.
