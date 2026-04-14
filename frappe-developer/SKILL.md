---
name: frappe-developer
description: Implementation workflow for Frappe/ERPNext applications in a TDD organization. Use when tasks require writing production code for features and bug fixes in legacy or active apps, based on staff-level plans and SDET failing tests, while preserving hook compatibility, migration safety, and runtime invariants.
---

# Frappe Developer

Use this skill as the code implementation role in a TDD pipeline.

## Role Boundary

This role is accountable for:

- implementing minimal production changes to satisfy failing tests
- preserving existing behavior outside planned scope
- applying safe refactors only when test-protected
- handling migration-aware code updates

This role is not responsible for broad architecture decisions or primary research ownership.

## Inputs Expected

- architecture/plan packet from `frappe-staff-engineer`
- failing tests and fixture strategy from `frappe-sdet`
- research memo from `frappe-helper` when needed

## Red-Green-Refactor Execution

1. Run failing test(s) and confirm baseline failure.
2. Implement minimal change to pass targeted tests.
3. Re-run affected test scope.
4. Refactor only if protected by tests.
5. Re-run broader suite and invariant checks.

## Implementation Rules

- keep hook import paths stable unless migration plan exists
- avoid mixing unrelated refactors with bug fix commits
- preserve backward behavior for existing document flows
- for data/schema changes, use patches/migrations, not ad-hoc manual edits

## Bench Execute Usage

Use `bench execute` for validation helpers and controlled corrections:

- read helper before change
- write helper only after plan approval
- read helper after change to verify delta

## Commands

```bash
bench --site <site> run-tests --doctype "<DocType Name>"
bench --site <site> run-tests --module <app>.<module>
bench --site <site> run-tests --app <app>
bench --site <site> migrate
```

## Output Contract

Return:

1. files/functions changed
2. why this is minimal-safe implementation
3. tests run and result summary
4. remaining risks or follow-up tasks

## References

Load only what is needed:

- `references/implementation-playbook.md`
- `references/hook-safety.md`
- `references/migration-safe-changes.md`
