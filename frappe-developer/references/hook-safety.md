# Hook Safety

## Risks

- stale dotted import path
- duplicate side effects between controller and `doc_events`
- behavior drift from changing event timing assumptions

## Rules

1. verify hook path imports before/after changes
2. preserve event semantics unless explicitly planned
3. add regression tests for hook side effects
4. avoid hidden writes in helper functions called by many hooks
