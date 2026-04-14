# DocType Hunt Playbook

## Goal

Build a reliable map of how one DocType is defined, triggered, mutated, and observed across a Frappe app.

## Context Lock

Capture these inputs before searching:

- bench root
- site
- app
- module
- target DocType
- exact business question

Useful commands:

```bash
pwd
bench --site <site> list-apps
bench --site <site> version
python3 scripts/doctype_arch_hunt.py --root apps/<app>/<app> --doctype "<DocType>"
```

## Static Sweep

Run focused searches after the first-pass script:

```bash
rg --files apps/<app>/<app> | rg "doctype/.+/.+\\.(json|py|js)$|hooks\\.py$|patches\\.txt$"
rg -n "\"<DocType>\"|frappe\\.get_doc\\(\"<DocType>\"|frappe\\.new_doc\\(\"<DocType>\"" apps/<app>/<app>
rg -n "\"options\": \"<DocType>\"|\"document_type\": \"<DocType>\"|\"doc_type\": \"<DocType>\"|\"ref_doctype\": \"<DocType>\"" apps/<app>/<app>
rg -n "doc_events|override_doctype_class|override_whitelisted_methods|scheduler_events|fixtures" apps/<app>/<app>/hooks.py
```

## Ownership Graph

Capture at least these columns:

- `doctype`
- `schema/controller/client`
- `lifecycle methods`
- `hook handlers`
- `shared utilities or services`
- `downstream doctypes`
- `entrypoints`
- `risk notes`

Use the `frappe-staff-engineer` framing: map control points first, then supporting utilities.

## Effectful Patterns

Prioritize functions containing:

- `insert(`
- `save(`
- `submit(`
- `cancel(`
- `amend`
- `rename_doc`
- `delete_doc`
- `db_set(`
- `frappe.db.set_value(`
- `frappe.db.sql(`
- `enqueue(`
- `publish_realtime(`

Treat these as likely write paths or side effects until proven otherwise.

## Runtime Truth

Use `frappe-bench-cli` discipline when static evidence is not enough:

1. write or reuse a read-only `bench execute` helper
2. run it with explicit site scope
3. record counts, samples, or invariant failures
4. keep write helpers out of the hunt unless the task changes

## Knowledge Merge Rules

When combining multiple traces into learning material:

- keep one canonical note per DocType
- keep one canonical note per business process
- append evidence instead of replacing earlier findings without explanation
- mark uncertain edges as open questions
- separate confirmed flows from suspected flows

## Hand-Off Rule

If the hunt turns into implementation work:

- switch to `frappe-staff-engineer` to define the change packet
- switch to `frappe-developer` only after the failure mode and target behavior are clear
