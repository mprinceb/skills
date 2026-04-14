# Docs and Forum Research Playbook

## Goal

Use external Frappe knowledge safely during implementation work on legacy apps.

## Preferred Sources

1. Official docs
   - `https://docs.frappe.io/`
   - `https://frappeframework.com/docs/`
2. Source of truth in code
   - Frappe/ERPNext GitHub repositories and current branch code
3. Community experience
   - `https://discuss.frappe.io/`

Treat forum content as advisory, not authoritative.

## When to Search

Search externally when local code inspection is insufficient for:

- lifecycle behavior (`validate`, `on_submit`, hooks order)
- doc_events and override semantics
- migration/patch edge cases
- testing framework behavior and fixtures
- specific errors that may vary by version

## Query Patterns

Use narrow, high-signal queries combining:

- exception text
- doctype name
- API/method name
- Frappe version (if known)

Examples:

- `frappe on_submit doc_events execution order`
- `frappe run-tests doctype FrappeTestCase`
- `discuss.frappe.io "OperationalError" "bench migrate"`
- `docs.frappe.io override_doctype_class`

## Evaluation Rules

Before using an external suggestion:

1. Confirm version relevance (v13/v14/v15+ differences matter).
2. Cross-check with at least one primary source (official docs or source code).
3. Verify fit against local hooks, doctypes, and custom overrides.
4. Prefer reversible changes when confidence is medium.

## Applying Findings

1. Convert insight into a concrete hypothesis for local code.
2. Validate via test or `bench execute` read helper.
3. Implement minimal fix/refactor.
4. Re-validate behavior and data invariants.

## Evidence Standard in Responses

When reporting work, include:

- links to consulted references
- what was adopted vs rejected
- any assumptions inferred from incomplete sources
- how local validation confirmed the final decision
