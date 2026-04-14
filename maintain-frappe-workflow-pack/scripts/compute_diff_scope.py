#!/usr/bin/env python3
"""Compute a workflow-doc refresh scope from a baseline commit."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


DOMAIN_PATTERNS = {
    "sales": (
        "sales_order",
        "sales_invoice",
        "customer",
        "payment_entry",
        "cheque_reciving_entry",
        "cheque_receiving_entry",
        "unit_",
        "apartment",
        "parking",
        "demand_letter",
        "project_change_request",
        "advance_return",
        "customer_to_booking_transfer",
        "customer_to_customer_payment_transfer",
        "supplier_to_customer_payment_transfer",
        "registry_approval_request",
        "registry_docs",
    ),
    "construction": (
        "construction_",
        "engineering_",
        "manpower_",
        "monthly_construction",
        "field_app_engineering",
        "services/cst",
    ),
    "purchase": (
        "purchase_order",
        "purchase_invoice",
        "purchase_receipt",
        "material_request",
        "supplier",
    ),
    "accounting": (
        "fund_",
        "stock_transfer",
        "journal_entry",
        "trial_balance_for_party_with_branch",
        "branch_transactions_report",
    ),
    "remaining": (
        "payroll",
        "salary_slip",
        "attendance",
        "asset",
        "selected_user_permission",
        "rolebased",
        "mcp.py",
        "call_",
    ),
}


WORKFLOW_DOCTYPE_HINTS = {
    "unit_change_entry": "Unit Change Entry",
    "project_change_request": "Project Change Request",
    "unit_booking_items_update": "Unit Booking Items Update",
    "customer_to_customer_payment_transfer": "Customer TO Customer Payment Transfer",
    "unit_booking_status_change_request": "Unit Booking Status Change Request",
}


CORE_TOUCHPOINT_HINTS = {
    "public/py/customer.py": "erpnext.selling.doctype.customer.customer.Customer",
    "public/py/sales_order.py": "erpnext.selling.doctype.sales_order.sales_order.SalesOrder",
    "public/py/payment_entry.py": "erpnext.accounts.doctype.payment_entry.payment_entry.PaymentEntry",
    "public/py/sales_invoice.py": "erpnext.accounts.doctype.sales_invoice.sales_invoice.SalesInvoice",
    "public/py/purchase_order.py": "erpnext.buying.doctype.purchase_order.purchase_order.PurchaseOrder",
    "public/py/purchase_invoice.py": "erpnext.accounts.doctype.purchase_invoice.purchase_invoice.PurchaseInvoice",
    "public/py/purchase_receipt.py": "erpnext.stock.doctype.purchase_receipt.purchase_receipt.PurchaseReceipt",
    "public/py/material_request.py": "erpnext.stock.doctype.material_request.material_request.MaterialRequest",
    "public/py/supplier.py": "erpnext.buying.doctype.supplier.supplier.Supplier",
}


def run(cmd: list[str], cwd: Path) -> str:
    return subprocess.check_output(cmd, cwd=str(cwd), text=True).strip()


def changed_files(repo_root: Path, baseline: str, head: str) -> list[str]:
    output = run(["git", "diff", "--name-only", f"{baseline}..{head}"], repo_root)
    return [line for line in output.splitlines() if line.strip()]


def classify_domains(paths: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {key: [] for key in DOMAIN_PATTERNS}
    result["unclassified"] = []
    for path in paths:
        lowered = path.lower()
        matched = False
        for domain, patterns in DOMAIN_PATTERNS.items():
            if any(pattern in lowered for pattern in patterns):
                result[domain].append(path)
                matched = True
        if not matched:
            result["unclassified"].append(path)
    return {key: value for key, value in result.items() if value}


def touched_workflows(paths: list[str]) -> list[str]:
    found = set()
    for path in paths:
        lowered = path.lower()
        for hint, doctype in WORKFLOW_DOCTYPE_HINTS.items():
            if hint in lowered:
                found.add(doctype)
    return sorted(found)


def touched_core_touchpoints(paths: list[str]) -> list[str]:
    found = set()
    normalized = {path.replace("\\", "/"): path for path in paths}
    for key, target in CORE_TOUCHPOINT_HINTS.items():
        for normalized_path in normalized:
            if normalized_path.endswith(key):
                found.add(target)
    return sorted(found)


def canonical_docs(domains: dict[str, list[str]]) -> list[str]:
    docs = ["business-workflow/00-system-customization-map.md"]
    for domain in domains:
        if domain in {"sales", "construction", "purchase", "accounting", "remaining"}:
            docs.append(f"business-workflow/{domain}/README.md")
    if any(domain in domains for domain in ("sales", "construction", "purchase", "accounting", "remaining")):
        docs.extend(
            [
                "business-workflow/_meta/baseline.md",
                "business-workflow/_meta/baseline.json",
                "business-workflow/_meta/legacy-doc-map.md",
            ]
        )
    return sorted(set(docs))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    head = run(["git", "rev-parse", args.head], repo_root)
    paths = changed_files(repo_root, args.baseline_commit, head)
    domains = classify_domains(paths)
    result = {
        "repo_root": str(repo_root),
        "baseline_commit": args.baseline_commit,
        "head": head,
        "changed_files": paths,
        "domains": domains,
        "workflow_doctypes_to_reread": touched_workflows(paths),
        "erpnext_core_touchpoints_to_reread": touched_core_touchpoints(paths),
        "canonical_docs_to_review": canonical_docs(domains),
    }
    json.dump(result, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
