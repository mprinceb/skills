#!/usr/bin/env python3
"""
Run a first-pass architecture hunt for a Frappe DocType.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_EXTENSIONS = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".sql",
    ".svg",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "dist",
    "build",
    "coverage",
    "env",
    "node_modules",
    "sites",
    "venv",
}
LIFECYCLE_METHODS = {
    "autoname",
    "before_insert",
    "after_insert",
    "validate",
    "before_save",
    "on_update",
    "before_submit",
    "on_submit",
    "before_cancel",
    "on_cancel",
    "before_update_after_submit",
    "on_update_after_submit",
    "on_trash",
}
WRITE_TOKENS = (
    ".insert(",
    ".save(",
    ".submit(",
    ".cancel(",
    ".db_set(",
    "frappe.db.set_value(",
    "frappe.db.sql(",
    "frappe.delete_doc(",
    "frappe.rename_doc(",
    "enqueue(",
    "publish_realtime(",
)
JSON_SIGNAL_KEYS = ('"options"', '"document_type"', '"doc_type"', '"ref_doctype"', '"reference_doctype"')


def scrub_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip()).strip("_").lower()
    return re.sub(r"_+", "_", cleaned)


def pascal_name(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value.strip())
    return "".join(part[:1].upper() + part[1:] for part in parts if part)


def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            yield path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def relpath(path: Path, root: Path) -> str:
    return str(path.relative_to(root))


def find_first_line(lines: list[str], needle: str) -> int:
    for index, line in enumerate(lines, start=1):
        if needle in line:
            return index
    return 1


def guess_symbol(lines: list[str], line_index: int) -> dict | None:
    patterns = (
        ("function", re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
        ("class", re.compile(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)")),
        ("function", re.compile(r"^\s*async\s+def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
        ("function", re.compile(r"^\s*(?:async\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")),
        (
            "function",
            re.compile(
                r"^\s*(?:const|let|var)\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_][A-Za-z0-9_]*)\s*=>"
            ),
        ),
    )
    start = max(0, line_index - 61)
    for idx in range(line_index, start - 1, -1):
        stripped = lines[idx].rstrip()
        for kind, pattern in patterns:
            match = pattern.match(stripped)
            if match:
                return {
                    "kind": kind,
                    "name": match.group(1),
                    "line": idx + 1,
                    "signature": stripped.strip(),
                }
    return None


def add_match(bucket: list[dict], path: Path, root: Path, line_no: int, snippet: str, symbol: dict | None = None, tags=None):
    tags = sorted(set(tags or []))
    item = {
        "path": relpath(path, root),
        "line": line_no,
        "snippet": snippet.strip(),
        "symbol": symbol,
        "tags": tags,
    }
    for existing in bucket:
        if (
            existing["path"] == item["path"]
            and existing["line"] == item["line"]
            and existing["snippet"] == item["snippet"]
            and existing["symbol"] == item["symbol"]
        ):
            existing["tags"] = sorted(set(existing["tags"]) | set(tags))
            return
    bucket.append(item)


def parse_json(path: Path):
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return None


def collect_controller_methods(controller_path: Path, root: Path) -> list[dict]:
    lines = read_text(controller_path).splitlines()
    methods = []
    pattern = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
    for idx, line in enumerate(lines, start=1):
        match = pattern.match(line)
        if not match:
            continue
        name = match.group(1)
        methods.append(
            {
                "path": relpath(controller_path, root),
                "line": idx,
                "method": name,
                "kind": "lifecycle" if name in LIFECYCLE_METHODS else "helper",
            }
        )
    return methods


def scan_controller_writes(controller_path: Path, root: Path, bucket: list[dict]):
    lines = read_text(controller_path).splitlines()
    for idx, line in enumerate(lines):
        if any(token in line for token in WRITE_TOKENS):
            add_match(bucket, controller_path, root, idx + 1, line, symbol=guess_symbol(lines, idx), tags=["write", "controller"])


def collect_schema_summary(schema_path: Path, root: Path) -> dict | None:
    data = parse_json(schema_path)
    if not isinstance(data, dict):
        return None
    fields = data.get("fields") or []
    outgoing_relations = []
    for field in fields:
        if not isinstance(field, dict):
            continue
        if field.get("fieldtype") in {"Link", "Dynamic Link", "Table"}:
            outgoing_relations.append(
                {
                    "fieldname": field.get("fieldname"),
                    "label": field.get("label"),
                    "fieldtype": field.get("fieldtype"),
                    "options": field.get("options"),
                }
            )
    return {
        "path": relpath(schema_path, root),
        "autoname": data.get("autoname"),
        "is_submittable": bool(data.get("is_submittable")),
        "track_changes": bool(data.get("track_changes")),
        "outgoing_relations": outgoing_relations,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a first-pass architecture hunt for a Frappe DocType.")
    parser.add_argument("--root", required=True, help="Frappe app or package root to scan")
    parser.add_argument("--doctype", required=True, help="Target DocType name")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"Root path does not exist or is not a directory: {root}", file=sys.stderr)
        return 2

    doctype = args.doctype
    doctype_slug = scrub_name(doctype)
    class_name = pascal_name(doctype)

    result = {
        "target": {
            "doctype": doctype,
            "slug": doctype_slug,
            "class_name": class_name,
            "root": str(root),
        },
        "doctype_files": [],
        "doctype_summary": None,
        "controller_methods": [],
        "incoming_relations": [],
        "hooks_refs": [],
        "workflow_refs": [],
        "print_refs": [],
        "report_refs": [],
        "code_refs": [],
        "write_refs": [],
        "next_queries": [],
        "summary": {},
    }

    schema_paths = []
    controller_paths = []
    client_paths = []

    for path in iter_text_files(root):
        normalized = path.as_posix()
        if f"/doctype/{doctype_slug}/{doctype_slug}.json" in normalized:
            schema_paths.append(path)
            result["doctype_files"].append({"role": "schema", "path": relpath(path, root)})
        elif f"/doctype/{doctype_slug}/{doctype_slug}.py" in normalized:
            controller_paths.append(path)
            result["doctype_files"].append({"role": "controller", "path": relpath(path, root)})
        elif f"/doctype/{doctype_slug}/{doctype_slug}.js" in normalized:
            client_paths.append(path)
            result["doctype_files"].append({"role": "client", "path": relpath(path, root)})

    if schema_paths:
        result["doctype_summary"] = collect_schema_summary(schema_paths[0], root)

    for controller_path in controller_paths:
        result["controller_methods"].extend(collect_controller_methods(controller_path, root))
        scan_controller_writes(controller_path, root, result["write_refs"])

    for path in iter_text_files(root):
        text = read_text(path)
        lines = text.splitlines()
        lowered_path = path.as_posix().lower()

        if path.suffix.lower() == ".json":
            data = parse_json(path)
            if isinstance(data, dict):
                fields = data.get("fields") or []
                for field in fields:
                    if not isinstance(field, dict):
                        continue
                    if field.get("options") != doctype:
                        continue
                    fieldtype = field.get("fieldtype")
                    if fieldtype not in {"Link", "Dynamic Link", "Table"}:
                        continue
                    owner = data.get("name") or path.parent.name.replace("_", " ").title()
                    result["incoming_relations"].append(
                        {
                            "owner_doctype": owner,
                            "path": relpath(path, root),
                            "fieldname": field.get("fieldname"),
                            "label": field.get("label"),
                            "fieldtype": fieldtype,
                            "options": field.get("options"),
                        }
                    )
                if data.get("document_type") == doctype or data.get("doc_type") == doctype or data.get("ref_doctype") == doctype:
                    bucket = result["workflow_refs"] if "/workflow/" in lowered_path else result["print_refs"] if "/print_format/" in lowered_path else result["report_refs"] if "/report/" in lowered_path else result["code_refs"]
                    needle = '"document_type"' if data.get("document_type") == doctype else '"doc_type"' if data.get("doc_type") == doctype else '"ref_doctype"' if data.get("ref_doctype") == doctype else doctype
                    line_no = find_first_line(lines, needle)
                    add_match(bucket, path, root, line_no, lines[line_no - 1] if lines else doctype)

        for idx, line in enumerate(lines):
            if doctype not in line:
                continue
            symbol = guess_symbol(lines, idx)
            line_no = idx + 1
            tags = []
            if any(token in line for token in WRITE_TOKENS):
                tags.append("write")
                add_match(result["write_refs"], path, root, line_no, line, symbol=symbol, tags=tags)
            for follow_idx in range(idx + 1, min(idx + 13, len(lines))):
                follow_line = lines[follow_idx]
                if any(token in follow_line for token in WRITE_TOKENS):
                    add_match(
                        result["write_refs"],
                        path,
                        root,
                        follow_idx + 1,
                        follow_line,
                        symbol=guess_symbol(lines, follow_idx) or symbol,
                        tags=["write", "near-doctype-ref"],
                    )
            if path.name == "hooks.py":
                add_match(result["hooks_refs"], path, root, line_no, line, symbol=symbol)
            elif "/workflow/" in lowered_path:
                if path.suffix.lower() != ".json" or any(key in line for key in JSON_SIGNAL_KEYS):
                    add_match(result["workflow_refs"], path, root, line_no, line, symbol=symbol)
            elif "/print_format/" in lowered_path:
                if path.suffix.lower() != ".json" or any(key in line for key in JSON_SIGNAL_KEYS):
                    add_match(result["print_refs"], path, root, line_no, line, symbol=symbol)
            elif "/report/" in lowered_path:
                if path.suffix.lower() != ".json" or any(key in line for key in JSON_SIGNAL_KEYS):
                    add_match(result["report_refs"], path, root, line_no, line, symbol=symbol)
            else:
                if path.suffix.lower() == ".json":
                    if any(key in line for key in JSON_SIGNAL_KEYS):
                        add_match(result["code_refs"], path, root, line_no, line, symbol=symbol, tags=tags)
                else:
                    add_match(result["code_refs"], path, root, line_no, line, symbol=symbol, tags=tags)

    if not result["hooks_refs"]:
        result["next_queries"].append("Search hooks.py for shared utilities or scheduler tasks that do not name the DocType directly.")
    if not result["write_refs"]:
        result["next_queries"].append("Search controller and service modules for save, submit, cancel, db_set, and set_value calls around the target flow.")
    if not result["workflow_refs"]:
        result["next_queries"].append("Check workflow, notification, and print artifacts for indirect references or custom fields.")

    result["summary"] = {
        "doctype_files": len(result["doctype_files"]),
        "controller_methods": len(result["controller_methods"]),
        "incoming_relations": len(result["incoming_relations"]),
        "hooks_refs": len(result["hooks_refs"]),
        "workflow_refs": len(result["workflow_refs"]),
        "print_refs": len(result["print_refs"]),
        "report_refs": len(result["report_refs"]),
        "code_refs": len(result["code_refs"]),
        "write_refs": len(result["write_refs"]),
    }

    if args.pretty:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
