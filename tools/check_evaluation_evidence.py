#!/usr/bin/env python3
"""Verify that an independent LLM evaluation has auditable evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


PLACEHOLDERS = {"", "{agent ID returned by the orchestrator}", "TBD", "TODO", None}
VALID_VERDICTS = {"Pass", "Fix", "Needs Review"}
EVALUATION_DIR = "evaluation"
REPRODUCIBILITY_FIELDS = (
    "evaluated_commit_sha",
    "requirements_hash",
    "eval_cases_hash",
    "artifact_hashes",
    "evaluator_model",
    "evaluator_prompt_version",
    "rubric_version",
    "temperature",
)


def has_substantive_content(path: Path) -> bool:
    if not path.is_file():
        return False
    lines = [line.strip() for line in path.read_text().splitlines()]
    return any(line and not line.startswith("#") for line in lines)


def has_traceability(project_dir: Path) -> bool:
    path = project_dir / EVALUATION_DIR / "traceability.md"
    if not has_substantive_content(path):
        return False
    content = path.read_text()
    return "REQ-" in content and "C-" in content and "E-" in content


def has_loop_log(project_dir: Path, run_id: str) -> bool:
    path = project_dir / EVALUATION_DIR / "evaluation-loop.md"
    if not has_substantive_content(path):
        return False
    content = path.read_text()
    return "```mermaid" in content and run_id in content


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_reproducibility(project_dir: Path, run_dir: Path, receipt: dict) -> list[str]:
    """Validate schema v2 receipts while accepting pre-v2 project history."""
    if receipt.get("receipt_schema_version", 1) < 2:
        return []
    failures: list[str] = []
    for field in REPRODUCIBILITY_FIELDS:
        value = receipt.get(field)
        if value in PLACEHOLDERS or value == {}:
            failures.append(f"{run_dir.name}: {field} is required for receipt schema v2")
    if not isinstance(receipt.get("artifact_hashes"), dict):
        failures.append(f"{run_dir.name}: artifact_hashes must be an object")
    if not isinstance(receipt.get("temperature"), (int, float)):
        failures.append(f"{run_dir.name}: temperature must be numeric")

    # These hashes bind a receipt to the evaluated inputs. They are intentionally
    # compared only when the files still exist; a later edit should not erase an
    # otherwise valid historical evaluation.
    for field, relative_path in (
        ("requirements_hash", "project-requirements.md"),
        ("eval_cases_hash", "evaluation/eval-cases.md"),
    ):
        path = project_dir / relative_path
        if path.is_file() and receipt.get(field) and receipt[field] != sha256_file(path):
            failures.append(f"{run_dir.name}: {field} does not match the evaluated file")
    return failures


def check_run(project_dir: Path, run_dir: Path) -> list[str]:
    failures: list[str] = []
    receipt_path = run_dir / "receipt.json"
    try:
        receipt = json.loads(receipt_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError) as error:
        return [f"{run_dir.name}: receipt.json is missing or invalid ({error})"]

    if receipt.get("evaluator_agent_id") in PLACEHOLDERS:
        failures.append(f"{run_dir.name}: evaluator_agent_id is missing")
    if receipt.get("context_isolation") != "fresh_context":
        failures.append(f"{run_dir.name}: context_isolation must be fresh_context")
    if not receipt.get("started_at") or not receipt.get("completed_at"):
        failures.append(f"{run_dir.name}: started_at and completed_at are required")
    if receipt.get("verdict") not in VALID_VERDICTS:
        failures.append(f"{run_dir.name}: verdict must be Pass, Fix, or Needs Review")
    failures.extend(check_reproducibility(project_dir, run_dir, receipt))
    if not has_substantive_content(run_dir / "evaluator-input.md"):
        failures.append(f"{run_dir.name}: evaluator-input.md is missing or empty")
    if not has_substantive_content(run_dir / "evaluator-result.md"):
        failures.append(f"{run_dir.name}: evaluator-result.md is missing or empty")
    if receipt.get("traceability_required") is not True or not has_traceability(project_dir):
        failures.append(f"{run_dir.name}: required traceability.md must link REQ, C, and E IDs")
    if not has_loop_log(project_dir, run_dir.name):
        failures.append(f"{run_dir.name}: evaluation-loop.md must contain Mermaid and this run ID")

    if receipt.get("evaluation_scope") == "web_app":
        ui_evaluation = receipt.get("ui_evaluation") or {}
        evidence_file = ui_evaluation.get("evidence_file")
        if (
            ui_evaluation.get("required") is not True
            or ui_evaluation.get("tool") != "Playwright"
            or ui_evaluation.get("status") != "completed"
            or not evidence_file
            or not has_substantive_content(run_dir / evidence_file)
        ):
            failures.append(f"{run_dir.name}: Web App evaluation requires completed Playwright evidence")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check evidence required before recording an independent LLM evaluation."
    )
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--run-id", help="Validate one completed run instead of all runs")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    runs_dir = project_dir / EVALUATION_DIR / "runs"
    run_dirs = sorted(path for path in runs_dir.glob("*") if path.is_dir())
    if args.run_id:
        run_dirs = [runs_dir / args.run_id]
    if not run_dirs:
        print("FAIL: no evaluation-runs directory with a completed evaluation was found.")
        return 1

    failures: list[str] = []
    valid_runs = 0
    for run_dir in run_dirs:
        run_failures = check_run(project_dir, run_dir)
        if run_failures:
            failures.extend(run_failures)
        else:
            valid_runs += 1

    if failures:
        print("FAIL: independent LLM evaluation evidence is incomplete.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PASS: {valid_runs} independent LLM evaluation run(s) have complete evidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
