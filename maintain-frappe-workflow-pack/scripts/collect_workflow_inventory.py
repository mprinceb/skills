#!/usr/bin/env python3
"""Collect a first-pass workflow inventory for a Frappe app repo."""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from pathlib import Path


SOURCE_ROOT_CANDIDATES = (
    "hooks.py",
    "public/js",
    "public/py",
    "api",
    "services",
    "scripts",
    "tests",
)


def run(cmd: list[str], cwd: Path | None = None) -> str:
    completed = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def find_app_package(repo_root: Path) -> Path | None:
    hooks = sorted(repo_root.glob("*/hooks.py"))
    return hooks[0].parent if hooks else None


def read_hooks_summary(hooks_path: Path) -> dict[str, object]:
    summary: dict[str, object] = {
        "path": str(hooks_path),
        "override_doctype_class_keys": [],
        "doctype_js_keys": [],
        "doctype_list_js_keys": [],
        "doc_events_keys": [],
        "override_doctype_dashboards_keys": [],
        "scheduler_event_buckets": [],
    }
    try:
        tree = ast.parse(hooks_path.read_text(encoding="utf-8"), filename=str(hooks_path))
    except Exception as exc:  # pragma: no cover - best effort inventory
        summary["parse_error"] = str(exc)
        return summary

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        value = node.value
        if isinstance(value, ast.Dict):
            keys = [k.value for k in value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
            if name == "override_doctype_class":
                summary["override_doctype_class_keys"] = sorted(keys)
            elif name == "doctype_js":
                summary["doctype_js_keys"] = sorted(keys)
            elif name == "doctype_list_js":
                summary["doctype_list_js_keys"] = sorted(keys)
            elif name == "doc_events":
                summary["doc_events_keys"] = sorted(keys)
            elif name == "override_doctype_dashboards":
                summary["override_doctype_dashboards_keys"] = sorted(keys)
            elif name == "scheduler_events":
                summary["scheduler_event_buckets"] = sorted(keys)
    return summary


def find_bench_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in [current] + list(current.parents):
        if (candidate / "sites").exists() and (candidate / "apps").exists():
            return candidate
    return None


def relative_paths(paths: list[Path], root: Path) -> list[str]:
    return [str(path.relative_to(root)) for path in sorted(paths)]


def site_workflows(bench_root: Path, site: str) -> dict[str, object]:
    workflows_json = run(
        [
            "bench",
            "--site",
            site,
            "execute",
            "frappe.get_all",
            "--kwargs",
            '{"doctype":"Workflow","filters":{"is_active":1},"fields":["name","document_type","is_active"]}',
        ],
        cwd=bench_root,
    )
    workflows = json.loads(workflows_json or "[]")
    return {
        "active_workflows": workflows,
        "workflow_names": sorted(row["name"] for row in workflows),
        "workflow_doctypes": sorted({row["document_type"] for row in workflows}),
    }


def build_inventory(repo_root: Path, site: str | None) -> dict[str, object]:
    app_package = find_app_package(repo_root)
    if not app_package:
        raise SystemExit(f"No app package with hooks.py found under {repo_root}")

    hooks_path = app_package / "hooks.py"
    bench_root = find_bench_root(repo_root)

    inventory: dict[str, object] = {
        "repo_root": str(repo_root.resolve()),
        "app_package": app_package.name,
        "git_head": run(["git", "rev-parse", "HEAD"], cwd=repo_root),
        "hooks": read_hooks_summary(hooks_path),
        "doctypes": relative_paths(list(app_package.glob("**/doctype/*/*.json")), repo_root),
        "reports": relative_paths(list(app_package.glob("**/report/*/*.py")), repo_root),
        "print_formats": relative_paths(list(app_package.glob("**/print_format/*/*.json")), repo_root),
        "custom_metadata": relative_paths(list(app_package.glob("**/custom/*.json")), repo_root),
        "public_js": relative_paths(list((repo_root / app_package.name / "public/js").glob("*.js")) if (repo_root / app_package.name / "public/js").exists() else [], repo_root),
        "public_py": relative_paths(list((repo_root / app_package.name / "public/py").glob("*.py")) if (repo_root / app_package.name / "public/py").exists() else [], repo_root),
        "api_modules": relative_paths(list(repo_root.glob("**/api/*.py")), repo_root),
        "service_modules": relative_paths(list(repo_root.glob("**/services/**/*.py")), repo_root),
        "script_modules": relative_paths(list(repo_root.glob("**/scripts/*.py")), repo_root),
        "tests": relative_paths(list(repo_root.glob("**/tests/test_*.py")), repo_root),
        "source_roots": [root for root in SOURCE_ROOT_CANDIDATES if (repo_root / app_package.name / root).exists() or (repo_root / root).exists()],
    }

    if site:
        if not bench_root:
            raise SystemExit(f"Could not determine bench root above {repo_root}")
        inventory["site"] = site
        inventory["bench_root"] = str(bench_root)
        try:
            inventory["site_workflows"] = site_workflows(bench_root, site)
        except subprocess.CalledProcessError as exc:
            inventory["site_workflows_error"] = {
                "message": "Could not read live site workflows. Rerun with a bench context that can write logs or with escalated permissions.",
                "command": exc.cmd,
                "returncode": exc.returncode,
                "stderr": getattr(exc, "stderr", None),
            }

    return inventory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--site", help="Optional bench site name for active workflow inventory")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    inventory = build_inventory(args.repo_root.resolve(), args.site)
    json.dump(inventory, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
