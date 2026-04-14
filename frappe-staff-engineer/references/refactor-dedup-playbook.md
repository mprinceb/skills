# Refactor and De-dup Playbook

## Goal

Reduce legacy complexity without changing business behavior.

## Safe Refactor Sequence

1. establish behavior baseline (tests + readback data checks)
2. isolate duplicate logic candidates
3. extract shared function/module with explicit input/output
4. migrate callers incrementally
5. re-run baseline and compare output

## Duplicate Detection Heuristics

Look for repeated patterns in:

- amount/tax calculation blocks
- document status transition guards
- cross-doctype validation predicates
- record creation/update templates

Command examples:

```bash
rg -n "validate_|calculate_|make_|create_|update_" apps/<app>/<app>
rg -n "frappe\.db\.set_value|frappe\.get_doc|frappe\.new_doc" apps/<app>/<app>
```

## Extraction Rules

- extracted logic must be pure where possible
- I/O (DB write, enqueue, API call) should be explicit and testable
- keep old entrypoint wrappers temporarily when external callers depend on them
- do not merge duplicates that differ in critical business semantics

## Validation

After refactor:

- run targeted doctype/module tests
- run invariant readback helpers via `bench execute`
- spot-check changed hooks/events with a real document flow
