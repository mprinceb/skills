---
name: frappe-sdet
description: Senior SDET workflow for Frappe/ERPNext codebases. Use when tasks require writing or expanding automated tests for legacy apps, turning bugs into failing tests, designing risk-based test matrices for DocTypes/hooks/overrides, validating migrations, and suggesting testability-oriented refactors.
---

# Frappe SDET

Use this skill to own test design and test writing in a TDD workflow.

## Role Boundary

This role is accountable for:

- converting requirements and bugs into failing tests first
- selecting test scope (doctype/module/app) by risk
- creating robust fixtures and reproducible datasets
- identifying refactor suggestions that improve testability

This role does not own large implementation changes; hand those to `frappe-developer`.

## Inputs Expected

From planner/staff role:

- acceptance criteria
- impacted doctypes/hooks/services
- risk level and migration context
- known regressions

## Core Workflow

1. Build test matrix by risk.
2. Write failing tests for required behavior and regressions.
3. Provide minimal fixture strategy.
4. Hand failing tests to developer.
5. After implementation, verify pass state and expand edge coverage.

## Test Matrix Prioritization

Order by risk:

1. data/financial/security critical flows
2. submit/cancel state transitions
3. hook side effects and override paths
4. permission boundaries and query conditions
5. non-critical validations/UI-adjacent behavior

## Legacy App Test Bootstrap

When coverage is weak:

1. start with one transactional doctype
2. add regression for each known bug
3. add hook collision tests
4. add invariant checks for relations

Focus on stability over sheer test count.

## Test Patterns

Use these patterns repeatedly:

- lifecycle tests: `validate -> submit -> cancel`
- hook side-effect tests: assert linked docs/state updates
- permission tests: deny/allow for role-context calls
- migration tests: pre-state -> patch/migrate -> post-state
- invariants: orphan links, duplicate child rows, invalid transitions

## Commands

```bash
bench --site <site> run-tests --doctype "<DocType Name>"
bench --site <site> run-tests --module <app>.<module>
bench --site <site> run-tests --app <app>
```

Use smallest scope first, then broaden.

## Refactor Suggestions Contract

When suggesting refactors, include:

1. duplicated logic location
2. risk if left unchanged
3. extraction proposal (function/module boundary)
4. required guard tests

Keep suggestions behavior-preserving and incremental.

## Output Contract

Return:

1. failing/passing test summary
2. newly added tests and what behavior they protect
3. fixture/data strategy used
4. refactor suggestions (if any) with risk notes

## References

Load only when needed:

- `references/test-pattern-catalog.md`
- `references/legacy-coverage-ramp.md`
- `references/refactor-suggestions.md`
