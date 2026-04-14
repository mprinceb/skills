# Refactor Suggestions from Test Signals

## Trigger Signals

Suggest refactor when tests reveal:

- duplicate logic across doctypes/hooks
- large methods with mixed concerns
- hidden side effects difficult to isolate
- repeated fixture complexity for same behavior

## Suggestion Format

1. `problem`
2. `evidence_from_tests`
3. `proposed_boundary`
4. `minimal_refactor_steps`
5. `guard_tests_required`

## Boundaries

- avoid semantic rewrites during first stabilization
- keep public hook entrypoints stable unless planned migration exists
