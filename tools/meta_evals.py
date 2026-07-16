#!/usr/bin/env python3
"""Small regression checks for the harness gates themselves.

This is deliberately not an eval runner: it verifies file-based guardrails fail
closed using temporary directories only.
"""

from __future__ import annotations

import hashlib
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


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def write_receipt(project: Path, name: str, data: dict) -> None:
    path = project / "evaluation" / "runs" / name
    path.mkdir(parents=True)
    (path / "receipt.json").write_text(json.dumps(data))


def write_evidence_context(project: Path, run_name: str) -> tuple[Path, dict]:
    run_dir = project / "evaluation" / "runs" / run_name
    run_dir.mkdir(parents=True)
    (project / "project-requirements.md").write_text("requirements")
    (project / "evaluation" / "eval-cases.md").write_text("E-01")
    (project / "evaluation" / "traceability.md").write_text("REQ-01 C-01 E-01")
    (project / "evaluation" / "evaluation-loop.md").write_text(
        f"```mermaid\nflowchart TD\n```\n{run_name}"
    )
    (project / "artifact.txt").write_text("evaluated artifact")
    (run_dir / "evaluator-input.md").write_text("input")
    (run_dir / "evaluator-result.md").write_text("result")
    return run_dir, receipt(0, "Pass") | {
        "run_id": run_name,
        "evaluator_agent_id": "evaluator",
        "context_isolation": "fresh_context",
        "started_at": "2026-01-01T00:00:00Z",
        "traceability_required": True,
        "evaluated_commit_sha": "a" * 40,
        "requirements_hash": sha256("requirements"),
        "eval_cases_hash": sha256("E-01"),
        "artifact_hashes": {"artifact.txt": sha256("evaluated artifact")},
        "evaluator_model": "test-model",
        "evaluator_prompt_version": "prompt-v1",
        "rubric_version": "rubric-v1",
        "temperature": 0,
    }


def expect_failure(label: str, result: subprocess.CompletedProcess[str], expected_text: str = "") -> str | None:
    output = result.stdout + result.stderr
    if result.returncode == 0:
        return f"{label}: expected failure, got success\n{output}"
    if expected_text and expected_text not in output:
        return f"{label}: failed for an unexpected reason\n{output}"
    return None


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        failures += filter(None, [expect_failure("Gate A", run("tools/check_preimplementation_readiness.py", "--project-dir", str(project)))])
        failures += filter(None, [expect_failure("Gate B", run("tools/check_evaluation_evidence.py", "--project-dir", str(project), "--run-id", "no-evidence"))])

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        run_dir, complete = write_evidence_context(project, "missing-reproducibility")
        incomplete = {
            key: value
            for key, value in complete.items()
            if key not in {"evaluated_commit_sha", "requirements_hash", "eval_cases_hash", "artifact_hashes", "evaluator_model", "evaluator_prompt_version", "rubric_version", "temperature"}
        }
        (run_dir / "receipt.json").write_text(json.dumps(incomplete))
        failures += filter(None, [expect_failure("schema v2 reproducibility", run("tools/check_evaluation_evidence.py", "--project-dir", str(project), "--run-id", "missing-reproducibility"), "evaluated_commit_sha is required")])

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        run_dir, complete = write_evidence_context(project, "artifact-changed")
        (run_dir / "receipt.json").write_text(json.dumps(complete))
        (project / "artifact.txt").write_text("changed after evaluation")
        failures += filter(None, [expect_failure("artifact hash mismatch", run("tools/check_evaluation_evidence.py", "--project-dir", str(project), "--run-id", "artifact-changed"), "artifact artifact.txt does not match the current file")])

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        write_receipt(project, "run-01", receipt(1, "Fix"))
        write_receipt(project, "run-02", receipt(2, "Pass"))
        allowed = run("tools/check_evaluation_loop_control.py", "--project-dir", str(project))
        if allowed.returncode != 0:
            failures.append(f"first Fix follow-up: expected success\n{allowed.stdout}{allowed.stderr}")

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        write_receipt(project, "run-01", receipt(1, "Needs Review"))
        write_receipt(project, "run-02", receipt(2, "Pass"))
        failures += filter(None, [expect_failure("Needs Review stop", run("tools/check_evaluation_loop_control.py", "--project-dir", str(project)))])

    with tempfile.TemporaryDirectory() as temp:
        project = Path(temp) / "project"
        project.mkdir()
        write_receipt(project, "run-01", receipt(1, "Fix"))
        write_receipt(project, "run-02", receipt(2, "Fix"))
        write_receipt(project, "run-03", receipt(3, "Pass"))
        failures += filter(None, [expect_failure("two Fix stop", run("tools/check_evaluation_loop_control.py", "--project-dir", str(project)), "two Fix results must stop")])

    if failures:
        print("FAIL: meta evals found an open gate.")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print("PASS: Gate A, Gate B, schema v2, artifact hashes, and loop stops fail closed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
