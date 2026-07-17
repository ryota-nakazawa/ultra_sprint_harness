#!/usr/bin/env python3
"""Fail when a project records a formal verdict without subagent evidence."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


FORMAL_VERDICT_RE = re.compile(r"\b(Pass|Fix|Needs Review)\b")
REFERENCE_MARKERS = ("参考確認", "self-check", "自己確認")
INDEPENDENT_MARKERS = ("独立 LLM 評価", "独立LLM評価", "評価サブエージェント", "fresh_context")
EVALUATION_DIR = "evaluation"


def read(path: Path) -> str:
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def has_formal_verdict(project_dir: Path) -> bool:
    evaluation_dir = project_dir / EVALUATION_DIR
    status = read(evaluation_dir / "evaluation-status.md")
    if not status:
        return False

    for line in status.splitlines():
        if any(marker in line for marker in REFERENCE_MARKERS):
            continue
        if "正式判定" in line and FORMAL_VERDICT_RE.search(line):
            return True
        if any(marker in line for marker in INDEPENDENT_MARKERS) and FORMAL_VERDICT_RE.search(line):
            return True

    for filename in ("acceptance-criteria.md", "eval-cases.md", "sprint-metrics.md"):
        content = read(evaluation_dir / filename)
        for line in content.splitlines():
            if any(marker in line for marker in REFERENCE_MARKERS):
                continue
            if any(marker in line for marker in INDEPENDENT_MARKERS) and FORMAL_VERDICT_RE.search(line):
                return True
    return False


def valid_llm_runs(project_dir: Path) -> list[Path]:
    runs_dir = project_dir / EVALUATION_DIR / "runs"
    valid: list[Path] = []
    for receipt_path in sorted(runs_dir.glob("*/receipt.json")):
        try:
            receipt = json.loads(receipt_path.read_text())
        except json.JSONDecodeError:
            continue
        if (
            receipt.get("evaluation_kind") == "independent_llm"
            and receipt.get("context_isolation") == "fresh_context"
            and receipt.get("evaluator_agent_id")
            and receipt.get("completed_at")
            and receipt.get("verdict") in {"Pass", "Fix", "Needs Review"}
        ):
            valid.append(receipt_path.parent)
    return valid


def check_evidence(project_dir: Path, run_id: str) -> tuple[bool, str]:
    command = [
        sys.executable,
        "tools/check_evaluation_evidence.py",
        "--project-dir",
        str(project_dir),
        "--run-id",
        run_id,
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    return result.returncode == 0, result.stdout + result.stderr


def check_loop_control(project_dir: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "tools/check_evaluation_loop_control.py", "--project-dir", str(project_dir)],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", action="append", help="Project directory to check. Can be repeated.")
    parser.add_argument("--projects-root", default="projects", help="Root used when --project-dir is omitted.")
    args = parser.parse_args()

    if args.project_dir:
        project_dirs = [Path(path).resolve() for path in args.project_dir]
    else:
        root = Path(args.projects_root)
        project_dirs = sorted(path.resolve() for path in root.iterdir() if path.is_dir())

    failures: list[str] = []
    checked = 0
    skipped = 0

    for project_dir in project_dirs:
        if not has_formal_verdict(project_dir):
            skipped += 1
            continue

        checked += 1
        runs = valid_llm_runs(project_dir)
        if not runs:
            failures.append(
                f"{project_dir.name}: formal verdict is recorded, but no completed fresh_context independent LLM evaluation run was found"
            )
            continue

        project_has_valid_evidence = False
        evidence_errors: list[str] = []
        for run_dir in runs:
            ok, output = check_evidence(project_dir, run_dir.name)
            if ok:
                project_has_valid_evidence = True
                break
            evidence_errors.append(f"{run_dir.name}: {output.strip()}")

        if not project_has_valid_evidence:
            failures.append(
                f"{project_dir.name}: independent LLM run exists, but evidence validation failed: "
                + " | ".join(evidence_errors)
            )
            continue

        loop_ok, loop_output = check_loop_control(project_dir)
        if not loop_ok:
            failures.append(f"{project_dir.name}: {loop_output.strip()}")

    if failures:
        print("FAIL: formal evaluation gate failed.")
        print("Formal Pass / Fix / Needs Review requires a completed fresh_context subagent evaluation run.")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"PASS: formal evaluation gate passed for {checked} project(s); "
        f"{skipped} project(s) had no formal verdict to enforce."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
