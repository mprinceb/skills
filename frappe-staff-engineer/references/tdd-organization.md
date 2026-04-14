# TDD Organization Playbook

## Goal

Convert raw product requirements into reliable Frappe delivery using role-specialized agents.

## Required Inputs

- requirement statement
- target site/app scope
- non-functional constraints (performance, security, migration window)

## Work Packet Format

Each delegated packet should contain:

- `objective`
- `scope_in`
- `scope_out`
- `acceptance_criteria`
- `risks`
- `validation_commands`

## Sequence

1. staff defines architecture and acceptance criteria
2. sdet creates failing tests and fixtures
3. developer implements minimal passing change
4. staff approves refactor pass
5. staff validates final risk closure

## Anti-Patterns

- implementation before failing tests
- refactor mixed with first-pass bug fix without guard tests
- untracked hook path changes
- migrations without backup/verification plan

## Done Criteria

- acceptance criteria satisfied
- all critical/high tests passing
- invariant checks show expected state
- migration impact documented
- no unresolved high-severity risk
