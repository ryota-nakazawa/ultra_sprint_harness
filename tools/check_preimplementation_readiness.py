#!/usr/bin/env python3
"""Check that a project has evaluation artifacts before implementation starts."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


EVALUATION_DIR = "evaluation"
REQUIRED_FILES = [
    "eval-profile.md",
    "acceptance-criteria.md",
    "eval-cases.md",
    "traceability.md",
    "evaluation-loop.md",
]

CASE_TYPES = ("代表", "境界", "失敗")
TEST_LEVELS = ("構成・単体", "連携", "業務シナリオ")


def read(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def has_substantive_content(path: Path) -> bool:
    content = read(path)
    return any(line.strip() and not line.strip().startswith("#") for line in content.splitlines())


def ids(pattern: str, content: str) -> set[str]:
    return set(re.findall(pattern, content))


def table_rows_with_id(content: str, id_pattern: str) -> list[str]:
    rows: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and re.search(id_pattern, stripped):
            rows.append(stripped)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    failures: list[str] = []

    evaluation_dir = project_dir / EVALUATION_DIR
    project_requirements_path = project_dir / "project-requirements.md"
    for filename in REQUIRED_FILES:
        path = evaluation_dir / filename
        if not has_substantive_content(path):
            failures.append(f"evaluation/{filename} is missing or has no substantive content")

    if not has_substantive_content(project_requirements_path):
        failures.append("project-requirements.md is missing or has no substantive content")

    acceptance = read(evaluation_dir / "acceptance-criteria.md")
    eval_cases = read(evaluation_dir / "eval-cases.md")
    traceability = read(evaluation_dir / "traceability.md")
    loop = read(evaluation_dir / "evaluation-loop.md")

    c_ids = ids(r"\bC-\d+\b", acceptance)
    e_ids = ids(r"\bE-\d+\b", eval_cases)
    req_ids = ids(r"\bREQ-\d+\b", traceability)

    if not c_ids:
        failures.append("acceptance-criteria.md must contain at least one C- ID")
    if not e_ids:
        failures.append("eval-cases.md must contain at least one E- ID")
    if not req_ids:
        failures.append("traceability.md must contain at least one REQ- ID")

    for case_type in CASE_TYPES:
        if case_type not in eval_cases:
            failures.append(f"eval-cases.md must include a {case_type} case")

    # Only the main case table has the test-level column. Later tables may
    # reference E- IDs as follow-up items and must not be treated as cases.
    eval_case_rows = [
        row for row in table_rows_with_id(eval_cases, r"\bE-\d+\b")
        if len(row.split("|")) >= 10
    ]
    for row in eval_case_rows:
        case_id = re.search(r"\bE-\d+\b", row)
        if case_id and not any(level in row for level in TEST_LEVELS):
            failures.append(f"{case_id.group(0)} must include a valid test level")

    missing_c_links = sorted(c_id for c_id in c_ids if c_id not in traceability)
    missing_e_links = sorted(e_id for e_id in e_ids if e_id not in traceability)
    if missing_c_links:
        failures.append(f"traceability.md does not link acceptance IDs: {', '.join(missing_c_links)}")
    if missing_e_links:
        failures.append(f"traceability.md does not link eval case IDs: {', '.join(missing_e_links)}")

    traceability_req_rows = table_rows_with_id(traceability, r"\bREQ-\d+\b")
    must_req_ids: set[str] = set()
    for row in traceability_req_rows:
        if "Must" in row:
            must_req_ids.update(ids(r"\bREQ-\d+\b", row))
    for req_id in sorted(must_req_ids):
        linked = any(req_id in row and "C-" in row and "E-" in row for row in traceability_req_rows)
        if not linked:
            failures.append(f"{req_id} Must requirement must link at least one C- ID and one E- ID")

    project_requirements = read(project_requirements_path)
    project_req_ids = ids(r"\bREQ-\d+\b", project_requirements)
    missing_req_links = sorted(req_id for req_id in project_req_ids if req_id not in traceability)
    if missing_req_links:
        failures.append(f"traceability.md does not include project requirement IDs: {', '.join(missing_req_links)}")

    if "```mermaid" not in loop:
        failures.append("evaluation-loop.md must include a Mermaid diagram")

    if "TBD" in acceptance or "TODO" in acceptance:
        failures.append("acceptance-criteria.md still contains TBD/TODO")
    if "TBD" in eval_cases or "TODO" in eval_cases:
        failures.append("eval-cases.md still contains TBD/TODO")

    if failures:
        print("FAIL: project is not ready for implementation.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: evaluation artifacts are ready before implementation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
