# Test Pattern Catalog (Frappe)

## Lifecycle Pattern

Validate status transitions and side effects across:

- draft validation
- submit transition
- cancel rollback behavior

## Hook Collision Pattern

Detect duplicate effects where both controller methods and `doc_events` fire.

Assertions:

- no duplicate rows
- no double ledger/value updates
- deterministic final status

## Permission Pattern

Validate record access and mutation constraints by role/user context.

## Invariant Pattern

Assert structural invariants:

- no orphan links
- child rows tied to valid parent
- required unique/business constraints preserved

## Regression Pattern

For every fixed bug:

1. add failing test from original scenario
2. verify pass after implementation
3. keep regression test permanent
