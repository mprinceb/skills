# Quick Parity Checklist

Use this for a fast pass. Use the richer references for details:
- `route-matrix.md`
- `decision-table.md`
- `reporting-patterns.md`
- `example-prompts.md`

## Before editing

- Read `engineering-frappe-api-contract.md`.
- Generate or update a parity worksheet.
- Identify the exact owning controller, bridge, hook, DocType, report, and test files.
- Confirm whether the task is review-only or implementation.

## Route checks

For each affected route, verify:
- route and HTTP method
- Frappe method path
- exposure mechanism
- param names
- actor/auth inputs
- response fields
- error behavior
- owning DocType/storage path
- current automated coverage

## Ownership checks

- Keep `Construction Status Tracker` and `Construction Status Detail` summary-only.
- Put sub-stages, criteria, daily manpower, submissions, and evidence in execution-layer docs.
- Do not let GET routes create execution docs.
- Do not filter shared manpower reads by actor identity unless the contract explicitly requires that.

## Safety checks

- Do not remove compatibility surfaces unless deployment state is explicitly confirmed safe.
- Do not silently switch auth posture between Cloudflare-forwarded and Frappe-session rules.
- Do not update the contract without updating tests and mirrored references.

## Verification checks

- `py_compile` for edited Python files
- targeted unit tests
- site migrate when schema/report/workspace changes
- site test module for changed surface
- cache clear when Desk/report filters changed

## Reporting checks

If reports are part of the task:
- keep a detailed mode
- prefer branch/project summary modes in the same report
- support `split_by_date` when date-bucket aggregation is needed
- verify query shape and site visibility
