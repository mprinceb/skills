# Testing Bootstrap for Legacy Frappe Apps

## Goal

Create meaningful test coverage quickly for high-risk legacy behavior.

## Coverage First Principles

- test business invariants, not implementation details
- cover hooks and side effects, not only return values
- start narrow around risky flows, then expand

## Initial Test Matrix

Prioritize these buckets:

1. submit/cancel flows on transactional doctypes
2. doctype overrides and custom hook handlers
3. permission-sensitive custom endpoints/methods
4. migration/patch outcomes

## Minimal Test Types

- `happy path`: valid creation and transition
- `guard rails`: expected validation failures
- `side effects`: linked docs/ledger/status updates
- `regression`: exact previously failing scenario

## Skeleton Pattern

```python
import frappe
from frappe.tests.utils import FrappeTestCase


class Test<MyDocType>(FrappeTestCase):
    def test_<behavior_name>(self):
        # setup
        doc = frappe.get_doc({
            "doctype": "<My DocType>",
            # fields
        }).insert()

        # action
        doc.submit()

        # assert
        self.assertEqual(doc.docstatus, 1)
```

## Running Strategy

- run smallest scope first (`--doctype`, `--module`)
- run app suite once targeted tests are stable
- keep flaky integration cases isolated and clearly tagged

Commands:

```bash
bench --site <site> run-tests --doctype "<DocType Name>"
bench --site <site> run-tests --module <app>.<module>
bench --site <site> run-tests --app <app>
```
