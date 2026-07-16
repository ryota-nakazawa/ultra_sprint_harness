#!/usr/bin/env python3
"""Small regression checks for the harness gates themselves.

This is deliberately not an eval runner: it only verifies that the file-based
guardrails fail closed in four representative situations.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, *args], cwd=ROOT, text=True, capture_output=True)


def receipt(iteration: int, verdict: str) -> dict:
    return {
        "receipt_schema_version": 2,
        "iteration": iteration,
        "completed_at": "2026-01-01T00:00:00Z",
        "verdict": verdict,
    }


def write_receipt(project: Path, name: str, data: dict) -> None:
    path = project / "evaluation" / "runs" / name
    path.mkdir(parents=True)
    (path / "receipt.json").write_text(json.dumps(data))


def expect_failure(label: str, result: subprocess.CompletedProcess[str]) -> str | None:
    if result.returncode == 0:
        return f"{label}: expected failure, got success\n{result.stdout}"
    return None


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        project = root / "project"
        project.mkdir()

        failures += filter(None, [expect_failure("Gate A", run("tools/check_preimplementation_readiness.py", "--project-dir", str(project)))])
        failures += filter(None, [expect_failure("Gate B", run("tools/check_evaluation_evidence.py", "--project-dir", str(project), "--run-id", "no-evidence"))])

        evidence_run = project / "evaluation" / "runs" / "missing-reproducibility"
        evidence_run.mkdir(parents=True)
        (project / "project-requirements.md").write_text("requirements")
        (project / "evaluation" / "eval-cases.md").write_text("E-01")
        (project / "evaluation" / "traceability.md").write_text("REQ-01 C-01 E-01")
        (project / "evaluation" / "evaluation-loop.md").write_text("```mermaid\nflowchart TD\n```\nmissing-reproducibility")
        (evidence_run / "evaluator-input.md").write_text("input")
        (evidence_run / "evaluator-result.md").write_text("result")
        incomplete = receipt(0, "Pass") | {
            "run_id": "missing-reproducibility",
            "evaluator_agent_id": "evaluator",
            "context_isolation": "fresh_context",
            "started_at": "2026-01-01T00:00:00Z",
            "traceability_required": True,
        }
        (evidence_run / "receipt.json").write_text(json.dumps(incomplete))
        failures += filter(None, [expect_failure("receipt reproducibility fields", run("tools/check_evaluation_evidence.py", "--project-dir", str(project), "--run-id", "missing-reproducibility"))])

        write_receipt(project, "run-01", receipt(1, "Needs Review"))
        write_receipt(project, "run-02", receipt(2, "Pass"))
        failures += filter(None, [expect_failure("Needs Review stop", run("tools/check_evaluation_loop_control.py", "--project-dir", str(project)))])

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        write_receipt(project, "run-01", receipt(1, "Fix"))
        write_receipt(project, "run-02", receipt(2, "Fix"))
        write_receipt(project, "run-03", receipt(3, "Pass"))
        failures += filter(None, [expect_failure("Two Fix stop", run("tools/check_evaluation_loop_control.py", "--project-dir", str(project)))])

    if failures:
        print("FAIL: meta evals found an open gate.")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("PASS: Gate A, Gate B, Needs Review stop, and two-Fix stop fail closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
