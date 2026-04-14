# Bug Pattern Catalog (Frappe Legacy)

## Hook and Lifecycle Collisions

Symptoms:

- duplicate child rows
- repeated ledger updates
- status changes applied twice

Common cause:

- same business action implemented in both controller hook and `doc_events`

Check:

- compare controller lifecycle methods with `hooks.py` handlers for same doctype/event

## Stale Hook Import Paths

Symptoms:

- runtime import error only on specific events

Common cause:

- refactor moved function/module, hooks not updated

Check:

- verify each dotted path in hooks resolves to importable callable

## Non-idempotent Submit/Cancel Logic

Symptoms:

- retrying action produces drift

Common cause:

- write logic assumes single execution path

Check:

- run submit/cancel cycles in tests and inspect side-effect counts

## Relation Integrity Drift

Symptoms:

- missing linked records, broken reports

Common cause:

- link/table writes bypass invariants

Check:

- execute read helpers for orphan links and invalid child-parent relations

## Permission Leakage

Symptoms:

- users can access or mutate records outside expected scope

Common cause:

- missing permission checks in custom methods/report queries

Check:

- audit custom endpoints and query conditions against role design
