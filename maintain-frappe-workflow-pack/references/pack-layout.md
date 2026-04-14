# Canonical Pack Layout

Use this layout as the default target structure for a workflow-pack repo.

```text
business-workflow/
├── README.md
├── 00-system-customization-map.md
├── _meta/
│   ├── baseline.md
│   ├── baseline.json
│   ├── rerun-protocol.md
│   └── legacy-doc-map.md
├── appendices/
│   ├── live-site-workflows.md
│   ├── erpnext-core-touchpoints.md
│   ├── reports-print-formats-and-dashboards.md
│   └── open-gaps-and-unresolved.md
├── sales/
│   ├── README.md
│   ├── 01-customer-project-unit-foundation.md
│   ├── 02-unit-booking-sales-order.md
│   ├── 03-cheque-collection-and-payment-entry.md
│   ├── 04-sales-invoice-demand-letter-and-tax.md
│   └── 05-booking-change-transfer-and-refund-flows.md
├── construction/
│   ├── README.md
│   ├── 01-construction-status-tracker-and-unit-sync.md
│   ├── 02-engineering-execution-and-manpower.md
│   └── 03-construction-to-sales-payment-sync.md
├── purchase/
│   ├── README.md
│   ├── 01-mr-po-pr-pi-buying-chain.md
│   └── 02-site-stock-and-transfer-flows.md
├── accounting/
│   ├── README.md
│   ├── 01-branch-fund-transfer-and-fit.md
│   └── 02-journal-payment-and-inter-branch-practices.md
└── remaining/
    ├── README.md
    ├── 01-registry-legal-and-post-booking.md
    ├── 02-payroll-incentive-and-attendance-support-flows.md
    └── 03-ops-permissions-and-integration-surfaces.md
```

## Rules

- `README.md` at the root is the entrypoint for humans and agents.
- `_meta/` stores rerun state and replacement policy, not business flow narratives.
- `appendices/` stores cross-cutting evidence that spans multiple domains.
- Domain docs should group behaviors by process, not by file.
- Use numbered filenames when the reading order matters.

## Minimal Pack

If the task is only one domain slice, still create:

- `business-workflow/README.md`
- `business-workflow/_meta/baseline.md`
- `business-workflow/_meta/baseline.json`
- `business-workflow/_meta/legacy-doc-map.md`
- at least one domain README and one domain doc
