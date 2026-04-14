# Example Prompts

Use these to keep outputs consistent.

## 1. Review parity only

Prompt:

```text
Use $vv-field-app-prity to review engineering-frappe-api-contract.md against the current backend and tell me what is missing or mismatched.
```

Expected deliverable:
- findings ordered by severity
- route or DocType ownership gaps
- test gaps
- no speculative code plan unless requested

## 2. Decide whether to reuse or create new DocTypes

Prompt:

```text
Use $vv-field-app-prity to decide whether this field-app requirement should extend existing DocTypes or introduce new execution-layer DocTypes.
```

Expected deliverable:
- decision per requirement
- why the current grain is right or wrong
- impact on CST/CSD vs execution layer

## 3. Implement missing endpoint incrementally

Prompt:

```text
Use $vv-field-app-prity to implement the missing field-app endpoint with contract parity and verify it.
```

Expected deliverable:
- what increment was implemented
- owning files changed
- verification commands and results
- any remaining contract gaps

## 4. Remove legacy compatibility safely

Prompt:

```text
Use $vv-field-app-prity to remove the legacy field-app compatibility surface if deployment state is safe.
```

Expected deliverable:
- explicit deployment-state check
- what was removed and why
- what stayed because safety was not proven

## 5. Add app-side reports

Prompt:

```text
Use $vv-field-app-prity to add Desk reports and branch/project summary views for engineering manpower and construction updates.
```

Expected deliverable:
- report ownership and backing DocTypes
- detailed vs summary mode design
- filters
- verification including site report tests and cache clear
