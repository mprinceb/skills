#!/usr/bin/env python3
"""Generate a markdown parity worksheet from the contract inventory table."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List, Tuple


def parse_contract_inventory(lines: Iterable[str]) -> List[Tuple[str, str, str, str, str]]:
    in_inventory = False
    rows: List[Tuple[str, str, str, str, str]] = []

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if line.strip() == "## Contract Inventory":
            in_inventory = True
            continue

        if not in_inventory:
            continue

        if line.startswith("## ") and line.strip() != "## Contract Inventory":
            break

        if not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] == "Frontend Route" or cells[0].startswith("---"):
            continue

        normalized = tuple(cell.strip("`").strip() for cell in cells)
        rows.append(normalized)

    return rows


def render_worksheet(rows: List[Tuple[str, str, str, str, str]]) -> str:
    output = [
        "# Parity Worksheet",
        "",
        "| Route | Method | Frappe Method | Priority | Storage Path | Exposure Source | Current Status | Owning Files | Tests | Gaps / Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for route, method, frappe_method, priority, storage_path in rows:
        output.append(
            f"| {route} | {method} | `{frappe_method}` | {priority} | {storage_path} |  |  |  |  |  |"
        )

    output.append("")
    return "\n".join(output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", help="Path to engineering-frappe-api-contract.md")
    parser.add_argument("-o", "--output", help="Optional output file path")
    args = parser.parse_args()

    contract_path = Path(args.contract)
    rows = parse_contract_inventory(contract_path.read_text(encoding="utf-8").splitlines())
    if not rows:
        raise SystemExit("No contract inventory table found.")

    worksheet = render_worksheet(rows)

    if args.output:
        Path(args.output).write_text(worksheet, encoding="utf-8")
    else:
        print(worksheet)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
