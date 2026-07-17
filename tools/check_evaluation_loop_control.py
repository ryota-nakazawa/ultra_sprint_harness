#!/usr/bin/env python3
"""Check the small, file-based stop rules for an evaluation loop."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def completed_runs(project_dir: Path) -> list[tuple[int, Path, dict]]:
    runs = []
    for receipt_path in (project_dir / "evaluation" / "runs").glob("*/receipt.json"):
        try:
            receipt = json.loads(receipt_path.read_text())
        except json.JSONDecodeError:
            continue
        # Existing history predates explicit loop-control receipts. Keep it
        # readable; enforce the stop rule for new schema v2 runs.
        if (
            receipt.get("receipt_schema_version", 1) >= 2
            and receipt.get("completed_at")
            and receipt.get("verdict") in {"Pass", "Fix", "Needs Review"}
        ):
            runs.append((int(receipt.get("iteration", 0)), receipt_path.parent, receipt))
    return sorted(runs, key=lambda item: (item[0], item[1].name))


def check(project_dir: Path) -> list[str]:
    runs = completed_runs(project_dir)
    failures: list[str] = []
    for index, (_, run_dir, receipt) in enumerate(runs):
        later = runs[index + 1 :]
        if receipt["verdict"] == "Needs Review" and later:
            failures.append(f"{run_dir.name}: Needs Review must stop the automatic loop")
        if receipt["verdict"] == "Fix":
            # Receipts store one verdict per run, not per eval-case ID. Count
            # Fix runs across the automatic loop and stop after the second.
            prior_fixes = [item for item in runs[: index + 1] if item[2]["verdict"] == "Fix"]
            if len(prior_fixes) >= 2 and later:
                failures.append(f"{run_dir.name}: two Fix results must stop the automatic loop")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", required=True)
    args = parser.parse_args()
    failures = check(Path(args.project_dir).resolve())
    if failures:
        print("FAIL: evaluation loop stop rule was violated.")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("PASS: evaluation loop stop rules are satisfied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
