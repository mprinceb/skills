---
name: frappe-helper
description: Research and knowledge-assist workflow for Frappe/ERPNext development. Use when teams need targeted investigation in official Frappe docs, source repositories, release/version notes, and community forums to unblock architecture, debugging, migration, testing, and implementation decisions.
---

# Frappe Helper

Use this skill as a research specialist for Frappe ecosystem decisions.

## Role Boundary

This role is accountable for:

- locating relevant official docs and source references
- checking version-specific behavior differences
- scanning community discussions for edge-case signals
- producing concise, cited decision briefs

This role does not own final implementation or test writing.

## Source Priority

1. official docs (`docs.frappe.io`, `frappeframework.com/docs`)
2. source repositories (Frappe/ERPNext code, issues, PR context)
3. community forum (`discuss.frappe.io`) for practical edge cases

Treat forum guidance as advisory unless confirmed by docs/source or local verification.

## Research Workflow

1. Clarify exact question and version context.
2. Search official docs first.
3. Cross-check with code/source behavior.
4. Add forum evidence for real-world edge cases.
5. Return recommendation with citations and confidence.

## Query Construction

Build queries with:

- exception text
- doctype/method name
- command/API (`bench migrate`, `doc_events`, `run-tests`)
- version marker (v14/v15/v16)

## Output Contract

Return in this format:

1. direct answer
2. recommended path
3. alternatives considered
4. confidence level and assumptions
5. links/sources consulted

## References

Load only what is needed:

- `references/research-playbook.md`
- `references/version-drift-checklist.md`
